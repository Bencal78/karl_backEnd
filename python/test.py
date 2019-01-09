import sys
import json

def test():
	return "works on python"

if __name__ == "__main__":
    #functions = {'test': test}
    #res_json = functions[sys.argv[1]]()

    clothes = json.loads(sys.argv[2])
    print(clothes["clothes"][2]["bodyparts"])
    #print(sys.argv[2][:3])