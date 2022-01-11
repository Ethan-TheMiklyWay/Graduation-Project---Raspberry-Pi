from tkinter import *

photo = None


class btn(Button):
    def __init__(self, master):
        Button.__init__(self, master)


class Application(Frame):

    def createWidgets(self):
        GIRLS = [
            ("西施", 1),
            ("王昭君", 2),
            ("貂蝉", 3),
            ("杨玉环", 4)]
        self.v = IntVar()
        self.button = []

        for girl, num in GIRLS:
            b = Radiobutton(self, text=girl, variable=self.v, value=num, indicatoron=False,
                            bg="#007DFA", fg="White", activebackground="#007DFA", activeforeground="White",
                            borderwidth=0, cursor="dot", height=2, width=8, font="Times 12",
                            selectcolor="#44A0FB", relief="flat", command=self.comm)
            self.button.append(b)
            b.pack()
        b.destroy()

    def comm(self):
        print(self.v.get())
        pass

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
root.geometry("300x400+300+300")
root.title("this is a test")
app = Application(master=root)
app.mainloop()
