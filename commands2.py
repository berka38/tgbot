from telegram import *
from telegram.ext import *
import pymongo

client = pymongo.MongoClient("mongodb+srv://bertkrc:jrsTA1JyDRKXw1IQ@cluster0.t4gqhpn.mongodb.net/?retryWrites=true&w=majority")  # MongoDB sunucu adresini ve portunu buraya girin
database = client["global"]  # Kullanmak istediğiniz veritabanını seçin
reporstdb = database["reports"]  # Kullanmak istediğiniz koleksiyonu seçin
admindb = database["admins"]  
ownerdb = database["owners"]

def startnew(update: Update, context: CallbackContext) -> None:
    id = ownerdb.count_documents({}) + 1
    userID = update.message.from_user.id
    groupID = update.message.chat.id
    yetkiliEkle = 1
    child = []
    values = {
        "id": id,
        "userID": userID,
        "groupID": groupID,
        "authority": yetkiliEkle,
        "child":child
    }
    ownerdb.insert_one(values)

def adminekle(update: Update, context: CallbackContext) -> None:
    id = admindb.count_documents({}) + 1
    userID = update.message.from_user.id
    ownerID = ownerdb.find_one({"userID": userID})
    groupID = update.message.chat.id
    yetkiliEkle = 0
    komut, *args = update.message.text.split()
    yetkiliID = " ".join(args)
    admins = ownerID.get("child", [])
    next_admin_id = len(admins) + 1
    values = {
        "id": id,
        "userID": userID,
        "groupID": groupID,
        "authority": yetkiliEkle,
        "yetkiliID":int(yetkiliID)
    }
    authorized = {
        "id": next_admin_id,
        "yetkiliID":int(yetkiliID),
        "authority": yetkiliEkle
    }
    query = {"userID": userID}
    updateValue = {"$addToSet": {"child": authorized}}
    admindb.insert_one(values)
    ownerdb.update_one(query, updateValue)


def adminsil(update: Update, context: CallbackContext) -> None:
    id = 1
    userID = update.message.from_user.id
    groupID = update.message.chat.id
    komut, *args = update.message.text.split()
    yetkiliID = " ".join(args)
    

def sikayet(update: Update, context: CallbackContext) -> None:
    id = 1
    userID = update.message.from_user.id
    username = update.message.from_user.username
    groupID = update.message.chat.id
    sikayetID = update.message.message_id
    sikayet = ""
    sikayetCevap = ""
    cevaplanma = 0
    raporBildiri = 0

def sikayetal(update: Update, context: CallbackContext) -> None:
    id = 1
    groupID = update.message.chat.id
    userID = update.message.from_user.id
    username = update.message.from_user.username
    sikayetID = update.message.message_id
    sikayet = ""
    groupID = update.message.chat.id

def sikayetkapat(update: Update, context: CallbackContext) -> None:
    id = 1
    groupID = update.message.chat.id
    userID = update.message.from_user.id
    sikayetCevap = ""
    cevaplanma = 0


