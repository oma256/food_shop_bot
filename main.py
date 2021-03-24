import telebot
import requests
from bs4 import BeautifulSoup


token = '1605357811:AAHCwIrnuHXnLx5v1XSQ9cB-D3NuiMMRi4Q'

bot = telebot.TeleBot(token)
welcome_text = """
	Здраствуйте, приветсвуем вас на нашем онлайн магазине!
	Выберите супермаркет!
"""
error_msg = """
	Введите правильно привет!
"""
list_product_category_names = """
	Список категорий продуктов
"""

shop_list = [
	{'name': 'Globus'},
	{'name': 'Народный'},
	{'name': 'Фрунзе'},
]

globus_product_category_list = []

globus_url = 'https://globus-online.kg/catalog/'


@bot.message_handler(content_types=['text'])
def send_welcome(message):
	chat_id = message.chat.id
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.row(
		shop_list[0].get('name'),
		shop_list[1].get('name'),
		shop_list[2].get('name'),
	)

	if message.text in globus_product_category_list:
		get_products_by_category(message.text)
	elif message.text.lower() == 'привет':
		bot.reply_to(message=message,
					 text=welcome_text,
					 reply_markup=markup)
	elif shop_list[0].get('name') == message.text:
		markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
		response = requests.get(globus_url)
		soup = BeautifulSoup(response.text, 'lxml')
		soup = soup.find_all('a', class_='parent')
		for s in soup[2:]:
			markup.add(s.text)
			globus_product_category_list.append(s.text)
		bot.send_message(chat_id=chat_id,
						 text=list_product_category_names,
						 reply_markup=markup)
	elif shop_list[1].get('name') == message.text:
		bot.send_message(chat_id=chat_id,
						 text=shop_list[1].get('name'))
	elif shop_list[2].get('name') == message.text:
		bot.send_message(chat_id=chat_id,
						 text=shop_list[2].get('name'))
	else:
		bot.send_message(chat_id=message.chat.id,
						 text=error_msg)


def get_products_by_category(category_name):
	for category in globus_product_category_list:
		if category == category_name:
			response = requests.get('https://globus-online.kg/catalog/myaso_ptitsa_ryba/')
			soup = BeautifulSoup(response.text, 'lxml')
			soup = soup.find_all('div', class_='list-showcase__name')
			for s in soup:
				print(s.text)
			break
#
# def choice_shop(message):
# 	chat_id = message.chat.id
#
# 	if shop_list[0].get('name') == message.text:
# 		bot.send_message(chat_id=chat_id,
# 						 text=shop_list[0].get('name'))
# 	if shop_list[1].get('name') == message.text:
# 		bot.send_message(chat_id=chat_id,
# 						 text=shop_list[1].get('name'))
# 	if shop_list[2].get('name') == message.text:
# 		bot.send_message(chat_id=chat_id,
# 						 text=shop_list[2].get('name'))
# 	if shop_list[3].get('name') == message.text:
# 		bot.send_message(chat_id=chat_id,
# 						 text=shop_list[3].get('name'))


bot.polling()
