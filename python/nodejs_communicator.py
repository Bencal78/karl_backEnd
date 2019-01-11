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
    print("eee")
    return
    functions = {'return_outfit': return_outfit}
    try:
        res_json = functions[sys.argv[1]]()
    except Exception as e:
            print(e)
    print({"outfit": res_json})
