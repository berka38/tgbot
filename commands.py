from telegram import *
from telegram.ext import *

şikayetler = [

]

kurucu = "1316760864"

admins = [123123123123 ,1316760864, 2131231231,13123213123,12312312312312]





def check_sikayetler(context: CallbackContext) -> None:
    for sikayet in şikayetler:
        if sikayet["cevaplanma"] == 1 and sikayet["sikayetBildiri"] == 0:
            context.bot.send_message(chat_id=sikayet["chatId"], 
            text="""
            selam {}, dostum
            gönderdiğin,
            {},
            şikayeti incelenip değerlendirilmiştir.

            {},
            """.format(sikayet["gonderen"], sikayet["sikayet"], sikayet["cevapMesaj"]), reply_to_message_id=sikayet["mesajId"])
            sikayet["sikayetBildiri"] = 1
    
def tekrar_mesaj(context: CallbackContext) -> None:
    
    kekec = "Selam dostum ben bir destek botuyum grupla yada üyelerle ilgili herhangi bir şikayet öneri ve talep için /sikayet mesajınız şeklinde istediğiniz öneri ve şikayeti yazabilirsiniz, daha detaylı bilgi için /yardım"
    
    context.bot.send_message(chat_id="-1001554994271", text=kekec)


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
    if update.message.from_user.id in admins:
        try:
            komut, id_str, *yeni_mesaj_parcalari = update.message.text.split(maxsplit=2)

            id_num = int(id_str)
                
            yeni_mesaj = " ".join(yeni_mesaj_parcalari)

            for sikayet in şikayetler:
                if sikayet["id"] == id_num:
                    sikayet["cevapMesaj"] = yeni_mesaj_parcalari
                    sikayet["cevaplanma"] = 1
                    update.message.reply_text("Şikayet başarıyla kapatılmıştır")

        except (ValueError, IndexError):
            update.message.reply_text("Geçersiz komut. Doğru format: /kapat id mesaj")
    else:
        print("izinsiz sikayet kapatma denemesi", update.message.from_user.username, update.message.from_user.id)




def sikayetal(update: Update, context: CallbackContext) -> None:
    print(admins)
    if update.message.from_user.id in admins:
        try:
            komut, *args = update.message.text.split()
            
            if len(args) == 0:
                # Eğer hiç argüman verilmediyse, tüm listeyi göster
                for sikayet in şikayetler:
                    if sikayet["cevaplanma"] == 0:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[{}] - {}".format(sikayet["id"],sikayet["sikayet"]))

            else:
                # Argüman olarak bir id verildiyse, sadece o id'ye sahip elemanı göster
                id_num = int(args[0])
                for sikayet in şikayetler:
                    if sikayet["id"] == id_num:
                        kekec = """
                            şikayet id: {0},
                            şikayetçi: {1}
                            sikayet:
                            {4}

                            Ek bilgi

                            mesaj id: {3}
                            chat id: {2}
                            
                            """.format(sikayet["id"],sikayet["gonderen"],sikayet["chatId"],sikayet["mesajId"],sikayet["sikayet"])
                        context.bot.send_message(chat_id=update.message.chat_id ,text=kekec)
        except ValueError:
            update.message.reply_text("Geçersiz komut. Doğru format: /liste [id]")
    else:
        print("izinsiz sikayet cekme denemesi", update.message.from_user.username, update.message.from_user.id)

def sikayet(update: Update,context: CallbackContext) -> None:

    sirket = len(şikayetler)
    id = int(sirket) + 1
    message = update.message.text[9:]
    messageId = update.message.message_id
    chatId = update.message.chat.id    
    gonderen = update.message.from_user.username
    cevaplanma = 0
    sikayetBildiri = 0
    cevapMesaj = ""

    şikayetler.append(
        {
            "id":id,
            "gonderen": gonderen,
            "chatId": chatId,
            "mesajId": messageId,
            "sikayet": message,
            "cevaplanma": cevaplanma,
            "cevapMesaj": cevapMesaj,
            "sikayetBildiri": sikayetBildiri
        }
    )


    update.message.reply_text("Şikayetiniz başarıyla oluşturuldu")


def adminekle(update: Update,context: CallbackContext) -> None:
    print(update.message.from_user.id)
    if update.message.from_user.id == int(kurucu):
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
                    admins.append(int(arguman))
        except ValueError:
            update.message.reply_text("Geçersiz komut. Doğru format: /adminekle [id]")




def adminsil(update: Update,context: CallbackContext) -> None:
    if update.message.from_user.id == int(kurucu):
        try:
                komut, *args = update.message.text.split()
                arguman = " ".join(args)
                if arguman.strip():
                    pass
                else:
                    for admin in admins:
                        if admin["id"] == int(arguman):
                            admins.remove(admin)
        except ValueError:
            update.message.reply_text("Geçersiz komut. Doğru format: /adminsil [id]")



def talep(update: Update,context: CallbackContext) -> None:
    if update.message.from_user.id in admins:
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