import os
import random
import discord
from replit import db
from discord.ext import commands


def value_check(id, key, default):
    """ Creates a default value if a user's value doesn't exist. \n
    id = user id | key = key you're looking for"""

    db_keys = db.keys() # lists all the database keys
    # print(db_keys)

    exists1 = False
    for i in db_keys:
        if str(id) == str(i):
            exists1 = True

    if exists1 == False: # checks if user id isn't on database
        # print(db_keys)
        db[str(id)] = {} # gives your id a value
        print("added user on database")
        # print(db[str(id)])
    # else:
        # print("user database check 1 completed")
    # this makes sure that errors won't happen

    id_value = db[str(id)] # easier to read your id's value

    exists2 = False
    for i in id_value:
        if key == i:
            exists2 = True

    if exists2 == False: # checks if key isn't on your id
        id_value[key] = default # adds a key into your id
        print(f"added key {str(key)} to user")
    # else:
        # print("user database check 2 completed")
    
    # print("List of user values:")
    # for i in id_value:
        # print(i)
    # this also makes sure that errors won't happen

def get_rank(userid):
    """ Returns the userid's rank from the leaderboard. """
    # var = db[str(ctx.author.id)]

    keys = db.keys()
    list_of_dicts = []

    for user_key in keys:
        # user_key is just a key (aka string)
        u = db[str(user_key)] # get the db value of the key
        lvl = u["lvl"]
        lvl_xp = u["lvl_xp"]
        # lvl_next = u["lvl_next"]
        # we don't need this lol

        user_dict = {
            "id": user_key,
            "level": lvl,
            "xp": lvl_xp
        } # this way, our data can be used easily

        list_of_dicts.append(user_dict)

    def myFunc(e):
        return e["level"]
    
    # orders the list
    list_of_dicts.sort(reverse=True, key=myFunc)

    iterator = 0

    for u in list_of_dicts:
        iterator += 1
        # iterates through ordered list
        # to look for matching user
        if str(u["id"]) == str(userid):
            return iterator

    """

    lvl = current level
    lvl_xp = current xp
    lvl_next = how much xp you need for next level

    """

def progress_bar(current, goal):
    done = current / goal
    # left = goal - done

    print(done)
    
    percent_done = round(done * 100)
    percent_left = round(100 - done)

    print(percent_done, percent_left)

    done_10 = round(percent_done / 10)
    left_10 = round(percent_left / 10)

    print(done_10, left_10)

    while done_10 + left_10 > 10:
        left_10 -= 1
    
    # txt.replace("bananas", "apples")
    # replace all bananas to apples

    string = ""

    for i in range(1, done_10 + 1):
        if i != 1:
            string += "<:2_green_bar:841292517307973632>"
        else:
            string += "<:3_left_green_bar:841292517156323369>"
    
    for i in range(1, left_10 + 1):
        if i != (left_10):
            string += "<:2_white_bar:841294390055796756>"
        else:
            string += "<:1_right_white_bar:841292517123031070>"
    
    # replace_1 = string.replace("1", "<:2_green_bar:841292517307973632>")
    # replace_0 = replace_1.replace("0", "<:2_white_bar:841294390055796756>")

    return string