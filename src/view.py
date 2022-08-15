#
# ============================================================================= 
# ==== Library
# =============================================================================
# from tkinter import *
import tkinter as tk
from tkinter import ttk
from src import model as model
import time

# ==== Disabled Library
# from tkinter import scrolledtext                   # :: gui library

# ============================================================================= 
# ==== Classes
# =============================================================================
class View(tk.Tk):
    # == Variables
    # :: colors
    col_blue = "#06b4ba"
    col_green = "#47E10C"
    col_vi = "#da1991"
    col_darkGray1 = "#202020"
    col_darkGray2 = "#242424"
    col_darkGray3 = "#262626"
    col_hellGray1 = "#dbdbdb"
    col_white = "#ffffff"
    col_test = "#ccc"
    # :: padding
    cnstPad = 25
    c_padx = 10

    # == constructor
    def __init__(self, controller):
        # :: inherit from tk
        super().__init__() 
        #
        self.controller = controller
        #
        self.title('Potato')
        #
        # self._crt_titlebar()
        # self._crt_ctrl_frame()
        self._crt_main_frame()
        self._crt_output()
        self._crt_ctrl_buttons()
        self._crt_input()

        # :: variables
        self.value = tk.StringVar()
        self.slideCounter = 0
        self.stopAnimation = False
        self.scale_Steps = None
        # self._crt_testentry()


    # == elements
    def start(self):
        self.geometry("720x480")
        self.resizable(False, False)
        # self.overrideredirect(True) # turn off title bar, geometry
        self.title("Maze Path Visualizer")
        self.iconbitmap()
        self.configure(background=self.col_darkGray1)
        self.mainloop()

    def _crt_titlebar(self):
        frm_title = tk.Frame(self, bg=self.col_darkGray1, relief="raised", bd=0, highlightthickness=0)
        frm_title.pack(fill='x')
        #
        btn_wndw_ext = tk.Button(frm_title, text="✕", padx=4, pady=2, command=self.destroy, fg=self.col_white, bg=self.col_darkGray1, bd= 0, highlightthickness=0)# &#xE106;
        btn_wndw_ext.pack(side='right')
        #
        # btn_wndw_max = tk.Button(frm_title, text="🗖", padx=4, pady=2, fg=self.col_white, bg=self.col_darkGray1, bd= 0, highlightthickness=0)# &#xE739;"
        # btn_wndw_max.pack(side='right')
        #
        # btn_wndw_min = tk.Button(frm_title, text="—", padx=4, pady=2, fg=self.col_white, bg=self.col_darkGray1, bd= 0, highlightthickness=0)# &#xE949;
        # btn_wndw_min.pack(side='right')

    def _crt_ctrl_frame(self):
        # :: main window
        self.frm_outliner = tk.Frame(self, bg=self.col_darkGray3, relief="raised", bd=0, highlightthickness=0, width=200)
        self.frm_outliner.pack(fill='y', side=tk.LEFT)
            

    def _crt_main_frame(self):
        # :: main window
        self.frm_main = tk.Frame(self, bg=self.col_darkGray2, relief="raised", bd=0, highlightthickness=0)
        self.frm_main.pack(fill='both', expand=1)
        #
        # self.main_frm = ttk.Frame(self)
        # self.main_frm.pack(padx=self.cnstPad, pady=self.cnstPad)

    def _crt_output(self):
        # :: input output screen
        self.cnvs = tk.Canvas(self.frm_main, bg=self.col_darkGray3, bd=1, highlightthickness=0)
        self.cnvs.pack(pady=10)
        # self.txt_io = tk.Text(self.frm_main, bg=self.col_darkGray3, fg=self.col_hellGray1, bd=1, highlightthickness=0)
        # self.txt_io.pack(pady=10)
        # :: report line
        # lbl_report = tk.Label(self.frm_main, bg="gray", width=60)
        # lbl_report.pack()

    def _crt_ctrl_buttons(self):
        frm_ctrl = tk.Frame(self.frm_main, bg=self.col_darkGray2, relief="raised", bd=0, highlightthickness=0)
        frm_ctrl.pack()

    #    scale_Steps = tk.Scale(frm_ctrl, from_=0, to=(self.slideCounter), orient="horizontal", command=self.controller.onscale_Steps)
    #     scale_Steps.pack() 
        #
        btn_toStart = tk.Button(frm_ctrl, text="Start", command=self.controller.onbtn_Start)
        btn_toStart.pack(side="left", padx=self.c_padx)
        btn_prev = tk.Button(frm_ctrl, text="prev", command=self.controller.onbtn_Prev)
        btn_prev.pack(side="left", padx=self.c_padx)   
        btn_play = tk.Button(frm_ctrl, text="Play", command=self.controller.onbtn_Play)
        btn_play.pack(side="left", padx=self.c_padx)   
        btn_stop = tk.Button(frm_ctrl, text="Stop", command=self.controller.onbtn_Stop)
        btn_stop.pack(side="left", padx=self.c_padx)  
        btn_next = tk.Button(frm_ctrl, text="next", command=self.controller.onbtn_Next)
        btn_next.pack(side="left", padx=self.c_padx)
        btn_toEnd = tk.Button(frm_ctrl, text="End", command=self.controller.onbtn_End)
        btn_toEnd.pack(side="left", padx=self.c_padx)

    def _crt_input(self):
        btn_toStart = tk.Button(self.frm_main, text="Browse", command=self.controller.onbtn_Browse)
        btn_toStart.pack(padx=self.c_padx, pady=self.c_padx)

    def _crt_slider(self, steps=10):
        self.scale_Steps = tk.Scale(self.frm_main, from_=0, to=steps, orient="horizontal", command=self.controller.onslider_Change)
        self.scale_Steps.pack()

    def _crt_testentry(self):
        ent = ttk.Entry(self.frm_main, textvariable=self.value)
        ent.pack()

    def update_monitor(self, input_maze):
        cnvs = self.cnvs        
        cnvs.delete('all')
        # cnvs.update()  # needed to do one pic at a time
        # time.sleep(1000)
        # cnvs.create_text(100,10, text="test", fill=self.col_blue)
        # cnvs.create_text(100,20, text="test", fill=self.col_vi)

        if input_maze == False:
            text = "False input \nYour maze should be surrounded by #\nContain only one enter '0' and one exit '1'\nInner elements could be either block '#' or path '.'\nMaze should be smaller than 20x20"
            self.cnvs.create_text(180,120,fill=self.col_white ,font="Times 12",
                        text=text)
            return

        color = self.col_blue
        recSize = 16
        paddingX = (cnvs.winfo_width() - (recSize * len(input_maze[0]))) / 2
        paddingY = (cnvs.winfo_height() - (recSize * len(input_maze))) / 2
        x,y = paddingX, paddingY

        color_map = {
            '#': self.col_blue,
            '.': self.col_darkGray1,
            ' ': self.col_darkGray1,
            '0': self.col_green,
            'O': self.col_green,
            '1': self.col_green,
            'X': self.col_green,
            '2': self.col_vi,
        }

        for line in input_maze:
            for char in line:
                if char in color_map:
                    color = color_map[char]
                cnvs.create_rectangle(x, y, x+recSize, y+recSize, fill=color)
                # cnvs.create_line(x,y, x+1, y, fill=color)
                # self.cnvs.create_line(10, 10, 10 + 1, 10, fill='white')  
                # cnvs.create_text(x,y, text=char, fill=color)
                x += recSize
            x = paddingX
            y += recSize

        if self.scale_Steps != None:
            self.scale_Steps.set(self.slideCounter)
        

        #         self.txt_io.insert('end', char + " ")
        #     self.txt_io.insert('end', '\n')
        # self.txt_io.config(state='disabled') # :: freeze widget

    def animation(self, input_maze, delay):
        # for ii in range(len(input_maze)-1):
        while not self.stopAnimation and self.slideCounter < len(input_maze):    
            self.cnvs.update()
            self.slideCounter += 1
            self.cnvs.after(delay, self.update_monitor(input_maze[self.slideCounter]))
            if self.scale_Steps:
                self.scale_Steps.set(self.slideCounter)


