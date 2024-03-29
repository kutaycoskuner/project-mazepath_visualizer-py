#
# ============================================================================= 
# ==== Libraries
# ============================================================================= 
import curses                           # :: main module
import copy                             # :: for shallow copy
from argparse import ArgumentParser     # :: to add command line arguments 
from src import view as View            # :: self gui definition
from src import model as Model          # :: logic
from Data import test as test           # :: test maze
from tkinter import filedialog as fd    # :: tkinter file dialog for input file
import time                             # :: for implementing delay



# ==== Disabled Library
# from curses import wrapper              # :: wrapper 

# ============================================================================= 
# ==== Classes
# ============================================================================= 
class Args:
    def __init__(self):
        self.args = None
        self.crt_Args()

    def crt_Args(self):
        # == argument decleration
        parser = ArgumentParser(description='Visualize path in MxN Maze')
        # :: 1 delay in seconds
        parser.add_argument('-t', metavar='delay', type=float,
                        help='delay time on visualization in seconds')
        # :: 2 data
        parser.add_argument('-d', metavar='data', type=str,
                        help='data path for visualization')
        # :: 3 depth first
        parser.add_argument('-df', nargs='?', const=1,       
                        help='apply depth first search')
        # :: 4 breadth first
        parser.add_argument('-bf', nargs='?', const=1,        
                        help='apply breadth first search')
        # :: 5 path color
        parser.add_argument('-cp', type=str,
                            choices=['red', "green", "blue"],
                            help="choose path color for maze")
        # :: 6 path obstacle
        parser.add_argument('-co', type=str,
                            choices=['red', "green", "blue"],
                            help="choose obstacle color for maze")
        # :: 7 add gui
        parser.add_argument('-gui', nargs='?', const=1,        
                        help='use gui instead of command line')
        # :: create args
        self.args = parser.parse_args()

    def validate(self):
        # :: 1: time
        if self.args.t == None:
            self.args.t = .2
        # :: 5: path color
        if self.args.cp != None:
            self.args.cp = Model.select_color(self.args.cp)
        else:
            self.args.cp = Model.select_color('green')
        # :: 6: obstacle color
        if self.args.co != None:
            self.args.co = Model.select_color(self.args.co)
        else:
            self.args.co = Model.select_color('blue')
        # todo 2: data
        if Model.read_input(self.args.d) != None:
            return Model.adapt_input(Model.read_input(self.args.d))

class Controller:
    def __init__(self):
        def start_curses():
            self.stdscr = curses.initscr()
            curses.start_color()
        start_curses()
        #
        self.args = Args()
        self.model = Model.Model(self, self.args)
        self.view = View.View(self)

        self.path_list = None


    def start(self):
        input = test.maze
        # :: select inteface
        if self.args.args.gui:
            self.view.start()
        else:
            # todo 2: data
            if self.args.args.d != None:
                test.maze = self.args.validate()
            if test.maze != None:
                self.model.start(self.stdscr, test.maze)
            else: 
                print("could not found the file")

    def onbtn_Start(self):
        if self.path_list == None:
            self.create_path_list()

        self.view.slideCounter = 0
        self.view.update_monitor(self.path_list[self.view.slideCounter])  # :: view e veriyi gonder

    def onbtn_End(self):
        if self.path_list == None:
            self.create_path_list()
        self.view.slideCounter = len(self.path_list)-1
        self.view.update_monitor(self.path_list[self.view.slideCounter])
        # todo if validate colorize

    def onbtn_Play(self):
        self.view.stopAnimation = False
        if self.path_list == None:
            self.onbtn_Start()
        
        self.view.animation(self.path_list, 200)  # :: view e veriyi gonder


    def onbtn_Stop(self):
        self.view.stopAnimation = True
        

    def onbtn_Next(self):
        if self.path_list == None:
            self.create_path_list()
        if self.view.slideCounter < len(self.path_list):
            self.view.slideCounter += 1
        self.view.update_monitor(self.path_list[self.view.slideCounter])

    def onbtn_Prev(self):
        if self.path_list == None:
            self.create_path_list()
        if self.view.slideCounter > 0:
            self.view.slideCounter -= 1
        self.view.update_monitor(self.path_list[self.view.slideCounter])

    def onbtn_Browse(self):
        if self.view.scale_Steps != None:
            self.view.scale_Steps.destroy()

        self.path_list = None
        filename = fd.askopenfilename()
        lines = self.model.read_input(filename)
        result = self.model.adapt_input(lines)
        if self.model.validate_input(result):
            test.maze = result
        else:
            self.view.update_monitor(False)  # :: view e veriyi gonder
            return

        # :: create slider
        if self.path_list == None:
            self.create_path_list()
        self.view._crt_slider(len(self.path_list)-1)

        # :: update monitor
        self.view.slideCounter = 0
        self.view.update_monitor(result)  # :: view e veriyi gonder

    def onslider_Change(self, value):
        self.view.slideCounter = int(value)
        if self.path_list == None:
            self.create_path_list()
        self.view.update_monitor(self.path_list[self.view.slideCounter])

    def create_path_list(self):
        input = copy.deepcopy(test.maze)
        self.path_list = Model.find_path_gui(input)


# ============================================================================= 
# ==== Start
# ============================================================================= 
def main():
    controller = Controller()
    controller.start()