import pymongo

client = pymongo.MongoClient("mongodb+srv://bertkrc:jrsTA1JyDRKXw1IQ@cluster0.t4gqhpn.mongodb.net/?retryWrites=true&w=majority")  # MongoDB sunucu adresini ve portunu buraya girin
database = client["folglad"]  # Kullanmak istediğiniz veritabanını seçin
reporstdb = database["reports"]  # Kullanmak istediğiniz koleksiyonu seçin
admindb = database["admins"]  
ownerdb = database["owners"]

result = []


results = reporstdb.find_one({"id"})
for result in results:
    print(result)