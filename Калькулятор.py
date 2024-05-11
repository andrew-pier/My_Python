#КАЛЬКУЛЯТОР
import tkinter
from tkinter import *
import time

win = Tk()
win.geometry('262x410')
win['bg'] = '#484848'
win.title('Калькулятор')
win.wm_attributes("-topmost", 1)  # поверх других окон

next_step_clear = False

calc1 = Entry(win, justify=tkinter.RIGHT, background="#575", font=('Garamond', 12), width=32)
calc1.grid(row=0, column=0, columnspan=4, padx=1)  #columnspan -объединение нескольких колонок
calc1.insert(0, '0')
calc = Entry(win, justify=tkinter.RIGHT, background="#575", font=('Arial', 38), width=9)
calc.grid(row=1, column=0, columnspan=4, padx=1)  #columnspan -объединение нескольких колонок
calc.insert(0, '0')



def press_screen_key(event):
    digit = event.char
    if digit in '/*': row_but = 2
    if digit in '789+': row_but = 3
    if digit in '456-': row_but = 4
    if digit in '123': row_but = 5
    if digit in '0.,': row_but = 6

    if digit in '741': col_but = 0
    if digit in '8520': col_but = 1
    if digit in '963.,/': col_but = 2
    if digit in '*+-': col_but = 3

    if event.keycode == 13: row_but, col_but, digit  = 6, 3, '='
    if event.keycode == 8: row_but, col_but , digit = 2, 1, '←'
    if event.keycode == 27 or event.keycode == 46: row_but, col_but, digit  = 2, 0, 'C'



    b1 = Button(text=digit, background="#FF8C00", font="16")
    if event.keycode == 13:
        b1.grid(row=5, column=3, rowspan=2, stick='wesn', padx=1, pady=1)
    else:
        b1.grid(row=row_but, column=col_but, stick='wesn', padx=1, pady=1)

    win.update()
    time.sleep(0.2)
    b1.destroy()



def press_key(event):
    print('event.char', repr(event.char))
    print('event.keycode', event.keycode)
    if event.char.isdigit(): number(event.char)
    if event.char == '.' or event.char == ',': separator(event.char)
    if event.char in '/*-+': oper(event.char)
    if event.keycode == 13: summa()
    if event.keycode == 8: delete()
    if event.keycode == 27 or event.keycode == 46: com_clear()
    press_screen_key(event)


def com_clear():
    calc.delete(0, END)
    calc.insert(0, '0')
    #
    calc1.delete(0, END)
    calc1.insert(0, '0')


def make_digit_button(digit):
    return Button(text=digit, background="#444", activebackground="#FF8C00", font="16", command=lambda: number(digit))


def make_operation_button(operation):
    return Button(text=operation, background="#555", activebackground="#FF8C00", font="16",
                  command=lambda: oper(operation))  # background="#444"


def number(num):
    global next_step_clear
    if next_step_clear:
        calc.delete(0, END)
        calc1.delete(0, END)
    value = calc.get()  # + str(num)
    if value == '0': value = ''
    calc.delete(0, END)
    calc.insert(0, value + str(num))
    #
    value = calc1.get()
    if value == '0': value = ''
    calc1.delete(0, END)
    calc1.insert(0, value + str(num))
    next_step_clear = False


def oper(num):
    global next_step_clear
    value = calc.get()
    if value == '0': return # если цифровое поле пустое, то ничего делать не надо
    if value[-1] in '+-*/.': value = value[:-1] # исключаем из конца поля знак операции
    if any(i in value for i in '/*-+'): # и если есть другие знаки математических операций, производим вычисление
        value = eval(value)
        if value % 1 == 0: # т.к. при делении EVAL() возвращает дробь (float), то если дробная часть равна 0,
            value = round(value)  # округляем до целого
        else:
            value = round(value, 2)  # иначе округляем до сотых
    calc.delete(0, END)
    calc.insert(0, str(value) + num)
    #
    value = calc1.get()
    calc1.delete(0, END)
    calc1.insert(0, value + num)
    next_step_clear = False


def separator(num):
    if num == ',': num = '.'  # Если нажат разделитель в русской раскладке, меняем на точку
    value = calc.get()
    for i in range(len(value) - 1, -1, -1):
        print(value[i])
        if value[i] == '.': return
        if value[i] in '/*-+': break
    if value[-1] in '/*-+': num = '0' + num
    calc.delete(0, END)
    calc.insert(0, value + str(num))
    calc1.delete(0, END)
    calc1.insert(0, value + str(num))


def summa():
    global next_step_clear
    value = calc.get()
    if value[-1] in '/*-+.': return
    value = eval(value)
    if value % 1 == 0: value = round(value)
    else: value = round(value, 2)
    calc.delete(0, END)
    calc.insert(0, value)
    #
    value1 = calc1.get()
    calc1.delete(0, END)
    calc1.insert(0, str(value1) + '=' + str(value))
    next_step_clear = True


def delete():
    global next_step_clear
    value = calc.get()
    value = value[:-1]
    if value == '': value = '0'
    calc.delete(0, END)
    calc.insert(0, value)
    next_step_clear = False


def change_znak():
    value = calc.get()
    temp = value[1:] if value[0] == '-' else value
    if any(item in temp for item in '/*-+'): return  # если value содержит знаки / * - +, то ничего не делаем
    if '.' in value:
        value = -float(value)
    else:
        value = -int(value)
    calc.delete(0, END)
    calc.insert(0, str(value))


b = Button(text='C', background="#754", activebackground="#FF8C00", font=("Arial", 16), command=com_clear)
b.grid(row=2, column=0,stick='wesn', padx=1,pady=1)
b = Button(text='←', background="#765", activebackground="#FF8C00", font=("Arial", 16), command=delete)
b.grid(row=2, column=1,stick='wesn', padx=1,pady=1)
make_operation_button('/').grid(row=2, column=2, stick='wesn', padx=1, pady=1)
make_operation_button('*').grid(row=2, column=3, stick='wesn', padx=1, pady=1)

make_digit_button(7).grid(row=3, column=0, stick='wesn', padx=1, pady=1)
make_digit_button(8).grid(row=3, column=1, stick='wesn', padx=1, pady=1)
make_digit_button(9).grid(row=3, column=2, stick='wesn', padx=1, pady=1)
make_operation_button('+').grid(row=3, column=3, stick='wesn', padx=1, pady=1)

make_digit_button(4).grid(row=4, column=0, stick='wesn', padx=1, pady=1)
make_digit_button(5).grid(row=4, column=1, stick='wesn', padx=1, pady=1)
make_digit_button(6).grid(row=4, column=2, stick='wesn', padx=1, pady=1)
make_operation_button('-').grid(row=4, column=3, stick='wesn', padx=1, pady=1)

make_digit_button(1).grid(row=5, column=0, stick='wesn', padx=1, pady=1)
make_digit_button(2).grid(row=5, column=1, stick='wesn', padx=1, pady=1)
make_digit_button(3).grid(row=5, column=2, stick='wesn', padx=1, pady=1)

b = Button(text='=', background="#557", activebackground="#FF8C00", font="16", command=summa)
b.grid(row=5, column=3, rowspan=2, stick='wesn', padx=1, pady=1)
b = Button(text='+/-', background="#555", activebackground="#FF8C00", font="16", command=change_znak)
b.grid(row=6, column=0, stick='wesn',padx=1, pady=1)
make_digit_button(0).grid(row=6, column=1, stick='wesn', padx=1, pady=1)
b = Button(text=',', background="#555", activebackground="#FF8C00", font="16", command=lambda: separator('.'))
b.grid(row=6,column=2,stick='wesn',padx=1, pady=1)

win.grid_columnconfigure(0, minsize=65)
win.grid_columnconfigure(1, minsize=65)
win.grid_columnconfigure(2, minsize=65)
win.grid_columnconfigure(3, minsize=65)

win.grid_rowconfigure(1, minsize=30)
win.grid_rowconfigure(2, minsize=65)
win.grid_rowconfigure(3, minsize=65)
win.grid_rowconfigure(4, minsize=65)
win.grid_rowconfigure(5, minsize=65)
win.grid_rowconfigure(6, minsize=65)

win.bind('<Key>', press_key)


win.mainloop()
