import tkinter
from tkinter import *

win = Tk()
win.geometry('262x410')
win['bg'] = 'grey'
win.title('For work')
win.wm_attributes("-topmost", 1)  # поверх других окон


def baraban():
    baraban_d = d_baraban.get()
    if not baraban_d.isdigit():
        baraban_d = 400
        d_baraban.delete(0, END)
        d_baraban.insert(0, '400')
    else:
        baraban_d = int(baraban_d)

    lenta = need_width.get()
    if not lenta.isdigit():
        lenta = 20
        need_width.delete(0, END)
        need_width.insert(0, '20')
    lenta = int(lenta) / 10

    value = baraban_d / 20  # из диаметра в мм. считаем радиус в см.
    value = value ** 2  # радиус в квадрате
    value = value * 3.14  # и умножить на Пи = площадь барабана см2
    value = value * lenta  # площадь барабана умножить на ширину ленты = ОБЪЁМ барабана см3
    value = value * 7.85  # ОБЪЁМ барабана см3 умножить на удельный вес металла = вес барабана гр.
    baraban_weight = round(value / 1000, 2)  # вес в граммах переводим в килограммы
    return baraban_weight


def start():
    baraban_weight = baraban()
    value = need_weight.get()
    lenta = int(need_width.get()) / 10
    radiubaraban_weighta = int(d_baraban.get()) / 20
    if not value.isdigit():
        value = 'ВВЕДИТЕ НУЖНЫЙ ВЕС'
    else:
        value = int(value) + baraban_weight  # прибавляем вес барабана
        value = value * 1000  # и переводим в граммы
        value = value / 7.85  # делим на удельный вес металла, что бы получить ОБЪЁМ металла
        value = value / lenta  # делим объём на щирину ленты в см., что бы получить ПЛОЩАДЬ металла
        value = (value / 3.14) ** 0.5  # Делим на Пи и извлекаем кв. корень, что бы узнать радиус (S=π r**)
        value = round(value - radiubaraban_weighta, 2)
        value = str(value) + ' см. нужный намот'
    result["text"] = value


# ДИАМЕТР БАРАБАНА
d_baraban = Entry(win, background="grey", font=('Garamond', 30), width=3)
d_baraban.place(x=10, y=30, height=34)
d_baraban.insert(0, '400')
label_baraban = Label(text='Ø барабана', font=('Arial', 11), bg='grey').place(x=75, y=43)

# ШИРИНА ЛЕНТЫ
need_width = Entry(win, background="white", fg='grey', justify=tkinter.CENTER, font=('Garamond', 15), width=5)
need_width.place(x=10, y=85, height=25)
need_width.insert(0, '20')
label_width = Label(text='ширина ленты (мм.)', font=('Arial', 11), bg='grey').place(x=70, y=87)

# НУЖНЫЙ ВЕС БУХТЫ
need_weight = Entry(win, background="white", justify=tkinter.CENTER, font=('Garamond', 15), width=5)
need_weight.place(x=10, y=111, height=25)
need_weight.insert(0, '50')
label_need = Label(text='нужный вес', font=('Arial', 11), bg='grey').place(x=70, y=114)

# ИТОГ
result = Label(text='', font=('Arial', 12), bg='grey')
result.place(x=40, y=140)

# КНОПКА "РАССЧИТАТЬ"
b1 = Button(win, text='Рассчитать', font=('Arial', 11), command=start)
b1.place(x=70, y=170, height=30, width=115)

def click_weight(event):
    need_weight.delete(0, END)

def click_width(event):
    need_width.delete(0, END)

def click_baraban(event):
    d_baraban.delete(0, END)

need_weight.bind("<ButtonPress>", click_weight)
need_width.bind("<ButtonPress>", click_width)
d_baraban.bind("<ButtonPress>", click_baraban)



win.mainloop()
