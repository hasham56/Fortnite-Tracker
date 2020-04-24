from tkinter import *
from PIL import Image, ImageTk
import mainPage
from tkinter.scrolledtext import *
from datetime import date, datetime
import sqlite3
import os
from pynput.keyboard import Listener, Key, Controller
import wx
import threading
from screenshotPage import viewr, viewDestroy
import sys


# this function destroys window in mainPage Tab
def newDestroy():
    new.destroy()


# screen shot variable
ss = 0


# this is the main function for newSession
def newSession(mode, a, n):
    global ss
    ss = 0
    db = sqlite3.connect('data\\dataBase.db')
    cursor = db.cursor()

    # trigger for if F12 is pressed
    def trigger(key):
        f = open('data\\scrnButton.txt', 'r')
        global ss
        ss += 10
        d = f.readline()
        f.close()
        ss += 1
        trigger = key
        if d == '':
            trig = Key.f12
        else:
            trigger = str(key)
            trig = f"'{d}'"
        if trigger == trig:
            app = wx.App()  # Need to create an App instance before doing anything
            screen = wx.ScreenDC()
            size = screen.GetSize()
            bmp = wx.Bitmap(size[0], size[1])
            mem = wx.MemoryDC(bmp)
            mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
            del mem  # Release bitmap
            bmp.SaveFile(f'data\\screenshots\\status{ss}.png', wx.BITMAP_TYPE_PNG)
        elif str(trigger) == "'|'":
            sys.exit()

    # listner of keyboard strokes begins here
    def screenShot():
        with Listener(on_press=trigger) as trr:
            trr.join()

    # screenshot thread begins here
    scrn = threading.Thread(target=screenShot)
    scrn.start()

    # screen shot viewer button here
    def view():
        try:
            warning.configure(text='')
            viewr()
        except:
            try:
                viewDestroy()
                warning.configure(text='No screenshots to show! Press "f12" and TryAgian')
            except:
                pass

    # for getting saved weapon list from text file in resources
    def weapon_list():
        file = open('resources\\weapons.txt', 'r')
        li = file.readlines()
        temp = []
        for b in li:
            temp += b.split('\n')
        data1 = [b1 for b1 in temp if b1]
        file.close()
        return data1

    # table for compitative mode
    def dataBaseCompe(time1, session, game, place, taken, dealt, survived, elim, acc, matused, mat, wep, sum):
        if a == 0:
            cursor.execute(f'CREATE TABLE {session} (game integer, time text, placement integer, eliminations integer, accuracy integer, damageDealt integer, damageTaken integer, matUsed integer, matGathered integer, weapon text, timeSurvived text, summary text)')
            cursor.execute(f'INSERT INTO {session} VALUES ({game}, "{time1}", {place}, {elim}, {acc}, {dealt}, {taken}, {matused}, {mat}, "{wep}", "{survived}", "{sum}")')
        else:
            cursor.execute(f'INSERT INTO {session} VALUES ({game}, "{time1}", {place}, {elim}, {acc}, {dealt}, {taken}, {matused}, {mat}, "{wep}", "{survived}", "{sum}")')

    # table for casual mode
    def dataBaseCasual(time1, session, game, place, taken, dealt, elim, acc, matused, mat, wep, sum):
        if a == 0:
            cursor.execute(f'CREATE TABLE {session} (game integer, time text, placement integer, eliminations integer, accuracy integer, damageDealt integer, damageTaken integer, matUsed integer, matGathered integer, weapon text, summary text)')
            cursor.execute(f'INSERT INTO {session} VALUES ({game}, "{time1}", {place}, {elim}, {acc}, {dealt}, {taken}, {matused}, {mat}, "{wep}", "{sum}")')
        else:
            cursor.execute(f'INSERT INTO {session} VALUES ({game}, "{time1}", {place}, {elim}, {acc}, {dealt}, {taken}, {matused}, {mat}, "{wep}", "{sum}")')

    # Counting games
    def count():
        if a == 0:
            return 0
        else:
            return n

    # submition for casual goes here
    def submitCasual():
        time1 = timeEntry.get()
        session = sessionName['text']
        game = gameEntry
        place = placeEntry.get()
        taken = damageTaken.get()
        dealt = damageDealt.get()
        elim = elimEntry.get()
        ac = acc.get()
        matused = matUEntry.get()
        mat = matEntry.get()
        wep = variable1.get()
        sum = sumBox.get('1.0', END)
        # just checking some errors
        try:
            if len(time1) <= 6:
                warning.configure(text='Short Time String!')
            elif int(place) > 100 or int(place) < 1:
                warning.configure(text='Please Enter Valid Placement!')
            elif int(taken) < 0:
                warning.configure(text='Please Enter Valid Damage Taken!')
            elif int(dealt) < 0:
                warning.configure(text='Please Enter Valid Damage Dealt!')
            elif int(ac) > 100 or int(ac) < 0:
                warning.configure(text='Please Enter Valid Accuracy!')
            elif int(matused) < 0:
                warning.configure(text='Wrong Material Used')
            elif int(mat) < 0:
                warning.configure(text='Wrong Material Gathered')
            elif wep == 'choose':
                warning.configure(text='Kindly Choose a Weapon')
            elif len(sum) < 0 or sum == 'Summarize Your Death...':
                sum = "You didn't want to summarize your death :P"
            else:
                warning.configure(text='')
                dataBaseCasual(time1, session, game, place, taken, dealt, elim, ac, matused, mat, wep, sum)
                db.commit()
                m = ()
                for m in cursor.execute(f"SELECT COUNT(*) FROM {session}"):
                    pass
                new.destroy()
                newSession(mode, 1, m[0])
        # if user inputs some string in input feilds
        except:
            warning.configure(text='Some Wrong Input.. Kindly Recheck!')

    # submition for compitative goes here
    def submitCompe():
        time1 = timeEntry.get()
        session = sessionName['text']
        game = gameEntry
        survived = tSEntry.get()
        place = placeEntry.get()
        taken = damageTaken.get()
        dealt = damageDealt.get()
        elim = elimEntry.get()
        ac = acc.get()
        matused = matUEntry.get()
        mat = matEntry.get()
        wep = variable1.get()
        sum = sumBox.get('1.0', END)
        time2 = tSEntry.get()
        # just checking some errors
        try:
            if len(time1) <= 6:
                warning.configure(text='Short Time String!')
            elif int(place) > 100 or int(place) < 1:
                warning.configure(text='Please Enter Valid Placement!')
            elif int(taken) < 0:
                warning.configure(text='Please Enter Valid Damage Taken!')
            elif int(dealt) < 0:
                warning.configure(text='Please Enter Valid Damage Dealt!')
            elif int(ac) > 100 or int(ac) < 0:
                warning.configure(text='Please Enter Valid Accuracy!')
            elif int(matused) < 0:
                warning.configure(text='Wrong Material Used')
            elif int(mat) < 0:
                warning.configure(text='Wrong Material Gathered')
            elif wep == 'choose':
                warning.configure(text='Kindly Choose a Weapon')
            elif int(time2) < 0 or int(time2) > 30:
                warning.configure(text='Wrong Material Gathered')
            elif len(sum) < 0 or sum == 'Summarize Your Death...':
                sum = "You didn't want to summarize your death :P"
            else:
                warning.configure(text='')
                dataBaseCompe(time1, session, game, place, taken, dealt, survived, elim, ac, matused, mat, wep, sum)
                n = ()
                for n in cursor.execute(f"SELECT COUNT(*) FROM {session}"):
                    pass
                db.commit()
                new.destroy()
                newSession(mode, 1, n[0])
        # if user inputs some string in input feilds
        except:
            warning.configure(text='Some Wrong Input.. Kindly Recheck!')

    # this function destroys mainPage before opening
    def back():
        key = Controller()
        key.press('|')
        key.release('|')
        path = 'data\\screenshots'
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if '.png' in file:
                    files.append(os.path.join(file))
        for img in files:
            os.remove(f'data\\screenshots\\{img}')
        db.close()
        mainPage.startPage()

    # show options when No is selected for late game
    def drop():
        rotate.place(x=130, y=330)
        rotateYCheck.place(x=375, y=330)
        rotateNCheck.place(x=475, y=330)
        labRY.place(x=395, y=333)
        labRN.place(x=495, y=333)
        height.place(x=130, y=370)
        heightYCheck.place(x=375, y=370)
        heightNCheck.place(x=475, y=370)
        labHY.place(x=395, y=373)
        labHN.place(x=495, y=373)
        sumBox.configure(height=3, width=38)
        summary.place(x=25, y=440)
        sumBox.place(x=130, y=420)

    # removes options when No is selected for late game
    def remove():
        rotate.place(x=95, y=-200)
        rotateYCheck.place(x=375, y=-200)
        rotateNCheck.place(x=475, y=-200)
        height.place(x=95, y=-200)
        heightYCheck.place(x=375, y=-200)
        heightNCheck.place(x=475, y=-200)
        sumBox.configure(height=6, width=38)
        summary.place(x=25, y=390)
        sumBox.place(x=130, y=340)

    # text 'Summarize your text' disappears on click here
    def active(*args):
        sumBox.delete('1.0', END)
        sumBox.configure(fg='black')

    # just getting current date and time
    time = datetime.now()
    currentTime = time.strftime('%H:%M')
    today = date.today()
    currentDate = today.strftime('%d-%b-%Y')

    # from here the design of window starts
    global new
    new = Tk()
    new.title('New Session')
    width, height = 650, 650
    s_width = new.winfo_screenwidth()
    s_height = new.winfo_screenheight()
    x = (s_width / 2) - (width / 2)
    y = (s_height / 2) - (height / 2)
    new.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    new.resizable(0, 0)

    new.iconbitmap('resources\\fortnite.ico')

    # background image here
    real1 = Image.open('resources\\newSessionBg.jpg')
    img1 = ImageTk.PhotoImage(real1)
    Label(new, image=img1).place(x=-100, y=-10)

    # session Name label here
    Tables = ()
    for Tables in cursor.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table'"):
        pass
    sessionName = Label(new, text='', font=('Times New Roman', 20, 'bold'), bd=4, relief=RAISED, bg='#333', fg='#F5F5F5', justify=CENTER)

    # current date and time implementation here
    timeEntry = Entry(new, font=('Times New Roman', 14, 'bold'), width=16, bg='#333', fg='#F5F5F5', justify=CENTER)
    timeEntry.insert(0, f'{currentTime}/{currentDate}')
    timeEntry.place(x=6, y=6)

    # Screenshots button here
    scrnshot = Button(new, text='Screenshots', bg='#333', fg='#F5F5F5', bd=4, relief=RAISED, width=10, height=1, font=('Times New Roman', 11, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=view)
    scrnshot.place(x=540, y=5)

    # mainFrame here
    mainFrame = Frame(new, bg='#333', width=610, height=520, pady=3, bd=4, relief=RAISED)

    # Mode Label here
    modeLabel = Label(mainFrame, text='', font=('Times New Roman', 20, 'bold'), bg='#333', fg='#F5F5F5')

    # game label and entry here
    gameLabel = Label(mainFrame, text=f'Game {count() + 1}:', font=('Times New Roman', 12, 'bold'), bg='#333', fg='#F5F5F5')
    gameEntry = int(count() + 1)

    # Placement label and entry here
    placement = Label(mainFrame, text='Placement:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    placeEntry = Entry(mainFrame,  font=('Times New Roman', 16, 'bold'), width=5, bg='#A9a9a9', fg='#333', justify=CENTER)
    placeEntry.insert(0, '0')

    # Eliminations label and entry here
    elimLabel = Label(mainFrame, text='Eliminations:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    elimEntry = Entry(mainFrame, font=('Times New Roman', 16, 'bold'),  width=5, bg='#A9a9a9', fg='#333', justify=CENTER)
    elimEntry.insert(0, '0')

    # Accuracy label and entry here
    accuracy = Label(mainFrame, text='Accuracy:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    acc = Entry(mainFrame, font=('Times New Roman', 16, 'bold'), width=5, bg='#A9a9a9', fg='#333', justify=CENTER)
    acc.insert(0, '0')

    # Time Survived label and entry here
    tSurvived = Label(mainFrame, text='Minutes Survived:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    tSEntry = Entry(mainFrame, font=('Times New Roman', 16, 'bold'), width=5, bg='#A9a9a9', fg='#333', justify=CENTER)
    tSEntry.insert(0, '0')

    # Damage Dealt label and Entry here
    Dealt = Label(mainFrame, text='Damage Dealt to Players:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    damageDealt = Entry(mainFrame, font=('Times New Roman', 16, 'bold'), width=5, bg='#A9a9a9', fg='#333', justify=CENTER)
    damageDealt.insert(0, '0')

    # Damage Taken label and entry here
    Taken = Label(mainFrame, text='Damage Taken:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    damageTaken = Entry(mainFrame, font=('Times New Roman', 16, 'bold'), width=5, bg='#A9a9a9', fg='#333', justify=CENTER)
    damageTaken.insert(0, '0')

    # Materials used label and entry here
    matUsed = Label(mainFrame, text='Materials Used:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    matUEntry = Entry(mainFrame, font=('Times New Roman', 16, 'bold'), width=5, bg='#A9a9a9', fg='#333', justify=CENTER)
    matUEntry.insert(0, '0')

    # Materials gathered label and entry here
    materials = Label(mainFrame, text='Materials Gathered:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    matEntry = Entry(mainFrame, font=('Times New Roman', 16, 'bold'), width=5, bg='#A9a9a9', fg='#333', justify=CENTER)
    matEntry.insert(0, '0')
    matEntry.bind('<Tab>', active)

    # Late Game checkbox and label
    late = Label(mainFrame, text='Did you make it to Late Game?', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    lateValue = IntVar()
    lateYCheck = Radiobutton(mainFrame, text='', variable=lateValue, value=1, command=drop, bg='#333', activebackground='#333', font=('Times New Roman', 16, 'bold'))
    lateNCheck = Radiobutton(mainFrame, text='', variable=lateValue, value=2, command=remove, bg='#333', activebackground='#333', font=('Times New Roman', 16, 'bold'))
    labLY = Label(mainFrame, text='Yes', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    labLN = Label(mainFrame, text='No', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')

    # Rotate checkbox and label here
    rotate = Label(mainFrame, text='How did you rotate?', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    rotateValue = IntVar()
    rotateYCheck = Radiobutton(mainFrame, text='', variable=rotateValue, value=1, bg='#333', activebackground='#333', font=('Times New Roman', 16, 'bold'))
    rotateNCheck = Radiobutton(mainFrame, text='', variable=rotateValue, value=2, bg='#333', activebackground='#333', font=('Times New Roman', 16, 'bold'))
    labRY = Label(mainFrame, text='Early', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    labRN = Label(mainFrame, text='Late', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')

    # Height checkbox and label here
    height = Label(mainFrame, text='Was height free?', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    heightValue = IntVar()
    heightYCheck = Radiobutton(mainFrame, text='', variable=heightValue, value=1, bg='#333', activebackground='#333', font=('Times New Roman', 16, 'bold'))
    heightNCheck = Radiobutton(mainFrame, text='', variable=heightValue, value=2, bg='#333', activebackground='#333', font=('Times New Roman', 16, 'bold'))
    labHY = Label(mainFrame, text='Yes', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    labHN = Label(mainFrame, text='No', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')

    # which weapon did you died with
    wepLabel = Label(mainFrame, text='Which weapon did you die to?', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    variable1 = StringVar(mainFrame)
    variable1.set('choose')
    weapon = OptionMenu(mainFrame, variable1, *weapon_list())

    # Summary Here
    summary = Label(mainFrame, text='Summary:', font=('Times New Roman', 16, 'bold'), bg='#333', fg='#F5F5F5')
    sumBox = ScrolledText(mainFrame, height=3, wrap=WORD, width=31, font=('Times New Roman', 16, 'bold'), bg='#A9a9a9', fg='#ECECEC')
    sumBox.insert(INSERT, 'Summarize Your Death...')
    sumBox.bind('<Button-1>', active)

    # Warning Label Goes here
    warning = Label(mainFrame, text='', font=('Times New Roman', 14), width=55, bg='#333', fg='#F5F5F5', justify=CENTER)

    # Submit button Goes here
    submit = Button(new, text='Next', bg='#333', fg='#F5F5F5', bd=4, relief=RAISED, width=10, height=1,font=('Times New Roman', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2')

    # back button here
    back = Button(new, text='Back', bg='#333', fg='#F5F5F5', bd=4, relief=RAISED, width=10, height=1,font=('Times New Roman', 14, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=back)

    # changing the text of back button here
    file = open('data\\deletionRecord.txt', 'r')
    h = file.readline()
    if a == 0:
        session = f'{Tables[0] + len(h) + 1}'
    else:
        session = f'{Tables[0] + len(h)}'
        back.configure(text='Save & Back', width=12)

    # placing everything of casual mode here
    if mode == 1:
        submit.configure(command=submitCasual)
        sessionName.configure(text=f'Session_{session}_Casual')
        sessionName.place(x=210, y=10)
        modeLabel.configure(text='Casual Mode', padx=15)
        modeLabel.place(x=215, y=10)
        gameLabel.place(x=45, y=15)
        placement.place(x=45, y=65)
        placeEntry.place(x=455, y=67)
        elimLabel.place(x=45, y=105)
        elimEntry.place(x=455, y=107)
        accuracy.place(x=45, y=145)
        acc.place(x=455, y=147)
        Dealt.place(x=45, y=185)
        damageDealt.place(x=455, y=187)
        Taken.place(x=45, y=225)
        damageTaken.place(x=455, y=227)
        matUsed.place(x=45, y=265)
        matUEntry.place(x=455, y=267)
        materials.place(x=45, y=305)
        matEntry.place(x=455, y=307)
        wepLabel.place(x=45, y=345)
        weapon.place(x=432, y=345)
        summary.place(x=45, y=410)
        sumBox.place(x=150, y=390)
        submit.place(x=507, y=590)
        back.place(x=20, y=590)
        warning.place(x=20, y=475)
        mainFrame.place(x=20, y=60)

    # placing everything of compitative mode here
    elif mode == 2:
        new.geometry('650x680')
        sessionName.configure(text=f'Session_{session}_Compi')
        sessionName.place(x=210, y=10)
        mainFrame.configure(height=550, width=610)
        submit.configure(command=submitCompe)
        modeLabel.configure(text='Competitive Mode', padx=15)
        modeLabel.place(x=177, y=10)
        gameLabel.place(x=25, y=15)
        placement.place(x=25, y=75)
        placeEntry.place(x=225, y=77)
        elimLabel.place(x=315, y=75)
        elimEntry.place(x=515, y=77)
        Dealt.configure(text='Damage Dealt:')
        Dealt.place(x=25, y=120)
        damageDealt.place(x=225, y=122)
        Taken.place(x=315, y=120)
        damageTaken.place(x=515, y=122)
        matUsed.place(x=25, y=165)
        matUEntry.place(x=225, y=167)
        materials.place(x=315, y=165)
        matEntry.place(x=515, y=167)
        accuracy.place(x=25, y=210)
        acc.place(x=225, y=212)
        tSurvived.place(x=315, y=210)
        tSEntry.place(x=515, y=212)
        wepLabel.place(x=25, y=250)
        weapon.place(x=315, y=253)
        late.place(x=25, y=290)
        lateYCheck.place(x=325, y=290)
        lateNCheck.place(x=415, y=290)
        labLY.place(x=345, y=293)
        labLN.place(x=435, y=293)
        submit.place(x=502, y=620)
        back.place(x=20, y=620)
        warning.place(x=20, y=505)
        sumBox.configure(height=6, width=38)
        summary.place(x=25, y=390)
        sumBox.place(x=130, y=340)
        mainFrame.place(x=20, y=60)

    new.mainloop()
