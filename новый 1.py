

from tkinter import *
import os

row = 4
num = -1

window = Tk()
window.title('Калькулятор')
window.geometry('300x350')
buttons = []
print('Hi!!!!!')
print(num)

for i in range(row, 0, -1):
    print(i)
    for j in range(row-1):
        print('=', j)
        print('NUM= ', num)
        numm = num
        print('numm= ', numm)
        if num == -1:
            numm = "C"
        if (i == 4 and j == 2):
            numm = ","
            num -= 1
        print ('numm= ', numm)
        b=Button(window,text=numm,justify=CENTER,background="#555", foreground="#ccc", activebackground="#FF8C00",
                  pady="10",padx="20", font="16")
        #b=Button(window,text=numm,justify=CENTER,background="#555", foreground="#ccc", activebackground="#FF8C00",
        #          width=5, pady="8", font="16")          
        b.grid(row=i, column=j, stick='wesn', padx=1, pady=1)
        num +=1

calc_entry = Entry(window, width = 33)
calc_entry.grid(row=0, column=0, columnspan=5)















window.mainloop()


