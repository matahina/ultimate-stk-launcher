# -*- coding: utf-8 -*-

# STK special XML handling

from copy import deepcopy
from lxml import etree
from threading import Lock
import shutil
import logging
from pathlib import Path

xml_lock = Lock()

def parser_of_the_universe(my_string):
    new_good_string = ""
    for char in my_string:
        if ord(char) >= 128 or char in '&<>" \t\n\r':
            new_good_string+=f"&#x{ord(char):X};"
        else:
            new_good_string+=char
    return new_good_string


def serialize_stk_xml(tree):
    work_tree = deepcopy(tree)
    replacements = {}

    original_xml = etree.tostring(tree, encoding="UTF-8")

    while True:
        with open("/dev/urandom","rb") as rand:
            prefix = "USTKL" + rand.read(4).hex()

        if prefix.encode("utf-8") not in original_xml:
            break

    i=0

    for addon in work_tree.getroot():

        for attr in ["name", "designer", "description"]:
            value = addon.get(attr)

            if value is not None:
                encoded = parser_of_the_universe(value)

                if encoded != value:
                    marker = prefix + f"{i:04d}"
                    replacements[marker] = encoded
                    addon.set(attr, marker)
                    i += 1

    xml = etree.tostring(work_tree, encoding="UTF-8", xml_declaration=True)

    for marker, value in replacements.items():
        old = ('"' + marker + '"').encode("utf-8")
        new = ('"' + value + '"').encode("utf-8")

        if xml.count(old) != 1:
            raise ValueError("Unexpected XML marker")

        xml = xml.replace(old, new)

    etree.fromstring(xml) # will cause error if xml syntax bröken, it's just a check

    return xml



def update_installed_addon(filename, the_type, attributes, mytree):

    root = mytree.getroot()
    tag = '{https://online.supertuxkart.net/}'+the_type

    matches = []

    for addon in root:
        if addon.get("id") == attributes["id"]:
            matches.append(addon)

    if not matches:
        matches.append(etree.SubElement(root, tag))

    for addon in matches:
        for key, value in attributes.items():
            addon.set(key, value)

    xml = serialize_stk_xml(mytree)

    tmp_file = filename + ".tmp"

    with open(tmp_file,"wb") as tmp:
        tmp.write(xml)

    shutil.move(tmp_file, filename)


def clean_addon_database(filename, catalogue_tree):
    '''The Graal function'''

    namespace = "{https://online.supertuxkart.net/}"
    types = ["track", "arena", "kart"]

    defaults = {
        "designer": "",
        "status": "0",
        "date": "0",
        "size": "0",
        "icon-name": "",
        "icon-revision": "0"
    }

    skipped = []
    to_remove = []
    resolved_collisions = set()

    def revision(value):
        try:
            return max(0, int(value or "0"))
        except ValueError:
            return 0

    with xml_lock:

        mytree = etree.parse(filename)
        root = mytree.getroot()

        if root.tag != namespace + "addons":
            raise ValueError("Unexpected installed addons XML")

        original_xml = etree.tostring(mytree)

        groups = {}
        catalogue = {}
        local = {}

        # Read catalogue
        if catalogue_tree != []:
            for addon in catalogue_tree.getroot():
                if addon.tag in types and addon.get("id"):
                    addon_id = addon.get("id")
                    if addon_id not in catalogue:
                        catalogue[addon_id] = []
                    catalogue[addon_id].append(addon)

        # Group existing entries by id
        for addon in root:
            if addon.tag in [namespace + t for t in types] and addon.get("id"):
                addon_id = addon.get("id")
                if addon_id not in groups:
                    groups[addon_id] = []
                groups[addon_id].append(addon)

        # Scan installed addons on disk
        for place in ["tracks", "karts"]:
            for folder in Path(Path(filename).parent, place).iterdir():

                the_type = place[:-1]

                if not folder.is_dir():
                    continue

                addon_id = folder.name
                if addon_id in skipped:
                    continue

                # Resolve collisions using the catalogue
                # Happens for one addon (Syncopia Stadium) but can happen for others... if both track.xml and kart.xml inside dir
                # Catalogue from stk_addons has authority upon type
                if addon_id in skipped:
                    continue

                other_place = "karts" if place == "tracks" else "tracks"

                if Path(Path(filename).parent, other_place, addon_id).is_dir():

                    catalogue_addons = catalogue.get(addon_id, [])

                    if not catalogue_addons:
                        skipped.append(addon_id)
                        continue

                    catalogue_place = "karts" if catalogue_addons[0].tag == "kart" else "tracks"

                    if place != catalogue_place:
                        continue

                    resolved_collisions.add(addon_id)

                try:
                    data = etree.parse(
                        str(Path(folder, the_type + ".xml")),
                        parser=etree.XMLParser(resolve_entities=False,no_network=True) # xml download in archive might not be perfect
                    ).getroot()

                    if data.tag != the_type or not data.get("name"):
                        raise ValueError("Unexpected addon XML")

                # other errors than I/O file error, xml syntax or bad type should break cleanup
                except (OSError, etree.XMLSyntaxError, ValueError):
                    logging.getLogger("ustkl").exception("Skipping invalid addon "+addon_id)
                    skipped.append(addon_id)
                    continue

                if place == "tracks":

                    arena = (data.get("arena") or "").lower()
                    soccer = (data.get("soccer") or "").lower()

                    if arena.startswith(("t", "y")) or arena in ["#t", "1"]:
                        the_type = "arena"

                    elif soccer.startswith(("t", "y")) or soccer in ["#t", "1"]:
                        the_type = "track"

                local[addon_id] = (the_type, data)

                if addon_id not in groups:
                    groups[addon_id] = []

        # Synchronize installed addons
        for addon_id, matches in groups.items():

            if addon_id in skipped:
                continue

            if addon_id not in local:
                to_remove.extend(matches)
                continue

            the_type, data = local[addon_id]

            installed_revision = revision(data.get("revision"))

            # Find reference in catalogue
            reference = None

            for addon in catalogue.get(addon_id, []):

                # Kart is kart and track is arena/track
                if the_type == "kart":
                    if addon.tag != "kart":
                        continue
                else:
                    if addon.tag not in ["track", "arena"]:
                        continue

                if installed_revision and revision(addon.get("revision")) == installed_revision:
                    reference = addon
                    break

                # no revision found for this track so we'll take metadata from last one, and keep revision as 0
                if reference is None or revision(addon.get("revision")) > revision(reference.get("revision")):
                    reference = addon

            # Use the catalogue category when available
            # Allows track to be arena and kart.xml being in track dir
            if reference is not None:
                the_type = reference.tag

            allowed_types = [the_type]

            if reference is not None and the_type in ["track", "arena"]:
                allowed_types = ["track", "arena"]

            if addon_id not in resolved_collisions:
                if any(addon.tag not in [namespace + t for t in allowed_types] for addon in matches):
                    skipped.append(addon_id)
                    continue

            # Rebuild attributes
            attributes = defaults.copy()
            attributes["name"] = data.get("name")

            for key in ["name", "designer", "status"]:
                if reference is not None and reference.get(key):
                    attributes[key] = reference.get(key)
                elif data.get(key):
                    attributes[key] = data.get(key)

            # Only retrieve date and size for matching revisions
            if reference is not None and installed_revision and revision(reference.get("revision")) == installed_revision:
                for key in ["date", "size"]:
                    if reference.get(key):
                        attributes[key] = reference.get(key)

            attributes["id"] = addon_id
            attributes["installed"] = "true"
            attributes["installed-revision"] = str(installed_revision)

            # Keep one entry
            if matches:
                keep = matches[0]
            else:
                keep = etree.SubElement(root, namespace + the_type)
            keep.tag = namespace + the_type
            keep.attrib.clear()
            for key, value in attributes.items():
                keep.set(key, value)

            # Mark duplicate entries for removal
            for addon in matches:
                if addon is not keep:
                    to_remove.append(addon)

        # Remove obsolete and duplicate entries
        for addon in to_remove:
            root.remove(addon)

        # Save only if something has changed
        if etree.tostring(mytree) != original_xml:
            xml = serialize_stk_xml(mytree)
            tmp_file = filename + ".tmp"
            with open(tmp_file,"wb") as tmp:
                tmp.write(xml)
            shutil.move(tmp_file, filename)

    return len(to_remove), skipped
