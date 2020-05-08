## imports
import logging
import telegram
from pprint import pprint
import requests
from random import choice
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import NetworkError, Unauthorized
from time import sleep
import sqlite3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


## imports


class Bot:
    def __init__(self):
        self.REQUEST_KWARGS = {
            'proxy_url': 'socks5://orbtl.s5.opennetwork.cc:999',
            'urllib3_proxy_kwargs': {
                'username': '158934764',
                'password': 'LhosT8Hc',
            }
        }
        self.updater = Updater("1166055541:AAGuaHZxazE3Z2O46xSf632wWLDohqC9WYk", use_context=True,
                               request_kwargs=self.REQUEST_KWARGS)



        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(MessageHandler(Filters.text, self.great_messages))
        #self.dp.add_handler(CallbackQueryHandler(self.button))

        self.great_messages_list = ['Почитать о воркауте',
                               'Глянуть на разряды',
                               'Посмотреть базу данных упражнений',
                               'Получить советы по тренировкам',
                               'Прочитать крутой лайфхак',
                               'Определить свой уровень',
                               'Связаться с Диной']
        self.exc_list = ['ОТЖИМАНИЯ ОТ ПОЛА',
                     'ПОДТЯГИВАНИЯ',
                    'ВИСЫ, БАЛАНСЫ И СТАТИКА',
                     'ПРОЧЕЕ',
                    'НАЗАД']


        self.categories = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'ОБРАТНО']

        self.my_id = '1269887405'


        self.updater.start_polling()
        self.updater.idle()

    def start(self, update, ctx):
        con = sqlite3.connect('for_wo.db')
        cur = con.cursor()
        user_id = update['message']['chat']['id']
        user_name = update['message']['chat']['first_name']
        req = """SELECT * from users WHERE user_id='{n}'""".format(n=user_id)
        res = cur.execute(req).fetchall()
        if res == []:
            #print('ddddddd')
            req = """INSERT INTO users VALUES ('{n1}', '{n2}', '', '', '', '', '', '', '')""".format(n1=user_id, n2=user_name)
            cur.execute(req).fetchall()
            con.commit()
            #print('adadadd')

            reply_keyboard = [['Почитать о воркауте',
                               'Глянуть на разряды'],
                              ['Посмотреть базу данных упражнений',
                               'Получить советы по тренировкам'],
                              ['Прочитать крутой лайфхак',
                               'Определить свой уровень'],
                               ['Связаться с Диной']]

            req = """SELECT some from other WHERE what='{n}'""".format(n='hello')
            hello = '\n'.join(cur.execute(req).fetchall()[0][0].split('&'''))

            update.message.reply_text(hello, reply_markup=ReplyKeyboardMarkup(reply_keyboard)) #one_time_keyboard=True))
        else:
            reply_keyboard = [['Почитать о воркауте',
                               'Глянуть на разряды'],
                              ['Посмотреть базу данных упражнений',
                               'Получить советы по тренировкам'],
                              ['Прочитать крутой лайфхак',
                               'Определить свой уровень'],
                              ['Связаться с Диной']]

            update.message.reply_text('Хорошо :)'
                ,
                reply_markup=ReplyKeyboardMarkup(reply_keyboard))

            req_list = ['read_about_wo', 'read_categories', 'read_db', 'read_s', 'read_lifehaks', 'read_level', 'read_con']
            for i in range(len(req_list)):
                req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i],n2=user_id)
                cur.execute(req).fetchall()
                con.commit()


    def great_messages(self, update, context):


        incorrect = False


        con = sqlite3.connect('for_wo.db')
        cur = con.cursor()
        user_id = update['message']['chat']['id']
        #user_name = update['message']['chat']['first_name']

        print(type(self.my_id), type(user_id))

        req = "SELECT * FROM users WHERE user_id='{n}'".format(n=user_id)
        big_res = cur.execute(req).fetchall()[0]

        some_text = update.message.text
        # print(big_res)

        if some_text in self.great_messages_list and big_res[2:] == ('', '', '', '', '', '', ''):
            if some_text == 'Почитать о воркауте':
                req = """UPDATE users SET read_about_wo = 'True' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                req = """SELECT some from other WHERE what=='{n}'""".format(n='about_WO')
                about_WO = cur.execute(req).fetchall()[0][0]
                update.message.reply_text(about_WO)

                req = """UPDATE users SET read_about_wo = '' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                req_list = ['read_categories', 'read_db', 'read_s', 'read_lifehaks', 'read_level',
                            'read_con']
                for i in range(len(req_list)):
                    req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                    cur.execute(req).fetchall()
                    con.commit()

            elif some_text == 'Глянуть на разряды':
                wich_category = 'Какой разряд вас интересует?'
                reply_keyboard = [['I',
                                   'II', 'III', 'IV'],
                                  ['V', 'VI', 'VII'],
                                  ['ОБРАТНО']]

                update.message.reply_text(wich_category
                                          ,
                                          reply_markup=ReplyKeyboardMarkup(reply_keyboard))

                req = """UPDATE users SET read_categories = 'True' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                req_list = ['read_about_wo', 'read_db', 'read_s', 'read_lifehaks', 'read_level',
                            'read_con']
                for i in range(len(req_list)):
                    req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                    # print(req)
                    cur.execute(req).fetchall()
                    con.commit()



            elif some_text == 'Прочитать крутой лайфхак':

                req = """UPDATE users SET read_lifehaks = 'True' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                req = """SELECT * from lifehaks"""
                lifehaks = cur.execute(req).fetchall()
                my_live_hak = choice(lifehaks)
                print(my_live_hak)
                maybe_image = my_live_hak[2][:]
                print('d', maybe_image)
                my_live_hak = my_live_hak[0] + '\n' + my_live_hak[1]
                update.message.reply_text(my_live_hak)
                update.message.reply_photo(maybe_image)

                req = """UPDATE users SET read_lifehaks = '' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                req_list = ['read_about_wo', 'read_categories', 'read_db', 'read_s', 'read_level',
                            'read_con']
                for i in range(len(req_list)):
                    req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                    print(req)
                    cur.execute(req).fetchall()
                    con.commit()

            elif some_text == 'Посмотреть базу данных упражнений':

                req = """UPDATE users SET read_db = 'True' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                reply_keyboard = [['ОТЖИМАНИЯ ОТ ПОЛА',
                                   'ПОДТЯГИВАНИЯ'],
                                  ['ВИСЫ, БАЛАНСЫ И СТАТИКА',
                                   'ПРОЧЕЕ'],
                                  ['НАЗАД']]

                update.message.reply_text(
                    'Выбери тот раздел, к которому относится упражнение, о котором ты хочешь узнать подробнее!'
                    ,
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard))  # one_time_keyboard=True))

                req_list = ['read_about_wo', 'read_categories', 'read_s', 'read_lifehaks', 'read_level',
                            'read_con']
                for i in range(len(req_list)):
                    req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                    cur.execute(req).fetchall()
                    con.commit()

            elif some_text == 'Определить свой уровень':

                req = 'UPDATE users SET read_level="True" WHERE user_id="{n}"'.format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                reply_keyboard = [['Я ПЕРЕДУМАЛ', ], ]

                update.message.reply_text('Введите через пробел, сколько раз вы можете'
                                          ' подтянуться, отжаться и продержать уголок под турником(в секундах)',
                                          reply_markup=ReplyKeyboardMarkup(reply_keyboard))

                req_list = ['read_about_wo', 'read_categories', 'read_db', 'read_s', 'read_lifehaks',
                            'read_con']
                for i in range(len(req_list)):
                    req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                    print(req)
                    cur.execute(req).fetchall()
                    con.commit()

            elif some_text == 'Получить советы по тренировкам':
                req = 'UPDATE users SET read_s="True" WHERE user_id="{n}"'.format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                update.message.reply_text(
                    'Это действие пока, к сожалению, недоступно, но могу посоветовать классную группу в ВК, где могут хорошо '
                    'помочь - https://vk.com/wfsng. Ну а если ты из Казани - добро пожаловать в нашу беседу! '
                    'https://vk.me/join/AJQ1dwun_giQYllkUmBt88fM')
                update.message.reply_sticker(
                    'CAACAgIAAxkBAAJfTl6x3vRTquhJCYJnrTVxE31T8871AAINAAPANk8TpPnh9NR4jVMZBA')

                req_list = ['read_about_wo', 'read_level', 'read_categories', 'read_db', 'read_s', 'read_lifehaks',
                            'read_con']
                for i in range(len(req_list)):
                    req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                    print(req)
                    cur.execute(req).fetchall()
                    con.commit()

            elif some_text == 'Связаться с Диной':
                if self.my_id == str(user_id):
                    print('dfdd')
                    update.message.reply_text('<Режим "хозяин" активирован>')

                    req = "SELECT * from comments WHERE is_read=''"
                    comments = cur.execute(req).fetchall()
                    print(comments)
                    if comments == []:
                        update.message.reply_text('Пока новых сообщений для тебя нет ')
                    else:
                        for i in range(len(comments)):
                            text = 'Пользователь с id {n} оставил сообщение: <{n2}>'.format(n=comments[i][0],
                                                                                          n2=comments[i][1])
                            comments[i] = text
                        req = "UPDATE comments SET is_read='True'"
                        cur.execute(req).fetchall()
                        con.commit()
                        text = '\n'.join(comments)
                        update.message.reply_text(text)

                    req_list = ['read_about_wo', 'read_level', 'read_categories', 'read_db', 'read_s', 'read_lifehaks',
                                'read_con']
                    for i in range(len(req_list)):
                        req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                        cur.execute(req).fetchall()
                        con.commit()

                else:
                    req = 'UPDATE users SET read_con="True" WHERE user_id="{n}"'.format(n=user_id)
                    cur.execute(req).fetchall()
                    con.commit()

                    dina = 'Если есть какие-то вопросы - пиши Дине в ВК, https://vk.com/dina_galeyeva. Лайкай фотки)'

                    update.message.reply_text(dina)
                    update.message.reply_sticker(
                        'CAACAgIAAxkBAAJfUF6x4F7CWcllCSIUU6zoiP2prC27AAIFAAPANk8T-WpfmoJrTXUZBA')

                    comment = 'Но лучше напиши свой вопрос мне сейчас, а я перешлю Дине. Не забудь оставить свои контакты!'
                    update.message.reply_text(comment)



            else:
                incorrect = True


        elif big_res[8] == 'True':
            if str(user_id) != self.my_id:

                req = 'INSERT INTO comments VALUES ("{n}", "{n2}", "")'.format(n=user_id, n2=some_text)
                cur.execute(req).fetchall()
                con.commit()


                update.message.reply_text('Отлично! Я отправил сообщение Дине. Если захочешь'
                                          ' написать еще какое-то сообщение по улучшению моей работы,'
                                          ' то еще раз нажми на "Связаться с Диной"')

                req_list = ['read_about_wo', 'read_level', 'read_categories', 'read_db', 'read_s', 'read_lifehaks',
                            'read_con']
                for i in range(len(req_list)):
                    req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                    cur.execute(req).fetchall()
                    con.commit()


        elif some_text in self.exc_list and big_res[4] != '':

            # req = """SELECT read_db from users WHERE user_id='{n}'""".format(n=user_id)
            # res = cur.execute(req).fetchall()

            if some_text != 'НАЗАД':

                # ТЫ остановилась здесь, нужно доделать верх этого элифа!!!!

                req = """UPDATE users SET  read_db= '{n1}' WHERE user_id = '{n2}'""".format(n1=some_text,
                                                                                            n2=user_id)
                cur.execute(req).fetchall()
                con.commit()

                req = """SELECT title, link FROM wo WHERE category = '{n}'""".format(n=some_text)
                con = sqlite3.connect('for_wo.db')
                cur = con.cursor()
                res = cur.execute(req).fetchall()
                for i in range(len(res)):
                    res[i] = str(i + 1) + '. ' + res[i][0]
                self.category = some_text[:]
                res.append('Выше ты увидел список известных мне упражнений. А хочешь увидеть'
                           ' исполнение? Напиши мне его номер без точки')

                update.message.reply_text('\n'.join(res))
                del res[-1]
            elif some_text == 'НАЗАД':

                req = """UPDATE users SET read_db = '' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                reply_keyboard = [['Почитать о воркауте',
                                   'Глянуть на разряды'],
                                  ['Посмотреть базу данных упражнений',
                                   'Получить советы по тренировкам'],
                                  ['Прочитать крутой лайфхак',
                                   'Определить свой уровень'],
                                  ['Связаться с Диной']]

                update.message.reply_text('Если что - обращайся!',
                                          reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            else:
                incorrect = True



        elif big_res[4] != '' and big_res[4] != 'True':
            try:
                number = int(some_text) - 1
                if number < 0:
                    proverka = 1 / 0
                req = """SELECT link FROM wo WHERE category = '{n}'""".format(n=big_res[4])
                res = cur.execute(req).fetchall()[number][0] + '.mp4'
                any_text = 'Тут ⬇️ видео - обучалка или просто запись элемента'
                update.message.reply_text(any_text)
                update.message.reply_text(res)
            except:
                incorrect = True

        elif some_text in self.categories and big_res[3] == 'True':
            if some_text != 'ОБРАТНО':
                req = 'SELECT about FROM categories WHERE category="{n}"'.format(n=some_text)
                res = '\n'.join(cur.execute(req).fetchall()[0][0].split('&'))
                update.message.reply_text(res)
            elif some_text == 'ОБРАТНО':
                req = """UPDATE users SET read_categories = '' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                reply_keyboard = [['Почитать о воркауте',
                                   'Глянуть на разряды'],
                                  ['Посмотреть базу данных упражнений',
                                   'Получить советы по тренировкам'],
                                  ['Прочитать крутой лайфхак',
                                   'Определить свой уровень'],
                                  ['Связаться с Диной']]

                update.message.reply_text('Если что - обращайся!',
                                          reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            else:
                incorrect = True



        elif big_res[7] == 'True':
            if some_text == 'Я ПЕРЕДУМАЛ':
                any_text = 'Если что - обращайся!'
                req = 'UPDATE users SET read_level="" WHERE user_id="{n}"'.format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                reply_keyboard = [['Почитать о воркауте',
                                   'Глянуть на разряды'],
                                  ['Посмотреть базу данных упражнений',
                                   'Получить советы по тренировкам'],
                                  ['Прочитать крутой лайфхак',
                                   'Определить свой уровень'],
                                  ['Связаться с Диной']]

                update.message.reply_text(any_text, reply_markup=ReplyKeyboardMarkup(reply_keyboard))
            else:
                try:
                    a, b, c = list(map(lambda x: abs(int(x)), some_text.split(' ')))
                    print(a, b, c)
                    level, res = self.your_level(a, b, c)
                    your_level = 'Вы - {n}, уровень вашего мастерства в WorkOut - {n2}%'.format(n=level, n2=res)

                    reply_keyboard = [['Почитать о воркауте',
                                       'Глянуть на разряды'],
                                      ['Посмотреть базу данных упражнений',
                                       'Получить советы по тренировкам'],
                                      ['Прочитать крутой лайфхак',
                                       'Определить свой уровень'],
                                      ['Связаться с Диной']]

                    update.message.reply_text(your_level, reply_markup=ReplyKeyboardMarkup(reply_keyboard))

                    req_list = ['read_about_wo', 'read_categories', 'read_db', 'read_s', 'read_lifehaks',
                                'read_level',
                                'read_con']
                    for i in range(len(req_list)):
                        req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                        cur.execute(req).fetchall()
                        con.commit()

                except:
                    update.message.reply_text('Введи-ка нормальные значения :)')
                    incorrect = True


        else:
            incorrect = True

        if incorrect:
            incorrect_list = ['malina', 'sticker', 'wolf']
            incorrect = choice(incorrect_list)
            if incorrect == 'malina':
                update.message.reply_text('Что-то неправильно... Посмотри лучше на малину!')
                update.message.reply_photo('https://i.ibb.co/C6hWm5B/222717-Sepik.jpg')
            elif incorrect == 'sticker':
                update.message.reply_text('Э-э, так не пойдет!')
                update.message.reply_sticker(
                    'CAACAgIAAxkBAAJfRF6x0_-vbNQKavUiHRm4jzarD6QaAAIgAAPANk8T9A8ruj5f9M8ZBA')
            elif incorrect == 'wolf':
                update.message.reply_text('Одумайся.')
                update.message.reply_photo('https://i.ibb.co/jbqS9rX/07ecd61ec447b9e88ab667cfb545693b.jpg')

            incorrect = False

    def button(self, update, context):
        print('dfdfdf')
        update.message.reply_video('')





    def your_level(self, a, b, c):
        if a > 50:
            a = 50
        if b > 100:
            b = 100
        if c > 50:
            c = 50
        res = (a + b // 2 + c) // 3 * 2
        if res < 11:
            level = 'новичок'
        elif res < 21:
            level = 'начинающий'
        elif res < 51:
            level = 'продолжающий'
        elif res < 76:
            level = 'опытный'
        elif res < 91:
            level = 'мастер'
        else:
            level = 'профессионал'
        print(level, res)
        return level, res


if __name__ == '__main__':
    bot = Bot()