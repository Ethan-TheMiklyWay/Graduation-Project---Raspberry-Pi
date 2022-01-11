from tkinter import *
import view_model.login_view_model as model
import variable
import sys

login_root_tk = Tk()
login_window_x = 360
login_window_y = 440


class LoginView(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.x, self.y = 0, 0
        self.window_size = str(login_window_x) + "x" + str(login_window_y)
        self.control_btn()
        self.top_label()
        self.login_area()

    def login_area(self):
        botton = Canvas(self, width=360, height=300, highlightthickness=0, bg="#FFFFFF")
        botton.grid(row=2, column=0)

        top_margin = Canvas(botton, height=20, width=360, highlightthickness=0, bg="#FFFFFF")
        top_margin.grid(row=0, columnspan=2)

        label = Canvas(botton, height=40, width=80, highlightthickness=0, bg="#FFFFFF")
        label.create_text(40, 20, text="用户名：", fill="#111111", font="20")
        label.grid(row=1, column=0)
        uid_text = Entry(botton, bd="1", font="20", width=23,
                         highlightthickness=1, highlightcolor="#007DFA")
        uid_text.bind("<Return>", lambda evemt: self.login_btn_press())
        uid_text.grid(row=1, column=1, ipady=9)
        uid_text.focus()
        self.uid_text = uid_text

        label = Canvas(botton, height=40, width=80, highlightthickness=0, bg="#FFFFFF")
        label.create_text(40, 20, text="密  码：", fill="#111111", font="18")
        label.grid(row=2, column=0, ipady=9)
        pwd_text = Entry(botton, bd="1", font="20", width=23,
                         highlightthickness=1, highlightcolor="#007DFA")
        pwd_text.grid(row=2, column=1, ipady=9)
        pwd_text.bind("<Return>", lambda evemt: self.login_btn_press())
        self.pwd_text = pwd_text

        middle_margin = Canvas(botton, height=15, width=360, highlightthickness=0, bg="#FFFFFF")
        middle_margin.grid(row=3, columnspan=2)

        login_btn = Button(botton, bd=0, bg="#007DFA", height=2, width=35, text="登  录", anchor='center',
                           font="20", fg="White", activebackground="#007DFA", activeforeground="White",
                           command=self.login_btn_press)
        login_btn.bind("<Enter>", lambda event: login_btn.configure(bg="#228EFB"))
        login_btn.bind("<Leave>", lambda event: login_btn.configure(bg="#007DFA"))
        login_btn.grid(row=4,column=0, columnspan=2)

        msg_text = Canvas(botton, height=40, width=200, highlightthickness=0, bg="#FFFFFF")
        msg_text.create_text(100, 20, text="", fill="red", font="Times 8")
        msg_text.grid(row=5,column=0, columnspan=2)
        self.msg_text = msg_text


    def login_btn_press(self):
        uid = self.uid_text.get()
        pwd = self.pwd_text.get()
        if model.login_test(uid, pwd):
            self.msg_text.delete("all")
            variable.login_state = True
            login_root_tk.destroy()
        else:
            self.msg_text.delete("all")
            self.msg_text.create_text(100, 20, text="用户名或密码错误 ", fill="red", font="8")
        pass

    def top_label(self):
        top = Canvas(self, width=360, height=80, bg="#007DFA", highlightthickness=0)
        top.grid(row=1, column=0)
        top.bind("<Button-1>", self.get_point)
        top.bind("<B1-Motion>", self.drag_move)

        top_margin = Canvas(top, width=360, height=5, bg="#007DFA", highlightthickness=0)
        top_margin.grid(row=0)
        top_margin.bind("<Button-1>", self.get_point)
        top_margin.bind("<B1-Motion>", self.drag_move)

        logo = Canvas(top, bg='white', height=100, width=100, highlightthickness=0)
        logo.background = PhotoImage(file='asset/image/image2.png')
        logo.create_image(50, 50, image=logo.background)
        logo.grid(row=1)
        logo.bind("<Button-1>", self.get_point)
        logo.bind("<B1-Motion>", self.drag_move)

        label = Canvas(top, width=360, height=60, bg="#007DFA", highlightthickness=0)
        label.grid(row=2)
        label.create_text(180, 30, text='MQTT客户端 — 张靖祥', fill="White", font="22")
        label.bind("<Button-1>", self.get_point)
        label.bind("<B1-Motion>", self.drag_move)

    def control_btn(self):
        ctr = Canvas(self, width=360, height=40)
        ctr.configure(width=360, height=40)
        ctr.grid(row=0)

        blank = Canvas(ctr)
        blank.configure(width=330, height=40, bg="#007DFA", highlightthickness=0)
        blank.grid(row=0, column=0)
        blank.bind("<Button-1>", self.get_point)
        blank.bind("<B1-Motion>", self.drag_move)

        close_btn = Canvas(ctr, width=30, height=40, bg="#007DFA", highlightthickness=0)
        close_btn.create_line(10, 15, 20, 25, fill="White")
        close_btn.create_line(20, 15, 10, 25, fill="White")
        close_btn.grid(row=0, column=1)
        close_btn.bind("<Enter>", lambda event: close_btn.configure(bg="#44A0FB"))
        close_btn.bind("<Leave>", lambda event: close_btn.configure(bg="#007DFA"))
        close_btn.bind("<Button-1>", lambda event: close_btn.configure(bg="#228EFB"))
        close_btn.bind("<ButtonRelease-1>", lambda event: login_root_tk.destroy()
        if event.x > 0 and event.x < 30 and event.y > 0 and event.y < 40 else True)


    def drag_move(self, event):
        new_x = (event.x - self.x) + login_root_tk.winfo_x()
        new_y = (event.y - self.y) + login_root_tk.winfo_y()
        s = f"{self.window_size}+{new_x}+{new_y}"
        login_root_tk.geometry(s)

    def get_point(self, event):
        self.x, self.y = event.x, event.y


def set_center(tk, width, heigh):
    sw = tk.winfo_screenwidth()
    sh = tk.winfo_screenheight()
    ww = width
    wh = heigh
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))


def start_login_view():
    global login_root_tk

    set_center(login_root_tk, login_window_x, login_window_y)
    login_root_tk.resizable(width=False, height=False)
    login_root_tk.title("MQTT登录")

    loginFrame = LoginView(master=login_root_tk).pack()

    login_root_tk.overrideredirect(1)
    login_root_tk.attributes('-topmost', 1)
    login_root_tk.mainloop()

