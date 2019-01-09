import numpy as np
import pandas as pd
import json


def create_outfit(clothes):

    clothes_df = pd.DataFrame(clothes)
    bodypart_df = pd.get_dummies(clothes_df.bodyparts.apply(pd.Series).stack()).sum(level=0).rename(columns=lambda x: "bp_{}".format(int(x)))
    clothes_df = pd.concat([clothes_df.drop(columns=['bodyparts']), bodypart_df], axis=1)
    outfit = list()

    outfit.append(clothes_df.loc[(clothes_df.bp_1 == 1) & (clothes_df.layer == 1), "_id"].sample(n=1).values[0])
    outfit.append(clothes_df.loc[(clothes_df.bp_5 == 1) & (clothes_df.layer == 1), "_id"].sample(n=1).values[0])
    if np.random.randint(2) == 0:
        outfit.append(clothes_df.loc[(clothes_df.bp_1 == 1) & (clothes_df.layer == 2), "_id"].sample(n=1).values[0])
    if np.random.randint(4) == 0:
        outfit.append(clothes_df.loc[(clothes_df.bp_1 == 1) & (clothes_df.layer == 3), "_id"].sample(n=1).values[0])

    print(clothes_df.loc[clothes_df._id.isin(outfit), ["name"]])


if __name__ == "__main__":
    with open('../database/clothes.json') as data_file:
        clothes = json.load(data_file)["clothes"]
    create_outfit(clothes)
