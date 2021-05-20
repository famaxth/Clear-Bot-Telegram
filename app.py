# -*- coding: utf-8 -*-

#Production by Berlin
#Telegram - @por0vos1k


import telebot
import config
import app_logger

user0 = config.admin_user

bot = telebot.TeleBot(config.token, parse_mode='HTML')
bot_info = bot.get_me()

logger = app_logger.get_logger(__name__)

logger.info('Бот начал работу!', name='Bot')



def scan_message(text):
    result = None
    for word in config.texts['bad_words']:
        if word == text:
            result = word
    return result


def def_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.add(config.texts['add_chat'], config.texts['help'])
    keyboard.add(config.texts['add_antispam'])
    return keyboard


@bot.message_handler(commands=['start'])
def bot_command_start(message):
    keyboard = None
    if message.chat.type == 'private':
        keyboard = def_keyboard()
    bot.send_message(message.chat.id, config.texts['start'] + config.texts["help_text"], reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def bot_command_help(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, config.texts['help_text'])


@bot.message_handler(commands=['antispam'])
def bot_command_antispam(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, config.texts['add_antispam_tutor'])


@bot.message_handler(content_types=['document'])
def delete_links_document(message):
	if (str(message.from_user.id) not in user0):
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['photo'])
def delete_links_photo(message):
	if (str(message.from_user.id) not in user0):
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['audio'])
def delete_links_audio(message):
	if (str(message.from_user.id) not in user0):
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['video'])
def delete_links_video(message):
	if (str(message.from_user.id) not in user0):
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['sticker'])
def delete_links_sticker(message):
	if (str(message.from_user.id) not in user0):
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['location'])
def delete_links_location(message):
	if (str(message.from_user.id) not in user0):
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['contact'])
def delete_links_contact(message):
	if (str(message.from_user.id) not in user0):
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['caption'])
def delete_links_caption(message):
	if (str(message.from_user.id) not in user0):
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['venue'])
def delete_links_venue(message):
	if (str(message.from_user.id) not in user0):
			bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(func=lambda message: message.entities is not None )
def delete_links(message):
	if (str(message.from_user.id) not in user0):
		j = 0
		for entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
			j = j + 1
			if (j == 1):
				if (entity.type in ["url"]):
					bot.delete_message(message.chat.id, message.message_id)
				if (entity.type in ["text_link"]):
					bot.delete_message(message.chat.id, message.message_id)
				if (entity.type in ["pre"]):
					bot.delete_message(message.chat.id, message.message_id)
				if entity.type in ["hashtag"]:
					bot.delete_message(message.chat.id, message.message_id)
				if entity.type in ["email"]:
					bot.delete_message(message.chat.id, message.message_id)
				if entity.type in ["code"]:
					bot.delete_message(message.chat.id, message.message_id)
				if entity.type in ["bot_command"]:
					bot.delete_message(message.chat.id, message.message_id)
				if entity.type in ["bold"]:
					bot.delete_message(message.chat.id, message.message_id)
				if entity.type in ["mention"]:
					bot.delete_message(message.chat.id, message.message_id)
				if (entity.type in ["italic"]):
					bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=config.all_content_types)
def bot_new_message(message):
    if message.text:
        text_save = message.text
    elif message.caption:
        text_save = message.caption
    else:
        text_save = None
    if message.chat.type == 'private':
        try:
            if text_save.lower() in config.texts['add_chat_list']:
                keyboard = telebot.types.InlineKeyboardMarkup()
                button = telebot.types.InlineKeyboardButton(text='Выбрать чат...', url=f't.me/{bot_info.username}?startgroup=true')
                keyboard.add(button)
                return bot.send_message(message.chat.id, config.texts['add_chat_tutor'], reply_markup=keyboard)
            elif text_save.lower() in config.texts['help_list']:
                return bot.send_message(message.chat.id, config.texts['help_text'], reply_markup=def_keyboard())
            elif text_save.lower() in config.texts['add_antispam_list']:
                return bot.send_message(message.chat.id, config.texts['add_antispam_tutor'])
        except AttributeError:
            print("Ошибка AttributeError!")
    if not text_save:
        return
    text = text_save.translate(config.regexp).lower()
    text = config.emoji_pattern.sub(r'', text).split(' ')
    for word in text:
        result = scan_message(word)
        if result:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                break
            except telebot.apihelper.ApiException:
                text = ''
                bot_chat_info = bot.get_chat_member(message.chat.id, bot_info.id)
                if not bot_chat_info.can_delete_messages:
                    admins_ = bot.get_chat_administrators(message.chat.id)
                    for admin in admins_:
                        if admin.user.is_bot:
                            pass
                        if admin.can_promote_members or admin.status == 'creator':
                            text += f'<a href="tg://user?id={admin.user.id}">{admin.user.first_name}</a>, '
                    bot.send_message(message.chat.id, config.texts['no_perm'].format(text))
            except Exception as e:
                logger.warning(f'Неизвестная ошибка: {e}', name=message.from_user.first_name)    


@bot.message_handler(content_types=['new_chat_members'])
def bot_join(message):
    for user in message.new_chat_members:
        if user.id == bot_info.id:
            logger.info(f'Пригласили в группу {message.chat.title}', name=message.from_user.first_name)


@bot.message_handler(content_types=['left_chat_member'])
def bot_left(message):
    user = message.left_chat_member
    if user.id == bot_info.id:
        logger.info(f'Выкинули из группы {message.chat.title}', name=message.from_user.first_name)


try:
    bot.polling()
except Exception as e:
    logger.error(e, name='ERROR')


logger.info('Бот закончил работу!', name='Bot')
