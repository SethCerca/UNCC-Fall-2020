from pomegranate import ConditionalProbabilityTable, DiscreteDistribution, Node, BayesianNetwork
import matplotlib.pyplot as plt

battery = DiscreteDistribution({'B': .95, '!B': .05})
gas = DiscreteDistribution({'G': .90, '!G': .10})

radio = ConditionalProbabilityTable(
    [['B', 'R', .99],
     ['B', '!R', .001],
     ['!B', 'R', .99],
     ['!B', '!R', .001]], [battery])

ignition = ConditionalProbabilityTable(
    [['B', 'I', .98],
     ['B', '!I', .02],
     ['!B', 'I', .002],
     ['!B', '!I', .998]], [battery])

starts = ConditionalProbabilityTable(
    [['I', 'G', 'S', .80],
     ['I', 'G', '!S', .20],
     ['I', '!G', 'S', .25],
     ['I', '!G', '!S', .75],
     ['!I', 'G', 'S', .001],
     ['!I', 'G', '!S', .999],
     ['!I', '!G', 'S', .001],
     ['!I', '!G', '!S', .999]], [ignition, gas])

moves = ConditionalProbabilityTable(
    [['S', 'M', .85],
     ['S', '!M', .15],
     ['!S', 'M', .005],
     ['!S', '!M', .995]], [starts])

s1 = Node(battery, name="battery")
s2 = Node(gas, name="gas")
s3 = Node(radio, name="radio")
s4 = Node(ignition, name="ignition")
s5 = Node(starts, name="starts")
s6 = Node(moves, name="moves")

model = BayesianNetwork("Car")
model.add_nodes(s1, s2, s3, s4, s5, s6)
model.add_edge(s1, s3)
model.add_edge(s1, s4)
model.add_edge(s4, s5)
model.add_edge(s2, s5)
model.add_edge(s5, s6)
model.bake()

print("\nAll true values:" + str(model.probability([['B', 'G', 'R', 'I', 'S', 'M']])))
print("All false values:" + str(model.probability([['!B', '!G', '!R', '!I', '!S', '!M']])))
print("Battery = false, everything else = true" + str(model.probability([['!B', 'G', 'R', 'I', 'S', 'M']])))
print("Moves = false, everything else = true" + str(model.probability([['B', 'G', 'R', 'I', 'S', '!M']])))
