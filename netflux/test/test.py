from netflux.core.component import ComponentBuilder
from netflux.components.datasender import DataSender
from netflux.core.executor import Executor

# Define the components
def adder(op1, op2):
    return op1 + op2
    
Adder = ComponentBuilder.build(adder, inports=['op1','op2'], name="Adder")

def mult(op1, op2):
    return op1 + op2
    
Multiplier = ComponentBuilder.build(mult,
    inports=['op1','op2'], name="Multipler")

#### Define the flow in python
# DataSender component is used to send data
data1 = DataSender(122, name="data1")
data2 = DataSender(232, name="data2")
data3 = DataSender(345, name="data3")
data4 = DataSender(645, name="data4")


# instantiate Adder and Multiplier
Adder1 = Adder(name="Adder1")
Adder2 = Adder(name="Adder2")
Multr = Adder(name="Multr")

# define flow graph in python built-in DSL
flow = (
    data1['out'] >> Adder1['op1'] |
    data2['out'] >> Adder1['op2'] |
    data3['out'] >> Adder2['op1'] |
    data4['out'] >> Adder2['op2'] |
    Multr['op1'] << Adder1['out'] | 
    Multr['op2'] << Adder2['out']
    )


# Build and run the flow
executor = Executor(ticks=5) #schedule the flow 5 times
executor.build(flow)
executor.run()


