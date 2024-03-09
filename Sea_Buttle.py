from tkinter import *
from tkinter import messagebox
import time

tk = Tk()
app_running = True

size_canvas_x = 400
size_canvas_y = 400
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
tk.resizable(None, None)  # запрещаем изменение размера окна
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
b0.place(x=size_canvas_x + 20, y=30)

b1 = Button(tk, text='Начать заново!', command=button_begin_again)
b1.place(x=size_canvas_x + 20, y=60)

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
