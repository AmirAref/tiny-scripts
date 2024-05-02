#!/usr/bin/python3
from argparse import ArgumentParser
from enum import StrEnum, auto
from pathlib import Path
from typing import Union
from pandas import DataFrame, read_csv
from pydantic import BaseModel, Field
from colorama import Style, Fore, Back

parser = ArgumentParser(
        prog='score calculator helper',
        description="a script to help calculating score of students and put the mon excel file",
        )

parser.add_argument('-f', '--file', type=Path, required=True)

class Question(BaseModel):
    name : str
    score : int | None = Field(default=None, ge=0)


questions_list = [
        Question(name="1"),
        Question(name="2-a"),
        Question(name="2-b"),
        Question(name="2-c"),
        Question(name="3"),
        Question(name="4"),
        Question(name="5"),
        Question(name="6"),
        Question(name="7"),
    ]

class StudentScore(BaseModel):
    name : str
    scores : list[Question]
    total : int

def calcuate(name : str, qs : list[Question]) -> StudentScore:
    scores : list[Question] = []
    n = len(qs)
    total = 0
    i=0
    while(i < n):
        try:
            q = qs[i].model_copy()
            score : str | int = input(Fore.LIGHTBLUE_EX + f"Enter score for question {q.name} (Enter for 10) : " + Style.RESET_ALL).strip()
            if not score:
                score = 10
            q.score = int(score)
            scores.append(q)
        except ValueError:
            print(Fore.RED + "invalid number, trying again ..." + Style.RESET_ALL)
            continue

        i+=1
    # show result
    total = sum([q.score for q in scores if q.score is not None])
    #clear_console()
    print(Fore.GREEN, "Total score of " + Fore.BLUE +name + Fore.GREEN + " is" + Fore.BLUE, total, Style.RESET_ALL)

    # save score
    return StudentScore(name=name, scores = scores, total=total)


def main():

    # check excel file exists or not
    args = parser.parse_args()
    dataframe_file = Path(args.file)
    if not dataframe_file.exists():
        # create new dataframe 
        fields = list(StudentScore.model_fields.keys())
        fields.remove('scores')
        columns = fields[:1] + [q.name for q in questions_list] + fields[1:]
        df = DataFrame(columns=columns, data=[])
    else:
        # load old df file
        df = read_csv(dataframe_file)
    
    name = input(Fore.CYAN + "Enter the name of student : " + Style.RESET_ALL)
    if not name:
        raise ValueError(Fore.RED + "name can't be empty!" + Style.RESET_ALL)


    student_score = calcuate(name=name, qs = questions_list)
    student_data : dict[str, Union[str, int, None]]  = {
            'name':student_score.name,
            }
    for q in student_score.scores:
        student_data[q.name] = q.score
    student_data['total'] = student_score.total

    n = len(df.index)
    df.loc[n] = student_data
    # export df
    df.to_csv(dataframe_file, index=False)


if __name__ == "__main__":
    main()
