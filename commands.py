from telegram import *
from telegram.ext import *
import pymongo

client = pymongo.MongoClient("mongodb+srv://bertkrc:jrsTA1JyDRKXw1IQ@cluster0.t4gqhpn.mongodb.net/?retryWrites=true&w=majority")  # MongoDB sunucu adresini ve portunu buraya girin
database = client["folglad"]  # Kullanmak istediğiniz veritabanını seçin
reporstdb = database["reports"]  # Kullanmak istediğiniz koleksiyonu seçin
admindb = database["admins"]  
ownerdb = database["owners"]

şikayetler = [

]







def check_sikayetler(context: CallbackContext) -> None:
        results = reporstdb.find({"$and":[{"cevaplanma":1}, {"sikayetBildiri":0}]})
        for result in results:
            print(result)
            context.bot.send_message(chat_id=result["chatId"], 
            text="""
            selam {}, dostum
            gönderdiğin,
            {},
            şikayeti incelenip değerlendirilmiştir.

            {},
            """.format(result["gonderen"], result["sikayet"], result["cevapMesaj"]), reply_to_message_id=result["mesajId"])
        reporstdb.update_many({"$and":[{"cevaplanma":1}, {"sikayetBildiri":0}]}, {"$set":{"sikayetBildiri": 1}})
    
def tekrar_mesaj(context: CallbackContext) -> None:
    try:  
        kekec = "Selam dostum ben bir destek botuyum grupla yada üyelerle ilgili herhangi bir şikayet öneri ve talep için /sikayet mesajınız şeklinde istediğiniz öneri ve şikayeti yazabilirsiniz, daha detaylı bilgi için /yardım"
        
        context.bot.send_message(chat_id="-1001554994271", text=kekec)
    except:
        print("gruba mesaj atamıyor")


def yardim(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""
    Merhaba! Benimle ilgili aşağıdaki komutları kullanarak işlemler yapabilirsiniz:

    /sikayet : Şikayet oluşturmak için kullanılır. Herkes tarafından kullanılabilir.

    /sikayetal : Sadece yetkililer tarafından kullanılabilir. Bu komutla tüm bekleyen şikayetleri görüntüleyebilirsiniz. Eğer /sikayetal <id> şeklinde kullanırsanız, belirli bir şikayeti detaylı olarak görüntüleyebilirsiniz.

    /sikayetkapat : Sadece yetkililer tarafından kullanılabilir. Bu komutla bir şikayeti kapatırsınız. Kapatılacak şikayetin <id> ve <mesaj> değerlerini belirtmelisiniz. <id>, kapatılacak şikayetin kimliği, <mesaj> ise kapatıldıktan sonra şikayeti yapan kişiye gösterilecek mesajdır.

    Örneğin:
    - /sikayetkapat 123 Şikayetiniz değerlendirildi, teşekkür ederiz!

    """)



def sikayetkapat(update: Update, context: CallbackContext) -> None:
    if admindb.find_one({"id": update.message.from_user.id}):
        try:
            komut, id_str, *yeni_mesaj_parcalari = update.message.text.split(maxsplit=2)

            id_num = int(id_str)
                
            yeni_mesaj = " ".join(yeni_mesaj_parcalari)

            reporstdb.update_many({"id":id_num}, {"$set":{"cevapMesaj": yeni_mesaj}})
            reporstdb.update_many({"id":id_num}, {"$set":{"cevaplanma": 1}})
            update.message.reply_text("Şikayet başarıyla kapatılmıştır")

        except (ValueError, IndexError):
            update.message.reply_text("Geçersiz komut. Doğru format: /kapat id mesaj")
    else:
        print("izinsiz sikayet kapatma denemesi", update.message.from_user.username, update.message.from_user.id)




def sikayetal(update: Update, context: CallbackContext) -> None:
    if admindb.find_one({"id": update.message.from_user.id}):
        try:
            komut, *args = update.message.text.split()
            
            if len(args) == 0:
                # Eğer hiç argüman verilmediyse, tüm listeyi göster
                result = reporstdb.find({"cevaplanma":0})
                for i in result:
                    context.bot.send_message(chat_id=update.message.chat_id, text="[{}] - {}".format(i["id"],i["sikayet"]))

            else:
                # Argüman olarak bir id verildiyse, sadece o id'ye sahip elemanı göster
                id_num = int(args[0])
                result = reporstdb.find({"$and":[{"cevaplanma":0},{"id":id_num}]})
                for i in result:
                        kekec = """
                            şikayet id: {0},
                            şikayetçi: {1}
                            sikayet:
                            {4}

                            Ek bilgi

                            mesaj id: {3}
                            chat id: {2}
                            
                            """.format(i["id"],i["gonderen"],i["chatId"],i["mesajId"],i["sikayet"])
                        context.bot.send_message(chat_id=update.message.chat_id ,text=kekec)
        except ValueError:
            update.message.reply_text("Geçersiz komut. Doğru format: /liste [id]")
    else:
        print("izinsiz sikayet cekme denemesi", update.message.from_user.username, update.message.from_user.id)

def sikayet(update: Update,context: CallbackContext) -> None:

    id = reporstdb.count_documents({}) + 1
    message = update.message.text[9:]
    messageId = update.message.message_id
    chatId = update.message.chat.id    
    gonderen = update.message.from_user.username
    cevaplanma = 0
    sikayetBildiri = 0
    cevapMesaj = ""

    şikayet = {
            "id":id,
            "gonderen": gonderen,
            "chatId": chatId,
            "mesajId": messageId,
            "sikayet": message,
            "cevaplanma": cevaplanma,
            "cevapMesaj": cevapMesaj,
            "sikayetBildiri": sikayetBildiri
        }
    reporstdb.insert_one(şikayet)
    


    update.message.reply_text("Şikayetiniz başarıyla oluşturuldu")


def adminekle(update: Update,context: CallbackContext) -> None:
    print(update.message.from_user.id)
    
    if ownerdb.find_one({"id": update.message.from_user.id}):
        print("kurucu")
        try:
                komut, *args = update.message.text.split()
                arguman = " ".join(args)
                print(arguman)
                if arguman == "" or arguman == " ":
                    print("dada")
                    pass
                else:
                    print(arguman,"sss")
                    admindb.insert_one({"id":int(arguman)})

        except ValueError:
            update.message.reply_text("Geçersiz komut. Doğru format: /adminekle [id]")




def adminsil(update: Update,context: CallbackContext) -> None:
    if ownerdb.find_one({"id": update.message.from_user.id}):
        try:
                komut, *args = update.message.text.split()
                arguman = " ".join(args)
                if arguman.strip():
                    pass
                else:
                    admindb.delete_one({"id":int(arguman)})

        except ValueError:
            update.message.reply_text("Geçersiz komut. Doğru format: /adminsil [id]")



def talep(update: Update,context: CallbackContext) -> None:
    if admindb.find_one({"id": update.message.from_user.id}):
        print("id var")
    else:
        print("id yok")


    for sikayet in şikayetler:            
        kekec = """

        şikayet id: {0},
        şikayetçi: {1}
        sikayet:
        {4}

        Ek bilgi

        mesaj id: {3}
        chat id: {2}
        cevaplanma: {5}
        bildiri: {6}
                            
        """.format(sikayet["id"],sikayet["gonderen"],sikayet["chatId"],sikayet["mesajId"],sikayet["sikayet"], sikayet["cevaplanma"], sikayet["sikayetBildiri"])
        context.bot.send_message(chat_id=update.message.chat_id ,text=kekec)