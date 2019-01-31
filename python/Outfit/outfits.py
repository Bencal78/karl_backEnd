import numpy as np
import pandas as pd
import json
import tastes as naive_bayes


def create_outfit_random(clothes):
    outfit = list()  # initialization of the outfit

    clothes_df = pd.DataFrame(clothes)  # dataframe containing the clothes
    # converts the column "bodyparts" in clothes_df into columns which values equals 1 if the bodypart is covered by the
    # clothes and 0 if not
    bodypart_df = pd.get_dummies(clothes_df.bodyparts.apply(pd.Series).stack()).sum(level=0).rename(columns=lambda x: "bp_{}".format(int(x)))
    # replacement of the old bodyparts column with the new ones
    clothes_df = pd.concat([clothes_df.drop(columns=['bodyparts']), bodypart_df], axis=1)

    # adds two random clothes to the outfit on for the top and one for the pants.
    outfit.append(clothes_df.loc[(clothes_df.bp_1 == 1) & (clothes_df.layer == 1), "_id"].sample(n=1).values[0])
    outfit.append(clothes_df.loc[(clothes_df.bp_5 == 1) & (clothes_df.layer == 1), "_id"].sample(n=1).values[0])

    # randomly adds two other clothes on the upper layers for the top of the body
    if np.random.randint(2) == 0:
        outfit.append(clothes_df.loc[(clothes_df.bp_1 == 1) & (clothes_df.layer == 2), "_id"].sample(n=1).values[0])
    if np.random.randint(4) == 0:
        outfit.append(clothes_df.loc[(clothes_df.bp_1 == 1) & (clothes_df.layer == 3), "_id"].sample(n=1).values[0])


    ids = clothes_df.loc[clothes_df._id.isin(outfit)].index.values
    outfit_list = [clothes[id_clothes] for id_clothes in ids]

    return outfit_list


def create_outfit(user, algo = "random"):
    """
    Creates an outfit with the algorithm specified
    :param user: information of the user, including clothes and tastes
    :param algo: the algorithm to be chosen to create an outfit
    :return: an outfit
    """

    outfit = list()

    if algo == "random":
        outfit = create_outfit_random(user["clothes"])
    if algo == "NB":
        outfit = naive_bayes.create_outfit_NB()
    if algo == "RL":
        pass

    return outfit


if __name__ == "__main__":
    with open('../database/clothes.json') as data_file:
        clothes = json.load(data_file)["clothes"]
    outfit = create_outfit_random(clothes)
