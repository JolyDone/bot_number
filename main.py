import telebot  # подключение библиотеки pyTelegramBotAPI
from telebot import types
import numexpr  # подключение библеотеки для работы с str
from sympy import *  # подключение математики
bot = telebot.TeleBot('token')  # токен
@bot.message_handler(commands=['start'])  # команда /start и создание кнопок
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Метод Бисекции")
    btn2 = types.KeyboardButton("Метод Ньютона")
    btn3 = types.KeyboardButton("Метод Эйлера")
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id,'Заменяем ^ на **', reply_markup=markup);
    # выше отправка сообщения с информацией по заполнению

@bot.message_handler(content_types=['text'])
# работа с текстом и выбор метода
def button_message(message):
    if message.text == 'Метод Бисекции':
        bot.send_message(message.from_user.id, "введите функцию");
        bot.register_next_step_handler(message, bisec);
    elif message.text == '/eiter':
        bot.send_message(message.from_user.id, "введите функцию");
        bot.register_next_step_handler(message, eiter);
    elif message.text == 'Метод Ньютона':
        bot.send_message(message.from_user.id, "введите функцию");
        bot.register_next_step_handler(message, newton);
    elif message.text == 'Метод Эйлера':
        bot.send_message(message.from_user.id, "введите функцию");
        bot.register_next_step_handler(message, eiler);

# метод Бисекции
def bisec(message):
    try:
        xer = message.text  # получение сообщения от пользователя
        zp = xer.split()  # разделение сообщения
        def f(x):  # функция для вычесления значения f(x)
            name = zp[0]  # выделение самой f(x) из разделенного словаря
            name = numexpr.evaluate(name)  # преобразование из str
            return name
        a = float(zp[1])  # получение значение левой границы 'a'
        b = float(zp[2])  # получение значение правой границы 'b'
        e = float(zp[3])  # получение условной погрешности
        x0 = (a+b)/2  # получение нулевого приближения
        ya = f(a)  # вычисление границы
        i = 0  # счетчик
        while b-a > 2*e:
            i+=1
            y = f(x0)
            if y*ya<0:
                b=x0
            else:
                a = x0
                ya = y
            x0 = (b+a)/2
            bot.send_message(message.chat.id, 'Значение корня'+ str(i) + " " + str(x0)[0:6])  # вывод значения
            print(message.chat.id, 'Значение корня'+ str(i) + " " + str(x0)[0:6])  # вывод значения
    except:
        bot.send_message(message.from_user.id, "Произошла ошибка. Проверьте правильность введённых данных.");

def eiter(message):###############################################################################################
    xer = message.text
    zp = xer.split()
    def f(x):
        name = zp[0]
        name = numexpr.evaluate(name)
        return name
    x0 = zp[1]
    M = zp[2]
    m = zp[3]
    e = zp[4]
    alpha = 2/(M + m)
    e = (2*m*e)/(M - m)
    x = x0 - alpha*f(x0)
    while abs(x-x0) > e:
        x0 = x
    bot.send_message(message.chat.id, 'Значение корня' +  " " + str(x)[0:6])
    print(message.chat.id, 'Значение корня'+ " " + str(x)[0:6])

# метод Ньютона
def newton(message):
    try:
        xer = message.text  # получение сообщения от пользователя
        zp = xer.split()  # разделение сообщения
        # функция получения значения f(x)
        def f(x):
            name = zp[0]
            name = eval(name)  # numexpr отказался работать и был заменен на функцию eval()
            return name
        # функция получения производной от f(x)
        def fd(y):
            name = zp[0]
            f = Symbol("x")  # обозначение по чему берем производную
            df = diff(name)  # взятие производной
            vf = str(df)  # приколы с типами
            x = float(y)
            zf = eval(vf)
            return zf
        x0 = float(zp[1])  # получение нулевого приближения
        e = float(zp[2])  # получение условного приюлижения
        alpha = 1/(fd(x0))
        x = x0 - alpha*f(x0)
        while abs(x-x0) > e:
            x0 = x
            alpha = 1 / (fd(x0))
            x = x0 - alpha * f(x0)
        bot.send_message(message.chat.id, 'Значение корня' +  " " + str(x)[0:6])
        print(message.chat.id, 'Значение корня'+ " " + str(x)[0:6])
    except:
        bot.send_message(message.from_user.id, "Произошла ошибка. Проверьте правильность введённых данных.");
#  Метод Эйлера
def eiler(message):
    try:
        xer = message.text  # получение сообщения от пользователя
        zp = xer.split()  # разделение сообщения
        def f(t,y):
            name = zp[0]
            print(name)
            name = eval(name)
            return name
        t0 = float(zp[1])  # получение левой границы
        y0 = float(zp[2])  # получение значения
        T = float(zp[3])  # получение макс значения
        h = float(zp[4])  # получение шага
        n = 1  # счетчик
        N = ((T-t0)/h)  # вычисление сетки
        hf = h*f(t0, y0)
        y = y0
        while n<=N:
            n+=1
            y = y + hf
            print(message.chat.id, 'Значение корня' + " " + str(y)[0:8])
            hf = h*f(t0+h, y)
            t0+=h
            print(message.chat.id, 'Значение функции' + " " + str(hf)[0:8])
        bot.send_message(message.chat.id, 'Значение корня' +  " " + str(y)[0:8])
        bot.send_message(message.chat.id, 'Значение функции' + " " + str(hf)[0:8])
        print(message.chat.id, 'Значение корня'+ " " + str(y)[0:6])
    except:
        bot.send_message(message.from_user.id, "Произошла ошибка. Проверьте правильность введённых данных.");


bot.infinity_polling()