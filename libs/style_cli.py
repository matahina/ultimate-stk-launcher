import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def output_title(text, level):
    if level == 1:
        print(color.PURPLE + color.BOLD + text.upper() + color.END)
    if level == 2:
        print(color.GREEN + text.upper() + color.END)

def prompt(text, important = False):
    if important:
        print(color.UNDERLINE + color.YELLOW + text + color.END)
    else:
        print(color.UNDERLINE + text + color.END)
