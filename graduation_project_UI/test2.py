from tkinter import *

from tkinter import ttk
import json
import tkinter.messagebox


class NodemcuCtrMainView(Frame):

    def __init__(self, master, info, main_frame):
        Frame.__init__(self, master)
        self.main_frame = main_frame

        self.top_button()
        self.info = self.tojson(info)
        self.combox()
        self.node_status()
        self.node_mqtt_pub_interview()
        self.wifi_wait_interview()
        self.mqttfinding_wait_interview()

        self.refresh()

        """
        head_btn = Label(self, text="test", width=3, height=1, justify='left',
                         font="Times 16", fg='White', bg='red', padx=20, pady=10)
        head_btn.grid(row=0)
        head_btn.bind("<Enter>", lambda event: head_btn.configure(bg="pink"))
        head_btn.bind("<Leave>", lambda event: head_btn.configure(bg="red"))
        head_btn.bind("<Button-1>", lambda event: 1)

        com = ttk.Combobox(self, state="readonly",font=("宋体",20))

        com.pack()
        com["value"] = ("河北", "河南", "山东")
        com.current(2)
        com.bind("<<ComboboxSelected>>", self.xFunc)
        self.com = com
        """

    def mqttfinding_wait_interview(self):
        cmd_text = Label(self, text="mqtt重连：", width=5, height=2, justify='left',
                         font="Times 16", fg='#111111', padx=20, pady=10)
        cmd_text.grid(row=5, column=0)

        com = ttk.Combobox(self, font=("宋体", 16), width=8)
        com.grid(row=5, column=1)

        namelist = ["5秒", "30秒", "1分钟", "5分钟"]
        com["value"] = namelist
        com.current(0)
        self.node_mqttfinding_wait_interview_value = com

    def wifi_wait_interview(self):
        cmd_text = Label(self, text="WiFi重连：", width=5, height=2, justify='left',
                         font="Times 16", fg='#111111', padx=20, pady=10)
        cmd_text.grid(row=4, column=0)

        com = ttk.Combobox(self, font=("宋体", 16), width=8)
        com.grid(row=4, column=1)

        namelist = ["5秒", "30秒", "1分钟", "5分钟"]
        com["value"] = namelist
        com.current(0)
        self.node_wifi_wait_interview_value = com

    def node_mqtt_pub_interview(self):
        cmd_text = Label(self, text="采集间隔：", width=5, height=2, justify='left',
                         font="Times 16", fg='#111111', padx=20, pady=10)
        cmd_text.grid(row=3, column=0)

        com = ttk.Combobox(self, font=("宋体", 16), width=8)
        com.grid(row=3, column=1)

        namelist = ["5秒", "30秒", "1分钟", "5分钟", "30分钟", "1小时"]
        com["value"] = namelist
        com.current(0)
        self.node_mqtt_pub_interview_value = com

    def node_status(self):
        cmd_text = Label(self, text="设备状态：", width=5, height=2, justify='left',
                         font="Times 16", fg='#111111', padx=20, pady=10)
        cmd_text.grid(row=2, column=0)

        radio_loc = Frame(self)
        radio_loc.grid(row=2, column=1)
        v = IntVar()
        btn_on = Radiobutton(radio_loc, text="开启", variable=v, value=1, font="Times 12")
        btn_on.grid(row=0, column=0)
        btn_off = Radiobutton(radio_loc, text="关闭", variable=v, value=2, font="Times 12")
        btn_off.grid(row=1, column=0)
        self.node_status_value = v

    def tojson(self, info):
        ret = []
        for line in info:
            line = str(line).replace("\'", "\"")
            ret.append(json.loads(line))
        return ret

    def combox(self):
        cmd_text = Label(self, text="设备列表：", width=5, height=2, justify='left',
                         font="Times 16", fg='#111111', padx=20, pady=10)
        cmd_text.grid(row=1, column=0)

        com = ttk.Combobox(self, state="readonly", font=("宋体", 16), width=8)
        com.grid(row=1, column=1)

        namelist = [line["name"] for line in self.info]
        com["value"] = namelist
        if len(namelist) != 0:
            com.current(0)
        com.bind("<<ComboboxSelected>>", lambda x: self.select(com.get()))
        self.node_name = com

    def select(self, value):
        self.refresh()

    def top_button(self):
        close_btn = Button(self, bd=0, bg="red", height=1, width=10,
                           text="关闭", anchor='center', font="15", fg="White",
                           activebackground="#FF4444", activeforeground="White",
                           command=lambda event=0: self.master.destroy())

        close_btn.bind("<Enter>", lambda event: close_btn.configure(bg="#FF4444"))
        close_btn.bind("<Leave>", lambda event: close_btn.configure(bg="red"))
        close_btn.grid(row=0, column=1, ipadx=5, padx=10, ipady=3, pady=20)

        save_btn = Button(self, bd=0, bg="#007DFA", height=1, width=10,
                          text="保存", anchor='center', font="15", fg="White",
                          activebackground="#007DFA", activeforeground="White",
                          command=lambda event=0: self.save())
        save_btn.bind("<Enter>", lambda event: save_btn.configure(bg="#228EFB"))
        save_btn.bind("<Leave>", lambda event: save_btn.configure(bg="#007DFA"))
        save_btn.grid(row=0, column=0, ipadx=5, padx=10, ipady=3, pady=20)

    def string2number(self, string):
        try:
            string = str(string)
            if string.endswith("小时"):
                num = int(string[0:-2]) * 3600000
            elif string.endswith("分钟"):
                num = int(string[0:-2]) * 60000
            elif string.endswith("秒"):
                num = int(string[0:-1]) * 1000
            else:
                num = int(string)
            if num <= 0:
                raise Exception("number can not be 0")
            return num
        except:
            raise Exception("error in parameter format: {}".format(string))

    def number2string(self, number):
        try:
            string = int(number)
            if string <= 0:
                raise Exception("number can not be 0")
            if string % 3600000 == 0:
                string = str(int(string / 3600000)) + "小时"
            elif string % 60000 == 0:
                string = str(int(string / 60000)) + "分钟"
            elif string % 1000 == 0:
                string = str(int(string / 1000)) + "秒"
            else:
                raise Exception("number must be the multiple of 1000")
            return string
        except:
            raise Exception("error in parameter format: {}".format(number))

    def save(self):
        name = self.node_name.get()
        status = 2 - self.node_status_value.get()
        mqtt_pub_interview = self.node_mqtt_pub_interview_value.get()
        wifi_wait_interview = self.node_wifi_wait_interview_value.get()
        mqttfinding_wait_interview = self.node_mqttfinding_wait_interview_value.get()

        try:
            mqtt_pub_interview = self.string2number(mqtt_pub_interview)
            wifi_wait_interview = self.string2number(wifi_wait_interview)
            mqttfinding_wait_interview = self.string2number(mqttfinding_wait_interview)
        except:
            tkinter.messagebox.showerror('错误', '时间格式错误')

        control_msg = "node set {} status={} mqtt_pub_interview={} " \
                      "wifi_wait_interview={} mqttfinding_wait_interview={}". \
            format(name, status, mqtt_pub_interview, wifi_wait_interview, mqttfinding_wait_interview)
        self.main_frame.cmd_line_input(control_msg)

    def refresh(self):
        name = self.node_name.get()
        for line in self.info:
            if line["name"] == name:
                self.node_status_value.set(2 - int(line["status"]))
                self.node_mqtt_pub_interview_value.set(
                    self.number2string(line["mqtt_pub_interview"]))
                self.node_wifi_wait_interview_value.set(
                    self.number2string(line["wifi_wait_interview"]))
                self.node_mqttfinding_wait_interview_value.set(
                    self.number2string(line["mqttfinding_wait_interview"]))


def set_center(tk, width, heigh):
    sw = tk.winfo_screenwidth()
    sh = tk.winfo_screenheight()
    ww = width
    wh = heigh
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))


def start_nodemcu_ctr_main_view(line):
    nodemcu_root_tk = Tk()
    nodemcu_window_x = 360
    nodemcu_window_y = 440

    set_center(nodemcu_root_tk, nodemcu_window_x, nodemcu_window_y)
    nodemcu_root_tk.resizable(width=False, height=False)
    nodemcu_root_tk.title("NodeMCU控制")

    NodemcuCtrMainView(master=nodemcu_root_tk, info=line).pack()
    nodemcu_root_tk.mainloop()


line = {'equipment': 0, 'name': '00101', 'status': '0', 'mqtt_pub_interview': 4000, 'mqttfinding_wait_interview': 5000,
        'wifi_wait_interview': 2000}
line2 = {'equipment': 0, 'name': '00102', 'status': '1', 'mqtt_pub_interview': 8000, 'mqttfinding_wait_interview': 5000,
         'wifi_wait_interview': 2000}
line3 = {'equipment': 0, 'name': '00103', 'status': '0', 'mqtt_pub_interview': 5000, 'mqttfinding_wait_interview': 5000,
         'wifi_wait_interview': 2000}
line = [str(line), str(line2), str(line3)]
start_nodemcu_ctr_main_view(line)
