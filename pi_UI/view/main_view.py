from tkinter import *
from view.main_view_btn import middle_ctr
from terminal.command_translate import Execute
from tkinter import ttk
from view.nodemcu_ctr_view import start_nodemcu_ctr_main_view

main_root_tk = Tk()
main_window_x = 1000
main_window_y = 600
execute = Execute(r"terminal/host.ini")


class MainView(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.label_select = dict()
        self.label_select["控制命令"] = None
        self.label_select["软件说明"] = None

        self.label_btn = list()
        self.label_select_func = dict()
        self.label_select_func["控制命令"] = self.middle_button
        self.label_select_func["软件说明"] = self.help

        self.form_data = dict()

        # self.label_select["控制命令"] = self.middle_ctr_button_canvas()
        self.x, self.y = 0, 0
        self.window_size = str(main_window_x) + "x" + str(main_window_y)
        self.control_btn()
        self.top_label()

        self.v = IntVar()
        self.select_area_init()
        self.select_area_repaint()

        self.middle_label_init()
        self.bottom_cmd()

    def help(self):
        self.middle_area.delete("all")
        middle = Canvas(self.middle_area, width=1000, height=250, bg="#FFFFFF", highlightthickness=0)
        middle.grid(row=0)
        text = '本软件为本科毕业设计软件\n请在控制命令选项卡中点击自己需要的功能，或者输入控制台命令\n'
        middle.create_text(370, 50, text=text, fill="#111111", font="Times 18")

        text = '作者：张靖祥，中国农业大学，计算机172班\n邮箱：1967527237@qq.com\n'
        middle.create_text(180, 100, text=text, fill="#111111", font="Times 12")

    def bottom_cmd(self):

        bottom = Canvas(self, width=1000, height=10, bg="#FFFFFF", highlightthickness=0)
        bottom.grid(row=4)

        scroll = Scrollbar(background="black")

        cmd_text = Text(bottom, bd="1", font="Times 12", height=8, width=124, bg="Black", fg="White",
                        highlightthickness=1, insertbackground="White", yscrollcommand=scroll.set)

        cmd_text.insert(INSERT, 'press help button to get more information\n\n>>')
        cmd_text.configure(state=DISABLED)
        # uid_text.bind("<Return>", lambda evemt: self.login_btn_press())
        cmd_text.grid(row=0)
        self.scroll = scroll
        self.cmd_text = cmd_text

    def middle_label_init(self):
        middle = Canvas(self, width=1000, height=250, bg="#FFFFFF", highlightthickness=0)
        middle.grid(row=3, column=0)
        self.middle_area = middle
        self.middle_button()

    def middle_button(self):
        self.middle_area.delete("all")
        middle_temp = Canvas(self.middle_area, width=1000, height=250, bg="#FFFFFF", highlightthickness=0)
        middle_temp.grid(row=0)

        middle = Canvas(self.middle_area, width=1000, height=250, bg="#FFFFFF", highlightthickness=0)
        middle.grid(row=0)

        help_btn = Button(middle, bd=0, bg="#007DFA", height=2, width=20,
                          text="帮助", anchor='center', font="20", fg="White",
                          activebackground="#007DFA", activeforeground="White",
                          command=lambda x=0: self.cmd_line_input("help"))
        help_btn.bind("<Enter>", lambda event: help_btn.configure(bg="#228EFB"))
        help_btn.bind("<Leave>", lambda event: help_btn.configure(bg="#007DFA"))
        help_btn.grid(row=0, column=0)

        show_btn = Button(middle, bd=0, bg="#007DFA", height=2, width=20,
                          text="展示全部数据", anchor='center', font="20", fg="White",
                          activebackground="#007DFA", activeforeground="White",
                          command=lambda x=0: self.cmd_line_input("show -all"))
        show_btn.bind("<Enter>", lambda event: show_btn.configure(bg="#228EFB"))
        show_btn.bind("<Leave>", lambda event: show_btn.configure(bg="#007DFA"))
        show_btn.grid(row=0, column=1)

        show_btn = Button(middle, bd=0, bg="#007DFA", height=2, width=20,
                          text="设置NodeMCU", anchor='center', font="20", fg="White",
                          activebackground="#007DFA", activeforeground="White",
                          command=lambda x=0: self.cmd_line_input("node get all"))
        show_btn.bind("<Enter>", lambda event: show_btn.configure(bg="#228EFB"))
        show_btn.bind("<Leave>", lambda event: show_btn.configure(bg="#007DFA"))
        show_btn.grid(row=0, column=2)

        cmd_text = Label(middle, text="控制命令：", width=5, height=2, justify='left',
                         font="Times 16", fg='#111111', bg='White', padx=20, pady=10)
        cmd_text.grid(row=3, column=0)

        self.cmd_entry = Entry(middle, bd="1", font="20", width=23,
                               highlightthickness=1, highlightcolor="#007DFA")
        self.cmd_entry.bind("<Return>", lambda evemt: self.cmd_line_input())
        self.cmd_entry.grid(row=3, column=1, ipady=9)
        self.cmd_entry.focus()

        cmd_btn = Button(middle, bd=0, bg="#007DFA", height=2, width=10,
                         text="执行", anchor='center', font="Times 12", fg="White",
                         activebackground="#007DFA", activeforeground="White",
                         command=self.cmd_line_input)
        cmd_btn.bind("<Enter>", lambda event: cmd_btn.configure(bg="#228EFB"))
        cmd_btn.bind("<Leave>", lambda event: cmd_btn.configure(bg="#007DFA"))
        cmd_btn.grid(row=3, column=2)

    def cmd_line_input(self, cmd=None):
        if cmd == None:
            cmd = self.cmd_entry.get().strip()
            if cmd == "":
                self.cmd_text.configure(state=NORMAL)
                self.cmd_text.insert(INSERT, "\n>>")
                self.cmd_text.configure(state=DISABLED)
                return
        stdout_new = open('temp.txt', 'w')
        stdout_old = sys.stdout
        sys.stdout = stdout_new
        try:
            result = execute.execute(cmd)
            sys.stdout = stdout_old
            stdout_new.close()
            stdout_new = open('temp.txt', 'r')
            if result == 0:
                self.cmd_text.configure(state=NORMAL)
                self.cmd_text.insert(INSERT, cmd + "\n")
                self.cmd_text.insert(INSERT, str("this function can not execute in this area"))
                self.cmd_text.insert(INSERT, "\n>>")
                self.cmd_text.configure(state=DISABLED)
                self.cmd_text.see(END)
            else:
                lines = stdout_new.readlines()
                if len(lines) == 0:
                    self.cmd_text.configure(state=NORMAL)
                    self.cmd_text.insert(INSERT, cmd + "\n")
                    self.cmd_text.insert(INSERT, "\n>>")
                    self.cmd_text.configure(state=DISABLED)
                    self.cmd_text.see(END)
                    return

                if lines[0].startswith("@formtype"):
                    msg = "".join(lines[1:])
                    head = lines[1].split()
                    form = []
                    for line in lines[2:]:
                        form.append(line.split())
                    self.show_form(lines[0].split()[1], head, form)
                elif lines[0].startswith("@nodemcu"):
                    msg = "".join(lines[1:])

                else:
                    msg = "".join(lines)
                self.cmd_text.configure(state=NORMAL)
                self.cmd_text.insert(INSERT, cmd + "\n")
                self.cmd_text.insert(INSERT, msg)
                self.cmd_text.insert(INSERT, "\n>>")
                self.cmd_text.configure(state=DISABLED)
                self.cmd_text.see(END)
                if lines[0].startswith("@nodemcu"):
                    start_nodemcu_ctr_main_view(lines[1:],self)
        except BaseException as e:
            sys.stdout = stdout_old
            stdout_new.close()
            self.cmd_text.configure(state=NORMAL)
            self.cmd_text.insert(INSERT, cmd + "\n")
            self.cmd_text.insert(INSERT, str(e))
            self.cmd_text.insert(INSERT, "\n>>")
            self.cmd_text.configure(state=DISABLED)
            self.cmd_text.see(END)
        pass

    def show_form(self, title, head, form):
        self.form_data["form"] = [title, head, form]
        self.label_select["form"] = None
        self.select_area_repaint()
        self.label_select_func["form"] = self.show_form_paint
        self.v.set(len(self.label_btn) - 1)
        self.show_form_paint()
        pass

    def show_form_paint(self):
        self.middle_area.delete("all")
        middle_temp = Canvas(self.middle_area, width=1000, height=250, bg="#FFFFFF", highlightthickness=0)
        middle_temp.grid(row=0)

        middle = Canvas(self.middle_area, width=1000, height=250, bg="#FFFFFF", highlightthickness=0)
        middle.grid(row=0)
        title, head, form = self.form_data["form"]

        head_text = Label(middle, text=str(title), width=5, height=1, justify='left',
                          font="Times 16", fg='#111111', bg='White', padx=20, pady=10)
        head_text.grid(row=0, column=0)

        head_btn = Label(middle, text="关闭", width=3, height=1, justify='left',
                         font="Times 16", fg='White', bg='red', padx=20, pady=10)
        head_btn.grid(row=0, column=1)
        head_btn.bind("<Enter>", lambda event: head_btn.configure(bg="pink"))
        head_btn.bind("<Leave>", lambda event: head_btn.configure(bg="red"))
        head_btn.bind("<Button-1>", lambda event: self.close_form())

        tree = ttk.Treeview(middle,height=8)
        tree["columns"] = head
        for name in head:
            tree.column(name, width=100)
            tree.heading(name, text=name)
        for i, line in enumerate(form):
            tree.insert("", 3, text=str(i), values=line)
        tree.grid(row=1, column=0, columnspan=2)
        pass

    def close_form(self):
        self.form_data.pop("form")
        self.label_select.pop("form")
        self.label_select_func.pop("form")
        self.select_area_repaint()
        self.middle_button()
        self.v.set(0)
        pass

    def select_area_repaint(self):
        for btn in self.label_btn:
            btn.destroy()
        self.label_btn.clear()
        self.select_area_canvas.delete("all")
        times = 0
        for key in self.label_select.keys():
            b = Radiobutton(self.select_area_canvas, text=key, variable=self.v, value=times,
                            indicatoron=False, bg="#007DFA", fg="White", activebackground="#007DFA",
                            activeforeground="White", borderwidth=0, cursor="dot", height=2,
                            width=8, font="Times 12", selectcolor="#44A0FB", relief="flat",
                            command=self.select_area_click)
            b.grid(row=0, column=times)
            self.label_btn.append(b)
            times += 1

        b = Radiobutton(self.select_area_canvas, text="", variable=self.v, value=100, indicatoron=False,
                        bg="#007DFA", fg="#007DFA", activebackground="#007DFA", activeforeground="#007DFA",
                        borderwidth=0, height=2, width=105 - 15 * len(self.label_select.keys()), font="Times 12",
                        selectcolor="#007DFA", relief="flat", state="disable")
        b.grid(row=0, column=10)

    def select_area_init(self):
        select = Canvas(self, width=1000, height=50, bg="#007DFA", highlightthickness=0)
        select.grid(row=2, column=0)
        self.select_area_canvas = select

    def select_area_click(self):
        value = self.v.get()
        name = list(self.label_select.keys())[value]
        self.label_select_func[name]()
        pass

    def top_label(self):
        top = Canvas(self, width=1000, height=80, bg="#007DFA", highlightthickness=0)
        top.grid(row=1, column=0)
        top.bind("<Button-1>", self.get_point)
        top.bind("<B1-Motion>", self.drag_move)

        top_margin = Canvas(top, width=1000, height=1, bg="#007DFA", highlightthickness=0)
        top_margin.grid(row=0)
        top_margin.bind("<Button-1>", self.get_point)
        top_margin.bind("<B1-Motion>", self.drag_move)

        middle = Canvas(top, width=1000, height=50, bg="#007DFA", highlightthickness=0)
        middle.grid(row=1)

        logo = Canvas(middle, bg='white', height=50, width=50, highlightthickness=0)
        logo.background = PhotoImage(file='asset/image/image3.png')
        logo.create_image(25, 25, image=logo.background)
        logo.grid(row=0, column=0, rowspan=2)
        logo.bind("<Button-1>", self.get_point)
        logo.bind("<B1-Motion>", self.drag_move)

        label = Canvas(middle, width=360, height=35, bg="#007DFA", highlightthickness=0)
        label.grid(row=0, column=1)
        label.create_text(140, 17, text='MQTT客户端 — 张靖祥', fill="White", font="Times 18")
        label.bind("<Button-1>", self.get_point)
        label.bind("<B1-Motion>", self.drag_move)

        label = Canvas(middle, width=360, height=15, bg="#007DFA", highlightthickness=0)
        label.grid(row=1, column=1)
        label.create_text(50, 7, text='毕业设计祥', fill="#88AADD", font="Times 10")
        label.bind("<Button-1>", self.get_point)
        label.bind("<B1-Motion>", self.drag_move)

        bottom_margin = Canvas(top, width=1000, height=20, bg="#007DFA", highlightthickness=0)
        bottom_margin.grid(row=2)
        bottom_margin.bind("<Button-1>", self.get_point)
        bottom_margin.bind("<B1-Motion>", self.drag_move)
        bottom_margin.create_line(0, 18, 1000, 18, fill="#88AADD")

    def control_btn(self):
        ctr = Canvas(self, width=1000, height=40)
        ctr.configure(width=360, height=40)
        ctr.grid(row=0)

        blank = Canvas(ctr)
        blank.configure(width=970, height=40, bg="#007DFA", highlightthickness=0)
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
        close_btn.bind("<ButtonRelease-1>", lambda event: main_root_tk.destroy()
        if event.x > 0 and event.x < 30 and event.y > 0 and event.y < 40 else True)

    def drag_move(self, event):
        new_x = (event.x - self.x) + main_root_tk.winfo_x()
        new_y = (event.y - self.y) + main_root_tk.winfo_y()
        s = f"{self.window_size}+{new_x}+{new_y}"
        main_root_tk.geometry(s)

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


def start_main_view():
    global main_root_tk
    set_center(main_root_tk, main_window_x, main_window_y)
    main_root_tk.resizable(width=False, height=False)
    main_root_tk.title("MQTT登录")

    loginFrame = MainView(master=main_root_tk).pack()

    # main_root_tk.overrideredirect(1)
    # main_root_tk.attributes('-topmost', 1)
    main_root_tk.mainloop()


if __name__ == "__main__":
    start_main_view()
