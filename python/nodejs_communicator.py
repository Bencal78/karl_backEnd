import sys
import json
import variables
import Outfit.outfit as outfit


def return_outfit():
    arg2 = sys.argv[2]
    clothes = json.loads(arg2)
    myoutfit_unjsoned = outfit.get_outfit(clothes["clothes"])
    myoutfit = {"clothes": myoutfit_unjsoned}
    return myoutfit

if __name__ == "__main__":
    functions = {'return_outfit': return_outfit}
    res_json = functions[sys.argv[1]]()
    print(res_json)
