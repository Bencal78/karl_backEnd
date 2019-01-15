import pandas as pd
import re
import json
import numpy as np
from itertools import product


def create_tastes_from_file(df_csv):
    # on choppe les données qui nous intéressent, les colonnes qui nous intéressent et on crée le dataframe
    relevant_columns = df_csv.iloc[:, 3:]
    l = list(relevant_columns.columns)
    df_ben = pd.DataFrame()

    for idrow, row in relevant_columns.iterrows():
        row = row.apply(lambda x: re.split('\, ', str(x)))
        df_ben = df_ben.append(row, ignore_index=True)

    dct = df_ben.iloc[-1].to_dict()
    a = list()
    for key, value in dct.items():
        key = [key]
        a = a + (list(product(key, value)))

    df_complete = pd.DataFrame(a, columns=["id_0", "id_1"])
    df_complete["decision"] = False

    df_tastes = pd.DataFrame(columns=["idUser", "id_0", "id_1", "decision"])

    for idrow, row in df_csv.iterrows():
        row = row.dropna().apply(lambda x: re.split('\, ', str(x)))
        for colname, col in row[3:].iteritems():
            for cloth in col:
                df_tastes = df_tastes.append(
                    pd.Series({"idUser": int(idrow), "id_0": colname, "id_1": cloth, "decision": True}),
                    ignore_index=True)

    df_merge_final = pd.DataFrame(columns=["idUser", "id_0", "id_1", "decision"])

    for id in range(max(df_tastes["idUser"]) + 1):
        df_merge_temp = pd.merge(df_tastes.loc[df_tastes["idUser"] == id], df_complete, how="right",
                                 on=['id_0', 'id_1'])
        df_merge_temp["decision_x"] = df_merge_temp["decision_x"].fillna(False)
        df_merge_temp["idUser"] = df_merge_temp["idUser"].fillna(1)
        df_merge_temp = df_merge_temp.iloc[:, 0:4]
        df_merge_temp = df_merge_temp.rename(index=str, columns={"decision_x": "decision"})
        df_merge_final = df_merge_final.append(df_merge_temp, ignore_index=True)
    #print(df_merge_final)
    return(df_merge_final)

def create_bayes_tables(df_tastes, df_clothes):
    print("coucou")

if __name__ == "__main__":

    df = pd.read_csv("../database/formulaire_test_2.csv")
    df_tastes = create_tastes_from_file(df)
    #print(df_tastes)

    file = '../database/clothes.json'
    with open(file) as train_file:
        dict_clothes = json.load(train_file)
    df_clothes = pd.DataFrame.from_dict(dict_clothes, orient='index')
    #df_clothes.reset_index(level=0, inplace=True)
    print(df_clothes)
    create_bayes_tables(df_tastes, df_clothes)
