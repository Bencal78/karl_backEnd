import numpy as np
import pandas as pd
import json
import variables as var
import sys


def return_outfit():
    args = sys.argv[2]
    args_json = json.loads(args)
    clothes = args_json["clothes"]
    rl_cat_score = args_json["rl_cat_score"]
    rl = RL(clothes, rl_cat_score)
    rl.create_outfit()

def update_value():
    args = sys.argv[2]
    args_json = json.loads(args)
    clothes = args_json["clothes"]
    rl_cat_score = args_json["rl_cat_score"]
    rl = RL(clothes, rl_cat_score)  
    rl.create_outfit()

class RL:
    def __init__(self, clothes, cat_score):
        self.clothes = clothes
        self.cat_score = {int(key): value for key, value in cat_score.items()}
        self.clothes_df = self.create_df_clothes(clothes)
        self.space = self.create_space()
        self.cat_score_s = self.create_cat_score()

    def create_cat_score(self):
        return {int(step): pd.Series(score_dict) for step, score_dict in self.cat_score.items()}

    def create_space(self):

        space = dict()
        for step, param in enumerate(var.params):
            bp, layer = param
            space[step] = {cat: self.clothes_df.loc[self.clothes_df.category == cat, ["_id", "rl_score"]].set_index("_id").rl_score
                           for cat in
                           list(self.clothes_df.loc[(self.clothes_df[bp] == 1) & (self.clothes_df.layer == layer), "category"].unique())}

            new_cats = set(space[step].keys()) - set(self.cat_score[step].keys())
            self.cat_score[step].update({cat: 0.0 for cat in new_cats})

        return space

    @staticmethod
    def create_df_clothes(clothes):
        clothes_df = pd.DataFrame(clothes)
        bodypart_df = pd.get_dummies(clothes_df.bodyparts.apply(pd.Series).stack()).sum(level=0).rename(
            columns=lambda x: "bp_{}".format(int(x)))
        clothes_df = pd.concat([clothes_df.drop(columns=['bodyparts']), bodypart_df], axis=1)
        return clothes_df

    def create_outfit(self):
        outfit_ids = list()
        for step in range(np.random.randint(1, var.n_step)+1):
            cat = self.cat_score_s[step].idxmax()
            outfit_ids.append(self.space[step][cat].idxmax())
        print(outfit_ids)
        outfit = self.prepare_outfit(outfit_ids)
        print({"outfit": outfit})

    def update_value_naive(self, taste):
        outfit, l3_not_l2 = self.reorganize_outfit(taste["outfit"])
        reward = 1 if taste["decision"] else -1

        for step, clothe in enumerate(outfit):
            if (step == 2) & l3_not_l2: step += 1
            self.space[step][clothe["category"]].loc[clothe["_id"]] += reward/(2*len(outfit))
            self.clothes_df.loc[self.clothes_df._id == clothe["_id"], "score"] = self.space[step][clothe["category"]].loc[clothe["_id"]]
            self.cat_score_s[step].loc[clothe["category"]] += reward/(2*len(outfit))

        self.prepare_update_value(taste)
        print({"clothes": self.clothes, "rl_cat_score": self.cat_score})

    @staticmethod
    def reorganize_outfit(outfit):
        outfit_df = RL.create_df_clothes(outfit)
        sorted_ids = list()
        l3_not_l2 = False
        for step in range(outfit_df.shape[0]):
            bp, layer = var.params[step]
            try:
                sorted_ids.append(outfit_df.loc[(outfit_df[bp] == 1) & (outfit_df.layer == layer)].index.values[0])
            except IndexError:
                sorted_ids.append(outfit_df.loc[(outfit_df[bp] == 1) & (outfit_df.layer == layer+1)].index.values[0])
                l3_not_l2 = True
        outfit_sorted = [outfit[cid] for cid in sorted_ids]
        return outfit_sorted, l3_not_l2

    def prepare_outfit(self, outfit_ids):
        df_ids = list(self.clothes_df.loc[self.clothes_df._id.isin(outfit_ids)].index.values)
        outfit = {'outfit': [self.clothes[cid] for cid in df_ids]}
        return outfit

    def prepare_update_value(self, taste):
        outfit, l3_not_l2 = self.reorganize_outfit(taste["outfit"])
        for clothe in outfit:
            s = self.clothes_df.loc[self.clothes_df._id == clothe["_id"], "score"]
            self.clothes[s.index.values[0]]["score"] = s.iloc[0]
        self.cat_score = {step: serie.to_dict() for step, serie in self.cat_score_s.items()}

if __name__ == "__main__":
    with open('../database/clothes3.json') as data_file:
        data = json.load(data_file)
    cat_score = data["rl_cat_score"]
    clothes = data["clothes"]
    for clothe in clothes:
        clothe["rl_score"] = 0.0

    rl = RL(clothes, cat_score)
    with open("tastes2.json") as file:
        tastes = json.load(file)

    print(rl.cat_score_s[0].to_dict())
    rl.update_value_naive(tastes[0])
