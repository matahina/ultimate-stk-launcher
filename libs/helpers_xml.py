# -*- coding: utf-8 -*-

# STK special XML handling

def parser_of_the_universe(my_string):
    new_good_string = ""
    for char in my_string:
        if ord(char) >= 128 or char in '&<>" ':
            new_good_string+=f"&#x{ord(char):X};"
        else:
            new_good_string+=char
    return new_good_string
