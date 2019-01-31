import pandas as pdimport reimport jsonimport numpy as npfrom itertools import productdef create_tastes_from_file(df_csv):    """    :param df_csv: contains the results of the google form test    :return: a dataframe containing the results of the from idUser | id_0 | id_1 | decision (True/False)    """    """PREMIERE PARTIE : création du dataframe contenant toutes les réponses à toutes les questions"""    # récupération des colonnes pertinentes pour la création de la table    relevant_columns = df_csv.iloc[:, 3:]    df_relevant = pd.DataFrame()    # division des vetements avec les virgules    for idrow, row in relevant_columns.iterrows():        row = row.apply(lambda x: re.split('\, ', str(x)))        df_relevant = df_relevant.append(row, ignore_index=True)    # récupération de la dernière ligne du test où on a répondu à toutes les question, transformation en dictionnaire    dict_all = df_relevant.iloc[-1].to_dict()    list_all = list()    for key, value in dict_all.items():        key = [key]        list_all = list_all + (list(product(key, value)))    # création du dataframe avex toutes les réponses à toutes les questions    df_complete = pd.DataFrame(list_all, columns=["id_0", "id_1"])    df_complete["decision"] = False    """DEUXIEME PARTIE : Traduction du fichier du google form"""    # initialisation du dataframe de sortie contenant tous les goûts    df_tastes_true = pd.DataFrame(columns=["idUser", "id_0", "id_1", "decision"])    # création du dataframe avec uniquement les goûts positifs    for idrow, row in df_csv.iterrows():        row = row.dropna().apply(lambda x: re.split('\, ', str(x)))        for colname, col in row[3:].iteritems():            for cloth in col:                df_tastes_true = df_tastes_true.append(                    pd.Series({"idUser": int(idrow), "id_0": colname, "id_1": cloth, "decision": True}),                    ignore_index=True)    """TROISIEME PARTIE : Ajout des goûts à false dans le dataframe."""    df_merge_final = pd.DataFrame(columns=["idUser", "id_0", "id_1", "decision"])    for id in range(max(df_tastes_true["idUser"])):        df_merge_temp = pd.merge(df_tastes_true.loc[df_tastes_true["idUser"] == id + 1], df_complete, how="right",                                 on=['id_0', 'id_1'])        df_merge_temp["decision_x"] = df_merge_temp["decision_x"].fillna(False)        df_merge_temp["idUser"] = df_merge_temp["idUser"].fillna(id + 1)        df_merge_temp = df_merge_temp.iloc[:, 0:4]        df_merge_temp = df_merge_temp.rename(index=str, columns={"decision_x": "decision"})        df_merge_final = df_merge_final.append(df_merge_temp, ignore_index=True)        # enregitrement dans un csv    df_merge_final.to_csv("../database/formulaire_result_names.csv", sep=",")    return df_merge_finaldef create_df_clothes(clothes_df):    """    Convert a dict of clothes to a dataframe, also dummify bodypart's features    :param clothes: a dictionnary of clothes    :return:    credits : benoit leguay    """    bodypart_df = pd.get_dummies(clothes_df.bodyparts.apply(pd.Series).stack()).sum(level=0).rename(        columns=lambda x: "bp_{}".format(int(x)))    clothes_df = pd.concat([clothes_df.drop(columns=['bodyparts']), bodypart_df], axis=1)    return clothes_dfdef get_test_clothes():    """    returns clothes to run tests    :return:    """    file = '../database/clothes.json'    with open(file) as train_file:        dict_clothes = json.load(train_file)    df_clothes = pd.DataFrame(dict_clothes["clothes"])    df_clothes = create_df_clothes(df_clothes)    df_clothes.reset_index(inplace=True, drop=True)    return df_clothesdef filter_clothes_for_user(clothes, dict_bayes):    """    returns clothes that are in the tastes of the user to avoid errors    :param clothes:    :param dict_bayes:    :return:    """    clothes = clothes[clothes["_id"].isin(dict_bayes["clothes_ids"]["scores"].columns)]    clothes.reset_index(inplace=True, drop=True)    return clothesdef add_col_row_to_bayes_dict(dict_bayes, feature):    """    Ajoute une ligne et une colonne pour la feature si besoin    :param dict_bayes: dictionnaire où sont les scores et les comptes pour les features    :param feature: feature à ajouter si besoin    :return: dictionnaire avec une colonne et ligne ajoutées pour la feature d'entrée si besoin    """    if feature not in dict_bayes['scores'].columns:        #création des lignes et colonnes dans le dataframe des scores si besoin        dict_bayes['scores'][feature] = pd.Series()        new_row = pd.Series()        new_row.name = feature        dict_bayes['scores'] = dict_bayes['scores'].append(new_row)        # création des lignes et colonnes dans le dataframe des comptes si besoin        dict_bayes['counts'][feature] = pd.Series()        new_row = pd.Series()        new_row.name = feature        dict_bayes['counts'] = dict_bayes['counts'].append(new_row)    return dict_bayesdef add_to_single_dict(dict_bayes, feature_1, feature_2, decision):    """    Remplit le dictionnaire des goûts à l'aides de deux features/ids et une variable indiquant si    l'utilisateur a aimé cette association de features/ids ou non.    D'une part, le dictionnaire "counts" est incrémenté pour les valeurs des features d'entrée.    D'autre part, le dictionnaire "scores" est augmenté pour les valeurs des features d'entrée d'après la formule:    (score + {(n'a pas aimé) : 0; (a aimé) : 1}) / (compte + 1)    :param dict_bayes:    :param feature_1: valeur de la feature pour le premier vêtement    :param feature_2: valeur de la feature pour le deuxième vêtement    :param decision: booléen désignant si l'utilisateur a aimé ou non l'association de ces vêtements    :return: le dictionnaire rempli en fonction des valeurs d'entrée    """    # on ajoute les valeurs des features aux colonnes si ce n'est pas deja fait    dict_bayes = add_col_row_to_bayes_dict(dict_bayes, feature_1)    dict_bayes = add_col_row_to_bayes_dict(dict_bayes, feature_2)    # on remplit les cases vides avec des 0, au cas où des colonnes ont été ajoutées    dict_bayes["scores"] = dict_bayes["scores"].fillna(0)    dict_bayes["counts"] = dict_bayes["counts"].fillna(0)    # valeur de la variable de score dépend de la décision    score = 1 if decision else 0    # la table "counts" est incrémentée, et le "score" est augmenté ou abaissé en fonction de si l'utilisateur a aimé    # ou non l'association des features    dict_bayes["counts"][feature_1][feature_2] += 1    dict_bayes["scores"][feature_1][feature_2] = (dict_bayes["scores"][feature_1][feature_2] * (dict_bayes["counts"][feature_1][feature_2] - 1) + score) / dict_bayes["counts"][feature_1][feature_2]    dict_bayes["counts"][feature_2][feature_1] += 1    dict_bayes["scores"][feature_2][feature_1] = (dict_bayes["scores"][feature_2][feature_1] * (dict_bayes["counts"][feature_2][feature_1] - 1) + score) / dict_bayes["counts"][feature_2][feature_1]    return dict_bayesdef add_to_all_dicts(dict_bayes, clothes_1, clothes_2, decision):    """    Remplit le dictionnaire des goûts à l'aides des informations de deux vêtements et une variable indiquant si    l'utilisateur a aimé cette association ou non    :param dict_bayes: dictionnaire contenant les données de l'utilisateur relatives à l'algo Naive Bayes    :param clothes_1: dataframe contenant les informations du premier vêtement    :param clothes_2: dataframe contenant les informations du deuxieme vêtement    :param decision: booléen désignant si l'utilisateur a aimé ou non l'association de ces vêtements    :return: dictionnaire rempli à l'aide des paramètres d'entrée    """    features_names = ["colors", "fabrics", "category", "pattern"]  # liste contenant les features qui nous intéressent    for feature in features_names:  # pour toutes les features        if not(clothes_1[feature].empty | clothes_2[feature].empty):  # si les deux vêtements ont cette feature            if type(clothes_1[feature].iloc[0]) == list:  # si la feature a plusieurs valeurs                for feature_1_n in range(len(clothes_1[feature].iloc[0])): # pour toutes les valeurs des features des ..                    for feature_2_n in range(len(clothes_2[feature].iloc[0])):  # .. 2 vetements                        #on nourrit le dictionnaire avec ces features                        dict_bayes[feature] = add_to_single_dict(dict_bayes[feature], clothes_1[feature].iloc[0][feature_1_n], clothes_2[feature].iloc[0][feature_2_n], decision)            else:  # si la feature a une seule valeur                # on nourrit le dictionnaire avec cette feature                dict_bayes[feature] = add_to_single_dict(dict_bayes[feature], clothes_1[feature].iloc[0],                                                         clothes_2[feature].iloc[0], decision)    # On nourrit le dictionnaire des ids de vêtements aussi    if not (clothes_1["_id"].empty | clothes_2["_id"].empty):        dict_bayes["clothes_ids"] = add_to_single_dict(dict_bayes["clothes_ids"], clothes_1["_id"].iloc[0],            clothes_2["_id"].iloc[0], decision)    return dict_bayesdef init_bayes_dictionary():    """    création du dictionnaire pour un utilisateur    :return: le dictionnaire en question    """    # création des dictionnaires contenant les informations pour la naive bayes, pour les couleurs, matières,    # catégories, motifs, et vêtements en entier    dict_clothes_bayes = {"scores": pd.DataFrame(), "counts": pd.DataFrame()}    dict_colors = {"scores": pd.DataFrame(), "counts": pd.DataFrame()}    dict_fabrics = {"scores": pd.DataFrame(), "counts": pd.DataFrame()}    dict_categories = {"scores": pd.DataFrame(), "counts": pd.DataFrame()}    dict_pattern = {"scores": pd.DataFrame(), "counts": pd.DataFrame()}    # On met tous les dictionnaires dans un seul    dict_bayes = {"clothes_ids": dict_clothes_bayes, "colors": dict_colors, "fabrics": dict_fabrics,                  "category": dict_categories, "pattern": dict_pattern}    return dict_bayesdef create_bayes_tables_from_form(df_tastes, df_clothes):    """    Creates a dictionary containing the information for Naive BAyes algorithms from users tastes and clothes    :param df_tastes: containing the tastes of the user in the shape of : id_user | id_cloth_1 | id_clothes_2 | decision (bool)    :param df_clothes: a dataframe containing the clothes of the user with all their information    :return: a dictionnary containing all the tastes of the user    """    all_users_bayes = list()  # initialisation de la liste de sortie    for iterId in range(max(df_tastes["idUser"])):  # pour tous les utilisateurs dans df_tastes        dict_bayes = init_bayes_dictionary()  # initialisation du dictionnaire d'utilisateur        # sélection des goûts uniquement pour l'utilisateur actuel        df_user = df_tastes.loc[df_tastes["idUser"] == iterId + 1]        df_user = df_user.dropna()        #pour tous les goûts de l'utilisateur, on les enregistre dans le dictionnaire.        for id_taste, taste in df_user.iterrows():            clothes_0 = df_clothes[df_clothes['_id'] == taste["id_0"]]            clothes_1 = df_clothes[df_clothes['_id'] == taste["id_1"]]            dict_bayes = add_to_all_dicts(dict_bayes, clothes_0, clothes_1, taste["decision"])        #ajout des goûts de l'utilisateur dans le dictionnaire        all_users_bayes.append(dict_bayes)    return all_users_bayesdef save_nb_data(dict_bayes):    """    Saves the naive bayes data in json files    :param dict_bayes:    :return:    """    for key_feature_category, value_feature_category in dict_bayes.items():        for key_data, value_data in value_feature_category.items():            filename = '../database/' + key_feature_category + '_' + key_data + '.json'            value_data_json = pd.DataFrame.to_json(value_data)            with open(filename, 'w') as outfile:                json.dump(value_data_json, outfile)def load_nb_data():    """    Load the naive bayes data for one user from json files    :return:    """    dict_bayes = init_bayes_dictionary()    for key_feature_category, value_feature_category in dict_bayes.items():        for key_data, value_data in value_feature_category.items():            filename = '../database/' + key_feature_category + '_' + key_data + '.json'            dict_data = json.loads(json.load(open(filename)))            dict_bayes[key_feature_category][key_data] = pd.DataFrame.from_dict(dict_data)    return dict_bayesdef select_clothes(clothes, category):    if category == "top_1":        bp = "bp_1"        layer = 1    if category == "top_2":        bp = "bp_1"        layer = 2    if category == "top_3":        bp = "bp_1"        layer = 3    if category == "bottom":        bp = "bp_5"        layer = 1    clothes_filtered = clothes.loc[(clothes[bp] == 1) & (clothes["layer"] == layer)]    return clothes_filtereddef select_first_garment_nb_curious(dict_bayes, df_clothes):    """    Selects the first garment to be added in an outfit in a "curious" way. It will choose a garment that has not been    very warden by the user    :param dict_bayes: dictionary containing all the information about the tastes    :param df_clothes: dataframe containing the candidate clothes to be added to the outfit    :return: a dataframe of the garment that matches the best the outfit and have not been tried too much with it in    the past    """    # filtering the ids of clothes countings for those we want to make a selection    id_clothes_counts_filtered = dict_bayes["clothes_ids"]["counts"].loc[df_clothes["_id"], df_clothes["_id"]]    # summing the number of uses for every clothes ids    summed_id_clothes_counts = id_clothes_counts_filtered.sum()    # selecting the clothes that have been the less used    id_clothes_less_used = summed_id_clothes_counts[summed_id_clothes_counts == min(summed_id_clothes_counts)].index    # selecting one of those clothes and assign it to output value    garment_id = id_clothes_less_used[np.random.randint(id_clothes_less_used.shape[0])]    garment = df_clothes[df_clothes["_id"] == garment_id]    #print(garment.iloc[0].to_dict())    return garmentdef select_first_garment_nb_safe(dict_bayes, df_clothes):    n_clothes = df_clothes.shape[0]    garment_index = np.random.randint(n_clothes)    garment = df_clothes.iloc[garment_index]    #print(garment)    return garmentdef compute_garment_counts_score_by_id(id_clothes_counts, garment_id, dict_bayes):    """    update the global score of weared clothes score with score of the current garment    :param id_clothes_counts: dataframe containing global score of weared clothes    :param garment_id: string containing the id of the garment which will be used to update the counts score    :return: dataframe containg the global score of weared clothes    """    # selecting the candidate clothes in the counting of associations with outfit clothes    id_clothes_counts_filtered = dict_bayes["clothes_ids"]["counts"].loc[df_clothes["_id"]]    # counting for every garment, the number of previous associations    id_garment_counts = id_clothes_counts_filtered.loc[:, garment_id]    # adding the results to the global number of associations    id_clothes_counts = pd.concat([id_clothes_counts, id_garment_counts], axis=1,                                  join_axes=[id_clothes_counts.index])    id_clothes_counts = id_clothes_counts.sum(axis=1)    # scaling the values    if id_clothes_counts.max() != 0:        id_clothes_counts /= id_clothes_counts.max()    id_clothes_counts = 1 - id_clothes_counts    return id_clothes_countsdef compute_garment_features_score_by_id(id_clothes_scores, garment, dict_bayes, df_clothes):    """    update the global score of weared clothes score with score of features associations    :param id_clothes_scores: dataframe containing global score of features associations    :param garment: dataframe containing the garment which will be used to update the feature score    :param dict_bayes: dictionary containing all the information about the tastes    :param df_clothes: dataframe containing the candidate clothes to be added to the outfit    :return: dataframe containg the global score of features associations    """    features_names = ["colors", "fabrics", "category", "pattern"]  # features to be iterated on    for key, value in dict_bayes.items():  # iterating for every feature type        if key in features_names:  # filter the features we are interested in (colors, fabrics,..)            if not garment[key].empty:  # check if the garment has a value for this feature                if type(garment[key].iloc[0]) == list:  # check whether the garment has several values for the feature                    for feature in garment[key].iloc[0]:  # for every value of the feature                        for id_clothes_candidate_scores in id_clothes_scores.index:  # for every candidate garment id                            # check if the candidate garment has several values                            if type(df_clothes[df_clothes["_id"] == id_clothes_candidate_scores][key].iloc[0]) == list:                                for feature_2 in \                                        df_clothes[df_clothes["_id"] == id_clothes_candidate_scores][key].iloc[                                            0]:  # for every value of the feature                                    # updating values for the feature score                                    id_clothes_scores.loc[id_clothes_candidate_scores, "scores"] += value["scores"].loc[                                        feature_2, feature]                                    id_clothes_scores.loc[id_clothes_candidate_scores, "n_scores"] += 1                            else:  # if only one value for the feature                                # updating values for the feature score                                id_clothes_scores.loc[id_clothes_candidate_scores, "scores"] += value["scores"].loc[                                        df_clothes[df_clothes["_id"] == id_clothes_candidate_scores][key], feature].iloc[                                    0].iloc[0]                                id_clothes_scores.loc[id_clothes_candidate_scores, "n_scores"] += 1                else:  # if only one value for the feature                    # updating values for the feature score                    for id_clothes_candidate_scores in id_clothes_scores.index:                        id_clothes_scores.loc[id_clothes_candidate_scores, "scores"] += value["scores"].loc[                                df_clothes[df_clothes["_id"] == id_clothes_candidate_scores][key], garment[key]].iloc[                            0].iloc[0]                        id_clothes_scores.loc[id_clothes_candidate_scores, "n_scores"] += 1    return id_clothes_scoresdef select_best_garment_with_score_curious(df_clothes, id_clothes_counts, id_clothes_scores):    """    compute the total scores for all the candidate clothes and select the one with the best score    :param df_clothes: dataframe containing all the candidate clothes    :param id_clothes_counts: dataframe containing the count scores for every clothes    :param id_clothes_scores: dataframe containing the feature scores for each clothes    :return: dataframe containing the garment with the best score    """    # scaling features scores    id_clothes_scores["scores"] = id_clothes_scores["scores"] / id_clothes_scores["n_scores"]    id_clothes_scores = id_clothes_scores.drop(["n_scores"], axis=1)    # creating the total scores dataframe    id_clothes_total = pd.concat([id_clothes_counts, id_clothes_scores], axis=1,                                 join_axes=[id_clothes_counts.index])    # compute the total score    id_clothes_total["total"] = (1 / 3) * id_clothes_total[0] + (2 / 3) * id_clothes_total["scores"]    max_score = id_clothes_total["total"].max()    # get the id of the garment with the best score take a random one if there are several clothes with the same score    random_index = np.random.randint(id_clothes_total[id_clothes_total["total"] == max_score].shape[0])    best_score_id = id_clothes_total[id_clothes_total["total"] == max_score][random_index].index[0]    #get the garment who has the id with the best score    garment = df_clothes[df_clothes["_id"] == best_score_id]    return garmentdef select_other_garment_nb_curious(dict_bayes, df_clothes, outfit):    """    :param dict_bayes: dictionary containing all the information about the tastes    :param df_clothes: dataframe containing the candidate clothes to be added to the outfit    :param outfit: list of clothes that are already in the outfit    :return: dataframe containing the garment to be added to the outfit    """    # ids of candidate clothes    id_clothes_filtered = dict_bayes["clothes_ids"]["counts"].loc[df_clothes["_id"]].index    # count score for each candidate clothes initialized to 0    id_clothes_counts = pd.DataFrame(0, index=id_clothes_filtered, columns=["init"])    # feature score for each candidate clothes initialized to 0    id_clothes_scores = pd.DataFrame(0, index=id_clothes_filtered, columns=["scores", "n_scores"])    for garment in outfit:  # for every outfit clothes        # computing the counting scores for every clothes        id_clothes_counts = compute_garment_counts_score_by_id(id_clothes_counts, garment["_id"], dict_bayes)        # computing the feature scores for every clothes        id_clothes_scores = compute_garment_features_score_by_id(id_clothes_scores, garment, dict_bayes, df_clothes)    garment = select_best_garment_with_score_curious(df_clothes, id_clothes_counts, id_clothes_scores)    return garmentdef select_best_garment_with_score_safe(df_clothes, id_clothes_counts):    max_score = id_clothes_counts.max()    random_index = np.random.randint(id_clothes_counts[id_clothes_counts == max_score].shape[0])    best_score_id = id_clothes_counts[id_clothes_counts == max_score].index[random_index]    # get the garment who has the id with the best score    garment = df_clothes[df_clothes["_id"] == best_score_id]    return garmentdef compute_safe_garment_counts_score_by_id(id_clothes_counts, garment_id, dict_bayes):    # selecting the candidate clothes in the counting of associations with outfit clothes    id_clothes_counts_filtered = dict_bayes["clothes_ids"]["scores"].loc[id_clothes_counts.index, garment_id]    # counting for every garment, the number of previous associations    #id_garment_counts = id_clothes_counts_filtered.loc[:, garment_id]    # adding the results to the global number of associations    id_clothes_counts = pd.concat([id_clothes_counts, id_clothes_counts_filtered], axis=1,                                  join_axes=[id_clothes_counts.index])    id_clothes_counts = id_clothes_counts.sum(axis=1)    return id_clothes_countsdef select_other_garment_nb_safe(dict_bayes, df_clothes, outfit):    # ids of candidate clothes    id_clothes_filtered = dict_bayes["clothes_ids"]["scores"].loc[df_clothes["_id"]].index    # count score for each candidate clothes initialized to 0    id_clothes_scores = pd.DataFrame(0, index=id_clothes_filtered, columns=["init"])    for garment in outfit:  # for every outfit clothes        # computing the counting scores for every clothes        id_clothes_scores = compute_safe_garment_counts_score_by_id(id_clothes_scores, garment["_id"], dict_bayes)    garment = select_best_garment_with_score_safe(df_clothes, id_clothes_scores)    return garmentdef select_garment_nb(dict_bayes, df_clothes, first_garment = False, outfit = [], choice_mode = "curious"):    """    Select a garment to add to an outfit in a "curious" way. It will choose a garment that has not been tried too much    with the clothes already present in the outfit, but has features compatible    :param dict_bayes: dictionary containing all the information about the tastes    :param df_clothes: dataframe containing the candidate clothes to be added to the outfit    :param first_garment: boolean indicating whether the garment to be selected is the first of the outfit    :param outfit: list of clothes that are already in the outfit    :return: a dataframe of the garment that matches the best the outfit and have not been tried too much with it in    the past    """    # if the garment to be added to the outfit is the first one    if first_garment:        garment = select_first_garment_nb_curious(dict_bayes, df_clothes) \            if choice_mode == "curious" \            else select_first_garment_nb_safe(dict_bayes, df_clothes)    # if the garment to be added is not the first one    else:        garment = select_other_garment_nb_curious(dict_bayes, df_clothes, outfit) \            if choice_mode == "curious" \            else select_other_garment_nb_safe(dict_bayes, df_clothes, outfit)    return garmentdef create_outfit_nb(dict_bayes, df_clothes, choice_mode="curious"):    """    Selects an outfit creation algorithm and returns an outfit made by one of these    :param user:    :param choice_mode:    :return:    """    outfit = []    first_garment_random_index = np.random.randint(2)    if first_garment_random_index == 0:        # premiere fringue est haut        clothes_selected = select_clothes(df_clothes, "top_1")    else:        # premiere fringue en bas        clothes_selected = select_clothes(df_clothes, "bottom")    first_garment = select_garment_nb(dict_bayes, clothes_selected, first_garment=True, choice_mode=choice_mode)    outfit.append(first_garment)    if first_garment_random_index == 0:        clothes_selected = select_clothes(df_clothes, "bottom")    else:        clothes_selected = select_clothes(df_clothes, "top_1")    second_garment = select_garment_nb(dict_bayes, clothes_selected, outfit=outfit, choice_mode=choice_mode)    outfit.append(second_garment)    third_garment_random_index = np.random.randint(2)    if third_garment_random_index == 0:        clothes_selected = select_clothes(df_clothes, "top_2")        third_garment = select_garment_nb(dict_bayes, clothes_selected, outfit=outfit, choice_mode=choice_mode)        outfit.append(third_garment)        fourth_garment_random_index = np.random.randint(2)        if fourth_garment_random_index == 0:            clothes_selected = select_clothes(df_clothes, "top_3")            fourth_garment = select_garment_nb(dict_bayes, clothes_selected, outfit=outfit, choice_mode=choice_mode)            outfit.append(fourth_garment)    for idx, garment in enumerate(outfit):        if isinstance(garment, pd.DataFrame):            outfit[idx] = garment.iloc[0].to_dict()        else:            outfit[idx] = garment.to_dict()    print(outfit)    return outfitif __name__ == "__main__":    '''    df_form = pd.read_excel("../database/formulaire_test_id.xlsx")    #print(df_form)    df_tastes = create_tastes_from_file(df_form)    '''    '''    df_tastes = pd.read_csv("../database/formulaire_result_ids.csv", index_col = 0)        df_clothes = get_test_clothes()    #print(df_clothes)    dict_bayes = create_bayes_tables_from_form(df_tastes, df_clothes)    save_nb_data(dict_bayes[0])    '''    dict_bayes = load_nb_data()    df_clothes = get_test_clothes()    df_clothes = filter_clothes_for_user(df_clothes, dict_bayes)    outfit = create_outfit_nb(dict_bayes, df_clothes)    id_clothes_counts = dict_bayes["clothes_ids"]["counts"].sum()    id_clothes_counts_scores = 1 - id_clothes_counts / id_clothes_counts.max()    id_clothes_less_used = id_clothes_counts[id_clothes_counts == min(id_clothes_counts)].index    #lol = id_clothes_less_used[np.random.randint(id_clothes_less_used.shape[0])]    #print(id_clothes_counts_scores)    #print(df_clothes)    #print(dict_bayes)