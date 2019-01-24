import numpy as np
import pandas as pd
import json
import sys

def create_outfit(clothes):
    """
    Create a Dataframe based on the dict of clothes
    Dummify the bodyparts' feature
    Create a pure random outfit with random nb of clothes (2 to 4)
    :param clothes:
    :return:
    """
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
    ids = clothes_df.loc[clothes_df._id.isin(outfit)].index.values
    outfits_list = [clothes[id_clothes] for id_clothes in ids]

    return {"outfit": outfits_list}


if __name__ == "__main__":
    with open('../database/clothes3.json') as data_file:
        clothes = json.load(data_file)["clothes"]
    dec = 0
    decisions = list()
    while dec != "q":
        print("-------------------")
        outfit = create_outfit(clothes)
        for clothe in outfit:
            print(clothe["name"])
        print()
        dec = input("y for yes; n for no; q to quit; c to cancel\n")
        print("-------------------")
        if dec == "c":
            sys.exit()
        if dec not in ["y", "n"]:
            continue
        decisions.append({"outfit": outfit, "decision": True if dec == "y" else False})

    with open('taste.json', 'w') as fp:
        json.dump(decisions, fp)