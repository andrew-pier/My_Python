from tkinter import *
from tkinter import messagebox, Tk, Button
from pygame import mixer
import time
import random
from PIL import Image, ImageTk

# initialize the pygame mixer
mixer.init(44100)


win = Tk()
app_running = True
screen_width = win.winfo_screenwidth() #    ОПРЕДЕЛЕНИЕ РАЗМЕРОВ ЭКРАНА ШИРИНА (ОСЬ Х)
# screen_height = win.winfo_screenheight()  #    ОПРЕДЕЛЕНИЕ РАЗМЕРОВ ЭКРАНА ВЫСОТА (ОСЬ Y)
print(screen_width, 'screen_height')
# side_x = side_y = '800'

#side_x = side_y = str(screen_height // 10 * 9) # УСТАНАВЛИВАЕМ РАМЕР ОКНА 90% ОТ РАЗМЕРА ЭКРАНА ПО ОСИ y
side_x = side_y = '804'  # УСТАНАВЛИВАЕМ РАМЕР ОКНА 804
win_resolution = str(side_x + 'x' + side_y)
# print(win_resolution)

# cell_width = int(side_x) // 12 # НАХОДИМ ЩИРИНУ КЛЕТКИ
# cell_height = int(cell_width * 1.5) # НАХОДИМ ДЛИНУ КЛЕТКИ
# print(cell_width, cell_height)


win.geometry('804x804+364+10')
win.title('MONOPOLY')
win.wm_attributes("-topmost", 1)  # поверх других окон
win.resizable(False, False)  # запрещаем изменение размера окна
py_image1 = PhotoImage(file="monopoly.png")
canvas = Canvas(win, width=side_x, height=side_y, bd=0, highlightthickness=0)
canvas.create_image(402, 402, image=py_image1)

chips_player1 = canvas.create_oval(727, 700, 771, 744, fill='red')
chips_player2 = canvas.create_oval(727, 750, 771, 794, fill='blue')
player1 = 0 # местоположение фишки игрока 1 на игровом поле (номер клетки)
player2 = 0 # местоположение фишки игрока 2 на игровом поле (номер клетки)
cash_player1 = 1500 # начальная сумма игрока 1
cash_player2 = 1500 # начальная сумма игрока 2
in_jail = [None, None ,0 , 0]
p1 = {} # СОБСТВЕННОСТЬ ИГРОКА 1
p2 = {} # СОБСТВЕННОСТЬ ИГРОКА 2

money = mixer.Sound("money.mp3")
add_money = mixer.Sound("coins-pour-out.mp3")
sound_dice1 = mixer.Sound("roll dice1.mp3")
sound_dice2 = mixer.Sound("roll dice2.mp3")
sound_dice3 = mixer.Sound("roll dice3.mp3")
sound_dice4 = mixer.Sound("roll dice4.mp3")
sound_jail = mixer.Sound("jail.mp3")
dice = PhotoImage(file="dice.png")
add_money.set_volume(0.5)
double = 0 # подсчёт выпавших дублей
player = chips_player1 # АКТИВНЫЙ ИГРОК (какой игрок начинает ход)
next_step = True # РАЗРЕШЕНИЕ ДЕЛАТЬ СЛЕДУЮЩИЙ ХОД

cash1 = Label(win, text='PLAYER 1 = ' + str(cash_player1) + '₽', font=('Helvetica', 16), bg='#ddf2df', relief="solid" ,borderwidth=1)
cash1.place(x=120, y=120)
cash2 = Label(win, text='PLAYER 2 = ' + str(cash_player2) + '₽', font=('Helvetica', 16), bg='#ddf2df', relief="solid" ,borderwidth=1)
cash2.place(x=120, y=155)

cells = {}
cells[1]=[0,60,2,'Grey', 'СЕННАЯ', 10, 30, 90, 160, 250, 50, 50]
cells[3]=[0,60,4,'Grey', 'СТ. АРБАТ', 20, 60, 180, 320, 450, 50, 50]
cells[6]=[0,100,6,'lightblue', 'пр. ЛЕНИНА', 30, 90, 270, 400, 550, 50, 50]
cells[8]=[0,100,6,'lightblue', 'пр. К. МАРКСА', 30, 90, 270, 400, 550, 50, 50]
cells[9]= [0,120,8,'lightblue', 'НЕВСКИЙ пр.', 40, 100, 300, 450, 600, 50, 50]
cells[11]=[0,140,10,'Pink', 'КАФЕ АРИЯ', 50, 150, 450, 625, 750, 100, 100]
cells[13]=[0,140,10,'Pink', 'ЬУРГЕР МАК', 50, 150, 450, 625, 750, 100, 100]
cells[14]=[0,160,12,'Pink', 'ПИЦЦА-РАН', 60, 180, 500, 700, 900, 100, 100]
cells[16]=[0,180,14,'Orange', 'КИНО-СТАР',70, 200, 550, 750, 950, 100, 100]
cells[18]=[0,180,14,'Orange', 'ТЕАТР БДТ', 70, 200, 550, 750, 950, 100, 100]
cells[19]=[0,200,16,'Orange', 'БОЛЬШОЙ ТЕАТР', 80, 220, 600, 800, 1000, 100, 100]
cells[21]=[0,220,18,'Red', 'САЛОН KIA', 90, 250, 700, 875, 1050, 150, 150]
cells[23]=[0,220,18,'Red', 'САЛОН UAZ', 90, 250, 700, 875, 1050, 150, 150]
cells[24]=[0,240,20,'Red', 'САЛОН BMW', 100, 300, 750, 925, 1100, 150, 150]
cells[26]=[0,260,22,'Yellow', 'БИЛАЙН', 110, 330, 800, 975, 1150, 150, 150]
cells[27]=[0,260,22,'Yellow', 'ТЕЛЕ2', 110, 330, 800, 975, 1150, 150, 150]
cells[29]=[0,280,24,'Yellow', 'МТС', 120, 360, 850, 1025, 1200, 150, 150]
cells[31]=[0,300,26,'Green', 'ПАРК ГОРЬКОГО', 130, 390, 900, 1100, 1278, 200, 200]
cells[32]=[0,300,26,'Green', 'ЛОМОНОСОВСКИЙ', 130, 390, 900, 1100, 1278, 200, 200]
cells[34]=[0,320,28,'Green', 'ПАРК ПОБЕДЫ', 150, 390, 900, 1200, 1400, 200, 200]
cells[37]=[0,350,35,'Blue', 'СЕННАЯ ПЛ.', 175, 500, 1100, 1300, 1500, 200, 200]
cells[39]=[0,400,50,'Blue', 'СТ. АРБАТ',175, 500, 1100, 1700, 2000, 200, 200]
cells[5]=[0,200,25,'Railway', 'ЛЕНИНГРАДСКИЙ ВОКЗАЛ']
cells[15]=[0,200,25,'Railway', 'ВОКЗАЛ КИНГИСЕПП']
cells[25]=[0,200,25,'Railway', 'МОСКОВСКИЙ ВОКЗАЛ']
cells[35]=[0,200,25,'Railway', 'ВОКЗАЛ ВЛАДИВОСТОК']
cells[12]=[0,150,4,'Com', 'РОСЭНЕРГО']
cells[28]=[0,150,4,'Com', 'ВОДОКАНАЛ']


# ДИСПЛЕЙ ОТОБРАЖЕНИЯ ХОДОВ
# text = Text(width=34, height=17, bg="lightgreen", fg='darkgreen', font=("TkDefaultFont", 11), wrap=WORD)
text = Text(width=39, height=17, bg="lightgreen", fg='darkgreen', font=('Arial', 10), wrap=WORD)
text.tag_configure("bold_tag", font=('Arial', 10, "bold"))
text.insert(1.0, ' ХОД 1-го ИГРОКА \n')
text.place(x=407, y=121)


# СОЗДАЁМ МЕТКИ СОБСТВЕННОСТИ ВОЗЛЕ ЯЧЕЕК ИГРОВОГО ПОЛЯ
x = 757 #692 + 65
y = 695
marker = [0] # СПИСОК id МЕТОК ПРИНАДЛЕЖНОСТИ КЛЕТОК
for i in range(1, 41):
    # print(i)
    # if i in [0, 2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38]: continue
    # else: a = cells[i][0]
    # if a == chips_player1: color = 'red'
    # elif a == chips_player2: color' = 'blue'
    # else: color = ''

    if i in (10, 20, 30, 40): marker.append('no-' + str(i)) # continue

    if i < 10:  #
        x -= 65
        marker.append(canvas.create_rectangle(x, y, x - 65, y - 7, fill='', width=0))
    elif i > 10 and i < 20:  #
        y -= 65
        x = 107
        marker.append(canvas.create_rectangle(x, y, x + 7, y + 65, fill='', width=0))
    elif i >20 and i < 30:  #
        x += 65
        y = 107
        marker.append(canvas.create_rectangle(x, y, x - 65, y + 7, fill='', width=0))
    elif i > 30 :
        x = 693#
        y += 65
        marker.append(canvas.create_rectangle(x, y, x - 7, y - 65, fill='', width=0))
# print(marker)
# canvas.itemconfig(marker[11], fill='red')

def sob (): # ПРОВЕРКА СОБСТВЕННОСТИ
    global p1, p2
    for i in range(1, 40): # ЗАПОЛНЯЕМ СПИСОК КУПЛЕННЫХ ПРЕДПРИЯТИЙ ИГРОКА 1 (p1) И ИГРОКА 2 (p2)
        if i in [0, 2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38]: continue
        else: a = cells[i][0]
        if a == chips_player1: p1[i]=[cells[i][2],cells[i][3]]
        elif a == chips_player2: p2[i] = [cells[i][2], cells[i][3]]

    # ПРОВЕРКА НА КОЛ-ВО ЭЛЕМЕНТОВ ОДНОЙ ГРУППЫ
    color_group = ['Grey', 'Lightblue', 'Pink', 'Orange', 'Red', 'Yellow', 'Green', 'Blue', 'Railway', 'Com']
    for i in color_group: # ПРОВЕРЯЕМ СПИСОК ПРЕДПРИЯТИЙ ИГРОКА 1 НА КОЛ-ВО ЭЛЕМЕНТОВ ОДНОГО ЦВЕТА
        n = (list([key for key, value in p1.items() if value[1] == i]))
        if len(n) > 1:
            if i == 'Com':
                for a in n:
                    p1[a][0] = 10
            if i == 'Railway':
                rent = [0, 25, 50, 100, 200]
                for a in n:
                    p1[a][0] = rent[len(n)]
            elif i == 'Brown' or i == 'Blue':
                for a in n:
                    p1[a][0] = p1[a][0] * 2
        if len(n) == 3 and i != 'Railway':
            for a in n:
                p1[a][0] = p1[a][0] * 2
    for i in color_group:  # ПРОВЕРЯЕМ СПИСОК ПРЕДПРИЯТИЙ ИГРОКА 2 НА КОЛ-ВО ЭЛЕМЕНТОВ ОДНОГО ЦВЕТА
        n = (list([key for key, value in p2.items() if value[1] == i]))
        if len(n) > 1:
            if i == 'Com':
                for a in n:
                    p2[a][0] = 10
            if i == 'Railway':
                rent = [0, 25, 50, 100, 200]
                for a in n:
                    p2[a][0] = rent[len(n)]
            elif i == 'Brown' or i == 'Blue':
                for a in n:
                    p2[a][0] = p2[a][0] * 2
        if len(n) == 3 and i != 'Railway':
            for a in n:
                p2[a][0] = p2[a][0] * 2
    # print('player 1 ', p1)
    # print('player 2 ', p2)








# win_r = Canvas(win, width=300, height=800, border=5, highlightthickness=0)
# win_r.pack(side="right")
# #win_r.create_rectangle(0, 0, 300, 804, fill="lightblue", outline='red')
# # ДИСПЛЕЙ ОТОБРАЖЕНИЯ ХОДОВ
# text = Text(width=38, height=50, bg="lightblue", fg='#323dbc', wrap=WORD)
# text.place(x=1115, y=0)

# win_l = Canvas(win, width=350, bd=5, highlightthickness=0)
# win_l.pack(side="left")

# picture = canvas.create_image(400, 400, image=dice)
# button_dice = Button(win, image=dice, highlightthickness=0 ,bd=0, height=105, bg='#ddf2df', activebackground='#ddf2df', command=roll_dice)
# button_dice.place(x=125, y=577)
# button_dice.place_forget() # скрыть кнопку

# img = ImageTk.PhotoImage(file="fire.png")
# #canvas.create_image(400, 400, image=img, anchor=CENTER)

# canvas.pack()
# win.update()
# time.sleep(1)

def display_cash():
    cash1.config(text='PLAYER 1 = ' + str(cash_player1) + ' ₽')
    cash2.config(text='PLAYER 2 = ' + str(cash_player2) + ' ₽')



def moveew(n, player):

    for n in range(1, n):  # делаем n- ходов фишкой
        chips_coords = canvas.coords(player)
        if chips_coords[2] < 110:  # ЕСЛИ ПО Х КООРДИНАТЫ В ЛЕВОЙ ЧАСТИ ПОЛЯ, ПО Y ДВИЖЕМСЯ ВВЕРХ
            step_y = -1
            step_x = 0
        elif chips_coords[2] > 695:  # ЕСЛИ ПО Х КООРДИНАТЫ В ПРАВОЙ ЧАСТИ ПОЛЯ, ПО Y ДВИЖЕМСЯ ВНИЗ
            step_y = 1
            step_x = 0
        elif chips_coords[3] < 110:  # ЕСЛИ ПО Y КООРДИНАТЫ В ВЕРХНЕЙ ЧАСТИ ПОЛЯ, ПО X ДВИЖЕМСЯ ВПРАВО
            step_x = 1
            step_y = 0
        elif chips_coords[3] > 695:  # ЕСЛИ ПО Y КООРДИНАТЫ В НИЖНЕЙ ЧАСТИ ПОЛЯ, ПО X ДВИЖЕМСЯ ВЛЕВО
            step_x = -1
            step_y = 0

        # ЕСЛИ ФИШКА В ПРАВОМ ВЕРХНЕМ УГЛУ
        if chips_coords[2] > 695 and chips_coords[3] < 110:
            if player == chips_player1:
                canvas.coords(player, 700, 55, 744, 99)
            elif player == chips_player2:
                canvas.coords(player, 750, 55, 794, 99)
            step_y = 1
            step_x = 0
        # ЕСЛИ ФИШКА В ПРАВОМ НИЖНЕМ УГЛУ
        if chips_coords[2] > 695 and chips_coords[3] > 695:
            if player == chips_player1: canvas.coords(player, 705, 700, 749, 744)
            if player == chips_player2: canvas.coords(player, 705, 750, 749, 794)
            step_y = 0
            step_x = -1
        # ЕСЛИ ФИШКА В ЛЕВОМ НИЖНЕМ УГЛУ
        if chips_coords[2] < 110 and chips_coords[3] > 695:
            if player == chips_player1: canvas.coords(player, 61, 704, 105, 748)
            if player == chips_player2: canvas.coords(player, 11, 704, 55, 748)
            step_y = -1
            step_x = 0
        # ЕСЛИ ФИШКА В ЛЕВОМ ВЕРХНЕМ УГЛУ
        if chips_coords[2] < 110 and chips_coords[3] < 110:
            if player == chips_player1: canvas.coords(player, 55, 60, 99, 104)
            if player == chips_player2: canvas.coords(player, 55, 10, 99, 54)
            step_y = 0
            step_x = 1

        # АНИМАЦИЯ ШАГА НА ОДНУ КЛЕТКУ (65 пикселей)
        for i in range(1, 66):
            time.sleep(0.0005)  # СКОРОСТЬ ПЕРЕМЕЩЕНИЯ ФИШКИ
            canvas.move(player, step_x, step_y)
            win.update()
        # print('step-', n, '  x,y = ', canvas.coords(player)) # показать координаты фишки после каждой клетки


def jail(player):
    global player1, player2
    time.sleep(0.3)
    sound_jail.set_volume(0.6)
    sound_jail.play()
    text.insert(1.0, ' ВЫ ОТПРАВЛЯЕТЕСЬ В ТЮРЬМУ! \n')
    text.tag_add("bold_tag", "1.0", "1.end")
    if player == chips_player1:
        canvas.coords(player, 61, 704, 105, 748)
        player1 = 10

    if player == chips_player2:
        canvas.coords(player, 11, 704, 55, 748)
        player2 = 10
    in_jail[player] = 3
    print(in_jail)



def buy(player, active):
    global cash_player1, cash_player2
    price = cells[int(active)][1]

    if player == chips_player1:
        if cash_player1 - price < 0 :
            text.insert(1.0, ' НЕДОСТАТОЧНО СРЕДСТВ! \n')
            return
        cash_player1 -= price
        color = 'red'
    else:
        if cash_player2 - price < 0 :
            text.insert(1.0, ' НЕДОСТАТОЧНО СРЕДСТВ! \n')
            return
        cash_player2 -= price
        color = 'blue'
    text.insert(1.0, ' ИГРОК '  + str(player - 1) + ' ПОКУПАЕТ ' + str(cells[int(active)][4]) + '\n')
    cells[int(active)][0] = player
    canvas.itemconfig(marker[active], fill=color)

    time.sleep(0.3)
    sob()
    return



def check(player, two_dice):
    global  cash_player1, cash_player2, double
    # print('ДЕЛАЕМ ПРОВЕРКУ!')
    if player == chips_player1:  active = player1 # АКТИВНАЯ КЛЕТКА
    else: active = player2

    if int(active) in [0,2,7,10,17,20,22,33,36]: return player, active # исключил проверку не введённых данных

    if active == 30: # JAIL
        jail(player)
        double = 0
        return player, active

    #print(cells[int(active)])

    if active == 4: # ПОДОХОДНЫЙ НАЛОГ
        if player == chips_player1:
            cash_player1 -= 200
            money.play()
            display_cash()
        else:
            cash_player2 -= 200
            money.play()
            display_cash()
        text.insert(1.0, ' ЗАПЛАТИТЕ ПОДОХОДНЫЙ НАЛОГ 200₽  \n')
        return player, active

    if active == 38: # ПАРКОВОЧНЫЙ ТАЛОН
        if player == chips_player1:
            cash_player1 -= 75
            money.play()
            display_cash()
        else:
            cash_player2 -= 75
            money.play()
            display_cash()
        text.insert(1.0, ' ОПЛАТИТЕ ПАРКОВКУ 75₽  \n')
        return player, active


    if cells[int(active)][0] == player:
        print('СВОЯ КЛЕТКА!)')

    if cells[int(active)][0] != 0 and cells[int(active)][0] != player:
        # pay = cells[int(active)][2]
        # print('ПЛАТИМ РЕНТУ!!!' + str(pay) + '₽')
        # ЕСЛИ ВЫПАЛА ЯЧЕЙКА КОММ. УСЛУГ
        if active == 12 or active == 28: n = sum(two_dice)  # ТО ПЛАТА УМНОЖАЕТСЯ НА ВЫПАВШИЕ КУБИКИ
        else:n = 1  # ИНАЧЕ ПЛАТА НЕ МЕНЯЕТСЯ

        if player == chips_player1:
            pay = p2[int(active)][0]
            cash_player1 -= pay * n
            cash_player2 += pay * n
            money.play()
            display_cash()
            text.insert(1.0, ' ЗАПЛПТИТЕ ИГРОКУ 2 ' + str(pay * n) + '₽ \n')
        if player == chips_player2:
            pay = p1[int(active)][0]
            cash_player2 -= pay * n
            cash_player1 += pay * n
            money.play()
            display_cash()
            text.insert(1.0, ' ЗАПЛПТИТЕ ИГРОКУ 1 ' + str(pay * n) + '₽ \n')

    if cells[int(active)][0] == 0:
        #print('ПОКУПАЕМ!')
        money.play()
        buy(player, active)
        display_cash()
    return player, active


def roll_dice():
    global player1, player2, cash_player1, cash_player2, player, double, next_step
    if not next_step: return

    i = random.randint(1, 6) # ВЫБИРАЕМ ЗВУК КУБИКОВ
    if i == 2: sound_dice2.play()
    elif i == 3: sound_dice3.play()
    elif i == 4: sound_dice4.play()
    else: sound_dice1.play()
    time.sleep(1.2)
    #####################################################################################################
    two_dice = [0, 0]
    next_step = False  # блокируем возможность следующего хода

    two_dice[0] = random.randint(1, 6)
    two_dice[1] = random.randint(1, 6)
    text.insert(1.0, ' ВЫПАЛО ' + str(two_dice[0]) + ' и ' + str(two_dice[1]) + '\n')
    if two_dice[0] == two_dice[1]: # ЕСЛИ ВЫПАЛ ДУБЛЬ
        double += 1
        text.insert(1.0, ' ДУБЛЬ!  \n')
        text.tag_add("bold_tag", "1.0", "1.end")
        if double == 3:
            double = 0
            text.insert(1.0, ' ТРИ ДУБЛЯ ПОДРЯД!  \n')
            text.tag_add("bold_tag", "1.0", "1.end")
            jail(player)
            if player == chips_player1: player = chips_player2
            else: player = chips_player1
            text.insert(1.0, ' --- \n')
            text.insert(1.0, ' ХОД ' + str(player - 1) + '-го ИГРОКА  \n')
            next_step = True
            return
        if in_jail[player] != 0: # ЕСЛИ В ТЮРЬМЕ, ВЫКИНУВ ДУБЛЬ ВЫХОДИМ ИЗ ТЮРЬМЫ
            in_jail[player] = 0
            double = 0
    else:  double = 0  # ЕСЛИ НЕ ВЫПАЛ ДУБЛЬ, СБРАСЫВАЕМ СЧЁТЧИК ДУБЛЕЙ

    if in_jail[player] != 0:
        in_jail[player] -=1 # ЕСЛИ В ТЮРЬМЕ, ПРОПУСКАЕМ 3 ХОДА
        if player == chips_player1: player = chips_player2
        else: player = chips_player1
        text.insert(1.0, ' ИГРОК ВСЁ ЕЩЁ В ТЮРЬМЕ!  \n')
        text.insert(1.0, ' \n')
        text.insert(1.0, ' ХОД ' + str(player - 1) + '-го ИГРОКА  \n')
        next_step = True
        return

    if player == chips_player1:
        player1 += sum(two_dice)
        if player1 >= 40:
            add_money.play()
            cash_player1 += 200
            player1 -= 40
            text.insert(1.0, ' +200₽ ЗА ПОЛНЫЙ КРУГ! \n')
            display_cash()
    if player == chips_player2:
        player2 += sum(two_dice)
        if player2 >= 40:
            add_money.play()
            cash_player2 += 200
            player2 -= 40
            text.insert(1.0, ' +200₽ ЗА ПОЛНЫЙ КРУГ! \n')
            display_cash()

    moveew(two_dice[0]+ 1, player)
    time.sleep(0.2)
    moveew(two_dice[1] + 1, player)
    time.sleep(0.2)
    player, active = check(player, two_dice)

    # ЕСЛИ НЕ БЫЛО ДУБЛЯ, ХОД СЛЕДУЮЩЕГО ИНРОКА
    if double == 0 and player == chips_player1:  player = chips_player2
    elif double == 0: player = chips_player1
    if double == 0: text.insert(1.0, ' ---  \n')
    text.insert(1.0, ' ХОД ' + str(player - 1) + '-го ИГРОКА  \n')
    next_step = True



display_cash()

button_dice = Button(win, image=dice, highlightthickness=0 ,bd=0, height=105, bg='#ddf2df', activebackground='#ddf2df', command=roll_dice)
button_dice.place(x=125, y=577)
button_dice.bind("<Enter>", lambda event: button_dice.place(x=127, y=579))
button_dice.bind("<Leave>", lambda event: button_dice.place(x=125, y=577))






canvas.pack()
win.mainloop()
