#Menu
#creating a menu
menu = Menu(root)
#configure the menu
root.config(menu=menu)

subMenu = Menu(root)                                           #its the first level of the bar
menu.add_cascade(label="file", menu=subMenu) #adding to the main
subMenu.add_command(label="Now Project....", command=doNothing) #add the sub menus
subMenu.add_command(label="New", command=doNothing)
subMenu.add_separator()                               #creates a saparators
subMenu.add_command(label="Exit", command=doNothing)

from tkinter import *
import tkinter.messagebox


root = Tk()
canvas = Canvas(root, width=200,height=100)
canvas.pack()

blackLine = canvas.create_line(0,0,200,50)#x,y
redLine = canvas.create_line(0,100,200,50, fill="red")

greenBox = canvas.create_rectangle(25,25,130,60, fill="green")

#delete the object
canvas.delete(redline)
canvas.delete(ALL)

root.mainloop()

root = Tk()

tkinter.messagebox.showinfo("Window Title","Monkey can live up to 300 years")# create a alert box
answer = tkinter.messagebox.askquestion("Question 1","Do you like silly faces?")# create a yes or no box
if answer == "yes" :
    print("8===D")
root.mainloop()

def doNothing():
    print("ok ok I won't....")



root = Tk()

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(root)
menu.add_cascade(label="file", menu=subMenu)
subMenu.add_command(label="Now Project....", command=doNothing)
subMenu.add_command(label="New", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

editMenu = Menu(root)
menu.add_cascade(label="edit", menu=editMenu)
editMenu.add_command(label="Now.", command=doNothing)

toolbar = Frame(root, bg="blue")

insertBu = Button(toolbar, text = "Insert Image", command= doNothing)
insertBu.pack(side=LEFT,padx=2, pady=2)
printbut = Button(toolbar, text = "Print", command = doNothing)
printbut.pack(side=LEFT,padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

#create a status bar
status = Label(root, text="Preparing to do nothing",bd=1,relief=SUNKEN,anchor=W)#creating a status bar
status.pack(side=BOTTOM, fill=X) #to fill up the page

root.mainloop()

class BuckysButtons:

    def __init__(self, master):
        frame = Frame(master,width=200,height=300)
        frame.pack()

        self.printButton = Button(frame, text="Print Message", command=self.printMessage)
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(frame, text="Quit", command= frame.quit)
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print("Wow, this actually worked!")




root =Tk()
b = BuckysButtons(root)
root.mainloop()


root = Tk()

def printName(event):
    print("Chello my name is Buky!")

#button_1 = Button(root, text='Print my name',command=printName)#binding a function
button_1 = Button(root, text='Print my name')
button_1.bind("<Button-1>",printName)

button_1.pack()

root.mainloop()

from tkinter import *

root = Tk()

label_1 = Label(root,text="Name")
label_2 =Label(root,text="Password")

entry_1 = Entry(root)
entry_2 = Entry(root)

label_1.grid(row=0, sticky=E)#sticy to adjust to right
label_2.grid(row=1, sticky=E)

entry_1.grid(row=0,column=1)
entry_2.grid(row=1,column=1)

c = Checkbutton(root, text="Keep me logged in")
c.grid(columnspan=2)#columnspan to merge columns

root.mainloop()


from tkinter import *

root = Tk()

one = Label(root, text="one", bg="red", fg="white")
one.pack()

two = Label(root,text="Two",bg="green",fg="black")
two.pack(fill=X)  #fill the page

three = Label(root, text="three", bg="blue", fg="white")
three.pack(side=LEFT,fill=Y)

root.mainloop()


from tkinter import *

root = Tk()

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

button1 = Button(topFrame, text="Button 1",fg="red")
button2 = Button(topFrame, text="Button 2",fg="blue")
button3 = Button(topFrame, text="Button 3",fg="green")
button4 = Button(bottomFrame, text="Button 4",fg="purple")

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)

root.mainloop()

#to access the element in tkinker entry
entry_obj.get()





