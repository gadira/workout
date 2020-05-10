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


class Bot:  ## создаем класс бота
    def __init__(self):
        self.REQUEST_KWARGS = {  ## чтобы обойти блокировку телеграма
            'proxy_url': 'socks5://orbtl.s5.opennetwork.cc:999',
            'urllib3_proxy_kwargs': {
                'username': '158934764',
                'password': 'LhosT8Hc',
            }
        }
        self.updater = Updater("1166055541:AAGuaHZxazE3Z2O46xSf632wWLDohqC9WYk", use_context=True,
                               request_kwargs=self.REQUEST_KWARGS)



        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("start", self.start))   ## обработка самой первой команды
        self.dp.add_handler(MessageHandler(Filters.text, self.great_messages))  ## обработка остальных текстовых сообщений


        self.great_messages_list = ['Почитать о воркауте',  ## основной список главных команд
                               'Глянуть на разряды',
                               'Посмотреть базу данных упражнений',
                               'Получить советы по тренировкам',
                               'Прочитать крутой лайфхак',
                               'Определить свой уровень',
                               'Связаться с Диной']
        self.exc_list = ['ОТЖИМАНИЯ ОТ ПОЛА',  ## список категорий упражнений
                     'ПОДТЯГИВАНИЯ',
                    'ВИСЫ, БАЛАНСЫ И СТАТИКА',
                     'ПРОЧЕЕ',
                    'НАЗАД']


        self.categories = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'ОБРАТНО']  ## разряды

        self.my_id = '1269887405'  ## id  хозяина, т.е. меня


        self.updater.start_polling()  ## постоянный прием сообщений
        self.updater.idle()

    def start(self, update, ctx):  ## команда начала работы бота
        con = sqlite3.connect('for_wo.db')  ## подключение курсора
        cur = con.cursor()
        user_id = update['message']['chat']['id']   ## получаем имя и id пользователя
        user_name = update['message']['chat']['first_name']
        req = """SELECT * from users WHERE user_id='{n}'""".format(n=user_id)
        res = cur.execute(req).fetchall()    ## проверяем, есть ли он в нашей бд
        if res == []:  ## если он впервые пользуется нашим ботом
            req = """INSERT INTO users VALUES ('{n1}', '{n2}', '', '', '', '', '', '', '')""".format(n1=user_id, n2=user_name)
            cur.execute(req).fetchall()
            con.commit()  ## заводим главные переменные, которые гарантируют
            ## работу бота без сбоев

            reply_keyboard = [['Почитать о воркауте',   ## предлагаем пользователю наши функции
                               'Глянуть на разряды'],
                              ['Посмотреть базу данных упражнений',
                               'Получить советы по тренировкам'],
                              ['Прочитать крутой лайфхак',
                               'Определить свой уровень'],
                               ['Связаться с Диной']]

            req = """SELECT some from other WHERE what='{n}'""".format(n='hello')  ## достаем из бд приветственный текст
            hello = '\n'.join(cur.execute(req).fetchall()[0][0].split('&'''))  ## приводим его к нормальному виду

            update.message.reply_text(hello, reply_markup=ReplyKeyboardMarkup(reply_keyboard))
        else:  ## есди пользователь есть в бд
            reply_keyboard = [['Почитать о воркауте',   ##  та же клавиатура
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
                con.commit()  ## обнуляем все главные переменные, чтобы не возникло сбоев в работе бота


    def great_messages(self, update, context):  ## обработка остальных сообщений


        incorrect = False   ## эта переменная нужна для ответа пользователю в случае неправильного ввода
        ## какого-лиюо текста


        con = sqlite3.connect('for_wo.db')  ##  подключаем бд
        cur = con.cursor()
        user_id = update['message']['chat']['id']  ## получаем id пользователя
        #user_name = update['message']['chat']['first_name']


        req = "SELECT * FROM users WHERE user_id='{n}'".format(n=user_id)
        big_res = cur.execute(req).fetchall()[0]  ## получаем значение переменных из бд

        some_text = update.message.text
        ## текст, введенный пользователем

        if some_text in self.great_messages_list and big_res[2:] == ('', '', '', '', '', '', ''):
            if some_text == 'Почитать о воркауте':   ##   ну, здесь и так понятно
                req = """UPDATE users SET read_about_wo = 'True' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                req = """SELECT some from other WHERE what=='{n}'""".format(n='about_WO')
                about_WO = cur.execute(req).fetchall()[0][0]
                update.message.reply_text(about_WO)  ## отправка сообщения на запрос пользователя

                req = """UPDATE users SET read_about_wo = '' WHERE user_id = '{n}'""".format(n=user_id)
                cur.execute(req).fetchall()
                con.commit()

                req_list = ['read_categories', 'read_db', 'read_s', 'read_lifehaks', 'read_level',
                            'read_con']
                for i in range(len(req_list)):
                    req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                    cur.execute(req).fetchall()
                    con.commit()  ## обнуляем переменные

            elif some_text == 'Глянуть на разряды':  ## аналогичная работа
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
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard))

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

                req = 'SELECT some FROM other WHERE what="{n}"'.format(n='my_s')
                my_s = cur.execute(req).fetchall()[0][0]

                update.message.reply_text(my_s)


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

                    reply_keyboard = [['В СЛЕДУЮЩИЙ РАЗ', ], ]

                    dina = 'Если есть какие-то вопросы - пиши Дине в ВК, https://vk.com/dina_galeyeva. Лайкай фотки)'

                    update.message.reply_text(dina, reply_markup=ReplyKeyboardMarkup(reply_keyboard))
                    update.message.reply_sticker(
                        'CAACAgIAAxkBAAJfUF6x4F7CWcllCSIUU6zoiP2prC27AAIFAAPANk8T-WpfmoJrTXUZBA')

                    comment = 'Но лучше напиши свой вопрос мне сейчас, а я перешлю Дине. Не забудь оставить свои контакты!'
                    update.message.reply_text(comment)



            else:
                incorrect = True


        elif big_res[8] == 'True': ## связь со мной
            if str(user_id) != self.my_id: ## если пользователь хочет отправить мне сообщение

                if some_text == 'В СЛЕДУЮЩИЙ РАЗ':  ## сли передумал
                    text = 'Если что - обращайся!'

                    reply_keyboard = [['Почитать о воркауте',  ##  та же клавиатура
                                       'Глянуть на разряды'],
                                      ['Посмотреть базу данных упражнений',
                                       'Получить советы по тренировкам'],
                                      ['Прочитать крутой лайфхак',
                                       'Определить свой уровень'],
                                      ['Связаться с Диной']]

                    update.message.reply_text(text,
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard))

                else:  ## если все-таки решил отправить сообщение

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


        elif some_text in self.exc_list and big_res[4] != '': ## помощь в показе категорий упражнений в воркауте

            if some_text != 'НАЗАД':

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



        elif big_res[4] != '' and big_res[4] != 'True': ## описание эллемента из бд
            try:
                number = int(some_text) - 1
                if number < 0:
                    ## если номер упражнения некорректный, то мы гордо уйдем в except 
                    proverka = 1 / 0
                req = """SELECT link FROM wo WHERE category = '{n}'""".format(n=big_res[4])
                res = cur.execute(req).fetchall()[number][0] + '.mp4'
                any_text = 'Тут ⬇️ видео - обучалка или просто запись элемента'
                update.message.reply_text(any_text)
                update.message.reply_text(res)
            except:
                incorrect = True

        elif some_text in self.categories and big_res[3] == 'True': ##  читаем о разрядах в воркауте
            if some_text != 'ОБРАТНО':
                req = 'SELECT about FROM categories WHERE category="{n}"'.format(n=some_text)
                res = '\n'.join(cur.execute(req).fetchall()[0][0].split('&'))
                update.message.reply_text(res) ## сообщение о том, что нужно для сдачи разряда
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



        elif big_res[7] == 'True': ## если вы захотели опредедить уровень подготовки в воркауте:
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

                    req_list = ['read_about_wo', 'read_categories', 'read_db', 'read_s',
                                'read_lifehaks', 'read_level', 'read_con']

                    for i in range(len(req_list)): ## обнуляем переменные
                        req = 'UPDATE users SET {n}="" WHERE user_id="{n2}"'.format(n=req_list[i], n2=user_id)
                        cur.execute(req).fetchall()
                        con.commit()

                except: ## ответ на некорректное значение
                    update.message.reply_text('Введи-ка нормальные значения :)')
                    incorrect = True


        else: ## иначе - ответ на некорректное значение
            incorrect = True

        if incorrect:
            ## на случай, когда было введено некорректное значение
            ## три варианта ответа бота:
            incorrect_list = ['malina', 'sticker', 'wolf']
            incorrect = choice(incorrect_list)
            if incorrect == 'malina': ## картинка с малиной,
                update.message.reply_text('Что-то неправильно... Посмотри лучше на малину!')
                update.message.reply_photo('https://i.ibb.co/C6hWm5B/222717-Sepik.jpg')
            elif incorrect == 'sticker': ## стикер с вишней
                update.message.reply_text('Э-э, так не пойдет!')
                update.message.reply_sticker(
                    'CAACAgIAAxkBAAJfRF6x0_-vbNQKavUiHRm4jzarD6QaAAIgAAPANk8T9A8ruj5f9M8ZBA')
            elif incorrect == 'wolf': ## фото волка
                update.message.reply_text('Одумайся.')
                update.message.reply_photo('https://i.ibb.co/jbqS9rX/07ecd61ec447b9e88ab667cfb545693b.jpg')

            incorrect = False ## на всякий случай обнуляем переменную, отвечающую за эту функцию


    def your_level(self, a, b, c):  ## функция для определения уровня подготовки в воркауте
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
        return level, res  ## возвращаем уровень подготовки на словах и в процентах


if __name__ == '__main__':
    bot = Bot()