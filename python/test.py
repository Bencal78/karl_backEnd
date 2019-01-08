import sys

def test():
	return "works on python"

if __name__ == "__main__":
    functions = {'test': test}
    res_json = functions[sys.argv[1]]()
    print(res_json)
