from view import MainView
from model import Model
import tkinter as tk
from controller import Controller

root = tk.Tk()
root.title("Nathanael Sargent and Logan Hewitt SPIDAM Project")

view = MainView(root)
model = Model()
controller = Controller(model, view)
view.setController(controller)
view.grid(row=0, column=0)

view.mainloop()