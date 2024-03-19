
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

ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Список все кораблей
enemy_ships = [[0 for i in range(s_x)] for i in range(s_y)]  # Пустая матрица игнового поля. Заполняем нолями
# print('МАТРИЦА ПОЛЯ:\n', *enemy_ships, sep='\n')
list_ids = []  # список объектов canvas
points = [[-1 for i in range(s_x)] for i in range(s_y)]  # Список координит, куда уже кликали мышкой
points2 = [[-1 for i in range(s_x)] for i in range(s_y)]  # Список координит, куда противник кликал мышкой
count_boom = sum(ships_list)  # Счётчик попаданий = сумме палуб всех кораблей


def draw_table(offset_x=0):  # Рисуем клетки на поле
    for i in range(0, s_x + 1):
        canvas.create_line(i * step_x + offset_x, 0, i * step_x + offset_x, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(offset_x, i * step_y, size_canvas_y + offset_x, i * step_y)



def on_closing():  # Закрываем окно программы
    global app_running
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
        app_running = False
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)  # функция при закрытии окна
tk.title('Игра "Морской бой"')  # Заголовок окна
tk.resizable(False, False)  # запрещаем изменение размера окна
tk.wm_attributes("-topmost", 1)  # поверх других окон

canvas = Canvas(tk, width=size_canvas_x * 2 + menu_x, height=size_canvas_y + menu_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")  # РИСУЕМ ПОЛЕ №1:
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x * 2 + menu_x, size_canvas_y, fill="lightblue")  # РИСУЕМ ПОЛЕ №2:
canvas.pack()
tk.update()

draw_table()  # рисуем клетки на 1-м поле
draw_table(size_canvas_x + menu_x)  # рисуем клетки на 2-м поле

t0 = Label(tk, text='Игрок №1', font = ('Helvetica', 16))
t0.place (x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
t1 = Label(tk, text='Игрок №2', font = ('Helvetica', 16))
t1.place (x=size_canvas_x // 2 + size_canvas_x + menu_x - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)
t0.configure(background='red')
t0.configure(background='white')

def button_show_enemy():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0: # Если по координатам есть корабль
                color = 'red'
                if points[j][i] == 0: # Если по этой клетке был выстрел ЛКМ
                    color = 'yellow'
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def show_my_ships():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if my_ships[j][i] > 0: # Если по координатам есть корабль
                color = 'darkred'
                # if points2[j][i] == 0: # Если по этой клетке был выстрел ЛКМ
                #     color = 'yellow'
                _id = canvas.create_rectangle(i * step_x + size_canvas_x + menu_x, j * step_y,
                                              i * step_x + step_x + size_canvas_x + menu_x,
                                              j * step_y + step_y, fill=color)
                list_ids.append(_id)


def button_begin_again():
    global list_ids
    global points, points2
    global enemy_ships, my_ships
    global count_boom
    for elemnt in list_ids:
        canvas.delete(elemnt)
    list_ids = []
    count_boom = sum(ships_list)
    points = [[-1 for i in range(s_x)] for i in range(s_y)]
    points2 = [[-1 for i in range(s_x)] for i in range(s_y)]
    # print('МАТРИЦА ПОЛЯ:\n', *points, sep='\n')
    enemy_ships = generate_enemy_ships(ships_list)
    my_ships = generate_enemy_ships(ships_list)


b0 = Button(tk, text='Показать корабли противника', command=button_show_enemy)
b0.place(x=size_canvas_x + menu_x / 8, y=30, width=menu_x / 4 * 3)  # отступ кнопки 1/8 от меню, ширина = 3/4 от меню

b1 = Button(tk, text='Показать мои корабли', command=show_my_ships)
b1.place(x=size_canvas_x + menu_x / 8, y=60, width=menu_x / 4 * 3)

b2 = Button(tk, text='Начать заново!', command=button_begin_again)
b2.place(x=size_canvas_x + menu_x / 8, y=90, width=menu_x / 4 * 3)


def draw_point(x, y, point, ship):
    global count_boom
    #global points
    print(f'Нвжвты координаты  X= {x}, Y= {y}, point = {point}')
    if point > 1:  # Если в мвтрице POINTS по этим координатам уже есть id
        print(f'POINT= {point}')
        canvas.delete(point)
        list_ids.remove(point)
        point = -1
        color = None
        return point
    elif point == 1: # Если кликнули ПКМ, рисуем зел. кружок и пишем его id в матрицу POINTS
        color = 'lightblue'
    elif ship != 0:
        color = 'red'
        count_boom -= 1
        print(f'Осталось {count_boom} {enemy_ships[y][x]}-х палубник))')
    else:
        color = 'blue'
    id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
    list_ids.append(id1)
    if color == 'lightblue':
        point = id1
    if count_boom == 0:
        print('ПОБЕДА!!!')
        button_show_enemy()
        points = [[10 for i in range(s_x)] for i in range(s_y)]  # Заполняем весь список координит
        print('УРАААА!!!')
    return point


def add_to_all(event):
    _type = 0  # ЛКМ
    if event.num == 3:
        _type = 1  # ПКМ

    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()  # Координаты курсора в общей системе координат
    # минус координаты верхнего левого угла рабочего окна в общей системе координат равно координаты курсора
    # в системе координат рабочего окна
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y

    print(ip_x, ip_y, '_type: ', _type)
    if ip_x < s_x and ip_y < s_y:  # Если клик мыши в пределах игрового поля
        ship = enemy_ships[ip_y][ip_x]
        print('points[ip_y][ip_x] = ', points[ip_y][ip_x])
        if points[ip_y][ip_x] == -1:  # Если в списке POINTS по данным  координатам -1, т.е. пустое поле
            point = _type  # то пишем туда клик мыши
            points[ip_y][ip_x] = draw_point(ip_x, ip_y, point, ship)  # и рисуем ПРОИАХ или ПОПАДАНИЕ
        elif points[ip_y][ip_x] > 0:  # Если в списке POINTS по данным  координатам есть id
            point = points[ip_y][ip_x]
            points[ip_y][ip_x] = draw_point(ip_x, ip_y, point, ship)
        print('return= ', points[ip_y][ip_x])




    # ПРОВЕРЯЕМ КООРДИНАТЫ КЛИКА В ПРЕДЕЛАХ ПОЛЯ № 2
    # if ip_x >= s_x + delta_x and ip_x < s_x * 2 + delta_x and ip_y < s_y:  # Если клик мыши в пределах игрового поля 2
    #     print(f'x={ip_x}, y={ip_y}  X-{s_x + delta_x}')


canvas.bind_all("<Button-1>", add_to_all)  # Левая кнопка мыши
canvas.bind_all("<Button-3>", add_to_all)  # Правая кнопка мыши


def generate_enemy_ships(ships_list):
    #global enemy_ships
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

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
