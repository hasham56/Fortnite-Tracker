from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mainPage
import graphPage
import sqlite3


# this function is called in other tabs
def yourDestroy():
    your.destroy()


# main your session tab code
def yourSessions():
    db = sqlite3.connect('data\\dataBase.db')
    cursor = db.cursor()

    # back button here
    def back():
        mainPage.startPage()

    # delete button here
    def delete():
        file = leftside.get('active')
        if file == '' or file == ' ':
            messagebox.showinfo('Error!', 'There is no session selected!', icon='info')
        else:
            result = messagebox.askquestion('Warning', 'Are You Sure, You wanna delete this session?')
            if result == 'yes':
                h = ''
                for x in range(len(file) - 1, 0, -1):
                    if file[x] == 'S':
                        h += file[x]
                        break
                    else:
                        h += file[x]
                cursor.execute(f'DROP TABLE IF EXISTS {h[::-1]}')
                deletion = open('data\\deletionRecord.txt', 'a')
                deletion.write('0')
                leftside.delete(0, 'end')
                scrollBar()

    # takes the selected session and calls graph page
    def pre(*args):
        file = leftside.get('active')
        if file == '':
            pass
        else:
            try:
                your.destroy()
            except:
                pass
            graphPage.graphPage(str(file))

    # sessions scrollbar here
    def scrollBar():
        sessions, date, tab = [], [], []
        script = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' order by name;")
        for tables in script:
            sessions += tables[0].split('\n')

        for temp in sessions:
            cursor.execute(f"SELECT time FROM {temp}")
            c = cursor.fetchall()
            date += str(c[0][0]).split('\n')

        for x in range(0, len(sessions), 1):
            tab += ('  ' + str(date[x]) + ' | ' + str(sessions[x])).split('\n')

        for line in tab:
            leftside.insert('end', str(line))
        leftside.selection_set(first=0)
        leftside.place(x=0, y=0)

    try:
        graphPage.graphDestroy()
    except:
        pass

    # designing starts here
    global your
    your = Tk()
    your.title('Your Sessions')
    width, height = 650, 650
    s_width = your.winfo_screenwidth()
    s_height = your.winfo_screenheight()
    x = (s_width / 2) - (width / 2)
    y = (s_height / 2) - (height / 2)
    your.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    your.resizable(0, 0)
    your.update()

    # icon
    your.iconbitmap('resources\\fortnite.ico')

    # background image
    real2 = Image.open('resources\\newSessionBg.jpg')
    img2 = ImageTk.PhotoImage(real2)
    Label(your, image=img2).place(x=-100, y=-10)

    # cavas on which scroll box is placed here
    canvas = Canvas(your, bg="#333", width=552, height=465, highlightbackground="#333", highlightthickness=3)
    canvas.place(x=47, y=80)

    # scroll bar code here
    scroll = Scrollbar(canvas, orient=VERTICAL)
    scroll.place(relx=1, rely=0, relheight=1, anchor=NE)
    canvas.config(yscrollcommand=scroll.set, scrollregion=(0, 0, 0, y))
    leftside = Listbox(canvas, bg='#333', fg='#ccc', yscrollcommand=scroll.set, width=33, height=10, selectbackground='#ccc', selectborderwidth=5, selectforeground='#333', activestyle='none', font=('Times New Roman', 24))
    scroll.config(command=leftside.yview)
    leftside.bind('<Double-Button-1>', pre)

    # your sessions label here
    Label(your, text='Your Sessions', bg='#333', fg='#fff', bd=10, relief=RAISED, width=12,font=('Times New Roman', 23, 'bold')).place(x=210, y=7)

    # main 3 buttons and scroll bar is placed here
    scrollBar()
    Button(your, text='Back', bg='#333', fg='#fff', bd=6, relief=RAISED, width=10, height=1, font=('Times New Roman', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=back).place(x=45, y=576)
    Button(your, text='Next', bg='#333', fg='#fff', bd=6, relief=RAISED, width=10, height=1, font=('Times New Roman', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=pre).place(x=478, y=576)
    Button(your, text='Delete', bg='#333', fg='#fff', bd=6, relief=RAISED, width=10, height=1, font=('Times New Roman', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=delete).place(x=265, y=576)
    your.mainloop()
