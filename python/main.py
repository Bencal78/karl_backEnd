import sys
import variables
sys.path.append(variables.DATABASE)
import python_functions.Outfit.outfit as outfit


if __name__ == '__main__':
    file = open("{}data.json".format(variables.DATABASE))
    outfit.get_outfit()
