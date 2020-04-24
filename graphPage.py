from tkinter import *
from PIL import Image, ImageTk
import sqlite3
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
from tkinter.scrolledtext import *
from matplotlib.figure import Figure
style.use('dark_background')
import yourSessions

# these are all basics so no comments here and also its underconstruction
def graphDestroy():
    graph.destroy()


# graph page code starts here
def graphPage(file):
    # back button here
    def back():
        yourSessions.yourSessions()

    # first graphs when selected a session
    def initialGraphs(column, game):
        col(column)
        mainL['text'] = 'Placement'
        cursor.execute(f'select {col(column)} from {h[::-1]}')
        data = cursor.fetchall()
        mData = []
        for x in range(0, len(data)):
            mData.append(str(data[x][0]))

        f = Figure(figsize=(7, 5), facecolor='grey')
        if len(mData) > 1:
            a = f.add_subplot(111)
        else:
            a = f.add_subplot(141)
        nData = []
        for d in mData:
            nData.append(int(d))
        a.set_ylabel(f'{column}')
        a.set_xlabel('Games')
        f.set_tight_layout(TRUE)
        a.plot(game, nData)
        canvas1 = FigureCanvasTkAgg(f, graph)
        canvas1.get_tk_widget().place(x=130, y=130)

    # counting games when input of games are changed
    def countGames():
        game = []
        for f in range(1, 250):
            try:
                if v[f'{f}'].get() == 1:
                    game.append(int(b[f'{f}']['text']))
            except:
                pass
        return game

    # plot graph button function
    def plotGraph():
        column = 'placement'
        nex(length - 7)
        backB['state'] = DISABLED
        mainL['text'] = 'Placement'
        graphing(column, countGames())

    # plotting graphs according to database in session
    def graphing(column, game):
        if column == 'weapon':
            return weapons(game)
        elif column == 'summary':
            return summary(game)
        else:
            data = []
            for p in game:
                cursor.execute(f'SELECT {column} from {h[::-1]} where game = {p}')
                data.append(cursor.fetchall())

            mData = []
            for x in range(0, len(data)):
                mData.append(str(data[x][0][0]))

            f = Figure(figsize=(7, 5), facecolor='grey')
            if len(mData) > 1:
                a = f.add_subplot(111)
            else:
                a = f.add_subplot(141)
            nData = []
            gam = []
            for ga in game:
                gam.append(str(ga))
            for d in mData:
                nData.append(int(d))
            a.set_ylabel(f'{reverse(column)}')
            a.set_xlabel('Games')
            f.set_tight_layout(TRUE)
            a.plot(gam, nData)
            canvas1 = FigureCanvasTkAgg(f, graph)
            canvas1.get_tk_widget().place(x=130, y=130)

    # altering column names according to database columns
    def col(col):
        if col == 'Placement':
            column = 'placement'
        elif col == 'Eliminations':
            column = 'eliminations'
        elif col == 'Accuracy':
            column = 'accuracy'
        elif col == 'Damage Dealt':
            column = 'damageDealt'
        elif col == 'Damage Taken':
            column = 'damageTaken'
        elif col == 'Materials Used':
            column = 'matUsed'
        elif col == 'Materials Gathered':
            column = 'matGathered'
        elif col == 'Weapon Died To':
            column = 'weapon'
        elif col == 'Time Survived':
            column = 'timeSurvived'
        else:
            column = 'summary'
        return column

    # altering columns on what i want to show user
    def reverse(col):
        if col == 'placement':
            column = 'Placement'
        elif col == 'eliminations':
            column = 'Eliminations'
        elif col == 'accuracy':
            column = 'Accuracy'
        elif col == 'damageDealt':
            column = 'Damage Dealt'
        elif col == 'damageTaken':
            column = 'Damage Taken'
        elif col == 'matUsed':
            column = 'Materials Used'
        elif col == 'matGathered':
            column = 'Materials Gathered'
        elif col == 'weapon':
            column = 'Weapon Died To'
        elif col == 'timeSurvived':
            column = 'Time Survived'
        else:
            column = 'Summary'
        return column

    # summary page
    def summary(game):
        data = []
        for y in game:
            cursor.execute(f'SELECT summary from {h[::-1]} where game = {y}')
            data.append(cursor.fetchall())

        summary = []
        for x in range(0, len(data)):
            summary.append(str(data[x][0][0]).strip())

        canvas = Canvas(graph, bg="#333", width=693, height=493, highlightbackground="#333", highlightthickness=3)
        scroll = Scrollbar(canvas, orient=HORIZONTAL, command=canvas.xview)
        b, v = {}, {}
        for x in range(0, len(summary)):
            x += 1
            v[f'{x}'] = IntVar(value=1)
            label = Label(canvas, text=f'Game {game[x - 1]} Summary', bg='#333', fg='#ccc',
                          font=('Times New Roman', 20))
            b[f'{x}'] = ScrolledText(graph, height=3, wrap=WORD, width=8, font=('Times New Roman', 16, 'bold'),
                                     bg='#A9a9a9', fg='#333')
            b[f'{x}'].insert(INSERT, f'{summary[x - 1]}')
            canvas.create_window(x * 390, 40, anchor=S, window=label, width=300, height=88)
            canvas.create_window(x * 390, 70, anchor=N, window=b[f'{x}'], width=300, height=325)

        canvas.config(scrollregion=canvas.bbox('all'), xscrollcommand=scroll.set)
        scroll.place(relx=0, rely=1, relwidth=1, anchor=SW)

        canvas.place(x=130, y=130)

    # weapons lost to page
    def weapons(game):
        canvas1 = Canvas(graph, bg="#333", width=686, height=478, highlightbackground="#333", highlightthickness=3)

        scroll = Scrollbar(canvas1, orient=VERTICAL)
        scroll.place(relx=1, rely=0, relheight=1, anchor=NE)
        canvas1.config(yscrollcommand=scroll.set, scrollregion=(0, 0, 0, 20))
        leftside = Listbox(canvas1, bg='#333', fg='#ccc', yscrollcommand=scroll.set, width=42, height=13, selectbackground='#333', selectborderwidth=0, selectforeground='#ccc', activestyle='none', font=('Times New Roman', 24))
        scroll.config(command=leftside.yview)
        data = []
        for x in game:
            cursor.execute(f'SELECT weapon from {h[::-1]} where game = {x}')
            data.append(cursor.fetchall())

        weapon = []
        for x in range(0, len(data)):
            weapon.append(str(data[x][0][0]))

        entries = []
        for x in range(len(game)):
            entries.append('Game: ' + str(game[x]) + ':               You died to ' + str(weapon[x]))

        for line in entries:
            leftside.insert('end', str(line))
        leftside.place(x=0, y=0)
        canvas1.place(x=134, y=137)

    # previous graph button
    def bac(number):
        if nextB['state'] == DISABLED or mainL['text'] == 'Placement':
            number += 1
            nextB.configure(state=NORMAL)
        mainL.configure(text=f'{attributes[number]}')
        if number <= 0:
            backB.configure(state=DISABLED)
        else:
            backB.configure(command=lambda: bac(number - 1))
            nextB.configure(command=lambda: nex(number + 1))
        column = col(str(attributes[number]))
        graphing(column, countGames())

    # next graph button
    def nex(number):
        nextB['state'] = NORMAL
        if backB['state'] == DISABLED:
            number -= 1
            backB.configure(state=NORMAL)
        mainL.configure(text=f'{attributes[number]}')
        if number == length:
            nextB.configure(state=DISABLED)
        else:
            nextB.configure(command=lambda: nex(number + 1))
            backB.configure(command=lambda: bac(number - 1))
        column = col(str(attributes[number]))
        graphing(column, countGames())

    # designing starts here
    global graph
    graph = Tk()
    graph.title('Your Sessions')
    width, height = 950, 850
    s_width = graph.winfo_screenwidth()
    s_height = graph.winfo_screenheight()
    x = (s_width / 2) - (width / 2)
    y = (s_height / 2) - (height / 2)
    graph.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    graph.resizable(0, 0)
    graph.update()

    # icon
    graph.iconbitmap('resources\\fortnite.ico')

    # data base connection
    db = sqlite3.connect('data\\dataBase.db')
    cursor = db.cursor()

    h = ''
    for x in range(len(file) - 1, 0, -1):
        if file[x] == 'S':
            h += file[x]
            break
        else:
            h += file[x]
    realFile = h[::-1]
    cursor.execute(f'select * from {realFile}')

    # data manipulation
    attrr = [description[0] for description in cursor.description]

    attributes = []
    for x in range(1, len(attrr)):
        if attrr[x] == 'placement':
            attributes.append('Placement')
        elif attrr[x] == 'eliminations':
            attributes.append('Eliminations')
        elif attrr[x] == 'accuracy':
            attributes.append('Accuracy')
        elif attrr[x] == 'damageDealt':
            attributes.append('Damage Dealt')
        elif attrr[x] == 'damageTaken':
            attributes.append('Damage Taken')
        elif attrr[x] == 'matUsed':
            attributes.append('Materials Used')
        elif attrr[x] == 'matGathered':
            attributes.append('Materials Gathered')
        elif attrr[x] == 'weapon':
            attributes.append('Weapon Died To')
        elif attrr[x] == 'timeSurvived':
            attributes.append('Time Survived')
        else:
            attributes.append('Summary')

    length = len(attributes) - 1

    cursor.execute(f'SELECT game from {realFile}')
    games = cursor.fetchall()
    g = []
    for x in range(0, len(games)):
        g.append(str(games[x][0]))

    # background image
    real2 = Image.open('resources\\graphBg.jpg')
    img2 = ImageTk.PhotoImage(real2)
    Label(graph, image=img2).place(x=-100, y=-10)

    # all labels and buttons here
    Label(graph, text=f'{h[::-1]}', bg='#333', fg='#fff', bd=8, relief=RAISED, width=18, font=('Times New Roman', 20, 'bold')).place(x=330, y=12)
    nextB = Button(graph, text='=>', state=NORMAL, bg='#333', fg='#fff', bd=4, relief=RAISED, width=7, height=1, font=('Calibri', 12, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=lambda: nex(length - 5))
    mainL = Label(graph, text=f'{attributes[0]}',bg='#333', fg='#fff', bd=6, relief=RAISED, width=16, font=('Times New Roman', 16, 'bold'))
    backB = Button(graph, text='<=', state=DISABLED, bg='#333', fg='#fff', bd=4, relief=RAISED, width=7, height=1, font=('Calibri', 12, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=lambda: bac(length))
    previous = Button(graph, text='Back', bg='#333', fg='#fff', bd=4, relief=RAISED, width=10, height=1, font=('Times New Roman', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=back)
    plot = Button(graph, text='Plot', bg='#333', fg='#fff', bd=4, relief=RAISED, width=10, height=1, font=('Times New Roman', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=plotGraph)

    # canvas on which game bar is placed
    canvas = Canvas(graph, bg="#333", width=845, height=105, highlightbackground="#333", highlightthickness=3)
    scroll = Scrollbar(canvas, orient=HORIZONTAL, command=canvas.xview)
    b, v = {}, {}
    for x in range(0, len(g)):
        x += 1
        v[f'{x}'] = IntVar(value=1)
        label = Label(canvas, text=f'Game {x}:', bg='#333', fg='#ccc', font=('Times New Roman', 20))
        b[f'{x}'] = Checkbutton(canvas, text=f'{x}', bg='#333', fg='#333', variable=v[f'{x}'], activebackground='#333',
                                activeforeground='#333')
        b[f'{x}'].select()
        canvas.create_window(x * 140, 20, anchor=SE, window=label, width=110, height=88)
        canvas.create_window(x * 140, -12, anchor=SW, window=b[f'{x}'], width=0, height=0)

    # canvas configration
    canvas.config(scrollregion=canvas.bbox('all'), xscrollcommand=scroll.set)
    scroll.place(relx=0, rely=1, relwidth=1, anchor=SW)

    # all placements
    nextB.place(x=840, y=350)
    mainL.place(x=383, y=80)
    backB.place(x=45, y=350)
    canvas.place(x=50, y=650)
    previous.place(x=25, y=785)
    plot.place(x=805, y=785)
    initialGraphs('Placement', g)

    # mainloop stops the tab on hold until user make a move
    graph.mainloop()
