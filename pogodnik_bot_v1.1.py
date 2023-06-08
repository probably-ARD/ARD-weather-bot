#python pogodnik_bot_v1.1.py
import telebot # module for telegram
from telebot import types # need for keyboard

bot = telebot.TeleBot("", parse_mode = None) # variable with bot and "TOKEN"

import pyowm # module for weather
from pyowm import OWM # I don't know (need to work module)
owm = OWM('') # is my API-key from openweathermap.org
mgr = owm.weather_manager()

import sqlite3 # special for create db

conn = sqlite3.connect(r"D:\Python projects\бот погодник\users_cities_for_v1_1.db") # connect with this db
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users_cities_for_v1_1(
	user_first_name TEXT,
	user_last_name TEXT,
	user_nick TEXT,
	user_id INTEGER,
	user_city TEXT,
	user_language TEXT)""")
conn.commit()

@bot.message_handler(commands=['start']) # handler for 1st message
def start(message):

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button_us = types.KeyboardButton('🇺🇸') # keyboard for 1st memorize a city
	button_ru = types.KeyboardButton('🇷🇺')
	markup.add(button_us, button_ru)

	bot.send_message(message.chat.id,'Выберите язык\nSelect a language'.format(message.from_user), reply_markup = markup)

@bot.message_handler(content_types=['text'])
def all_messages(message): # all messages and commands hanler
	conn = sqlite3.connect(r"D:\Python projects\бот погодник\users_cities_for_v1_1.db") # connect with this db
	cursor = conn.cursor()
	
	if (message.text == '🇺🇸') or (message.text == '🇷🇺'):

		language = message.text
		if language == '🇺🇸':
			language = 'us'
		elif language == '🇷🇺':
			language = 'ru'
		
		u_id = message.chat.id

		info = cursor.execute('''SELECT 'user_city' FROM users_cities_for_v1_1 WHERE user_id = ?''', (u_id, ))

		if info.fetchone() is None:

			if language == 'us':
				
				sql = """INSERT INTO users_cities_for_v1_1 VALUES (?, ?, ?, ?, ?, ?)"""
				data = ('None', 'None', 'None',u_id, 'None', language)

				cursor.execute(sql, data)
				conn.commit()
				

				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				button_remember_city = types.KeyboardButton("Let's remember my city") # keyboard for 1st memorize a city
				markup.add(button_remember_city)

				bot.send_message(message.chat.id,f'OK, now your language: {language}', language.format(message.from_user), reply_markup = markup)

			elif language == 'ru':
				
				sql = """INSERT INTO users_cities_for_v1_1 VALUES (?, ?, ?, ?, ?, ?)"""
				data = ('None', 'None', 'None',u_id, 'None', language)

				cursor.execute(sql, data)
				conn.commit()

				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				button_remember_city = types.KeyboardButton("Давай запомним мой город") # keyboard for 1st memorize a city
				markup.add(button_remember_city)

				bot.send_message(message.chat.id,f'ОК, теперь твой язык: {language}', language.format(message.from_user), reply_markup = markup)
		else:
			u_id = message.chat.id

			sql = '''UPDATE users_cities_for_v1_1 SET user_language = ? WHERE user_id = ?'''
			data = (language, u_id)
		
			cursor.execute(sql, data)
			conn.commit()

			if language == 'us':
				
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				button_remember_city = types.KeyboardButton("well done") # keyboard for 1st memorize a city
				markup.add(button_remember_city)

				bot.send_message(message.chat.id,f'OK, now your language: {language}', language.format(message.from_user), reply_markup = markup)

			elif language == 'ru':
				
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				button_remember_city = types.KeyboardButton("отлично") # keyboard for 1st memorize a city
				markup.add(button_remember_city)

				bot.send_message(message.chat.id,f'ОК, теперь твой язык: {language}', language.format(message.from_user), reply_markup = markup)

	elif (message.text == 'Let\'s remember my city') or (message.text == 'Давай запомним мой город') or (message.text == 'change city') or (message.text == 'изменить город'):
		
		if (message.text == 'Let\'s remember my city') or (message.text == 'change city'):
			
			msg = bot.send_message(message.chat.id,'Write the name of your city')
			bot.register_next_step_handler(msg, get_user_city) # need to know user's city
		
		elif (message.text == 'Давай запомним мой город') or (message.text == 'изменить город'):
			
			msg = bot.send_message(message.chat.id,'Напиши название своего города')
			bot.register_next_step_handler(msg, get_user_city) # need to know user's city

	elif (message.text == 'weather now') or (message.text == 'погода сейчас'):
		weather_at_city_now(bot, message)

	elif (message.text == '⚙️'):
		u_id = message.chat.id

		language = str(cursor.execute('''SELECT user_language FROM users_cities_for_v1_1 WHERE user_id = ?''', (u_id, )).fetchone())

		language = language.replace("[", "")
		language = language.replace("]", "")
		language = language.replace("'", "")
		language = language.replace("(", "")
		language = language.replace(")", "")
		language = language.replace(",", "")

		if language == 'us':
			
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("🔙") # keyboard
			button2 = types.KeyboardButton("change language") # keyboard
			markup.add(button1, button2)
			button3 = types.KeyboardButton("change city") # keyboard
			markup.add(button3)

			bot.send_message(message.chat.id,'you have entered the settings', language.format(message.from_user), reply_markup = markup)

		elif language == 'ru':

			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("🔙") # keyboard
			button2 = types.KeyboardButton("изменить язык") # keyboard
			markup.add(button1, button2)
			button3 = types.KeyboardButton("изменить город") # keyboard
			markup.add(button3)

			bot.send_message(message.chat.id,'вы вошли в настройки', language.format(message.from_user), reply_markup = markup)

	elif (message.text == 'weather tomorrow') or (message.text == 'погода на завтра'):
		pass

	elif (message.text == '🔙'):
		u_id = message.chat.id

		language = str(cursor.execute('''SELECT user_language FROM users_cities_for_v1_1 WHERE user_id = ?''', (u_id, )).fetchone())

		language = language.replace("[", "")
		language = language.replace("]", "")
		language = language.replace("'", "")
		language = language.replace("(", "")
		language = language.replace(")", "")
		language = language.replace(",", "")

		if (language == 'us'):
			
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("weather now") # keyboard
			button2 = types.KeyboardButton("⚙️") # keyboard
			markup.add(button1, button2)
			button3 = types.KeyboardButton("weather tomorrow") # keyboard
			markup.add(button3)

			bot.send_message(message.chat.id,'you have entered the menu', language.format(message.from_user), reply_markup = markup)

		elif (language == 'ru'):
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("погода сейчас") # keyboard
			button2 = types.KeyboardButton("⚙️") # keyboard
			markup.add(button1, button2)

			bot.send_message(message.chat.id,'вы вошли в меню', language.format(message.from_user), reply_markup = markup)

	elif (message.text == 'change language') or (message.text == 'изменить язык'):
		start(message)

	elif (message.text == 'well done') or (message.text == 'отлично'):
		u_id = message.chat.id


		language = str(cursor.execute('''SELECT user_language FROM users_cities_for_v1_1 WHERE user_id = ?''', (u_id, )).fetchone())

		language = language.replace("[", "")
		language = language.replace("]", "")
		language = language.replace("'", "")
		language = language.replace("(", "")
		language = language.replace(")", "")
		language = language.replace(",", "")

		if (language == 'us'):
			
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("weather now") # keyboard
			button2 = types.KeyboardButton("⚙️") # keyboard
			markup.add(button1, button2)

			bot.send_message(message.chat.id,'you have entered the menu', language.format(message.from_user), reply_markup = markup)

		elif (language == 'ru'):
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("погода сейчас") # keyboard
			button2 = types.KeyboardButton("⚙️") # keyboard
			markup.add(button1, button2)

			bot.send_message(message.chat.id,'вы вошли в меню', language.format(message.from_user), reply_markup = markup)

def get_user_city(message):
	
	conn = sqlite3.connect(r"D:\Python projects\бот погодник\users_cities_for_v1_1.db") # connect with this db
	cursor = conn.cursor()

	u_id = message.chat.id

	city = message.text

	info = str(cursor.execute('''SELECT user_city FROM users_cities_for_v1_1 WHERE user_id = ?''', (u_id, )).fetchone())

	info = info.replace("[", "")
	info = info.replace("]", "")
	info = info.replace("'", "")
	info = info.replace("(", "")
	info = info.replace(")", "")
	info = info.replace(",", "")

	if info == ('None'):

		u_first_name = message.chat.first_name
		u_last_name = message.chat.last_name
		u_nick = message.chat.username
		
		sql = """UPDATE users_cities_for_v1_1 SET user_first_name = ?,  user_last_name = ?,  user_nick = ?,  user_city = ? WHERE user_id = ?"""
		data = (u_first_name, u_last_name, u_nick , city, u_id)

		cursor.execute(sql, data)
		conn.commit()

	else:

		sql = '''UPDATE users_cities_for_v1_1 SET user_city = ? WHERE user_id = ?'''
		data = (city, u_id)
		
		cursor.execute(sql, data)
		conn.commit()

	weather_at_city_now(bot, message)

def weather_at_city_now(bot, message):
	
	conn = sqlite3.connect(r"D:\Python projects\бот погодник\users_cities_for_v1_1.db") # connect with this db
	cursor = conn.cursor()

	try:
		u_id = message.chat.id

		city = str(cursor.execute('''SELECT user_city FROM users_cities_for_v1_1 WHERE user_id = ?''', (u_id, )).fetchone())

		city = city.replace("[", "")
		city = city.replace("]", "")
		city = city.replace("'", "")
		city = city.replace("(", "")
		city = city.replace(")", "")
		city = city.replace(",", "")

		language = str(cursor.execute('''SELECT user_language FROM users_cities_for_v1_1 WHERE user_id = ?''', (u_id, )).fetchone())

		language = language.replace("[", "")
		language = language.replace("]", "")
		language = language.replace("'", "")
		language = language.replace("(", "")
		language = language.replace(")", "")
		language = language.replace(",", "")

		from pyowm.utils.config import get_default_config #special for ru language
		config_dict = get_default_config() # special for ru language
		config_dict['language'] = language # special for different languages

		observation = mgr.weather_at_place(city)
		w = observation.weather # variable with weather

		w_detailed_status = w.detailed_status # clouds
		w_wind_speed = w.wind()['speed'] # wind speed
		w_wind_deg = w.wind()['deg'] # wind degree

		if w_wind_deg == 0:
			ru_w_wind_deg = 'С \n(северное⬆️)'
			us_w_wind_deg = 'N \n(North⬆️)'
		elif w_wind_deg <= 45:
			ru_w_wind_deg = 'СВ \n(северо-восточное↗️)'
			us_w_wind_deg = 'NE \n(North-East↗️)'
		elif w_wind_deg <= 90:
			ru_w_wind_deg = 'В \n(восточное➡️)'
			us_w_wind_deg = 'E \n(East➡️)'
		elif w_wind_deg <= 135:
			ru_w_wind_deg = 'ЮЗ \n(юго-восточное↘️)'
			us_w_wind_deg = 'SE \n(South-East↘️)'
		elif w_wind_deg <= 180:
			ru_w_wind_deg = 'Ю \n(южное⬇️)'
			us_w_wind_deg = 'S \n(South⬇️)'
		elif w_wind_deg <= 225:
			ru_w_wind_deg = 'ЮЗ \n(юго-западное↙️)'
			us_w_wind_deg = 'SW \n(South-West↙️)'
		elif w_wind_deg <= 270:
			ru_w_wind_deg = 'З \n(западное⬅️)'
			us_w_wind_deg = 'W \n(West⬅️)'
		elif w_wind_deg <= 315:
			ru_w_wind_deg = 'СЗ \n(северо-западное↖️)'
			us_w_wind_deg = 'NW \n(North-West↖️)'
		elif w_wind_deg <= 360:
			ru_w_wind_deg = 'С \n(северное⬆️)'
			us_w_wind_deg = 'N \n(North⬆️)'

		w_humidity = w.humidity # humidity

		w_max_temp = w.temperature('celsius')['temp_max'] # max temp
		w_min_temp = w.temperature('celsius')['temp_min'] # min temp
		w_temp = w.temperature('celsius')['temp'] # now temp

		w_clouds = w.clouds

		ru_message = (f'{city}\nСейчас: {w_detailed_status}\nСкорость ветра: {w_wind_speed}м/с\nНаправление: {ru_w_wind_deg}\nВлажность: {w_humidity}%\nМакс. темп.: {w_max_temp}°\nМин.темп.: {w_min_temp}°\nТемп. сейчас: {w_temp}°\nОблачность: {w_clouds}%')
		us_message = (f'{city}\nnow: {w_detailed_status}\nwind speed: {w_wind_speed}m/s\nwind degree: {us_w_wind_deg}\nhumidity: {w_humidity}%\nmax temp: {w_max_temp}°\nmin temp: {w_min_temp}°\ntemp now: {w_temp}°\nClouds: {w_clouds}%')

		if (language == 'us'):
			
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("weather now") # keyboard
			button2 = types.KeyboardButton("⚙️") # keyboard
			markup.add(button1, button2)

			bot.send_message(message.chat.id,us_message, language.format(message.from_user), reply_markup = markup)

		elif (language == 'ru'):
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("погода сейчас") # keyboard
			button2 = types.KeyboardButton("⚙️") # keyboard
			markup.add(button1, button2)

			bot.send_message(message.chat.id,ru_message, language.format(message.from_user), reply_markup = markup)

		

	except Exception as e:
		
		language = str(cursor.execute('''SELECT user_language FROM users_cities_for_v1_1 WHERE user_id = ?''', (u_id, )).fetchone())

		language = language.replace("[", "")
		language = language.replace("]", "")
		language = language.replace("'", "")
		language = language.replace("(", "")
		language = language.replace(")", "")
		language = language.replace(",", "")

		if (language == 'us'):
			
			bot.send_message(message.chat.id,"Oops I don't know this city...")
			bot.send_message(message.chat.id,"try again")

			msg = bot.send_message(message.chat.id,'Write the name of your city')
			bot.register_next_step_handler(msg, get_user_city)

		elif (language == 'ru'):
			bot.send_message(message.chat.id,"Упс, я не знаю такого города...")
			bot.send_message(message.chat.id,"Попробуй заново")

			msg = bot.send_message(message.chat.id,'Напиши название города')
			bot.register_next_step_handler(msg, get_user_city)
		print(e)

bot.infinity_polling()