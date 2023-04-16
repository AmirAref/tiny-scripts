import sys

def test_list_gen(start, end, step , level=1
     ):
         if level > step :
             raise ValueError("the level can't be bigger than step !")
         test_list = list(range(start+level-1, end+1, step))
         return test_list

def main():
    try:
        start, end, step, level = map(int, sys.argv[1:5])
    except (IndexError, ValueError):
        return print("please give the arguments : start, end, step, level as Integer format")

    # get test list
    test_list = test_list_gen(start, end, step, level)
    print(test_list)
    print(f"\n\nCount of tests : {len(test_list)}")


if __name__ == "__main__":
    main()
