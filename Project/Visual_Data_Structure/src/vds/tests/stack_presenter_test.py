from vds.core.stack import Stack
from vds.presenter.stack_presenter import StackPresenter

s = Stack()
s.push(10)
s.push(20)
s.push(30)

presenter = StackPresenter()
scene = presenter.present_from_values(s.snapshot())

print(scene.meta)
print(len(scene.items))
print([getattr(it, "key") for it in scene.items][:10])