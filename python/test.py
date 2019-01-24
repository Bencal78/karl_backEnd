import sys
import json

if __name__ == "__main__":
    args = sys.argv[2]
    args_json = json.loads(args)
    clothes = args_json["clothes"]
    rl_cat_score = args_json["rl_cat_score"]
    last_taste = args_json["last_taste"]
    print(last_taste)