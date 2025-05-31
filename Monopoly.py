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
# screen_width = win.winfo_screenwidth()  #    ОПРЕДЕЛЕНИЕ РАЗМЕРОВ ЭКРАНА ШИРИНА (ОСЬ Х)
# screen_height = win.winfo_screenheight()  #    ОПРЕДЕЛЕНИЕ РАЗМЕРОВ ЭКРАНА ВЫСОТА (ОСЬ Y)
# print(screen_width, screen_height)
# side_x = side_y = '800'

#side_x = side_y = str(screen_height // 10 * 9) # УСТАНАВЛИВАЕМ РАМЕР ОКНА 90% ОТ РАЗМЕРА ЭКРАНА ПО ОСИ y
side_x = side_y = '804'  # УСТАНАВЛИВАЕМ РАМЕР ОКНА 90% ОТ РАЗМЕРА ЭКРАНА ПО ОСИ y
win_resolution = str(side_x + 'x' + side_y)
# print(win_resolution)

# cell_width = int(side_x) // 12 # НАХОДИМ ЩИРИНУ КЛЕТКИ
# cell_height = int(cell_width * 1.5) # НАХОДИМ ДЛИНУ КЛЕТКИ
# print(cell_width, cell_height)


#win.geometry(win_resolution)
win.title('MONOPOLY')
win.wm_attributes("-topmost", 1)  # поверх других окон
win.resizable(False, False)  # запрещаем изменение размера окна
py_image1 = PhotoImage(file="monopoly.png")
canvas = Canvas(win, width=side_x, height=side_y, bd=0, highlightthickness=0)
canvas.create_image(402, 402, image=py_image1)

chips_player1 = canvas.create_oval(727, 700, 771, 744, fill='red')
chips_player2 = canvas.create_oval(727, 750, 771, 794, fill='blue')
player1 = 0
player2 = 0
cash_player1 = 200
cash_player2 = 200
money = mixer.Sound("money.mp3")
sound_dice1 = mixer.Sound("roll dice1.mp3")
sound_dice2 = mixer.Sound("roll dice2.mp3")
sound_dice3 = mixer.Sound("roll dice3.mp3")
sound_dice4 = mixer.Sound("roll dice4.mp3")
sound_jail = mixer.Sound("jail.mp3")
dice = PhotoImage(file="dice.png")
double = 0 # подсчёт выпавших дублей
player = chips_player1 # какой игрок начинает ход
post_dice = 0

# picture = canvas.create_image(400, 400, image=dice)
# button_dice = Button(win, image=dice, highlightthickness=0 ,bd=0, height=105, bg='#ddf2df', activebackground='#ddf2df', command=roll_dice)
# button_dice.place(x=125, y=577)
# button_dice.place_forget() # скрыть кнопку

# img = ImageTk.PhotoImage(file="fire.png")
# #canvas.create_image(400, 400, image=img, anchor=CENTER)

# canvas.pack()
# win.update()
# time.sleep(1)


def moveew(n, player):  # ПЕРЕЛВИЖЕНИЕ ФИШКИ

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
    time.sleep(0.3)
    sound_jail.set_volume(0.6)
    sound_jail.play()
    if player == chips_player1: canvas.coords(player, 61, 704, 105, 748)
    if player == chips_player2: canvas.coords(player, 11, 704, 55, 748)


def check(player):
    print('ДЕЛАЕМ ПРОВЕРКУ!')
    if player == chips_player1:  active = player1
    else: active = player2
    print('ACTIVE PLAYER=', active)

    if active == 30: # JAIL
        jail(player)
        if player == chips_player1: player = chips_player2
        else:  player = chips_player1

    return (player, active)


def roll_dice():
    global player1, player2, cash_player1, cash_player2, player, double

    i = random.randint(1, 7) # ВЫБИРАЕМ ЗВУК КУБИКОВ
    if i == 2: sound_dice2.play()
    elif i == 3: sound_dice3.play()
    elif i == 4: sound_dice4.play()
    else: sound_dice1.play()
    time.sleep(1.2)
#########################################################################################################
    two_dice = [0, 0]
    for i in range(2):
        random_dice = random.randint(1, 6)
        print('i=', i)
        print(i + 1, '-й кубик ', random_dice)
        #if i == 0: post_dice = 0
        two_dice[i] = random_dice
        #if post_dice == random_dice:
        print('СРАВНИВАЕМ ',two_dice)
        if two_dice[0] == two_dice[1] and i == 1:
            double += 1
            print('ДУБЛЬ!!!', double)
        elif i == 1: double = 0

        if double == 3:
            double = 0
            print('ТЮРЬМА!!!')
            jail(player)
            if player == chips_player1: player = chips_player2
            else: player = chips_player1
            return

        #post_dice = random_dice
        #print('post_dice', post_dice)

        if player == chips_player1:
            player1 += random_dice
            if player1 >= 40:
                money.play()
                cash_player1 += 200
                player1 -= 40
        if player == chips_player2:
            player2 += random_dice
            if player2 >= 40:
                money.play()
                cash_player2 += 200
                player2 -= 40

        moveew(random_dice + 1, player)
        time.sleep(0.2)
        #########################################################################################################
    player, active = check(player)
    print('after check PLAYER=', player, 'ACTIVE=', active)
    # ЕСЛИ НЕ БЫЛО ДУБЛЯ, ХОД СЛЕДУЮЩЕГО ИНРОКА
    if double == 0 and player == chips_player1:  player = chips_player2
    elif double == 0: player = chips_player1
    if active == 30: double = 0
    print('player1= ', player1, 'CASH=', cash_player1)
    print('player2= ', player2, 'CASH=', cash_player2)
    print('double= ', double)



button_dice = Button(win, image=dice, highlightthickness=0 ,bd=0, height=105, bg='#ddf2df', activebackground='#ddf2df', command=roll_dice)
button_dice.place(x=125, y=577)





#################     БРОСАЕМ КОСТИ    ########################
# while n < 15:
#     for i in range(2):
#         random_dice = random.randint(1, 6)
#         print(i+1, '-й кубик ', random_dice)
#         moveew(random_dice + 1, player)
#         if player == chips_player1:
#             player1 += random_dice
#             if player1 >= 40:
#                 money.play()
#                 cash_player1 += 200
#                 player1 -= 40
#                 print("КРУГ!!!", player1)
#                 n = 6
#         if player == chips_player2:
#             player2 += random_dice
#             if player2 >= 40:
#                 money.play()
#                 cash_player2 += 200
#                 player2 -= 40
#         time.sleep(0.2)
#     #print('chips_player', player)
#     if player == chips_player1: player = chips_player2
#     else: player = chips_player1
#     print('player1= ', player1)
#     print('player2= ', player2)
#     time.sleep(2)
#     n += 1




canvas.pack()
win.mainloop()
