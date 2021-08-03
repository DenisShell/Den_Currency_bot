import telebot
from config_cb import keys,TOKEN
from extensions_cb import ConversionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Привет!\nЯ бот, который конвертирует валюты в режиме реального времени!\
    \nДля начала работы задай Боту следующие параметры в одну строку через пробел: \n<имя валюты> \
    \n<в какую валюту перевести> \
    <количество валюты> \
    \nНАПРИМЕР: доллар евро 1 \
    \nСписок доступных валют можно увидеть по команде:\n /values"
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Я могу конвертировать такие валюты:"
    for key in keys.keys():
        text = '\n'.join((text,key ))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Ошибка в параметрах, нужно три!\nпопробуй снова!')

        quote, base, amount = map(lambda x: x.lower(), values) #Название валют можно вводить с любым регистром
        total_base = CryptoConverter.convert(quote, base, amount)
        counter = float(values[2])
        total_summ = total_base * counter #подсчитываем количество валюты
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} равен {total_summ}'
        bot.send_message(message.chat.id, text)

bot.polling()
