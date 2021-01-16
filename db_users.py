from pymongo import MongoClient
from datetime import datetime
import random

cluster = MongoClient("localhost", 27017)

db = cluster["tgbot"]

collection = db["users"]


def check_and_add_user(message):
    if db.users.find_one({'user_id': message.from_user.id}) == None:
        new_user = {
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'user_id': message.from_user.id,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'words': []
        }
        db.users.insert_one(new_user)
    return


def add_word_in_bd(word, translate, user_id):
    results = collection.find_one({'user_id': user_id})
    dom = ''
    for result in results:
        dom = result
    if word.lower() in dom:
        pass
    else:
        word = word.lower()
        translate = translate.lower()
        list_of_words = {word: translate}
        collection.update_one({'user_id': user_id}, {'$push': {'words': list_of_words}})


def take_word(user_id):
    results = collection.find_one({'user_id': user_id})
    list_of_words = results['words']
    num_of_words = 0
    for i in list_of_words:
        num_of_words += 1
    num = random.randrange(0, num_of_words)
    words = list_of_words[num]
    return words
