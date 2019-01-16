#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 15:33:50 2019

@author: benoit
"""

import pandas as pd 
import re
from itertools import product


if __name__ == "__main__":
    #on choppe les données qui nous intéressent, les colonnes qui nous intéressent et on crée le dataframe
    df = pd.read_csv("../database/formulaire_test_2.csv")
    relevant_columns = df.iloc[:, 3:]
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
    df_complete["taste"] = False
    print(df_complete)
