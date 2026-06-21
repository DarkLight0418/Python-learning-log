'''
객체 연결(DI)
Stack, Usecase, Presenter, View, Animator 연결
'''

from __future__ import annotations

import tkinter as tk

from vds.app.stack_panel import StackPanel
from vds.presenter.stack_presenter import StackPresenter
from vds.usecases.stack_usecase import StackUsecase

def create_stack_panel(master: tk.Misc) -> StackPanel:
    usecase = StackUsecase()
    presenter = StackPresenter()
    
    return StackPanel(
        master=master, 
        usecase=usecase, 
        presenter=presenter
    )