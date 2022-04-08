import telebot
import config
import requests
import time

from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def commands(message):
	if message.text == "/start":
		bot.send_message(message.chat.id, "Добрий день!\nВідтепер ви отримуватимете новини з порталу Громадське \nОстання новина:")

		
		URL = "https://hromadske.ua/news"

		page = requests.get(URL)
		soup =BeautifulSoup(page.content, "html.parser")

		post = soup.find("a", class_="NewsPublicationCard")
		#print(post)
		bot.send_message(message.chat.id, post["data-vr-contentbox"]+"\n--------------------------------------------------"
			+"\nЧитати новину повністю можна тут "+ "https://hromadske.ua"+post["data-vr-contentbox-url"])



		back_post_id = post.find("div", class_="NewsPublicationCard-time").text.strip()

		#print("id is " + back_post_id)
		while True:
			post_text = parser(back_post_id)
			back_post_id = post_text[1]

			if post_text[0] != None:
				bot.send_message(message.chat.id, (post_text[0]+"\n--------------------------------------------------"
			+"\nЧитати новину повністю можна тут "+ "https://hromadske.ua"+post_text[2]))
				time.sleep(50)



def parser(back_post_id):
	URL = "https://hromadske.ua/news"

	page = requests.get(URL)
	soup =BeautifulSoup(page.content, "html.parser")

	post = soup.find("a", class_="NewsPublicationCard")
	post_id = post.find("div", class_="NewsPublicationCard-time").text.strip()
	#print("id is " + post_id)
	#url = soup.find("a", class_="href", id=True)#.text.strip()

	text = post["data-vr-contentbox"]

	if post_id != back_post_id:
		#print("post_id " + post_id + "!= back_post_id " + back_post_id)
		return f"{text}", post_id, post["data-vr-contentbox-url"]
	else:
		return None, post_id

# RUN
bot.polling()