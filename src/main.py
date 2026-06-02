from data_structures.process_tree import Node
from data_structures.process_tree_operator import Operator
from data_structures.activity import Activity

TestTree = Node(Operator.Exclusive)
TestTree.add_child(Activity("a"))
TestTree.add_child(Activity("b"))

print(str(TestTree))