from tkinter import *
from tkinter import messagebox
import time
import random

tk = Tk()
app_running = True

#  ОПРЕДЕЛЯЕИ РАЗМЕРЫ ИГРОВОГО ПОЛЯ
size_canvas_x = 500
size_canvas_y = 500
s_x = s_y = 10  # Кол-во клеток игрового поля
step_x = size_canvas_x // s_x  # шаг клетки (размер каждой клетки)
step_y = size_canvas_y // s_y
delta_x = 4  # Ширина меню в клетках игрового поля
menu_x = step_x * delta_x  # Место для меню справа от поля
menu_y = 40  # size_canvas_y / 10  # Место для меню внизу поля

letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Список все кораблей
enemy_ships = [[0 for i in range(s_x)] for i in range(s_y)]  # Пустая матрица игнового поля. Заполняем нолями
# print('МАТРИЦА ПОЛЯ:\n', *enemy_ships, sep='\n')
list_ids = []  # список объектов canvas
ids_menu_ships = []  # id список кораблей, нарисованных в меню
boom_list = {}  # Список изображений взрыва
points = [[-1 for i in range(s_x)] for i in range(s_y)]  # Список координит, куда уже кликали мышкой
points2 = [[-1 for i in range(s_x)] for i in range(s_y)]  # Список координит, куда противник кликал мышкой
killed_ships1 = []  # Список подбитых кораблей
killed_ships2 = []  # Список подбитых кораблей
your_move = True  # Ход 1-го игрока
vs_computer = True  # Игра против компьютера
win = False
around = True
add_label = ' (Computer)' if vs_computer else ''


def draw_table(offset_x=0):
    # РИСУЕМ КЛЕТКИ НА ПОЛЕ
    for i in range(0, s_x + 1):
        canvas.create_line(i * step_x + offset_x, 0, i * step_x + offset_x, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(offset_x, i * step_y, size_canvas_y + offset_x, i * step_y)

    # ПИШЕМ БУКВЕННЫЕ ОБОЗНАЧЕНИЯ ПОЛЕЙ
    second_pole = 0
    for n in range(2):
        for i in range(len(letters)):
            label = Label(tk, text=letters[i], font=('Helvetica', 12))
            c = i * step_y + abc_y + (step_y / 2 - 6)
            label.place(x=c + second_pole, y=6)
        second_pole = size_canvas_y + menu_x

    # ПИШЕМ ЦИФРОВЫЕ ОБОЗНАЧЕНИЯ ПОЛЕЙ
    second_pole = 0
    for n in range(2):
        for i in range(1, 11, 1):
            label = Label(tk, text=i, font=('Helvetica', 11))
            label.place(x=16 + second_pole, y=i * step_y + 8, anchor='center')
        second_pole = (size_canvas_x * 2) + menu_x + abc_y


def on_closing():  # Закрываем окно программы
    global app_running
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
        app_running = False
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)  # функция при закрытии окна
tk.title('Игра "Морской бой"')  # Заголовок окна
tk.resizable(False, False)  # запрещаем изменение размера окна
tk.wm_attributes("-topmost", 1)  # поверх других окон
# ОБОЗНАЧИМ ОБЛАСТЬ ДЛЯ ИГРОВЫХ ПОЛЕЙ
canvas = Canvas(tk, width=size_canvas_x * 2 + menu_x + 1, height=size_canvas_y + menu_y, bd=0, highlightthickness=0)
boom = PhotoImage(file="boom.png")
fire = PhotoImage(file="fire.png")

# РИСУЕМ ПОЛЕ №1:
# canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
py_image1 = PhotoImage(file="SeaBFon.png")
canvas.create_image(250, 250, image=py_image1)
# РИСУЕМ ПОЛЕ №2:
# canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x * 2 + menu_x, size_canvas_y,
#                         fill="lightblue")
py_image2 = PhotoImage(file="SeaBFon.png")
canvas.create_image(950, 250, image=py_image2)
# РИСУЕМ ВЕРХНЮЮ ПОЛОВИНУ МЕНЮ:
canvas.create_rectangle(size_canvas_x, 0, size_canvas_x + menu_x, size_canvas_y // 2,
                        fill="white")
# РИСУЕМ НИЖНЮЮ ПОЛОВИНУ МЕНЮ:
canvas.create_rectangle(size_canvas_x, size_canvas_y // 2, size_canvas_x + menu_x, size_canvas_y,
                        fill='#D7ECF2')

# РИСУЕМ ВЕРХНЕЕ БУКВЕННОЕ ПОЛЕ
abc_y = step_y * 0.66  # высота буквенной зоны
abc = Canvas(tk, width=size_canvas_x * 2 + menu_x + (abc_y * 2), height=abc_y, bd=0, highlightthickness=0)
# abc.create_rectangle(0, 0, size_canvas_x * 2 + menu_x + (abc_y * 2), abc_y, fill="white", outline='white')

# РИСУЕМ БОКОВЫЕ ЦИФРОВЫЕ ПОЛЯ
abc_left = Canvas(tk, width=abc_y, height=size_canvas_y + menu_y, bd=0, highlightthickness=0)
# abc_left.create_rectangle(0, 0, abc_y, size_canvas_x, fill="white", outline='white')
abc_right = Canvas(tk, width=abc_y, height=size_canvas_y + menu_y, bd=0, highlightthickness=0)
# abc_right.create_rectangle(0, 0, abc_y, size_canvas_x, fill="white", outline='white')


abc.pack()
abc_left.pack(side="left")
abc_right.pack(side="right")
canvas.pack()
tk.update()

draw_table()  # рисуем клетки на 1-м поле
draw_table(size_canvas_x + menu_x)  # рисуем клетки на 2-м поле

t0 = Label(tk, text='Игрок №1', font=('Helvetica', 16))
t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2 + abc_y, y=size_canvas_y + abc_y + 3)
t1 = Label(tk, text='Игрок №2' + add_label, font=('Helvetica', 16))
t1.place(x=size_canvas_x // 2 + size_canvas_x + menu_x - t1.winfo_reqwidth() // 2 + abc_y, y=size_canvas_y + abc_y + 3)
t0.configure(background='red')
t0.configure(background='white')
# canvas.create_image(275, 275, image=fire)
# canvas.create_image(275, 225, image=fire)
# canvas.create_image(275, 175, image=fire)


def menu_ships():
    global ids_menu_ships
    step_menu = size_canvas_y // 22
    delta_y = 100
    list = killed_ships2
    for elemnt in ids_menu_ships:
        canvas.delete(elemnt)
    ids_menu_ships = []

    for n in range(2):

        # 4 ТРУБНИК
        color4 = 'lightgrey' if 4 in list else 'red' # Если 4-х палубник есть в списке подбитых кораблей killed_ships2,
        # то цвет серый, иначе красный

        for i in range(1, 5, 1):
            id = canvas.create_rectangle(i * step_menu + size_canvas_x, step_menu * 0.5 + delta_y,
                                         i * step_menu + step_menu + size_canvas_x, step_menu * 1.5 + delta_y,
                                         fill=color4, outline="black")
            ids_menu_ships.append(id)  # Записываем id клеток нарисованного корабля в список ids_menu_ships

        # 3 ТРУБНИК
        color31 = 'lightgrey' if list.count(3) > 0 else 'red'
        color32 = 'lightgrey' if list.count(3) > 1 else 'red'

        for i in range(1, 4, 1):
            id = canvas.create_rectangle(i * step_menu + size_canvas_x, step_menu * 2 + delta_y,
                                         i * step_menu + size_canvas_x + step_menu, step_menu * 3 + delta_y,
                                         fill=color31, outline="black")
            ids_menu_ships.append(id)
            id = canvas.create_rectangle(i * step_menu + (step_menu * 4) + size_canvas_x, step_menu * 2 + delta_y,
                                         i * step_menu + (step_menu * 5) + size_canvas_x, step_menu * 3 + delta_y,
                                         fill=color32, outline="black")
            ids_menu_ships.append(id)

        # 2 ТРУБНИК
        color21 = 'lightgrey' if list.count(2) > 0 else 'red'
        color22 = 'lightgrey' if list.count(2) > 1 else 'red'
        color23 = 'lightgrey' if list.count(2) > 2 else 'red'

        for i in range(1, 3, 1):
            id = canvas.create_rectangle(i * step_menu + size_canvas_x, step_menu * 3.5 + delta_y,
                                         i * step_menu + step_menu + size_canvas_x, step_menu * 4.5 + delta_y,
                                         fill=color21, outline="black")
            ids_menu_ships.append(id)
            id = canvas.create_rectangle(i * step_menu + (step_menu * 2.5) + size_canvas_x, step_menu * 3.5 + delta_y,
                                         i * step_menu + (step_menu * 3.5) + size_canvas_x, step_menu * 4.5 + delta_y,
                                         fill=color22, outline="black")
            ids_menu_ships.append(id)
            id = canvas.create_rectangle(i * step_menu + (step_menu * 5) + size_canvas_x, step_menu * 3.5 + delta_y,
                                         i * step_menu + (step_menu * 6) + size_canvas_x, step_menu * 4.5 + delta_y,
                                         fill=color23, outline="black")
            ids_menu_ships.append(id)

        # 1 ТРУБНИК
        color11 = 'lightgrey' if list.count(1) > 0 else 'red'
        color12 = 'lightgrey' if list.count(1) > 1 else 'red'
        color13 = 'lightgrey' if list.count(1) > 2 else 'red'
        color14 = 'lightgrey' if list.count(1) > 3 else 'red'

        id = canvas.create_rectangle(step_menu + size_canvas_x, step_menu * 5 + delta_y,
                                     step_menu * 2 + size_canvas_x, step_menu * 6 + delta_y,
                                     fill=color11, outline="black")
        ids_menu_ships.append(id)
        id = canvas.create_rectangle(step_menu * 3 + size_canvas_x, step_menu * 5 + delta_y,
                                     step_menu * 4 + size_canvas_x, step_menu * 6 + delta_y,
                                     fill=color12, outline="black")
        ids_menu_ships.append(id)
        id = canvas.create_rectangle(step_menu * 5 + size_canvas_x, step_menu * 5 + delta_y,
                                     step_menu * 6 + size_canvas_x, step_menu * 6 + delta_y,
                                     fill=color13, outline="black")
        ids_menu_ships.append(id)
        id = canvas.create_rectangle(step_menu * 7 + size_canvas_x, step_menu * 5 + delta_y,
                                     step_menu * 8 + size_canvas_x, step_menu * 6 + delta_y,
                                     fill=color14, outline="black")
        ids_menu_ships.append(id)
        delta_y = 100 + size_canvas_y // 2
        list = killed_ships1


menu_ships()


def button_begin_again():
    global list_ids
    global points, points2
    global enemy_ships, my_ships
    global your_move, win
    global killed_ships1, killed_ships2
    global vs_computer, ids_menu_ships
    for elemnt in list_ids:
        canvas.delete(elemnt)
    for elemnt in ids_menu_ships:
        canvas.delete(elemnt)
    ids_menu_ships = []
    list_ids = []
    killed_ships1 = []
    killed_ships2 = []
    points = [[-1 for i in range(s_x)] for i in range(s_y)]
    points2 = [[-1 for i in range(s_x)] for i in range(s_y)]
    # print('МАТРИЦА ПОЛЯ:\n', *points, sep='\n')
    enemy_ships = generate_enemy_ships(ships_list)
    my_ships = generate_enemy_ships(ships_list)
    menu_ships()
    your_move = True  # Ход 1-го игрока
    win = False
    text.delete("1.0", END)
    if vs_computer: show_my_ships()
    # ЦЕНТРУЕМ РАСПОЛОЖЕНИЕ НАДПИСИ "ИГРОК №2"
    t1.place(x=size_canvas_x // 2 + size_canvas_x + menu_x - t1.winfo_reqwidth() // 2 + abc_y,
             y=size_canvas_y + 3 + abc_y)


def change_rb():
    global vs_computer, add_label
    if sum(x.count(0) for x in points2):
        if not messagebox.askokcancel("Перезапуск игры", "Хотите начать заново?"):
            rb2.select() if rb_var.get() else rb1.select()
            return
    # print(rb_var.get())
    if rb_var.get():
        vs_computer = True
        t1['text'] = 'Игрок №2 (Computer)'
    else:
        vs_computer = False
        t1['text'] = 'Игрок №2'
    button_begin_again()


def aroundtrue():
    global around
    around = che.get()


rb_var = BooleanVar()
rb1 = Radiobutton(tk, text='Player vs. Computer', variable=rb_var, value=1, command=change_rb)
rb2 = Radiobutton(tk, text='Player vs. Player', variable=rb_var, value=0, command=change_rb)
rb1.place(x=size_canvas_x + menu_x / 8 + abc_y, y=40 + abc_y)  # отступ кнопки 1/8 от меню, ширина = 3/4 от меню
rb2.place(x=size_canvas_x + menu_x / 8 + abc_y, y=60 + abc_y)
if vs_computer:
    rb1.select()
else:
    rb2.select()
che = BooleanVar()
che.set(True)
check = Checkbutton(tk, text="Обводить корабли", variable=che, onvalue=True, offvalue=False, command=aroundtrue)
check.place(x=size_canvas_x + menu_x / 8 + abc_y, y=80 + abc_y)
print('che= ', che.get())

# ДИСПЛЕЙ ОТОБРАЖЕНИЯ ХОДОВ
text = Text(width=23, height=5, bg="#323dbc", fg='#d2eaf4', wrap=WORD)
text.place(x=size_canvas_x + 7 + abc_y, y=size_canvas_y / 2 + 7 + abc_y)


def button_show_enemy():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:  # Если по координатам есть корабль
                color = 'red'
                if points[j][i] == 0:  # Если по этой клетке был выстрел ЛКМ
                    color = 'yellow'
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def show_my_ships():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if my_ships[j][i] > 0:  # Если по координатам есть корабль
                color = 'red'
                if points2[j][i] == 0:  # Если по этой клетке был выстрел ЛКМ
                    color = 'yellow'
                _id = canvas.create_rectangle(i * step_x + size_canvas_x + menu_x, j * step_y,
                                              i * step_x + step_x + size_canvas_x + menu_x,
                                              j * step_y + step_y, fill=color)
                list_ids.append(_id)


def check_win():
    global points, points2
    global win
    global your_move
    survivors = ships_list[:]
    for i in killed_ships1:
        survivors.remove(i)
    print(f'Игрок 1  {killed_ships1} остались - {survivors}')
    survivors = ships_list[:]
    for i in killed_ships2:
        survivors.remove(i)
    print(f'Игрок 2  {killed_ships2} остались - {survivors}')
    if len(killed_ships1) == len(enemy_ships):
        winner = 'ПОБЕДА ИГРОКА 1 !!!'
    elif len(killed_ships2) == len(enemy_ships):
        winner = 'ПОБЕДА ИГРОКА 2 !!!'
    else:
        return
    button_show_enemy()
    show_my_ships()
    points = points2 = [[10 for i in range(s_x)] for i in range(s_y)]  # Заполняем весь список координат
    win = True
    your_move = True
    print(winner, ' УРАААА!!!')
    text.insert(1.0, ' \n')
    text.insert(1.0, winner + '\n')
    text.insert(1.0, 'УРАААА!!! \n')


def biggest_ship(killed_ships):
    temp_list = ships_list[:]
    [temp_list.remove(i) for i in killed_ships]
    if temp_list:
        # print('BIGGEST SHIP - ', temp_list[0])
        # print('Осталось: ', temp_list)
        return temp_list[0]


def direction(x, y, ships):  # ОПРЕДЕЛЯЕМ НАПРАВЛЕНИЕ КОРАБЛЯ
    # print('длина корабля = ', ships[y][x])
    linee = ""  # горизонтальное либо вертикальное расположение корабля
    right_check = left_check = up_check = below_check = 1
    if x + 1 > 9:  # проверяем, что корабль не расположен на краю поля
        right_check = -1  # если корабль на правом краю поля, не проверяем соседнюю правую клетку, что бы не выйти за пределы массива
    if x - 1 < 0:
        left_check = -1
    if y + 1 > 9:
        below_check = -1
    if y - 1 < 0:
        up_check = -1

    if ships[y][x - left_check] == ships[y][x] or ships[y][x + right_check] == ships[y][x]:
        linee = 'horizont'
    elif ships[y - up_check][x] == ships[y][x] or ships[y + below_check][x] == ships[y][x]:
        linee = 'vertical'
    return linee


def dead_or_alive(x, y, linee, ships, points):  # ПРОВЕРЯЕМ РАНЕН ИЛИ УБИТ возвращает статус и если убит,
    # то все клетки корабля по X или Y (горизонт. или вертикаль. соответственно)
    # аргументы x,y,- координаты
    dead_x, dead_y = [x], [y]
    if linee == 'horizont':
        # ЦИКЛ В МИНУС ГОРИЗОНТАЛЬНОЕ РАСПОЛОЖЕНИЕ
        n = 0

        for i in range(1, ships[y][x]):  # цикл в минус
            if x - i < 0:  # Проверяем, не вышли ли мы за пределы поля
                n = ships[y][x] - i + 1  # Добавим 1, что бы в цикле на "+" пропустить нулевую итеррацию
                break

            if ships[y][x - i] != 0 and points[y][x - i] == 0:
                dead_x.append(x - i)
            elif ships[y][x - i] == 0:
                n = ships[y][x] - i
                break
        # ЦИКЛ В ПЛЮС
        for i in range(1, n + 1):  # Цикл в плюс
            if ships[y][x + i] != 0 and points[y][x + i] == 0:
                dead_x.append(x + i)

    if linee == 'vertical':
        # ЦИКЛ В МИНУС ВЕРТИКАЛЬНОЕ РАСПОЛОЖЕНИЕ
        n = 0
        for i in range(1, ships[y][x]):  # цикл в минус
            if y - i < 0:  # Проверяем, не вышли ли мы за пределы поля
                n = ships[y][x] - i + 1  # Добавим 1, что бы в цикле на "+" пропустить нулевую итеррацию
                break

            if ships[y - i][x] != 0 and points[y - i][x] == 0:
                dead_y.append(y - i)
            elif ships[y - i][x] == 0:
                n = ships[y][x] - len(dead_y)
                break
        # ЦИКЛ В ПЛЮС ВЕРТИКАЛЬНОЕ РАСПОЛОЖЕНИЕ
        for i in range(1, n + 1):  # Цикл в плюс
            if y + i > 9: break
            if ships[y + i][x] != 0 and points[y + i][x] == 0:
                dead_y.append(y + i)

    dead_x.sort()
    dead_y.sort()
    status = 'УБИТ!' if len(dead_x) == ships[y][x] or len(dead_y) == ships[y][x] else 'РАНЕН!'
    if status == 'УБИТ!':
        menu_ships()
    return status, dead_x, dead_y


b0 = Button(tk, text='Показать корабли противника', command=button_show_enemy)
b0.place(x=size_canvas_x + menu_x / 19 + abc_y, y=115, width=menu_x * 0.9)  # отступ кнопки 1/15 от меню, ширина = 3/4 от меню
# #
# b1 = Button(tk, text='Показать мои корабли', command=show_my_ships)
# b1.place(x=size_canvas_x + menu_x / 8, y=150, width=menu_x / 4 * 3)

b2 = Button(tk, text='Начать заново!', command=button_begin_again)
b2.place(x=size_canvas_x + menu_x / 8 + abc_y, y=10 + abc_y, width=menu_x / 4 * 3)


def draw_point(x, y, point, ship):  # координаты удара x, y; point - клик мыши 0 или 1....
    global your_move, boom_list
    if point > 1:  # Если в матрице POINTS по этим координатам уже есть id
        canvas.delete(point)
        list_ids.remove(point)
        point = -1
        return point, 0
    elif point == 1:  # Если кликнули ПКМ, рисуем голубой кружок и пишем его id в матрицу POINTS
        color = 'lightblue'
    elif ship != 0:
        color = 'red'
        boom_l = canvas.create_image(x * step_x + 25, y * step_y + 25, image=boom)
        boom_list[str(x) + str(y)] = boom_l
        print('boom', boom_list, str(x) + str(y))
        return point, color
    else:
        color = 'blue'
        your_move = not your_move
    id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
    list_ids.append(id1)
    if color == 'lightblue':
        point = id1
    return point, color


def around_destroyed_ship(x, y):  # ОБРИСОВЫВАЕМ ПОДБИТЫЙ КОРАБЛЬ
    if your_move:
        delta = 0
        point = points
    else:
        delta = s_x + delta_x
        point = points2
    print(your_move)

    if type(x) == int:
        x = [x]
    if type(y) == int:
        y = [y]
    if min(x) > 0:  # Допустимый сдвиг по оси X
        x.append(min(x) - 1)
    if max(x) < 9:
        x.append(max(x) + 1)
    if min(y) > 0:  # Допустимый сдвиг по оси Y
        y.append(min(y) - 1)
    if max(y) < 9:
        y.append(max(y) + 1)

    for i in x:
        for j in y:
            if point[j][i] == -1:
                if around:
                    id1 = canvas.create_oval((i + delta) * step_x, j * step_y, (i + delta) * step_x + step_x,
                                             j * step_y + step_y,
                                             fill='lightblue')
                    list_ids.append(id1)
            point[j][i] = 0
    # print('x, y', x, y)
    # print('МАТРИЦА ПОЛЯ:\n', *points2, sep='\n')
    # print()


def auto_killer(x, y):
    global points2, my_ships, killed_ships2
    draw_x = s_x + delta_x  # Поправка на Х для отрисовки объектов на втором поле.
    tk.update()
    time.sleep(0.6)

    # ДЕЛАЕМ ВЫСТРЕЛ ПО ДАННЫМ КООРДИНАТАМ
    if points2[y][x] != 0:
        points2[y][x], color = draw_point(x + draw_x, y, 0, my_ships[y][x])
    else:
        color = 'red'

    # ЕСЛИ КОРАБЛЬ ОДНОПАЛУБНЫЙ
    if my_ships[y][x] == 1:
        around_destroyed_ship(x, y)
        tk.update()
        time.sleep(0.5)
        text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + ' УБИТ!!!' + '\n')
        id1 = canvas.create_oval((x + draw_x) * step_x, y * step_y, (x + draw_x) * step_x + step_x,
                                 y * step_y + step_y, fill='darkred')
        id2 = canvas.create_image((x + draw_x) * step_x + 25, y * step_y + 20, image=fire)
        canvas.delete(boom_list[str(x + draw_x) + str(y)])
        del boom_list[str(x + draw_x) + str(y)]
        list_ids.append(id1)
        list_ids.append(id2)
        # around_destroyed_ship(x, y)
        killed_ships2.append(my_ships[y][x])
        menu_ships()
        check_win()
        return

    # ЕСЛИ ПРОМАЗАЛИ
    if color != 'red':
        text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + '\n')
        return

    linee = direction(x, y, my_ships)
    status, dead_x, dead_y = dead_or_alive(x, y, linee, my_ships, points2)
    text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + ' ' + status + '\n')

    # ЕСЛИ КОРАБЛЬ РАНЕЕ НЕДОБИТ.========================================================================
    if len(dead_x) > len(dead_y):  # Или 'if linee == 'horizontal'
        x = min(dead_x)
    elif len(dead_y) > len(dead_x):
        y = max(dead_y)
    #####################################################################################################

    previous_x, previous_y = x, y

    # НАЧИНАЕМ ПЕРЕБОР ПО КЛЕТКАМ
    # ПРОВЕРЯЕМ КЛЕТКИ СПРАВА ОТ ТОЧКИ ПОПАДАНИЯ.
    if x < 9 and len(dead_y) == 1:  # ЕСЛИ КОРАБЛЬ НЕ НА КРАЙНЕЙ ПРАВОЙ КЛЕТКЕ И НЕ РАСПОЛОЖЕН ПО ОСИ Y
        if points2[y][x + 1] != 0:  # проверяем, что раньше мы не стреляли по соседней правой клетке.
            # ДО ТЕХ ПОР, ПОКА НЕ ДОШЛИ ДО КРАЙНЕЙ ПРАВОЙ ГРАНИЦЫ ИЛИ НЕ ПРОМАЗАЛИ, ИДЁМ ВПРАВО
            while color == 'red':
                x += 1
                if x == s_x: break
                # ДЕЛАЕМ ВЫСТРЕЛ ПО НОВЫМ КООРДИНАТАМ
                tk.update()
                time.sleep(0.5)
                points2[y][x], color = draw_point(x + draw_x, y, 0, my_ships[y][x])
                # ПРОВЕРКА УБИТ ИЛИ РАНЕН + ПОБЕДИЛ ИЛИ НЕТ
                if color == 'red':
                    status, dead_x, dead_y = dead_or_alive(x, y, linee, my_ships, points2)
                    text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + ' ' + status + '\n')
                print('проверяем статус- ', status)
                if status == 'УБИТ!':
                    around_destroyed_ship(dead_x[:], dead_y[:])
                    tk.update()
                    time.sleep(0.5)
                    for i in dead_x:
                        for j in dead_y:
                            id1 = canvas.create_oval((i + draw_x) * step_x, j * step_y,
                                                     (i + draw_x) * step_x + step_x,
                                                     j * step_y + step_y, fill='darkred')
                            id2 = canvas.create_image((i + draw_x) * step_x + 25, j * step_y + 20, image=fire)
                            list_ids.append(id1)
                            list_ids.append(id2)
                            print(str(i + draw_x) + str(j))
                            canvas.delete(boom_list[str(i + draw_x) + str(j)])
                            del boom_list[str(i + draw_x) + str(j)]
                            list_ids.append(id1)
                    # around_destroyed_ship(dead_x, dead_y)
                    killed_ships2.append(my_ships[y][x])
                    menu_ships()
                    check_win()
                    return
                # Если промазали, то обозначаем клетку первого попадания как 'r' и выходим из auto_killer
                if color != 'red':
                    text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + '\n')
                    points2[previous_y][previous_x] = 'r'
                    return
            x, y = previous_x, previous_y  # Если достигли крайнего правого поля,
            #                              то меняем координаты на точку первого попадания.

    # ПРОВЕРЯЕМ КЛЕТКИ СЛЕВА ОТ ТОЧКИ ПОПАДАНИЯ.
    if x > 0 and len(dead_y) == 1:  # ЕСЛИ КОРАБЛЬ НЕ НА КРАЙНЕЙ ЛЕВОЙ КЛЕТКЕ И НЕ РАСПОЛОЖЕН ПО ОСИ Y.
        if points2[y][x - 1] != 0:  # Проверяем, что раньше мы не стреляли по соседней левой клетке. ??????????
            while color == 'red':
                x -= 1
                if x < 0: break
                # ДЕЛАЕМ ВЫСТРЕЛ ПО НОВЫМ КООРДИНАТАМ
                tk.update()
                time.sleep(0.5)
                points2[y][x], color = draw_point(x + draw_x, y, 0, my_ships[y][x])
                # ПРОВЕРКА УБИТ ИЛИ РАНЕН + ПОБЕДИЛ ИЛИ НЕТ
                if color == 'red':
                    status, dead_x, dead_y = dead_or_alive(x, y, linee, my_ships, points2)
                    text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + ' ' + status + '\n')
                if status == 'УБИТ!':
                    around_destroyed_ship(dead_x[:], dead_y[:])
                    tk.update()
                    time.sleep(0.5)
                    for i in dead_x:
                        for j in dead_y:
                            id1 = canvas.create_oval((i + draw_x) * step_x, j * step_y,
                                                     (i + draw_x) * step_x + step_x,
                                                     j * step_y + step_y, fill='darkred')
                            id2 = canvas.create_image((i + draw_x) * step_x + 25, j * step_y + 20, image=fire)
                            list_ids.append(id1)
                            list_ids.append(id2)
                            print(str(i + draw_x) + str(j))
                            canvas.delete(boom_list[str(i + draw_x) + str(j)])
                            del boom_list[str(i + draw_x) + str(j)]
                            list_ids.append(id1)
                    # around_destroyed_ship(dead_x, dead_y)
                    killed_ships2.append(my_ships[y][x])
                    menu_ships()
                    check_win()
                    return
            points2[previous_y][previous_x] = 'r'  # Обозначаем клетку первого попадания как 'r'
            text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + '\n')
            # и выходим из auto_killer
            return

    if y > 0:  # ЕСЛИ КОРАБЛЬ НЕ НА КРАЙНЕЙ ВЕРХНЕЙ ГПАНИЦЕ.
        if points2[y - 1][x] != 0:  # Проверяем, что раньше мы не стреляли по соседней верхней клетке.
            # ДО ТЕХ ПОР, ПОКА НЕ ДОШЛИ ДО ВЕРХНЕЙ ГРАНИЦЫ ИЛИ НЕ ПРОМАЗАЛИ, ИДЁМ ВВЕРХ.
            while color == 'red':
                y -= 1
                if y < 0: break
                # ДЕЛАЕМ ВЫСТРЕЛ ПО НОВЫМ КООРДИНАТАМ
                tk.update()
                time.sleep(0.5)
                points2[y][x], color = draw_point(x + draw_x, y, 0, my_ships[y][x])
                # ПРОВЕРКА УБИТ ИЛИ РАНЕН + ПОБЕДИЛ ИЛИ НЕТ
                if color == 'red':
                    status, dead_x, dead_y = dead_or_alive(x, y, linee, my_ships, points2)
                    text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + ' ' + status + '\n')
                if status == 'УБИТ!':
                    around_destroyed_ship(dead_x[:], dead_y[:])
                    tk.update()
                    time.sleep(0.5)
                    for i in dead_x:
                        for j in dead_y:
                            id1 = canvas.create_oval((i + draw_x) * step_x, j * step_y,
                                                     (i + draw_x) * step_x + step_x,
                                                     j * step_y + step_y, fill='darkred')
                            id2 = canvas.create_image((i + draw_x) * step_x + 25, j * step_y + 20, image=fire)
                            list_ids.append(id1)
                            list_ids.append(id2)
                            print(str(i + draw_x) + str(j))
                            canvas.delete(boom_list[str(i + draw_x) + str(j)])
                            del boom_list[str(i + draw_x) + str(j)]
                            list_ids.append(id1)
                    # around_destroyed_ship(dead_x, dead_y)
                    killed_ships2.append(my_ships[y][x])
                    menu_ships()
                    check_win()
                    return
                if color != 'red':
                    points2[previous_y][previous_x] = 'r'
                    text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + '\n')
                    return
            x, y = previous_x, previous_y  # Если достигли крайнего правого поля,
            #                              то меняем координаты на точку первого попадания.

    # ПРОВЕРЯЕМ КЛЕТКИ СНИЗУ ОТ ТОЧКИ ПОПАДАНИЯ.
    if y < 9:  # ЕСЛИ КОРАБЛЬ НЕ НА НИЖНЕЙ ГРАНИЦЕ.
        if points2[y + 1][x] != 0:  # проверяем, что раньше мы не стреляли по соседней нижней клетке.
            # ДО ТЕХ ПОР, ПОКА НЕ ДОШЛИ ДО НИЖНЕЙ ГРАНИЦЫ ИЛИ НЕ ПРОМАЗАЛИ, ИДЁМ ВНИЗ.
            while color == 'red':
                y += 1
                if y == s_y: break
                # ДЕЛАЕМ ВЫСТРЕЛ ПО НОВЫМ КООРДИНАТАМ
                tk.update()
                time.sleep(0.5)
                points2[y][x], color = draw_point(x + draw_x, y, 0, my_ships[y][x])
                # УБИТ ИЛИ РАНЕН + ПОБЕДИЛ ИЛИ НЕТ
                if color == 'red':
                    status, dead_x, dead_y = dead_or_alive(x, y, linee, my_ships, points2)
                    text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + ' ' + status + '\n')
                if status == 'УБИТ!':
                    around_destroyed_ship(dead_x[:], dead_y[:])
                    tk.update()
                    time.sleep(0.5)
                    for i in dead_x:
                        for j in dead_y:
                            id1 = canvas.create_oval((i + draw_x) * step_x, j * step_y,
                                                     (i + draw_x) * step_x + step_x,
                                                     j * step_y + step_y, fill='darkred')
                            id2 = canvas.create_image((i + draw_x) * step_x + 25, j * step_y + 20, image=fire)
                            list_ids.append(id1)
                            print(str(i + draw_x) + str(j))
                            canvas.delete(boom_list[str(i + draw_x) + str(j)])
                            del boom_list[str(i + draw_x) + str(j)]
                            list_ids.append(id1)
                            list_ids.append(id2)
                    # around_destroyed_ship(dead_x, dead_y)
                    killed_ships2.append(my_ships[y][x])
                    menu_ships()
                    check_win()
                    return
            points2[previous_y][previous_x] = 'r'  # Обозначаем клетку первого попадания как 'r'
            text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(y + 1) + '\n')
            # и выходим из auto_killer
            return


def step_computer():
    # if your_move:
    #     print('Ход игрока 1\n')
    # else:
    #     print('Ходит клмпьютер\n')  # Знвчение your_move при отрисовке кружочка(хода)
    global killed_ships2
    global points2, my_ships
    while not your_move:
        big = biggest_ship(killed_ships2)  # максимально большой оставшийся корабль
        begin = 0  # Первая клетка отсчёта
        if sum(x.count('r') for x in points2):
            for i in range(10):  # Находим ячейку с отметкой R
                if points2[i].count('r'):
                    x = points2[i].index('r')
                    y = i
                    points2[y][x] = 0
                    # canvas.delete(boom_list[str(x + s_x + delta_x ) + str(y)])
            auto_killer(x, y)
            if win: return
            if your_move: return
            big = biggest_ship(killed_ships2)  # максимально большой оставшийся корабль
        # НАЧИНАЕМ АЛГОРИТМ ПОИСКА КЛЕТКИ
        for y in range(10):
            for x in range(begin, 10, big):
                if points2[y][x] == -1:
                    chans = random.randrange(0, 8)
                    if chans == 1:
                        auto_killer(x, y)
                        if win: return
                        if your_move: return
            begin += 1
            if begin == big:
                begin = 0


def add_to_all(event):
    global killed_ships1, killed_ships2
    global vs_computer
    global your_move, boom_list
    if vs_computer and not your_move: return  # Если нажал клавишу вне очереди
    color = ""
    _type = 0  # ЛКМ
    if event.num == 3:
        _type = 1  # ПКМ

    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()  # Координаты курсора в общей системе координат
    # минус координаты верхнего левого угла рабочего окна в общей системе координат равно координаты курсора
    # в системе координат рабочего окна
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y

    # ПРОВЕРЯЕМ КООРДИНАТЫ КЛИКА В ПРЕДЕЛАХ ПОЛЯ № 1
    if ip_x < s_x and ip_y < s_y and your_move and not win:  # Если клик мыши в пределах игрового поля 1
        ship = enemy_ships[ip_y][ip_x]
        if points[ip_y][ip_x] == -1:  # Если в списке POINTS по данным  координатам -1, т.е. пустое поле
            point = _type  # то пишем туда клик мыши
            points[ip_y][ip_x], color = draw_point(ip_x, ip_y, point, ship)  # и рисуем ПРОИАХ или ПОПАДАНИЕ
            if color == 'blue': text.insert(1.0, 'ИГРОК 1 - ' + letters[ip_x] + str(ip_y + 1) + '\n')
        elif points[ip_y][ip_x] > 0:  # Если в списке POINTS по данным  координатам есть id
            point = points[ip_y][ip_x]
            points[ip_y][ip_x], color = draw_point(ip_x, ip_y, point, ship)
        if color == 'red':
            if enemy_ships[ip_y][ip_x] == 1:  # Если корабль однопалубный
                if around: around_destroyed_ship(ip_x, ip_y)  # Если включена обводка, обводим
                tk.update()
                time.sleep(0.5)
                print('координаты', ip_x, ip_y)
                print('boom_list', boom_list)
                canvas.delete(boom_list[str(ip_x) + str(ip_y)])
                # del boom_list[ip_x + ip_y] - Здесь удаление из списка не делаем,
                # т.к. удаление будет ниже "if status == 'УБИТ!':"
                id1 = canvas.create_oval(ip_x * step_x, ip_y * step_y, ip_x * step_x + step_x, ip_y * step_y + step_y,
                                         fill='darkred')
                #canvas.create_image(ip_x * step_x + 25, ip_y * step_y + 25, image=fire)

                list_ids.append(id1)
            linee = direction(ip_x, ip_y, enemy_ships)
            status, x, y = dead_or_alive(ip_x, ip_y, linee, enemy_ships, points)
            print(status)
            text.insert(1.0, 'ИГРОК 1 - ' + letters[ip_x] + str(ip_y + 1) + ' ' + status + '\n')
            if status == 'УБИТ!':
                if around: around_destroyed_ship(x[:], y[:])
                killed_ships1.append(ship)
                biggest_ship(killed_ships1)
                tk.update()
                if enemy_ships[ip_y][ip_x] != 1: time.sleep(0.5) # Если корабль однопалубный, задержку не делаем
                for i in x:
                    for j in y:
                        id1 = canvas.create_oval(i * step_x, j * step_y, i * step_x + step_x,
                                                 j * step_y + step_y, fill='darkred')
                        id2 = canvas.create_image(i * step_x + 25, j * step_y + 20, image=fire)
                        canvas.delete(boom_list[str(i) + str(j)])  # Удаляем картинку BOOM c координатами xy
                        del boom_list[str(i) + str(j)]  # Удаляем из словаря запись с ключом xy
                        print(boom_list)
                        list_ids.append(id1)
                        list_ids.append(id2)
                menu_ships()
                check_win()
    if vs_computer and not your_move:
        step_computer()

    # ПРОВЕРЯЕМ КООРДИНАТЫ КЛИКА В ПРЕДЕЛАХ ПОЛЯ № 2
    if ip_x >= s_x + delta_x and ip_x < s_x * 2 + delta_x and ip_y < s_y and not your_move:  # Если клик мыши
        # в пределах игрового поля 2
        x = ip_x - s_x - delta_x
        ship = my_ships[ip_y][x]
        if points2[ip_y][x] == -1:  # Если в списке POINTS по данным  координатам -1, т.е. пустое поле
            point = _type  # то пишем туда клик мыши
            points2[ip_y][x], color = draw_point(ip_x, ip_y, point, ship)  # и рисуем ПРОИАХ или ПОПАДАНИЕ
            if color == 'blue': text.insert(1.0, 'ИГРОК 2 - ' + letters[x] + str(ip_y + 1) + '\n')
        elif points2[ip_y][x] > 0:  # Если в списке POINTS по данным  координатам есть id
            point = points2[ip_y][x]
            points2[ip_y][x], color = draw_point(x, ip_y, point, ship)
        if color == 'red':
            linee = direction(x, ip_y, my_ships)
            status, x, y = dead_or_alive(x, ip_y, linee, my_ships, points2)
            print(status)
            text.insert(1.0, 'ИГРОК 2 - ' + letters[ip_x - s_x - delta_x] + str(ip_y + 1) + ' ' + status + '\n')
            if status == 'УБИТ!':
                if around: around_destroyed_ship(x[:], y[:])
                killed_ships2.append(ship)
                biggest_ship(killed_ships2)
                tk.update()
                time.sleep(0.5)
                for i in x:
                    for j in y:
                        id1 = canvas.create_oval((i + s_x + delta_x) * step_x, j * step_y, (i + s_x + delta_x) * step_x
                                                 + step_x, j * step_y + step_y, fill='darkred')
                        canvas.delete(boom_list[str(i + s_x + delta_x) + str(j)])
                        del boom_list[str(i + s_x + delta_x) + str(j)]
                        id2 = canvas.create_image((i + s_x + delta_x) * step_x + 25, j * step_y + 20, image=fire)
                        print(boom_list)
                        list_ids.append(id1)
                        list_ids.append(id2)
                menu_ships()
                check_win()


canvas.bind_all("<Button-1>", add_to_all)  # Левая кнопка мыши
canvas.bind_all("<Button-3>", add_to_all)  # Правая кнопка мыши


def generate_enemy_ships(ships_list):
    # global enemy_ships
    enemy_ships = [[0 for i in range(s_x)] for i in range(s_y)]  # Пустая матрица игнового поля. Заполняем нолями
    count_ships = 0

    while count_ships <= len(ships_list) - 1:  # Берём из списка по одному кораблю
        # i = count_ships
        ship = ships_list[count_ships]  # текущий корабль
        horizont_vertikal = random.choice(['горизонт', 'вертикаль'])
        if horizont_vertikal == 'горизонт':
            a, b = ship - 1, 0
        else:
            b, a = ship - 1, 0

        # СЛУЧАЙНЫМ ОБРАЗОМ ГЕНЕРИРУЕМ КООРДИНАТЫ ДЛЯ РАЗМЕЩЕНИЯ КОРАБЛЯ
        primerno_x = random.randrange(0, s_x)
        if primerno_x + a > s_x - 1:
            primerno_x = primerno_x - (primerno_x + a - s_x + 1)  # если точка Х + длина корабля дленее поля,
            # то смещаем точку Х на лишние клетки

        primerno_y = random.randrange(0, s_y)
        if primerno_y + b > s_y - 1:
            primerno_y = primerno_y - (primerno_y + b - s_y + 1)

        x, y = primerno_x, primerno_y

        if x > 0:
            x_min = x - 1
        else:
            x_min = x
        if x + a < 9:
            x_max = x + a + 1
        else:
            x_max = x + a

        if y > 0:
            y_min = y - 1
        else:
            y_min = y
        if y + b < 9:
            y_max = y + b + 1
        else:
            y_max = y + b

        # print('Ставим ', count_ships, '-й корабль')
        # print(ship, '-палубник  x=', x_min, x_max, ' y=', y_min, y_max)
        test = []  # СПИСОК ПРОВЕРЕННЫХ КЛЕТОК ПОЛЯ

        for n in range(y_min, y_max + 1):
            for j in range(x_min, x_max + 1):
                test.append(enemy_ships[n][j])  # ЗАНОСИМ В СПИСОК СОДЕРЖИМОЕ ТЕКУЩЕЙ КЛЕТКИ ПОЛЯ
        if sum(test) == 0:  # ЕСЛИ ВСЕ ПРОВЕРЕННЫЕ КЛЕТКИ = 0
            count_ships += 1  # ТО УВЕЛИЧИВАЕМ СЧЁТЧИК НА 1, ДЛЯ ПРОВЕРКИ СЛЕДУЮЩЕГО КОРАБЛЯ
            # ЗАПИСЫВАЕМ В МАТРИЦЕ ИГРОВОГО ПОЛЯ РАСПОЛОЖЕНИЕ КОРОБЛЯ
            for n in range(y, y + b + 1):
                for j in range(x, x + a + 1):
                    enemy_ships[n][j] = ship
    return enemy_ships


enemy_ships = generate_enemy_ships(ships_list)
my_ships = generate_enemy_ships(ships_list)
if vs_computer:
    show_my_ships()
while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
