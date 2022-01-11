from tkinter import *

class middle_ctr:
    def middle_ctr_button_canvas(self):
        middle = Canvas(width=1000, height=300, bg="#FFFFFF", highlightthickness=0)
        middle.grid(row=0)

        help_btn = Button(middle, bd=0, bg="#007DFA", height=2, width=35,
                          text="帮助", anchor='center', font="20", fg="White",
                          activebackground="#007DFA", activeforeground="White",
                          command=self.help_btn)
        help_btn.bind("<Enter>", lambda event: help_btn.configure(bg="#228EFB"))
        help_btn.bind("<Leave>", lambda event: help_btn.configure(bg="#007DFA"))
        help_btn.grid(row=0, column=0)
        return middle

    def help_btn(self):
        pass

