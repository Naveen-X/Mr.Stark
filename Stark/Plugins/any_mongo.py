import re
import pymongo
from time import sleep
from bson import ObjectId
from Stark import error_handler
from pyrogram import Client as app, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dic = {}

def mongo_keyboard(id_):
    mongo_keyboard_ = InlineKeyboardMarkup(
        [[InlineKeyboardButton("MongoDB", callback_data="mongo_"+f"[{id_}]")]])
    return mongo_keyboard_


@app.on_message(filters.command("showdb"))
@error_handler
def start_command(client, message):
    if dic.get(str(message.from_user.id)) is not None:
        message.reply_text(
            "Welcome to My Bot! You can start interacting with the bot.", reply_markup=mongo_keyboard(message.from_user.id))
    else:
        message.reply_text(
            "use /adddb [mongo uri]")
@app.on_message(filters.command("adddb"))
@error_handler
def start_command(client, message):
    db = message.text.split(" ")[1]
    dic[str(message.from_user.id)] = db
    message.reply_text("Done!")

    

def mongo_keyboard(id_):
    mongo_keyboard_ = InlineKeyboardMarkup(
        [[InlineKeyboardButton("MongoDB", callback_data="mongo_"+f"[{id_}]")]])
    return mongo_keyboard_
  
pattern = re.compile(r".*\[(\d+)\].*")
@app.on_callback_query(filters.regex(pattern))
def button_callback(client, callback_query):
    if f"[{callback_query.from_user.id}]" in str(callback_query.data):
        try:
            mongo_uri = dic.get(str(callback_query.from_user.id))
            if mongo_uri:
                if callback_query.data.startswith("mongo_"):
                    # sleep(2)
                    change_message_to_list_db(callback_query,mongo_uri)
                if callback_query.data.startswith("db_"):
                    # sleep(2)
                    db_name = callback_query.data.split("db_")[1]
                    show_collection(callback_query, db_name,mongo_uri)
                if "|:|" in callback_query.data:
                    # sleep(2)
                    coll, db = callback_query.data.split("|:|")
                    show_docs(callback_query, db, coll,mongo_uri)
                if "|_|" in callback_query.data:
                    # sleep(2)
                    coll, db, _id = callback_query.data.split("|_|")
                    show_fukindata(callback_query, coll, db, _id,mongo_uri)
            else:
                print(dic.get(str(callback_query.from_user.id)))
        except Exception as e:
            print(e)
            
    else:
        print(f"[{callback_query.from_user.id}]" in str(callback_query.data))


def change_message_to_list_db(callback_query,mongo_uri):
    try:
        mongo_client = pymongo.MongoClient(mongo_uri)
        id = f"[{callback_query.from_user.id}]"
        # reply_markup=mongo_keyboard)
        callback_query.message.edit("Please wait!",)
        database_names = mongo_client.list_database_names()
        k = []
        for name in database_names:
            k.append([InlineKeyboardButton(name, callback_data=f"db_{name}"+id)])
        # k.append([InlineKeyboardButton("Go Back <-", callback_data=f"mongo_")])
        kb = InlineKeyboardMarkup(k)
        sleep(2)
        callback_query.message.edit("Select db to get Coll:", reply_markup=kb)
    except:
        # callback_query.answer("An error occured",show_alert=True)
        sleep(2)
        callback_query.message.edit(
            "Start Interacting with me", reply_markup=mongo_keyboard(callback_query.from_user.id))


def show_collection(callback_query, db_name,mongo_uri):
    try:
        id = f"[{callback_query.from_user.id}]"
        db_name = db_name.replace(f"[{callback_query.from_user.id}]","")
        mongo_client = pymongo.MongoClient(mongo_uri)
        callback_query.message.edit(f"Loading collection: {db_name}")
        database = mongo_client[db_name]
        collection_names = database.list_collection_names()
        k = []
        for collection_name in collection_names:
            k.append([InlineKeyboardButton(collection_name,
                                           callback_data=f"{collection_name}|:|{db_name}"+id)])
        k.append([InlineKeyboardButton("Go Back <-", callback_data=f"mongo_"+id)])
        kb = InlineKeyboardMarkup(k)
        sleep(2)
        callback_query.message.edit("Select db to get List:", reply_markup=kb)
    except Exception as e:
        print(e)
        # callback_query.answer("An error occured",show_alert=True)
        sleep(2)
        change_message_to_list_db(callback_query,mongo_uri)


def show_docs(callback_query, db, coll,mongo_uri):
    try:
        id = f"[{callback_query.from_user.id}]"
        db = db.replace(f"[{callback_query.from_user.id}]","")
        coll = coll.replace(f"[{callback_query.from_user.id}]","")
        mongo_client = pymongo.MongoClient(mongo_uri)
        callback_query.message.edit(f"Loading Documents from {coll} in {db}")
        database = mongo_client[db]
        collection = database[coll]
        documents = collection.find()
        k = []
        for document in documents:
            k.append([InlineKeyboardButton(document['_id'],
                                           callback_data=f"{coll}|_|{db}|_|{document['_id']}"+id)])
        k.append([InlineKeyboardButton(
            "Go Back <-", callback_data=f"db_{db}"+id)])
        kb = InlineKeyboardMarkup(k)
        sleep(2)
        callback_query.message.edit("Select db to get List:", reply_markup=kb)
    except:
        # callback_query.answer("An error occured",show_alert=True)
        sleep(2)
        show_collection(callback_query, db,mongo_uri)


def show_fukindata(callback_query, collection, db, _id,mongo_uri):
    db = db.replace(f"[{callback_query.from_user.id}]","")
    collection = collection.replace(f"[{callback_query.from_user.id}]","")
    _id = _id.replace(f"[{callback_query.from_user.id}]","")
    mongo_client = pymongo.MongoClient(mongo_uri)
    database = mongo_client[db]
    col = database[collection]
    document = col.find_one({"_id": _id})
    if document:
        callback_query.message.reply_text(f"Document details:\n\n{document}")
    else:
        doc_id = ObjectId(_id)
        document = col.find_one({"_id": doc_id})
        if document:
            callback_query.message.reply_text(f"Document details:\n\n{document}")
        else:
            document = col.find_one({"_id": int(_id)})
            if document:
                callback_query.message.reply_text(
                    f"Document details:\n\n{document}")
            else:
                callback_query.message.reply_text("Document not found.")
