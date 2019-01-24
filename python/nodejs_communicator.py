import sys
import json
import Outfit.outfit as outfit
import Outfit.reinforcement_learning as rl


def return_outfit():
    #arg2 contient les vetements de l'utilisateur spécifié dans la requete, on dirait un json mais c'est un string
    arg2 = sys.argv[2]
    #c'est pourquoi on utilise la fonction json.loads pour transformer la string en json
    clothes = json.loads(arg2)
    #on veut envoyer une list et pas un dictionnary, du coup on envoit clothes["clothes"] et pas juste clothes.
    outfits = outfit.create_outfit(clothes["clothes"])
    return outfits


if __name__ == "__main__":

    functions = {'return_outfit': return_outfit,
                 'return_outfit_rl': rl.return_outfit}

    res_json = functions[sys.argv[1]]()

    print({"outfit": res_json})
