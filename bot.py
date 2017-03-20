import telebot
import cherrypy
import config
import db
import constants

WEBHOOK_HOST = '188.73.151.218'
WEBHOOK_PORT = 88  # на других портах не работает
WEBHOOK_LISTEN = '188.73.151.218'

WEBHOOK_SSL_CERT = './YOURPUBLIC.pem'
WEBHOOK_SSL_PRIV = './YOURPRIVATE.key'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % config.token

bot = telebot.TeleBot(config.token)


# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(commands=['start'])
def handle_message(message):
    bot.send_message(message.chat.id, """
    Я могу показать тебе распиание твоих уроков!
    если ты первый раз пользуешься мной, то введи команду '/hello'
    """)


@bot.message_handler(commands=['hello'])
def handle_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('11A', '11B', '11C', '11D', '11E')
    user_markup.row('10A', '10B', '10C', '10D', '10E')
    user_markup.row('9A', '9B', '9C', '9D', '9E')
    user_markup.row('8A', '8B', '8C', '8D', '8E')
    user_markup.row('7A', '7B', '7C', '7D', '7E')
    user_markup.row('6A', '6B', '6C', '6D', '6E')
    user_markup.row('5A', '5B', '5C', '5D', '5E')
    bot.send_message(message.from_user.id, 'Выбери класс', reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_message(message):
    profile = db.get_schedule_user(message.from_user.id)
    schedule = constants.schedule[str(profile)]
    print(str(message.from_user.first_name) + ' ' + str(message.from_user.last_name) + ' ' + str(message.from_user.id))
    for day in schedule:
        bot.send_message(message.from_user.id, day)
        for curr in schedule[day]:
            bot.send_message(message.from_user.id, curr)


@bot.message_handler(commands=['schedule_today'])
def handle_message(message):
    schedule = db.get_today_schedule(db.get_schedule_user(message.from_user.id))
    for curr in schedule:
        bot.send_message(message.from_user.id, curr)


@bot.message_handler(commands=['lesson'])
def handle_message(message):
    lesson = db.get_now_lesson(db.get_schedule_user(message.from_user.id))
    bot.send_message(message.from_user.id, lesson)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if constants.list_of_classes.count(message.text) != 0:
        db.update_user(message.from_user.id, message.text)
    else:
        bot.send_message(message.from_user.id, 'Ты ввел неправильный класс! Попробуй снова:)')

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
