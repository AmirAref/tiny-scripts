import sys
from colorama import Fore, Style

def get_test_list(message):
    # get list
    test_list = input(message)
        # make correct list
    test_list = tuple(map(int, test_list.split() ))
    if not test_list:
        raise ValueError("List is empty !")

    return test_list

def read_from_file(file_name):
    # read the file content
    with open(file_name, 'r') as file:
        data = file.read().split('\n')
    # first line is correct answers
    correct_list = tuple(map(int, data[0].split() ))
    user_list = tuple(map(int, data[1].split() ))
    
    return correct_list, user_list


def get_user_input(correct_list = None):
    
    
    # get correct answers
    if not correct_list:
        correct_list = get_test_list("Enter the correct answers : ")
        
        # correct list confirmation
        print("\n".join((f"{i+1}. {j}" for i,j in enumerate(correct_list))))
        
        while True:
            # get confirmation
            confirm = input("\n\nAre you confirm the correct list answers (y/n, Enter=y) ? ")
            if confirm.lower() == 'n':
                return get_user_input()
            elif confirm.lower() in ('', 'y'):
                break

    # get user answers
    user_list = get_test_list("Enter your (user) answers (set 5 for empty answers) : ") 
    if len(user_list) != len(correct_list):
        raise ValueError("the count of correct answers and user answers if not equal !")

    # correct list confirmation
    print("\n".join((f"{i+1}. {j}" for i,j in enumerate(user_list))))

    while True:
        # get confirmation
        confirm = input("\n\nAre you confirm the user list answers (y/n, Enter=y) ? ")
        if confirm.lower() == 'n':
            return get_user_input(correct_list)
        elif confirm.lower() in ('', 'y'):
            break
    
    return correct_list, user_list

def answers_correction(correct_list, user_list):
    # calculate the score

    correct, incorrect, empty = 0, 0, 0
    for i in range(len(user_list)):
        if user_list[i] == 5:
            empty += 1
        elif user_list[i] == correct_list[i]:
            correct += 1
        else:
            incorrect += 1
    
    return correct, incorrect, empty

def calculate_score(correct, incorrect, empty):
    # calculate score
    total = correct + incorrect + empty
    score = ((3 * correct - incorrect) / (3 * total)) * 100
    # calculate positive score
    pos_score = (correct / total) * 100
    
    return score, pos_score

def main():
    # check input
    correct_list, user_list = None, None
    try:
        file_name = sys.argv[1]
        correct_list, user_list = read_from_file(file_name)
    except IndexError:
        pass
    
    # check input
    if not correct_list:
        try:
            correct_list, user_list = get_user_input()
        except Exception as e:
            return print("Error :", e)
    
    # correction answers
    correct, incorrect, empty = answers_correction(correct_list, user_list)
    print(Style.RESET_ALL)
    print(f"{Fore.BLUE}Total answers : {Fore.YELLOW}{len(correct_list)}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Correct : {correct}\n{Fore.RED}Incorrect : {incorrect}\n{Fore.YELLOW}Empty : {empty}{Style.RESET_ALL}")
    
    #calculate the score
    score, pos_score = calculate_score(correct, incorrect, empty)
    print()
    print(f"{Fore.BLUE}Your score is : {score:.2f} %{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Your score (without negative) : {pos_score:.2f} %{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
