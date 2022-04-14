from tkinter import *
import sys
import json

RADIUS = 6


def draw_point(canvas, x, y):
    canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="black")


def draw_points(canvas, nodes):
    for node in nodes:
        draw_point(canvas, node[0], node[1])


def draw_lines(canvas, nodes):
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            first_point = nodes[i]
            second_point = nodes[j]
            canvas.create_line(first_point[0], first_point[1],
                               second_point[0], second_point[1], fill="red")


def get_json():
    json_string = sys.stdin.read()
    return json.loads(json_string)


if __name__ == '__main__':
    root = Tk()
    root.after(3000, lambda: root.destroy())
    canvas_info = get_json()
    canvas = Canvas(root, bg="orange", height=canvas_info["size"], width=canvas_info["size"], highlightthickness=0)
    draw_lines(canvas, canvas_info["nodes"])
    draw_points(canvas, canvas_info["nodes"])
    canvas.pack()
    root.mainloop()


