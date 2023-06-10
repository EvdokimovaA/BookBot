import telebot
from BookSearch import BookSearch

bot = telebot.TeleBot("6065979245:AAEUB997rDjEwu41KF02h2ufmOhBZT-uDk8")


@bot.message_handler(commands=["start"])
def instruction(message):
    bot.send_message(message.chat.id, "Введите название книги")


@bot.message_handler(content_types=["text"])
def search(message):
    book_name = BookSearch(message.json["text"])
    bot.send_message(message.chat.id, "Ожидайте, осуществляется поиск")
    try:
        books = book_name.get_request()
        if len(books) > 0:
            for i in books:
                links = "\n".join(i.url_download.copy())
                bot.send_message(message.chat.id, f"Книга: {i.name}\nРасширение: {i.extension}\nСтраницы: {i.pages}\nСкачать: {links}")
                print(i)
        else:
            bot.send_message(message.chat.id, "По запросу ничего не найдено 🥴")
    except:
        bot.send_message(message.chat.id, "По запросу ничего не найдено 🥴")
        print("Прога вылетела")

if __name__ == "__main__":
    bot.polling(none_stop=True)
