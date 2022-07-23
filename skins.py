import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    mes_start = (f'Welcome {message.from_user.first_name}!'
                f'\nPrint "/help" to see what i can do')
    bot.send_message(message.chat.id, mes_start)

@bot.message_handler(commands=['help'])
def help(message):
    mes_help = f'To get started, enter the name of the skin in this order:\nName | Quality | Purchase Price | Selling Price\nFor Example: M4A1-S|Nitro Field-Tested 100 75\n\nOr you can print "/temp" to see your last request!'
    bot.send_message(message.chat.id, mes_help)

@bot.message_handler(commands=['temp'])
def temp(message):
       temp = (config.temp).split()
       if temp[0] == 'ERROR':
           config.temp = 'Nothing here'
           bot.send_message(message.chat.id, config.temp)
       else:
           bot.send_message(message.chat.id, config.temp)

@bot.message_handler(content_types=['text'])
def skins(message):
    mes = str(message.text).split()
    mes_massive = len(mes)
    try:
        if mes_massive == 4:
            quality = mes[1]
            if quality in config.quality:
                try:
                    about = str(f'Your skin = {mes[0]}'
                    f'\nQuality = {quality}'
                    f'\nPurchase Price = {float(mes[2])} rub'
                    f'\nSelling Price = {float(mes[3])} rub'
                    f'\nGain = {float(mes[3]) - float(mes[2])} rub')
                except:
                    about = 'ERROR #1\nPrice Error'
                finally:
                    pass
            else:
                if mes_massive > 4:
                    about = 'ERROR #2\nMassive Error (Not enough values)'
                elif mes_massive < 4:
                    about = 'ERROR #3\nMassive Error (Not enough values)'
                elif mes_massive == 4:
                    quality = mes[1]
                    if quality in config.quality:
                        try:
                            about = str(f'Your skin = {mes[0]}'
                                        f'\nQuality = {quality}'
                                        f'\nPurchase Price = {float(mes[2])} rub'
                                        f'\nSelling Price = {float(mes[3])} rub'
                                        f'\nGain = {float(mes[3]) - float(mes[2])} rub')
                        except:
                            about = 'ERROR #4\nPrice Error'
                        finally:
                            pass
                    else:
                        about = 'ERROR #5\nPrice Error'
                else:
                    about = 'ERROR #6\nQuality is not in config'
        elif mes_massive == 5:
            quality = f'{mes[1]} {mes[2]}'
            if quality in config.quality:
                try:
                    about = str(f'Your skin = {mes[0]}'
                                f'\nQuality = {quality}'
                                f'\nPurchase Price = {float(mes[3])} rub'
                                f'\nSelling Price = {float(mes[4])} rub'
                                f'\nGain = {float(mes[4]) - float(mes[3])} rub')
                except:
                    about = 'ERROR #7\nPrice Error'
                finally:
                    pass
            else:
                about = 'ERROR #8\nPrice or Quality Error'
        elif mes_massive == 6:
            quality = mes[3]
            if quality in config.quality:
                try:
                    about = str(f'Your skin = {mes[0]} {mes[1]} {mes[2]}'
                                f'\nQuality = {quality}'
                                f'\nPurchase Price = {float(mes[4])} rub'
                                f'\nSelling Price = {float(mes[5])} rub'
                                f'\nGain = {float(mes[5]) - float(mes[4])} rub')
                except:
                    about = 'ERROR #9\nPrice Error'
            else:
                if mes_massive >6:
                    about = 'ERROR #10\nMassive Error (Not enough values)'
                elif mes_massive <6:
                    about = 'ERROR #11\nMassive Error (Not enough values)'
                elif mes_massive == 6:
                    quality = f'{mes[1]} {mes[2]} {mes[3]}'
                    if quality in config.quality:
                        try:
                            about = str(f'Your skin = {mes[0]}'
                                        f'\nQuality = {quality}'
                                        f'\nPurchase Price = {float(mes[4])} rub'
                                        f'\nSelling Price = {float(mes[5])} rub'
                                        f'\nGain = {float(mes[5]) - float(mes[4])} rub')
                        except:
                            about = 'ERROR #12\nPrice Error'
                    else:
                        about = 'ERROR #13\nQuality is not in config'
                else:
                    about = 'ERROR #14\nPrice Error'
        else:
            about = 'ERROR #15\nMassive Error (Not enough values)'
    finally:
        config.temp = about
        bot.send_message(message.chat.id, about)

#RUN
bot.polling(none_stop=True)

# cd C:\Users\coolm\Desktop\skins_bot\
# python skins_2.py