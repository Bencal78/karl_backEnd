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
    ids = clothes_df.loc[clothes_df._id.isin(outfit)].index.values
    outfits_list = [clothes[id_clothes] for id_clothes in ids]
    return outfits_list


if __name__ == "__main__":
    with open('../database/clothes.json') as data_file:
        clothes = json.load(data_file)["clothes"]
    dec = 0
    decisions = list()
    while dec != "q":
        print("-------------------")
        outfit = create_outfit(clothes)
        for clothe in outfit:
            print(clothe["name"])
        print()
        dec = input("y for yes; n for no; q to quit\n")
        print("-------------------")
        if dec not in ["y", "n"]:
            continue
        decisions.append({"outfit": outfit, "decision": True if dec == "y" else False})

    with open('taste.json', 'w') as fp:
        json.dump(decisions, fp)