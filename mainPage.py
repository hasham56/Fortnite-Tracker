from newSession import *
from yourSessions import *
from bs4 import BeautifulSoup
import urllib.request
import requests

# main function for mainPage
def startPage():
    # destroying main window before opening newSession
    def pre1():
        if button['text'] == 'Casual':
            window.destroy()
            newSession(1, 0, 0)
        else:
            window.destroy()
            newSession(2, 0, 0)

    # destroying main window before opening yourSessions
    def pre2():
        try:
            window.destroy()
        except:
            pass
        yourSessions()

    # user name Tag disappear when clicked on entry
    def active(*args):
        nameEntry.delete(0, 'end')
        nameEntry.configure(fg='black')

    # function for saving username and showing other content
    def save(*args):
        name = nameEntry.get()
        file = open('resources\\user.txt', 'w')
        file.write(name)
        file.close()
        Hide.destroy()
        Label(window, text=f'Welcome {name}!', font=('Times New Roman', 24, 'bold'), width=40, bg='#333', fg='#fff').pack()
        button.place(x=255, y=310)
        newS.place(x=50, y=420)
        yourS.place(x=300, y=420)

    # checking internet connection and updating weapons list
    def update():
        try:
            urllib.request.urlopen('http://216.58.192.142', timeout=1)
            if update['text'] == 'Update':
                weapons_url = 'https://db.fortnitetracker.com/weapons'
                weapons_page = requests.get(weapons_url)
                soup = BeautifulSoup(weapons_page.content, 'html.parser')
                weapons = []
                for weapon in soup.find_all('h3', class_="trn-card__header-title"):
                    weapon_title = weapon.text
                    weapons.append(weapon_title)
                    weapons.sort()
                file1 = open('resources\\weapons.txt', 'w')
                file1.write('None\n')
                file1.close()
                file1 = open('resources\\weapons.txt', 'a')
                for s in weapons:
                    file1.write(f'{s}\n')
                file1.close()
                update.configure(text='Updated', state=DISABLED)
                hint.configure(text='Done Updating!')
        except:
            hint.configure(text='No Internet Connection!')

    # function for changing the text of button Casual & Compitative
    def change():
        if button['text'] == 'Casual':
            button.configure(text='Competitive')
        else:
            button.configure(text='Casual')

    # function for changing username
    def change1():
        # on pressing enter this will renew the username
        def enter(*args):
            data = changeEntry.get()
            title.configure(text=f'Welcome Back {data}!')
            changeEntry.destroy()
            file = open('resources\\user.txt', 'w')
            file.write(data)
            file.close()
            change.configure(text='Change', command=change1)

        change.configure(text='OK', command=enter)
        changeEntry = Entry(window, font=('Times New Roman', 16, 'bold'), width=50, bg='powder blue', fg='#333',
                            justify=CENTER)
        changeEntry.bind('<Return>', enter)
        changeEntry.place(x=0, y=10)

    # Main starts here
    # it will destroy any window that has been opened before pressing back
    try:
        try:
            newDestroy()
        except:
            yourDestroy()
    except:
        pass

    # window design starts here
    global window
    window = Tk()
    window.title('Fortnite Tracker')
    # next lines only centralize the window
    width, height = 550, 550
    s_width = window.winfo_screenwidth()
    s_height = window.winfo_screenheight()
    x = (s_width / 2) - (width / 2)
    y = (s_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    window.resizable(0, 0)

    #window icon
    window.iconbitmap('resources\\fortnite.ico')

    # background image
    real = Image.open('resources\\mainPageBg.jpg')
    img = ImageTk.PhotoImage(real)
    Label(window, image=img).place(x=-40, y=-10)

    # all the buttons and labels of main screen
    title = Label(window, text='', font=('Times New Roman', 24, 'bold'), width=40, bg='#333',fg='#fff')
    button = Button(window, text='Casual', bg='#333', fg='#fff', bd=6, relief=RAISED, width=12, height=1, font=('Times New Roman', 19, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=change)
    newS = Button(window, text='New Session', bg='#333', fg='#fff', bd=6, relief=RAISED, width=12, height=1, font=('Times New Roman', 19, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=pre1)
    yourS = Button(window, text='Your Sessions', bg='#333', fg='#fff', bd=6, relief=RAISED, width=12, height=1, font=('Times New Roman', 19, 'bold'), activebackground='#737373', activeforeground='#f2f2f2', command=pre2)
    change = Button(window, text='Change', bg='#333', fg='#fff', bd=1, width=7, height=1, font=('Times New Roman', 9), activebackground='#737373', activeforeground='#f2f2f2', command=change1)
    update = Button(window, text='Update', bg='#333', fg='#fff', bd=1, width=7, height=1, font=('Times New Roman', 9), activebackground='#737373', activeforeground='#f2f2f2', command=update)
    hint = Label(window, text='If you are having issues with new stuff, click Update!', font=('Times New Roman', 16), width=46, bg='#333',fg='#fff', justify=CENTER)
    Hide = Frame(window, width=380, height=100, bg='#333', bd=4, relief=RAISED)

    # Real Main Function
    # taking username from text file
    file = open('resources\\user.txt', 'r')
    username = file.readline()
    file.close()

    # placing everythong in window here
    if username == '' or username == ' ':
        nameEntry = Entry(Hide, font=('Times New Roman', 25, 'bold'), width=15, bg='powder blue', fg='grey', justify=CENTER)
        nameEntry.insert(0, 'Username')
        nameEntry.bind('<Button-1>', active)
        nameEntry.bind('<Return>', save)
        nameEntry.place(x=53, y=25)
        Hide.place(x=80, y=270)
    else:
        title.configure(text=f'Welcome Back {username}!')
        title.pack()
        button.place(x=255, y=310)
        newS.place(x=50, y=420)
        yourS.place(x=300, y=420)
        change.place(x=495, y=42)
        update.place(x=0, y=42)
        hint.place(x=0, y=520)

    window.mainloop()
