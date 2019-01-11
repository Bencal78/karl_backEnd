import sys
import json
import variables
import Outfit.outfits as outfit


def return_outfit():
    arg2 = sys.argv[2]
    clothes = json.loads(arg2)
    outfits = outfit.create_outfit(clothes["clothes"])
    return outfits

if __name__ == "__main__":
    functions = {'return_outfit': return_outfit}
    res_json = functions[sys.argv[1]]()

    print({"outfit": res_json})
