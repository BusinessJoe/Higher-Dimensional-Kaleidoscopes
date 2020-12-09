import tkinter as tk
from functools import partial
from gui import CoxeterRenderer
from diagram import CoxeterDiagram


def create_coxeter_entries():
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
    for index in range(size - 1):
        coxeter_list[index] = tk.Entry(coxeter_frame, width=2)
        coxeter_list[index].grid(row=index + 1, column=0, pady=2)
    for index in range(size):
        active_list[index] = tk.Entry(coxeter_frame, width=2)
        active_list[index].grid(row=index + 1, column=1, pady=2)


def generate_diagram(renderer):
    coxeter_angles = []
    active = []

    for entry in coxeter_list.values():
        coxeter_angles.append(int(entry.get()))
    coxeter_angles.append(0)
    for entry in active_list.values():
        active.append(int(entry.get()))

    renderer.diagram = CoxeterDiagram(active, coxeter_angles)
    renderer.dimension = renderer.diagram.dimension
    renderer.points = renderer.diagram.polytope()
    renderer.draw()

    confirm_message.set('Success')


# GUI
coxeter_list = dict()
active_list = dict()

screenWidth = 900
screenHeight = 600

root = tk.Tk()
root.title("Projection")
root.resizable(0, 0)

confirm_message = tk.StringVar()

# Create frames for the layout
left_frame = tk.Frame(root, borderwidth=2, relief="groove")
right_frame = tk.Frame(root, borderwidth=2, relief="groove")

# Create a frame for the diagram entries
coxeter_frame = tk.Frame(right_frame, width=300, borderwidth=2, relief="groove")

# Put frames in the root window
left_frame.grid(row=0, column=0, sticky=tk.NSEW)
right_frame.grid(row=0, column=1, sticky=tk.NSEW)
coxeter_frame.grid(row=0, column=0, sticky=tk.EW)

# Set up the canvas in the left frame
renderer = CoxeterRenderer(left_frame, screenWidth, screenHeight)

# Create scale bars for angles and put them in the left frame
bar = dict()
for i in range(3):
    bar[i] = tk.Scale(left_frame, from_=0, to=360, resolution=0.1, orient=tk.HORIZONTAL, length=200,
                      command=partial(renderer.update_angle, i))
    bar[i].grid(row=i + 1, column=0, sticky=tk.W, padx=10)

# Create scale bars for scaling amount and distances
scale = tk.Scale(left_frame, from_=0, to=300, length=200, label='Scaling', orient=tk.HORIZONTAL,
                 command=partial(renderer.set_scale))
dot_size_scale = tk.Scale(left_frame, from_=0, to=100, length=200, label='Dot Size', orient=tk.HORIZONTAL,
                          command=partial(renderer.set_dot_size))
screen_scale = tk.Scale(left_frame, from_=0, to=1000, length=200, label='Screen Distance', orient=tk.HORIZONTAL,
                        command=partial(renderer.set_screen_dist))
eye_scale = tk.Scale(left_frame, from_=0, to=1000, length=200, label='Eye Distance', orient=tk.HORIZONTAL,
                     command=partial(renderer.set_eye_dist))
scale.set(100)
dot_size_scale.set(20)
screen_scale.set(300)
eye_scale.set(600)

# Create the generation related widgets
diagram_size = tk.Entry(coxeter_frame, width=5)
submit_size = tk.Button(coxeter_frame, text='Set size', command=create_coxeter_entries)

# Create button to confirm diagram settings
confirm = tk.Button(right_frame, text='Confirm', command=partial(generate_diagram, renderer))
confirm.grid(row=1, column=0, pady=5)

# Create label for the confirm result
confirm_result = tk.Label(right_frame, textvariable=confirm_message, width=20)
confirm_result.grid(row=2, column=0)

# Layout canvas in left frame
renderer.grid(row=0, column=0, columnspan=3)

# Layout scale bars for scaling amount and distances in left frame
scale.grid(row=1, column=1, sticky=tk.W, pady=10)
dot_size_scale.grid(row=1, column=2, sticky=tk.W)
screen_scale.grid(row=2, column=1, sticky=tk.W, pady=10)
eye_scale.grid(row=3, column=1, sticky=tk.W, pady=10)

# Layout the widgets in the right frame
diagram_size.grid(row=0, column=0, sticky=tk.W, padx=10)
submit_size.grid(row=0, column=1, sticky=tk.E, pady=5)

renderer.draw()
root.mainloop()
