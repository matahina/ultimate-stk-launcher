# -*- coding: utf-8 -*-


def break_line(long_string,cut_length):
    trigger_a = False
    trigger_b = False
    if len(long_string)>cut_length:
        while not trigger_b:
            if not trigger_a:
                pos = long_string.find(" ", cut_length)
                long_string = long_string[0:pos]+"\n"+long_string[pos+1:]
                trigger_a=True
            else:
                pos = long_string.rfind("\n")
                if len(long_string)-pos > cut_length:
                    pos2 = long_string.find(" ", pos+cut_length)
                    long_string = long_string[0:pos2]+"\n"+long_string[pos2+1:]
                else:
                    trigger_b=True
    return long_string

def quantity(number, action):
    if number == 0:
        result = "No addon to "+action
    else:
        result = str(number)+" addon to "+action
    if action == "install":
        result = result.replace("addon","new addon")
    if number>1:
        result = result.replace("addon","addons")
    return result+" "

def parser_of_the_year(my_string):
    not_illegal='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_,".@()[]{{|}}*+'
    new_good_string = ""
    for char in my_string:
        if char in not_illegal:
            new_good_string+=char
        else:
            new_good_string+="&#x"+hex(ord((char)))[2:].upper()+";"
    return new_good_string
