import santa.graphsanta as graphsanta
import random

random.seed(4)

gsantaC = graphsanta.Constraints()
gsantaC.add_constraints("a",["c"])
graphsanta.allocate(["a","b","c"],gsantaC)