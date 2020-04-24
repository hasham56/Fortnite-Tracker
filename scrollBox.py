from tkinter import Tk, Listbox, Button, Scrollbar


def get():
    userline = leftside.get('active')
    print(userline)


thescale = Tk()
thescale.geometry('600x600')
scroll = Scrollbar(thescale)
scroll.pack(side='right', fill='y')

leftside = Listbox(thescale, bg='#333', fg='#ccc', yscrollcommand=scroll.set, width=10, selectbackground='#333', font=('Times New Roman', 24))
for line in range(101):
    leftside.insert('end', "Scale "+str(line))

leftside.place(x=0, y=0)
scroll.config(command=leftside.yview)

selectbutton=Button(thescale, text="Select")
selectbutton.pack()

thescale.mainloop()

