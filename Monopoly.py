

from tkinter import *
from tkinter import messagebox
from pygame import mixer
import time
import random

win = Tk()
screen_width = win.winfo_screenwidth() #    ОПРЕДЕЛЕНИЕ РАЗМЕРОВ ЭКРАНА ШИРИНА (ОСЬ Х)
screen_height = win.winfo_screenheight() #    ОПРЕДЕЛЕНИЕ РАЗМЕРОВ ЭКРАНА ВЫСОТА (ОСЬ Y)
print(screen_width, screen_height)
# side_x = side_y = '800'

#side_x = side_y = str(screen_height // 10 * 9) # УСТАНАВЛИВАЕМ РАМЕР ОКНА 90% ОТ РАЗМЕРА ЭКРАНА ПО ОСИ y
side_x = side_y = '804' # УСТАНАВЛИВАЕМ РАМЕР ОКНА 90% ОТ РАЗМЕРА ЭКРАНА ПО ОСИ y
win_resolution = str(side_x + 'x' + side_y)
print(win_resolution)

cell_width = int(side_x) // 12 # НАХОДИМ ЩИРИНУ КЛЕТКИ
cell_height = int(cell_width * 1.5) # НАХОДИМ ДЛИНУ КЛЕТКИ
print(cell_width, cell_height)

#win.geometry(win_resolution)
win.title('MONOPOLY')
win.wm_attributes("-topmost", 1)  # поверх других окон
py_image1 = PhotoImage(file="monopoly.png")
canvas = Canvas(win, width=side_x, height=side_y, bd=0, highlightthickness=0)
canvas.create_image(402, 402, image=py_image1)

# canvas.create_line(110, 0, 110, 804, fill='red')
# canvas.create_line(175, 0, 175, 804, fill='red')
# canvas.create_line(0, 110, 804, 110, fill='red')
print(cell_height)
# canvas.create_line(int(side_y) - cell_height, 0, int(side_y) - cell_height, int(side_y))
# canvas.create_line(0, cell_height, int(side_y), cell_height)
# canvas.create_line(0, int(side_y) - cell_height, int(side_y), int(side_y) - cell_height)
fish_player1 = canvas.create_oval( 120, 50, 164, 95, fill='red')
canvas.pack()
win.update()
time.sleep(2)
def moveew(n): # ПЕРЕЛВИЖЕНИЕ ФИШКИ
    for n in range(1, n):
        for i in range(1, 66):
            time.sleep(0.0005) # СКОРОСТЬ ПЕРЕМЕЩЕНИЯ ФИШКИ
            canvas.move(fish_player1, 1, 0)
            win.update()
    #     print('step-', n, '  x,y = ', canvas.coords(fish_player1)) # показать координаты фишки после каждой клетки
    # print('x,y = ', canvas.coords(fish_player1)) # показать координаты фишки в конце хода

moveew(4)


for i in range(694, 110, -65): # отрисовка границ и центра ячеек
    canvas.create_line(i, 0, i, 804, fill='red')
    canvas.create_line(i - 32, 0, i - 32, 804, fill='green')
    print('green=', i - 32)


canvas.pack()





win.mainloop()
