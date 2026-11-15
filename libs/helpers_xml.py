# -*- coding: utf-8 -*-

# STK special XML handling

from copy import deepcopy
from lxml import etree
from threading import Lock
import shutil

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
