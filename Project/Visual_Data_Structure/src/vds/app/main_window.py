import tkinter as tk
from vds.app.wiring import create_stack_panel

class MainWindow:
  def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("VDS 테스트")
    self.root.geometry("1100x700")

    self._build_layout()
    
  def _build_layout(self) -> None:
    self.title_label = tk.Label(
      self.root,
      text="VDS 테스트(MVP)",
      font=("Arial", 16, "bold"),
    )
    
    self.title_label.pack(fill=tk.X, pady=8)

    self.container = tk.Frame(self.root)
    self.container.pack(fill=tk.BOTH, expand=True)

  def mount(self, panel: tk.Widget) -> None:
      panel.pack(fill=tk.BOTH, expand=True)

def run_app() -> None:
  root = tk.Tk()

  window = MainWindow(root)
  stack_panel = create_stack_panel(window.container)
  window.mount(stack_panel)

  root.mainloop()