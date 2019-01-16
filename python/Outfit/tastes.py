import pandas as pdimport reimport jsonimport numpy as npfrom itertools import productdef create_tastes_from_file(df_csv):    """    :param df_csv: contains the results of the google form test    :return: a dataframe containing the results of the from idUser | id_0 | id_1 | decision (True/False)    """    """PREMIERE PARTIE : création du dataframe contenant toutes les réponses à toutes les questions"""    # récupération des colonnes pertinentes pour la création de la table    relevant_columns = df_csv.iloc[:, 3:]    df_relevant = pd.DataFrame()    # division des vetements avec les virgules    for idrow, row in relevant_columns.iterrows():        row = row.apply(lambda x: re.split('\, ', str(x)))        df_relevant = df_relevant.append(row, ignore_index=True)    # récupération de la dernière ligne du test où on a répondu à toutes les question, transformation en dictionnaire    dict_all = df_relevant.iloc[-1].to_dict()    list_all = list()    for key, value in dict_all.items():        key = [key]        list_all = list_all + (list(product(key, value)))    # création du dataframe avex toutes les réponses à toutes les questions    df_complete = pd.DataFrame(list_all, columns=["id_0", "id_1"])    df_complete["decision"] = False    """DEUXIEME PARTIE : Traduction du fichier du google form"""    # initialisation du dataframe de sortie contenant tous les goûts    df_tastes_true = pd.DataFrame(columns=["idUser", "id_0", "id_1", "decision"])    # création du dataframe avec uniquement les goûts positifs    for idrow, row in df_csv.iterrows():        row = row.dropna().apply(lambda x: re.split('\, ', str(x)))        for colname, col in row[3:].iteritems():            for cloth in col:                df_tastes_true = df_tastes_true.append(                    pd.Series({"idUser": int(idrow), "id_0": colname, "id_1": cloth, "decision": True}),                    ignore_index=True)    """TROISIEME PARTIE : Ajout des goûts à false dans le dataframe."""    df_merge_final = pd.DataFrame(columns=["idUser", "id_0", "id_1", "decision"])    for id in range(max(df_tastes_true["idUser"])):        df_merge_temp = pd.merge(df_tastes_true.loc[df_tastes_true["idUser"] == id + 1], df_complete, how="right",                                 on=['id_0', 'id_1'])        df_merge_temp["decision_x"] = df_merge_temp["decision_x"].fillna(False)        df_merge_temp["idUser"] = df_merge_temp["idUser"].fillna(id + 1)        df_merge_temp = df_merge_temp.iloc[:, 0:4]        df_merge_temp = df_merge_temp.rename(index=str, columns={"decision_x": "decision"})        df_merge_final = df_merge_final.append(df_merge_temp, ignore_index=True)        # enregitrement dans un csv    df_merge_final.to_csv("../database/formulaire_result_names.csv", sep=",")    return df_merge_finaldef create_bayes_tables(df_tastes, df_clothes):    #for iterId in range(max(df_tastes["idUser"]) + 1):    iterId = 0    df_user = df_tastes.loc[df_tastes["idUser"] == iterId + 1]if __name__ == "__main__":    df_form = pd.read_excel("../database/formulaire_test_id.xlsx")    #print(df_form)    df_tastes = create_tastes_from_file(df_form)    #df_form2 = pd.read_csv("../database/formulaire_test_2.csv")    #df_tastes = create_tastes_from_file(df_form)    """    df_tastes = pd.read_csv("../database/formulaire_result_ids.csv")    file = '../database/clothes.json'    with open(file) as train_file:        dict_clothes = json.load(train_file)    df_clothes = pd.DataFrame.from_dict(dict_clothes, orient='index')    #df_clothes.reset_index(level=0, inplace=True)    #print(df_clothes)    create_bayes_tables(df_tastes, df_clothes)"""