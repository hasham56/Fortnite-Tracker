from tkinter import *
from tkinter.scrolledtext import *
import sqlite3

graph = Tk()
graph.geometry('1000x600')
graph.resizable(0, 0)

db = sqlite3.connect('data\\dataBase.db')
cursor = db.cursor()

game = [1, 2, 3, 4, 5, 6, 7]
data = []
for y in game:
   cursor.execute(f'SELECT summary from Session_3_Casual where game = {y}')
   data.append(cursor.fetchall())

summary = []
for x in range(0, len(data)):
   summary.append(str(data[x][0][0]).strip())

print(summary)


canvas = Canvas(graph, bg="#333", width=688, height=480, highlightbackground="#333", highlightthickness=3)
scroll = Scrollbar(canvas, orient=HORIZONTAL, command=canvas.xview)
b, v = {}, {}
for x in range(0, len(summary)):
   x += 1
   v[f'{x}'] = IntVar(value=1)
   label = Label(canvas, text=f'Game {game[x-1]} Summary', bg='#333', fg='#ccc', font=('Times New Roman', 20))
   b[f'{x}'] = ScrolledText(graph, height=3, wrap=WORD, width=8, font=('Times New Roman', 16, 'bold'), bg='#A9a9a9', fg='#333')
   b[f'{x}'].insert(INSERT, f'{summary[x-1]}')
   canvas.create_window(x * 390, 40, anchor=S, window=label, width=300, height=88)
   canvas.create_window(x * 390, 70, anchor=N, window=b[f'{x}'], width=300, height=325)

canvas.config(scrollregion=canvas.bbox('all'), xscrollcommand=scroll.set)
scroll.place(relx=0, rely=1, relwidth=1, anchor=SW)

canvas.place(x=200, y=0)

graph.mainloop()
