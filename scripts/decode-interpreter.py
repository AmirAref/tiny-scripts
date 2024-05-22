#!/usr/bin/env python

from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
import ast


def dictionary(astring) -> dict[str, str]:
    try:
        return ast.literal_eval(astring)
    except SyntaxError:
        raise ArgumentTypeError("your define's syntax is not correct!")


parser = ArgumentParser(
    prog="Decode-Python-Interpreter",
    description='this is a command line tool to use C++ like "define" in python code.',
)

parser.add_argument(
    "file",
    help="path of the your regular python code",
    type=Path,
)
parser.add_argument(
    "-t",
    "--tab",
    help="size of spaces in a tab for replacing the TAB define (default=4)",
    default=4,
    type=int,
)
parser.add_argument(
    "-d",
    "--define",
    help="a dictionay of defines characters. example : \"{'if':'li', 'for':'lil', 'TAB':'lili'}\"\nuse TAB to define the tabs, default tab size 4 spaces, but if you want to change it, pass the -t option.",
    type=dictionary,
    required=True,
)


def main():
    args = parser.parse_args()
    python_file: Path = args.file
    tab_size: int = args.tab
    defines: dict[str, str] = args.define
    # example : {"TAB": "fff", ":": "ff", "for": "ffff", "if": "fl"}

    # open file
    with open(python_file) as file:
        raw_python_code = file.read()

    # add hint comments
    output_code = "#----------defines----------\n"
    output_code += "\n".join(["{} -> {}".format(key, defines[key]) for key in defines])
    output_code += "\n#--------end-defines-------\n\n"
    output_code += "#---------code-block---------\n"
    # replace defines
    output_code_block = raw_python_code
    for key, value in defines.items():
        if key == "TAB":
            key = tab_size * " "
        output_code_block = output_code_block.replace(key, value)

    # append code block
    output_code += output_code_block
    output_code += "\n#------end-code-block-------"
    # save output code
    output_file_path = python_file.name.rstrip(".py") + ".py_defined"
    with open(output_file_path, "w") as file:
        file.write(output_code)

    print(f"output file saved into : {output_file_path}")


if __name__ == "__main__":
    main()
