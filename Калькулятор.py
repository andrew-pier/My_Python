#КАЛЬКУЛЯТОР

from tkinter import *
import os

win=Tk()
win.geometry('240x260')
#win['bg'] = '#33ffe6'
win.title('Калькулятор')

calc = Entry(win)
calc.grid(row=0, column=0, columnspan=3) #columnspan -объединение нескольких колонок

Button(text='1', background="#555", font="16").grid(row=1, column=0, stick='wesn', padx=1, pady=1)
Button(text='2', background="#555", font="16").grid(row=1, column=1, stick='wesn', padx=1, pady=1)
Button(text='3', background="#555", font="16").grid(row=1, column=2, stick='wesn', padx=1, pady=1)
Button(text='4', background="#555", font="16").grid(row=2, column=0, stick='wesn', padx=1, pady=1)
Button(text='5', background="#555", font="16").grid(row=2, column=1, stick='wesn', padx=1, pady=1)
Button(text='6', background="#555", font="16").grid(row=2, column=2, stick='wesn', padx=1, pady=1)
Button(text='7', background="#555", font="16").grid(row=3, column=0, stick='wesn', padx=1, pady=1)
Button(text='8', background="#555", font="16").grid(row=3, column=1, stick='wesn', padx=1, pady=1)
Button(text='9', background="#555", font="16").grid(row=3, column=2, stick='wesn', padx=1, pady=1)
Button(text='0', background="#555", font="16").grid(row=4, column=0, stick='wesn', padx=1, pady=1)

win.grid_columnconfigure(0,minsize=60)
win.grid_columnconfigure(1,minsize=60)
win.grid_columnconfigure(2,minsize=60)

win.grid_rowconfigure(1,minsize=60)
win.grid_rowconfigure(2,minsize=60)
win.grid_rowconfigure(3,minsize=60)
win.grid_rowconfigure(4,minsize=60)








win.mainloop()