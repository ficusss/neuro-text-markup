import tkinter as tk
from time import sleep
# import threading


class Reader:
    def __init__(self, filename):
        self.TIME_MIN_PAUSE = 0.05
        self.TIME_MAX_PAUSE = 0.3
        self.filename = filename
        self.curr_line_pos = 1
        self.work = False
        self.curr_time_pause = 0.11
        self.isOpen = False
        self.curr_state = 0
        self.all_state = {
            '$$$0$$$': 0,   # раслабленность
            '$$$1$$$': 1    # сосредоточенность
        }

    def up_work(self, event):
        self.work = not self.work

    def up_speed(self, event):
        if self.curr_time_pause > self.TIME_MIN_PAUSE:
            self.curr_time_pause -= 0.01

    def down_speed(self, event):
        if self.curr_time_pause < self.TIME_MAX_PAUSE:
            self.curr_time_pause += 0.01

    def sliding_update_position(self):
        self.curr_line_pos += 1

    @staticmethod
    def symbol_control(symbol):
        return symbol if symbol != '\n' else ' '

    def update_state(self, key):
        key = "".join(key)
        if key in self.all_state:
            self.curr_state = self.all_state[key]
        else:
            print("unknow key")

    def sliding_read(self, countSymb=86):
        '''Open window with sliding text'''

        root = tk.Tk(className=" Sliding Line")
        self.isOpen = True
        T = tk.Text(root, height=1, width=70,
                    font=('Arial', 20))

        Pause = tk.Button(root, text="pause")
        SpeedUp = tk.Button(root, text="+")
        SpeedDown = tk.Button(root, text="-")
        T.pack(side=tk.LEFT, fill=tk.Y)
        Pause.pack(side=tk.RIGHT)
        SpeedUp.pack(side=tk.RIGHT)
        SpeedDown.pack(side=tk.RIGHT)

        f = open(self.filename, "r")
        full_text = list(f.read())
        for _ in range(countSymb):
            if full_text[0] == '$':
                self.update_state(full_text[0:7])
                for i in range(7):
                    T.insert(tk.END, Reader.symbol_control(full_text.pop(0)))
            T.insert(tk.END, Reader.symbol_control(full_text.pop(0)))
        for _ in range(len(full_text)):
            if full_text[0] == '$':
                self.update_state(full_text[0:7])
                for i in range(7):
                    T.insert(tk.END, Reader.symbol_control(full_text.pop(0)))
            symbol = full_text.pop(0)
            T.insert(tk.END, Reader.symbol_control(symbol))
            self.sliding_update_position()
            Pause.bind('<Button-1>', self.up_work)
            SpeedUp.bind('<Button-1>', self.up_speed)
            SpeedDown.bind('<Button-1>', self.down_speed)
            while not self.get_work():
                Pause.bind('<Button-1>', self.up_work)
                root.update()
            root.update()
            T.delete('1.0')
            sleep(self.curr_time_pause)
        f.close()

        root.mainloop()
        self.isOpen = False

    def get_pos(self):
        return self.curr_line_pos

    def get_work(self):
        return self.work

    def get_time_pause(self):
        return self.curr_time_pause

    def is_open(self):
        return self.isOpen

    def get_state(self):
        return self.curr_state
