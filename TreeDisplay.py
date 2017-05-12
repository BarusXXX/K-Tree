from NodeClass import *
import time
from tkinter import messagebox

def _create_circle(self, x, y, r, *args, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
Canvas.create_circle = _create_circle

def doNothing():
    print("Did abs nothin")

# ****** Help System  ******

class ProgramInfo():

    def About(self):
        messagebox.showinfo('About',
        '\n'+
        'D3\n'+
        '\n'+
        'Author:                           BarusXXX\n'+
        'Version:                                    v0.1\n'+
        'Date:                            20/04/2017\n'+
        'Licence:                         linktolicence' +
        '\n'
        )
    def Help(self):
        print('Help Documentation')
GlobalInfo = ProgramInfo()

root = Tk()

root.iconbitmap("\\icon\\Tree.ico")


menu = Menu(root)
root.config(menu=menu)
root.wm_title("Tree View")
PreferencesSubMenu=Menu()
fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label='New Search', command=doNothing)
fileMenu.add_command(label='Save Search', command=doNothing)
fileMenu.add_command(label='Save Images', command=doNothing)
fileMenu.add_separator()
fileMenu.add_cascade(label='Preferences', menu=PreferencesSubMenu)
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command=root.quit)
PreferencesSubMenu.add_command(label='Startup Windowed/Fullscreen',command=doNothing)
os.chdir('C:\\Users\\Kane\\OneDrive\\Documents\\00_Kane\\02_Research\\Mepa_ObliqueFetchTool_HOL')
editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label='Load Malta Map', command=lambda: doNothing)
editMenu.add_command(label='Load Gozo Map', command=lambda: doNothing)
editMenu.add_separator()
editMenu.add_command(label='Find', command=doNothing)

HelpMenu = Menu(menu)
#menu.add_cascade(label="Help", menu=HelpMenu)
HelpMenu.add_command(label='About', command=lambda: GlobalInfo.About())
canvas = Canvas(root, width=canvasx, height=canvasy)
canvas.grid()


def NewTree():
    global MasterName
    MasterName = ((MasterDir.split("\\"))[-1])
    root.title("D3" + " - " + MasterDir)
    MyTest = NodeCollection(MasterDir, canvas)
    for x in range(0, iterations):
        MyTest.Refresh()
        root.update()
        time.sleep(0.05)
        #print("### Iteration %s ###" %x)

    bindings(canvas, MyTest.Nodes[1:])

NewTree()

root.mainloop()
