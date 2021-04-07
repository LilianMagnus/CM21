# DynaView.py
# Dynamics Viewer for an example of creating GUI by Tkinter.  
# Dec 2017, 2018 by Kenji Doya

import matplotlib
# for using matplotlib in Tk window
# see http://matplotlib.org/examples/user_interfaces/embedding_in_tk.html
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

import numpy as np
from scipy.integrate import odeint

# List of system: name, initial state, and parameters
system_list = []

# Import dynamical systems and add to system_list
import first
system_list.append(first.name_state_parameters)
import second
system_list.append(second.name_state_parameters)

print(system_list)

# System names to show in the listbox
system_names = ""
for s in system_list:
    system_names = system_names+s[0]+" "
print(system_names)

# Make a Tk window and place widgets

def make_window():
    """make a window and place widgets"""
    global listbox, fig, ax, canvas
    root = tk.Tk()
    root.title("Dynamics Viewer")
    root.geometry("800x600")
    # Label for the system listbox
    system_label = tk.Label(root, text="System: ")
    system_label.grid(row=0, column=0, sticky=tk.E) 
    # Scroll bar for system listbox
    yScroll = tk.Scrollbar(root, orient=tk.VERTICAL)
    yScroll.grid(row=0, column=2, sticky=tk.W+tk.N+tk.S)
    # Listbox for choosing the system
    names = tk.StringVar()
    names.set(system_names)
    listbox = tk.Listbox(root, listvariable=names, height=3, yscrollcommand=yScroll.set)
    listbox.selection_set(0)  # initial selection
    listbox.grid(row=0, column=1, sticky=tk.E+tk.W)
    yScroll['command'] = listbox.yview
    # Select button
    select_button = tk.Button(root, text="Select")
    select_button.bind("<Button-1>", select) 
    select_button.grid(row=0, column=3)
    # Reset button
    reset_button = tk.Button(root, text="Reset")
    reset_button.bind("<Button-1>", reset) 
    reset_button.grid(row=1, column=3)
    # Run button
    run_button = tk.Button(root, text="Run")
    run_button.bind("<Button-1>", run) 
    run_button.grid(row=2, column=3)
    # Figure window
    fig = Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    #canvas.show()  # show() is replaced by draw()
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0, columnspan=4)
    return(root)

# Functions to be called when a button is pressed

def select(event):
    """select the system from listbox"""
    global system, dynamics, initial_state, parameters
    sid = listbox.curselection()[0]  # index of selected system
    system = system_list[sid][0]
    dynamics = eval(system).dynamics   # convert name to function
    initial_state = system_list[sid][1]  # initial state
    parameters = system_list[sid][2]  # parameters
    print(system, initial_state, parameters)
    reset([])

def reset(event):
    """reset the system"""
    global time, state
    time = 0.
    state = initial_state
    ax.cla()
    ax.set_title(system)
    ax.set_xlabel('Time')
    #canvas.show()
    canvas.draw()

trun = 10.   # time of single run
dt = 0.1   # time step of output

def run(event):
    global time, state
    """simulate the selected system"""
    t = np.arange(time, time+trun+dt/2, dt) # +dt/2 to include time+trun
    y = odeint(dynamics, state, t, args=parameters)
    ax.plot(t, y)
    #canvas.show()
    canvas.draw()
    # update the time and state
    time = t[-1]
    state = y[-1,:]
    print(time, state)

# Now actually make a window and start the event loop

root = make_window()
select([])  # default selection
root.mainloop()
