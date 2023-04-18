from colorama import Fore, Style
def main():
	#get the data input
	correct = int(input(f"{Fore.GREEN}correct answers : {Style.RESET_ALL}"))
	incorrect = int(input(f"{Fore.RED}incorrect answers : {Style.RESET_ALL}"))
	empty = int(input("empty answers : "))
	
	#calculate the score
	total = correct + incorrect + empty
	score = ((3 * correct - incorrect) / (3 * total)) * 100
	# calculate positive score
	pos_score = (correct / total) * 100
	
	score = round(score, 2)
	pos_score = round(pos_score, 2)
	print(f"{Fore.GREEN}Your score is : {score:.2f} %{Style.RESET_ALL}")
	print(f"{Fore.BLUE}Your score (without negative) : {pos_score:.2f} %{Style.RESET_ALL}")
	
	
if __name__ == "__main__":
	main()
