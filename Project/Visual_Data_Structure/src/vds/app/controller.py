import tkinter as tk
from vds.core.stack import Stack

def run_app():
  root = tk.Tk()
  root.title("VDS 테스트")
  
  stack = Stack()
  
  label = tk.Label(root, text="VDS 테스트(MVP)")
  label.pack()
  
  root.mainloop()