import pandas as pd
import re
import numpy as np


if __name__ == "__main__":
    df_csv = pd.read_csv('../database/formulaire_test.csv')
    #df2 = pd.DataFrame(data=df.loc[:, ['Genre','Age']])
    #re.split('\, ', df.iloc[:, 3])
    df_tastes = pd.DataFrame(columns=["idUser", "id1", "id2", "decision"])

    for idrow, row in df_csv.iterrows():
        row = row.dropna().apply(lambda x: re.split('\, ', str(x)))
        #print(idrow)
        for colname, col in row[3:].iteritems():
            #print(colname, col)
            for cloth in col:
                df_tastes = df_tastes.append(
                    pd.Series({"idUser": int(idrow), "id1": colname, "id2": cloth, "decision": True}),
                    ignore_index=True)
    print(df_tastes)