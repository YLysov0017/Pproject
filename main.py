import time
from tkinter import Tk, Label, mainloop 

root = Tk()
root.title('clocks')
root.geometry('+10+10')
root.overrideredirect(True)

lb = Label(root, bg='black', fg='purple', text='dfh', font = 'arial 210')
lb.pack(padx=10, pady=20)



def gettime():
    p = ':' if int(time.strftime('%S')) % 2 == 0 else ' '
    lb['text'] = time.strftime(f'%H{p}%M{p}%S')
    lb.after(1000, gettime)

def close(event):
    root.destroy()

    
root.bind("<Escape>", close)
lb.after_idle(gettime)
root.mainloop()
.0