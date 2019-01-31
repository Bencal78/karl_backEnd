import sys
import Outfit.outfit as outfit
import Outfit.reinforcement_learning as rl


def return_outfit():
    """
    arg2 contient les vetements de l'utilisateur spécifié dans la requete, on dirait un json mais c'est un string
    c'est pourquoi on utilise la fonction json.loads pour transformer la string en json
    on veut envoyer une list et pas un dictionnary, du coup on envoit clothes["clothes"] et pas juste clothes.
    :return:
    """
    outfits = outfit.create_outfit()
    return outfits


if __name__ == "__main__":

    functions = {'return_outfit': return_outfit,
                 'return_outfit_rl': rl.return_outfit,
                 'return_outfit_quizz_start': return_outfit}

    res_json = functions[sys.argv[1]]()
    print(res_json)
