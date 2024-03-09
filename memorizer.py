# PATH

print ('MemoriZer')
SIDE=6 #кол-во строк и столбцов на поле
QSIDE=SIDE**2//2 #сколько парных чисел нужно сделать
print(QSIDE)
prev = None #координаты предыдущей кнопки 



def hide_both(btns, prev, i, j):
    btns[i][j].configure(text=' x ')
    btns[prev[0]][prev[1]].configure(text=' x ')
    
    

def change(btns, nums, i, j):
    global prev
    btns[i][j].configure(text='{:>3}'.format(str(nums[SIDE*i+j])))
    
    if prev:
        if nums[SIDE * i + j] != nums[SIDE * prev[0] + prev[1]]:
            pass # спрятать обе кнопки через таймоут
            main_window.after(1000, hide_both, btns, prev, i, j)
        prev=None 
        
        
    else:
        prev = (i, j)
        
    
    

    
def hide_all(btns):
    for i in range(SIDE):
        for j in range(SIDE):
         btns[i][j].configure(text=' x ')

    
def show_all(btns,nums):
        for i in range(SIDE):
            for j in range(SIDE):
                btns[i][j].configure.text='{:>3}'.format(str(nums[SIDE*i+j]))


from tkinter import *
from random import randint, shuffle
import os





main_window = Tk()
main_window.title ("Запоминалка")
faq = PhotoImage(file='q.gif')

#numbers=[]
#for i in range(1,100):
#   numbers.append(i)
    
numbers=[a for a in range(1,100)]
    
shuffle(numbers)
numbers=numbers[0:QSIDE]*2
shuffle(numbers)
    

print(numbers)

buttons = []

for i in range(SIDE):
    buttons.append([])
    for j in range(SIDE):
        b=Button(main_window, 
            image=faq,
            #text='{:>3}'.format(str(numbers[SIDE*i+j])),
            font=('Courier New', 14, 'normal'),
            relief=FLAT,
            command=lambda ii=i, jj=j: change(buttons, numbers, ii, jj))
        buttons[i].append(b)    
        b.grid(row=i, column=j)
pass



main_window.after(3000, hide_all, buttons)
main_window.mainloop()
    
