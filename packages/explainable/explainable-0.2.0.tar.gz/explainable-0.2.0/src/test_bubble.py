import random
import time
import explainable
import explainable.display
from explainable import widget, source

explainable.init(wait_client=True)

test_list = [
  random.randint(0, 100) for _ in range(200)
]

print("The original list is : " + str(test_list))

wgt = widget.ListWidget(
  item_widget=widget.TileWidget(
    height=source.Reference("item"),
    width=source.Number(10),
  ),
)
wgt = None
test_list = explainable.observe("view1", test_list, widget=wgt)


def bubble_sort(elements):
  for n in range(len(elements) - 1, 0, -1):
    swapped = False
    for i in range(n):
      if elements[i] > elements[i + 1]:
        swapped = True
        time.sleep(0.001)
        elements[i], elements[i + 1] = elements[i + 1], elements[i]
    if not swapped:
      return


bubble_sort(test_list)

print("The sorted list is : " + str(test_list))
