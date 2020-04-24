from tkinter import *
from PIL import ImageTk, Image, ImageOps
from glob import glob


# callin this function in other new session tab
def viewDestroy():
    viewer.destroy()


# viewer function starting here
def viewr():

    # saving any text button as a screen shot
    def save(*args):
        button = entryIntake.get()
        applied.place(x=203, y=812)
        entryLabel.place(x=500, y=-50)
        entryIntake.place(x=800, y=-50)
        f = open('data\\scrnButton.txt', 'w')
        f.write(button)
        f.close()

    # settings button
    def setting():
        bSetting.place(x=0, y=-50)
        entryLabel.place(x=320, y=812)
        entryIntake.place(x=790, y=812)

    # previous screen shot button
    def backward(number):
        if next['state'] == DISABLED:
            number += 1
            next.configure(state=NORMAL)
        imageLabel = Label(viewer, image=l2[number])
        imageLabel.place(x=3, y=0)
        if number <= 0:
            back.configure(state=DISABLED)
        else:
            back.configure(command=lambda: backward(number-1))
            next.configure(command=lambda: forward(number+1))

    # next screen shot button
    def forward(number):
        if back['state'] == DISABLED:
            number -= 1
            back.configure(state=NORMAL)
        imageLabel = Label(viewer, image=l2[number])
        imageLabel.place(x=3, y=0)
        if number == length:
            next.configure(state=DISABLED)
        else:
            next.configure(command=lambda: forward(number+1))
            back.configure(command=lambda: backward(number-1))

    # screen shot design starting here
    global viewer
    viewer = Toplevel()
    viewer.title('Screen Shot Veiwer')
    viewer.configure(bg='#ccc')
    viewer.resizable(0, 0)
    width, height = 1260, 850
    s_width = viewer.winfo_screenwidth()
    s_height = viewer.winfo_screenheight()
    x = (s_width / 2) - (width / 2)
    y = (s_height / 2) - (height / 2)
    viewer.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    viewer.iconbitmap('resources\\fortnite.ico')

    l = glob('data\screenshots\*.png')

    l2 = []
    for img in l:
        temp = Image.open(str(img))
        temp1 = ImageOps.fit(temp, (1250, 800), Image.ANTIALIAS)
        temp2 = ImageTk.PhotoImage(temp1)
        l2.append(temp2)
    length = len(l2) - 1
    imageLabel = Label(viewer, image=l2[length])

    # all the buttons and labels code here
    back = Button(viewer, text='<==', bg='#333', fg='#F5F5F5', bd=4, relief=RAISED, width=10, height=1, font=('Calibri', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=lambda: backward(length-2))
    bSetting = Button(viewer, text='Button Setting', bg='#333', fg='#F5F5F5', bd=4, relief=RAISED, width=12, height=1,font=('Times New Roman', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=setting)
    next = Button(viewer, text='==>', bg='#333', fg='#F5F5F5', state=DISABLED, bd=4, relief=RAISED, width=10, height=1, font=('Calibri', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=lambda: forward(length))
    entryLabel = Label(viewer, text='Type in the button you want to take screenshots ingame!', font=('Times New Roman', 14, 'bold'), fg='#333', bg='#ccc')
    entryIntake = Entry(viewer, font=('Times New Roman', 14, 'bold'), width=16, bg='#A9a9a9', fg='#333', justify=CENTER)
    applied = Label(viewer, text="Settings will be applied after a restart! (if button text is more then 1 character the button won't work)", font=('Times New Roman', 14, 'bold'), fg='#333', bg='#ccc')
    entryIntake.bind('<Return>', save)

    # placing here
    imageLabel.place(x=3, y=0)
    back.place(x=20, y=805)
    bSetting.place(x=555, y=805)
    next.place(x=1125, y=805)

    viewer.mainloop()
