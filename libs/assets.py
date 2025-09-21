# -*- coding: utf-8 -*-

import libs.common

class AssetDict:
    def __init__(self):
        self.asset_dict = {}

    def reset(self):
        self.asset_dict = {}
        messagerella = libs.common.dl_file("https://raw.githubusercontent.com/matahina/Miscellaneous-STK-files/refs/heads/main/ustkl_assets/sources.csv","sources",".csv")
        return messagerella

    def add_asset(self,da_id,da_name,da_version,da_powerup,da_kartchar="standard"):
        self.asset_dict |= { da_id:(da_name,da_powerup,da_kartchar,da_version) }

    def add_standard(self,da_name,da_version,da_powerup,da_kartchar):
        self.asset_dict |= { "standard"+da_version:(da_name,da_powerup,da_kartchar,da_version) }

    def list_assets(self,da_version):
        da_list = []
        for da_id in self.asset_dict.keys():
            if self.asset_dict[da_id][3] == str(da_version):
                da_list.append(da_id.replace("standard"+str(da_version),"standard"))
        return(da_list)

    def get_assets(self,da_id,da_version):
        da_list = []
        if da_id == "standard":
            da_list.append("powerup_"+self.asset_dict[da_id+ str(da_version)][0])
            da_list.append("kart_"+self.asset_dict[da_id+ str(da_version)][0])
        else:
            if self.asset_dict[da_id][1] == "standard":
                da_list.append("powerup_"+self.asset_dict["standard" + str(da_version)][0])
            else:
                da_list.append("powerup_"+self.asset_dict[da_id][0])
            if self.asset_dict[da_id][2] == "standard":
                da_list.append("kart_"+self.asset_dict["standard" + str(da_version)][0])
            else:
                da_list.append("kart_"+self.asset_dict[da_id][0])
        return(da_list)




class RecipeDict:
    def __init__(self):
        self.recipe_dict = {}

    def reset(self):
        self.recipe_dict = {}
        messagerella = libs.common.dl_file("https://api.github.com/repos/matahina/Miscellaneous-STK-files/contents/ustkl_assets/recipes","recipes",".json","tmp_files")
        return messagerella

    def add_recipe(self,da_id,da_name,da_version,da_upgradable):
        self.recipe_dict |= { da_id:(da_name,da_version,da_upgradable) }

    def list_recipes(self):
        da_list_dict = {}
        for da_id in self.recipe_dict.keys():
            if "fficial" in self.recipe_dict[da_id][0]:
                da_list_dict |= { da_id:self.recipe_dict[da_id][0] }
        for da_id in self.recipe_dict.keys():
            if not "fficial" in self.recipe_dict[da_id][0]:
                da_list_dict |= { da_id:self.recipe_dict[da_id][0] }
        return(da_list_dict)

    def list_updatable_recipes(self):
        da_list_dict = {}
        for da_id in self.recipe_dict.keys():
            if self.recipe_dict[da_id][2]:
                da_list_dict |= { da_id:self.recipe_dict[da_id][0] }
        return(da_list_dict)
