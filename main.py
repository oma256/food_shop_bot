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
list_products_names = """
	Список всех продуктов и их цен
"""

shop_list = [
	{'name': 'Globus'},
	{'name': 'Народный'},
	{'name': 'Фрунзе'},
]

globus_product_category_data = []
globus_product_category_names = []
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

	if message.text in globus_product_category_names:
		get_products_by_category(message)
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
			data = {
				'name': s.text,
			 	'url': f'https://globus-online.kg{s.get("href")}',
			}
			globus_product_category_data.append(data)
			globus_product_category_names.append(s.text)
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


def get_products_by_category(message):
	chat_id = message.chat.id

	for category in globus_product_category_data:
		if category.get('name') == message.text:
			response = requests.get(category.get('url'))
			soup = BeautifulSoup(response.text, 'lxml')
			list_products_name = soup.find_all('div', class_='list-showcase__name')
			list_products_price = soup.find_all('span', class_='c-prices__value js-prices_pdv_ГЛОБУС Розничная')
			markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)

			for i, product in enumerate(list_products_name):
				markup.add(f'{product.text} - {list_products_price[i].text}')

			bot.send_message(chat_id=chat_id,
							 text=list_products_names,
							 reply_markup=markup)
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
