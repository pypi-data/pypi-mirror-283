from dataclasses import dataclass
import random
from time import sleep
from typing import Optional
import explainable
import explainable.display
from explainable import widget, source


# @explainable.display_as(widget.ListWidget([
#     source.Reference("item.age"),
#     source.Reference("item.age"),
#     source.Reference("item.age"),
# ]))
@dataclass
class Kilo:
    name: str
    age: int
    third: Optional["Kilo"]


explainable.init()


def create_kilo(complexity: int):
    name = random.choice(["Mike", "Martha", "John", "Cillian", "Jack", "Anna", "Bob", "Mary", "Jane"])
    age = random.randint(0, 100)

    if complexity > 0:
        third = create_kilo(complexity=complexity - 1)
    else:
        third = None
      
    return Kilo(age=age, name=name, third=third)


obj = create_kilo(complexity=0)

# obj = {
#   "nodes": [{
#     "uuid": "1",
#     "fields": {
#       "first_name": "John",
#       "last_name": "Malkovich",
#       "age": 45,
#     },
#   }, {
#     "uuid": "2",
#     "fields": {
#       "first_name": "Cillian",
#       "last_name": "Murphy",
#       "age": 35,
#     },
#   }],
#   "edges": [{
#     "start": "1",
#     "end": "2",
#     "name": "movie",
#     "weight": "0.8",
#   }]
# }
# wgt = widget.GraphWidget(
#   nodes=widget.GraphNode(
#     source=source.Reference("item.nodes"),
#     id=source.Reference("item.uuid"),
#     widget=widget.ListWidget(
#       source=[
#           source.String(
#             format="{item.fields.first_name} {item.fields.last_name}",
#           ),
#           source.Reference(
#             path="item.fields.age",
#           ),
#       ]
#     ),
#   ),
#   edges=widget.GraphEdge(
#     source=source.Reference("item.edges"),
#     start=source.Reference("item.start"),
#     end=source.Reference("item.end"),
#     label=source.Reference("item.name"),
#   ),
# )
# obj = [30000.23242]
# wgt = widget.NumberWidget(
#     source=source.Reference("item.0"),
#     separation=True,
#     round=2,
# )
obj = explainable.observe("view1", obj, widget=None)


while True:
    # obj["nodes"][0]["fields"]["age"] += 1
    # obj["nodes"][1]["fields"]["age"] += 1
    obj.age += 1
    # obj["a"] = str(int(obj["a"]) + 1)
    # obj.first = [1, 2, 3]
    # obj[0] += 1
    print(obj)
    sleep(1)
