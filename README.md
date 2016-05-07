# NetFlux
### Component-Oriented Flow based Programming in Python

This repository provides the python classes to:
 - *Build Components*
 - *Define the flow graph/network* (a.k.a NetFlux)
 - *Execute Flows* (a.k.a Flux)

### Terminology
Component: 
>A Component is the basic block in FBP(Flow Based Programming). It has a set of inports and outports. Components are build using `netflux.core.component.ComponentBuilder`'s classmethod `build`.

Port:
>Ports allow Components to interact with each other. A Component comes with a set of built-in ports called `in`,`out`,`control`,`error`.

Tranporter:
>Transporter links the `sourcePort` of a `sourceComponent` to `sinkPort` of a `sinkComponent`. It is the class `netflux.core.transporter.Transporter`.

Flux:
>Flux is the flow between two components. NetFlux is the network or say graph of flow among components. Flux can be of data, signal, error, back pressure, result, or anything that flows. It is the class `netflux.core.flux.Flux`, and NetFlux is the class `netflux.core.flux.NetFlux`

Executor:
>Executor is the build-time and runtime engine. Given some NetFlux object it links/builds it, schedules the microthreads of components and executes the built network.


### Example

Lets build some netflux. We will build a simple network of Adders and Multipliers.

```
# NetFlux DSL

# Define the components
Adder1 := Math/Adder
Adder2 := Math/Adder
Multr  := Math/Multiplier

# Build the flow graph
# Syntax SourceComponent [SomeOutPort] >> [SomeInPort] SinkComponent

123 >> op1 Adder1 # op1 port of adder gets number 123
234 >> op2 Adder1

# you can also discribe flow in the other direction
345 >> op1 Adder2 op2 << 645

#send data at "out" port of Adder1 to op1 port of Multr 
Adder1 out >> op1 Multr | Adder2 out >> op2 Multr 
# use | to write multiple flows in same line
Multr >> STDOUT
```


The compiler for this DSL in not yet ready. But we will see how we can implement this completely in python.

#### Define the components in python
```python
from netflux.core.component import ComponentBuilder

def adder(op1, op2):
    return op1 + op2
    
Adder = ComponentBuilder.build(adder, inports=['op1','op2'], name="Adder")
```

As you can see components are closely modelled as functions in python. Here we defined a function `adder`. And we used `ComponentBuilder` to build `Adder`

Similarly, `Multiplier` is defined as follows.
```python
# code continued 

def mult(op1, op2):
    return op1 + op2
    
Multiplier = ComponentBuilder.build(mult,
    inports=['op1','op2'], name="Multipler")
```

#### Define the flow in python
```python
# code continued

from netflux.components.datasender import DataSender
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
```

#### Build and run the flow
```python
# ... code is continued all the way
from netflux.core.executor import Executor

executor = Executor(ticks=5) #schedule the flow 5 times
executor.build(flow)
executor.run()
```

Save the file and run with python. Make sure you have the NetFlux diretory in your python path. This file is already present as `NetFlux/netflux/test/test.py`. Open Terminal and run.
```sh
$ cd ~
$ git clone https://github.com/Mizzlr/NetFlux.git
$ echo "export PYTHONPATH=~/NetFlux:" >> ~/.bashrc
$ cd NetFlux/netflux/test
$ python test.py
```

More to come. DSL with my own Compiler. Please fork and develop this feature.
I will upload BNF grammar and specs for my DSL.

