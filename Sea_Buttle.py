from tkinter import *
from tkinter import messagebox
import time

tk = Tk()
app_running = True

size_canvas_x = 500
size_canvas_y = 500
s_x = s_y = 10  # Размер игрового поля
step_x = size_canvas_x // s_x  # шаг клетки
step_y = size_canvas_y // s_y

menu_x = 167  # Место для меню справа от поля (размер примерно = Поле_по_Х // 2,4)


def draw_table():
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
tk.wm_attributes("-topmost", 1)  # поверх окон

canvas = Canvas(tk, width=size_canvas_x + menu_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.pack()
tk.update()

draw_table()


def button_show_enemy():
    pass


def button_begin_again():
    pass


b0 = Button(tk, text='Показать корабли противника', command=button_show_enemy)
b0.place(x=size_canvas_x + 20, y=30, width=127)

b1 = Button(tk, text='Начать заново!', command=button_begin_again)
b1.place(x=size_canvas_x + 20, y=60, width=127)


def add_to_all(event):
    _type = 0  # ЛКМ
    if event.num == 3:
        _type = 1  # ПКМ
    print(_type)

    # mouse_x1 = event.x
    # mouse_y1 = event.y
    # ip_x1 = mouse_x1 // step_x
    # ip_y1 = mouse_y1 // step_y

    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y

    print(mouse_x, mouse_y)
    print(ip_x, ip_y, '_type: ', _type)
    # print(ip_x1, ip_y1, '_type: ', _type)


canvas.bind_all("<Button-1>", add_to_all)  # Левая кнопка мыши
canvas.bind_all("<Button-3>", add_to_all)  # Правая кнопка мыши


while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
