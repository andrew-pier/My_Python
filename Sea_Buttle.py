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
menu_x = size_canvas_x // 2.8  # Место для меню справа от поля

ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Список все кораблей
enemy_ships = [[0 for i in range(s_x)] for i in range(s_y)]  # Пустая матрица игнового поля. Заполняем нолями
# print('МАТРИЦА ПОЛЯ:\n', *enemy_ships, sep='\n')
list_ids = []  # список объектов canvas
points = [[-1 for i in range(s_x)] for i in range(s_y)]  # Список координит, куда уже кликали мышкой
count_boom = sum(ships_list)



def draw_table():  # Рисуем клетки на поле
    for i in range(0, s_x + 1):
        canvas.create_line(i * step_x, 0, i * step_x, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(0, i * step_y, size_canvas_y, i * step_y)


def on_closing():
    global app_running
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
        app_running = False
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)  # функция при закрытии окна
tk.title('Игра "Морской бой"')  # Заголовок окна
tk.resizable(False, False)  # запрещаем изменение размера окна
tk.wm_attributes("-topmost", 1)  # поверх других окон

canvas = Canvas(tk, width=size_canvas_x + menu_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.pack()
tk.update()

draw_table()


def button_show_enemy():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:
                color = 'red'
                if points[j][i] != -1:
                    color = 'yellow'
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_begin_again():
    global list_ids
    global points
    for elemnt in list_ids:
        canvas.delete(elemnt)
    list_ids = []
    points = [[-1 for i in range(s_x)] for i in range(s_y)]
    print('МАТРИЦА ПОЛЯ:\n', *points, sep='\n')
    generate_enemy_ships(ships_list)


b0 = Button(tk, text='Показать корабли противника', command=button_show_enemy)
b0.place(x=size_canvas_x + menu_x / 8, y=30, width=menu_x / 4 * 3)  # отступ кнопки 1/8 от меню, ширина = 3/4 от меню

b1 = Button(tk, text='Начать заново!', command=button_begin_again)
b1.place(x=size_canvas_x + menu_x / 8, y=60, width=menu_x / 4 * 3)


def draw_point(x, y):
    # print('Нвжвты координаты  X=', x, 'Y=', y)
    global count_boom
    global points
    if enemy_ships[y][x] == 0:
        color = 'blue'
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        list_ids.append(id1)
    else:
        color = 'red'
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        count_boom -= 1
        if count_boom == 0:
            print('ПОБЕДА!!!')
            points = [[10 for i in range(s_x)] for i in range(s_y)]  # Заполняем весь список координит


def add_to_all(event):
    _type = 0  # ЛКМ
    if event.num == 3:
        _type = 1  # ПКМ

    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y
    # print(ip_x, ip_y, '_type: ', _type)
    if ip_x < s_x and ip_y < s_y:  # Если клик мыши в пределах игрового поля
        if points[ip_y][ip_x] == -1:  # Если в списке POINTS gj данным  координатам -1,
            points[ip_y][ip_x] = _type  # то пишем туда клик мыши
            draw_point(ip_x, ip_y)  # и рисуем ПРОИАХ или ПОПАДАНИЕ
        # print(list_ids)


canvas.bind_all("<Button-1>", add_to_all)  # Левая кнопка мыши
canvas.bind_all("<Button-3>", add_to_all)  # Правая кнопка мыши


def generate_enemy_ships(ships_list):
    global enemy_ships
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


generate_enemy_ships(ships_list)

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
