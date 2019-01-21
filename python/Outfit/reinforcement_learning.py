import numpy as np
import pandas as pd
import json
import variables as var

class RL:
    def __init__(self, clothes, cat_score):
        self.clothes = clothes
        self.cat_score = {int(key): value for key, value in cat_score.items()}
        self.clothes_df = self.create_df_clothes()
        self.space = self.create_space()
        self.cat_score_s = self.create_cat_score()

    def create_cat_score(self):
        return {int(step): pd.Series(score_dict) for step, score_dict in self.cat_score.items()}

    def create_space(self):

        space = dict()
        for step, param in enumerate(var.params):
            if step == 1:
                space[step] = {cat: self.clothes_df.loc[self.clothes_df.category == cat, ["_id", "rl_score"]].set_index("_id").rl_score
                                for cat in
                                list(self.clothes_df.loc[(self.clothes_df.bp_5 == param[0]) & (self.clothes_df.layer == param[1]), "category"].unique())}
            else:
                space[step] = {cat: self.clothes_df.loc[self.clothes_df.category == cat, ["_id", "rl_score"]].set_index("_id").rl_score
                                for cat in
                                list(self.clothes_df.loc[(self.clothes_df.bp_1 == param[0]) & (self.clothes_df.layer == param[1]), "category"].unique())}

            new_cats = set(space[step].keys()) - set(self.cat_score[step].keys())
            self.cat_score[step].update({cat: 0.0 for cat in new_cats})

        return space

    def create_df_clothes(self):

        clothes_df = pd.DataFrame(self.clothes)
        bodypart_df = pd.get_dummies(clothes_df.bodyparts.apply(pd.Series).stack()).sum(level=0).rename(
            columns=lambda x: "bp_{}".format(int(x)))
        clothes_df = pd.concat([clothes_df.drop(columns=['bodyparts']), bodypart_df], axis=1)
        return clothes_df

    def create_outfit(self):
        outfit = list()
        for step in range(np.random.randint(1, var.n_step)+1):
            cat = self.cat_score_s[step].idxmax()
            outfit.append(self.space[step][cat].idxmax())
            print(cat, step)
        return outfit

    def update_value(self, taste):
        pass

if __name__ == "__main__":
    with open('../database/clothes3.json') as data_file:
        data = json.load(data_file)
    cat_score = data["rl_cat_score"]
    clothes = data["clothes"]
    for clothe in clothes:
        clothe["rl_score"] = 0.0

    rl = RL(clothes, cat_score)
    print(rl.create_outfit())

    # reform = {(outerKey, innerKey): values for outerKey, innerDict in rl.space.items() for innerKey, values in
    #           innerDict.items()}
    # print(reform)
    # print((pd.DataFrame.from_dict(reform, orient='index').T.head()))


