import numpy as np
import pandas as pd
import json

def update_value(taste):
    pass




class RL:
    def __init__(self, clothes):
        self.clothes = clothes
        self.clothes_df = self.create_df_clothes()
        self.space = self.create_space()

    def create_space(self):

        cat = dict()

        cat["1"] = {cat: list(self.clothes_df.loc[self.clothes_df.category == cat, "_id"]) for cat in
                    list(self.clothes_df.loc[(self.clothes_df.bp_1 == 1) & (self.clothes_df.layer == 1), "category"].unique())}

        cat["2"] = {cat: list(self.clothes_df.loc[self.clothes_df.category == cat, "_id"]) for cat in
                    list(self.clothes_df.loc[(self.clothes_df.bp_5 == 1) & (self.clothes_df.layer == 1), "category"].unique())}

        cat["3"] = {cat: list(self.clothes_df.loc[self.clothes_df.category == cat, "_id"]) for cat in
                    list(self.clothes_df.loc[(self.clothes_df.bp_1 == 1) & (self.clothes_df.layer == 2), "category"].unique())}

        cat["4"] = {cat: list(self.clothes_df.loc[self.clothes_df.category == cat, "_id"]) for cat in
                    list(self.clothes_df.loc[(self.clothes_df.bp_1 == 1) & (self.clothes_df.layer == 3), "category"].unique())}

        return cat

    def create_df_clothes(self):

        clothes_df = pd.DataFrame(self.clothes)
        bodypart_df = pd.get_dummies(clothes_df.bodyparts.apply(pd.Series).stack()).sum(level=0).rename(
            columns=lambda x: "bp_{}".format(int(x)))
        clothes_df = pd.concat([clothes_df.drop(columns=['bodyparts']), bodypart_df], axis=1)
        return clothes_df

    def update_value(self, taste):
        pass

if __name__ == "__main__":
    with open('../database/clothes.json') as data_file:
        clothes = json.load(data_file)["clothes"]
    for clothe in clothes:
        clothe["rl_score"] = 0.0
