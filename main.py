# TODO find another method of rotation
from tkinter import *
import math
from functools import partial
from project_down import v_project
from rotate import v_rotate
import numpy as np
from diagram import CoxeterDiagram

# Generation of points
diagram = CoxeterDiagram([True, False, False], [5, 3])
dimension = diagram.dimension
scaling = 100
dotSize = 20
screenDist = 300
eyeDist = 600
iterations = 10
points = diagram.polytope()

# Set up a zero array for the angles
angles = [0]*3


# Takes in points and their sizes and draws them onto the canvas
def draw():
    c.delete('all')

    rotated_points = v_rotate(points * scaling, float(angles[0]), 0, 1, dimension)
    rotated_points = v_rotate(rotated_points, float(angles[1]), 0, 2, dimension)
    rotated_points = v_rotate(rotated_points, float(angles[2]), 1, 2, dimension)

    proj_points = np.copy(rotated_points)
    while proj_points.shape[1] != 2:
        proj_points, heights = v_project(proj_points, screenDist, eyeDist)

    heights = np.reshape(heights, (-1, 1))
    heights *= dotSize

    points_and_heights = np.concatenate((proj_points, heights), axis=1)

    for p in points_and_heights:
        c.create_oval(p[0] - p[2] + screenWidth/2, p[1] - p[2] + screenHeight/2,
                           p[0] + p[2] + screenWidth/2, p[1] + p[2] + screenHeight/2)


def update(index, value):
    angles[index] = float(value)*math.pi/180
    draw()


def set_scale(scale):
    global scaling
    scaling = float(scale)
    draw()


def set_dot_size(size):
    global dotSize
    dotSize = float(size)
    draw()


def set_screen_dist(dist):
    global screenDist
    screenDist = float(dist)
    draw()


def set_eye_dist(dist):
    global eyeDist
    eyeDist = float(dist)
    draw()


def create_coxeter_entries():
    global coxeter_list
    global active_list

    try:
        size = int(diagram_size.get())
    except ValueError:
        # TODO fix
        diagram_size.delete(0)
        diagram_size.insert(0, '0')
        size = 0

    # Destroy the existing widgets and clear the dictionary
    for entry in coxeter_list.values():
        entry.destroy()
    for entry in active_list.values():
        entry.destroy()
    coxeter_list.clear()
    active_list.clear()

    # Create new widgets
    for index in range(size-1):
        coxeter_list[index] = Entry(coxeter_frame, width=2)
        coxeter_list[index].grid(row=index+1, column=0, pady=2)
    for index in range(size):
        active_list[index] = Entry(coxeter_frame, width=2)
        active_list[index].grid(row=index+1, column=1, pady=2)


def generate_diagram():
    global points
    global dimension
    coxeter_angles = []
    active = []

    for entry in coxeter_list.values():
        coxeter_angles.append(int(entry.get()))
    coxeter_angles.append(0)
    for entry in active_list.values():
        active.append(int(entry.get()))

    diagram = CoxeterDiagram(active, coxeter_angles)
    dimension = diagram.dimension
    points = diagram.polytope()
    draw()

    confirm_message.set('Success')


# GUI
coxeter_list = dict()
active_list = dict()

screenWidth = 900
screenHeight = 600

root = Tk()
root.title("Projection")
root.resizable(0, 0)

confirm_message = StringVar()

# Create frames for the layout
left_frame = Frame(root, borderwidth=2, relief="groove")
right_frame = Frame(root, borderwidth=2, relief="groove")

# Create a frame for the diagram entries
coxeter_frame = Frame(right_frame, width=300, borderwidth=2, relief="groove")

# Put frames in the root window
left_frame.grid(row=0, column=0, sticky=NSEW)
right_frame.grid(row=0, column=1, sticky=NSEW)
coxeter_frame.grid(row=0, column=0, sticky=EW)

# Set up the canvas in the left frame
c = Canvas(left_frame, width=screenWidth, height=screenHeight, borderwidth=5, relief="groove")

# Create scale bars for angles and put them in the left frame
bar = dict()
for i in range(3):
    bar[i] = Scale(left_frame, from_=0, to=360, resolution=0.1, orient=HORIZONTAL, length=200,
                   command=partial(update, i))
    bar[i].grid(row=i+1, column=0, sticky=W, padx=10)

# Create scale bars for scaling amount and distances
scale = Scale(left_frame, from_=0, to=300, length=200, label='Scaling', orient=HORIZONTAL, command=partial(set_scale))
dot_size_scale = Scale(left_frame, from_=0, to=100, length=200, label='Dot Size', orient=HORIZONTAL,
                       command=partial(set_dot_size))
screen_scale = Scale(left_frame, from_=0, to=1000, length=200, label='Screen Distance', orient=HORIZONTAL,
                     command=partial(set_screen_dist))
eye_scale = Scale(left_frame, from_=0, to=1000, length=200, label='Eye Distance', orient=HORIZONTAL,
                  command=partial(set_eye_dist))
scale.set(100)
dot_size_scale.set(20)
screen_scale.set(300)
eye_scale.set(600)

# Create the generation related widgets
diagram_size = Entry(coxeter_frame, width=5)
submit_size = Button(coxeter_frame, text='Set size', command=create_coxeter_entries)

# Create button to confirm diagram settings
confirm = Button(right_frame, text='Confirm', command=generate_diagram)
confirm.grid(row=1, column=0, pady=5)

# Create label for the confirm result
confirm_result = Label(right_frame, textvariable=confirm_message, width=20)
confirm_result.grid(row=2, column=0)


# Layout canvas in left frame
c.grid(row=0, column=0, columnspan=3)

# Layout scale bars for scaling amount and distances in left frame
scale.grid(row=1, column=1, sticky=W, pady=10)
dot_size_scale.grid(row=1, column=2, sticky=W)
screen_scale.grid(row=2, column=1, sticky=W, pady=10)
eye_scale.grid(row=3, column=1, sticky=W, pady=10)

# Layout the widgets in the right frame
diagram_size.grid(row=0, column=0, sticky=W, padx=10)
submit_size.grid(row=0, column=1, sticky=E, pady=5)


draw()
root.mainloop()
