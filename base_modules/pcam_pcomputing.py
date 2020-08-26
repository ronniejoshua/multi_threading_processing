
"""
Partitioning
------------
Partitioning, is about breaking down the problem into discreet chunks of work that can be distributed to
multiple tasks. At this beginning stage, we're not concerned with practical issues like the number of
processors in our computer. We'll consider that later. For now, our goal is to simply decompose the problem
at hand into as many small tasks as possible, and there are two basic ways to approach partitioning:
    1. Domain Decomposition
    2. Functional Decomposition

Domain Decomposition
--------------------
Domain, or data decomposition, focuses on dividing the data associated with the problem into lots of
small and, if possible, equally-sized partitions. The secondary focus is then to consider the computations
to be performed and associating them with that partition data.

Different ways of decomposing data can have different advantages and disadvantages depending on the problem and
hardware involved. Once we've partitioned the data, we can turn our focus towards the processing that needs to
be applied to each section.

Functional Decomposition
------------------------
The other form of decomposition, functional decomposition, provides a different, complimentary way to break down
the problem. Rather than focusing on the data being manipulated, functional decomposition begins by considering
all of the computational work that a program needs to do. And then divides that into separate tasks that perform
different portions of the overall work. The data requirements for those tasks are a secondary consideration.

Note
----
Keep in mind that domain and functional decomposition are complimentary ways to approach a problem. And it's
natural to use a combination of the two. Programmers typically start with domain decomposition because it forms
a foundation for a lot of parallel algorithms. But sometimes taking a functional approach instead can provide
different ways of thinking about these problems. It's worth taking the time to explore alternative perspectives.
It can reveal problems or opportunities for better optimization that would be missed by considering data alone.
by considering data alone.
"""


"""
Communication
-------------
After decomposing the problem into separate tasks, the next step in our design process is to establish communication, 
which involves figuring out how to coordinate execution and share data between the tasks. 

Some problems can be decomposed in ways that do not require tasks to share data between them. 

Although our separate tasks can execute concurrently, They are sometimes no longer completely independent 
from each other. In this type of situation, we might establish a network of direct point-to-point communication 
links between neighboring tasks. For each link, one task is acting as the sender, or producer of data, and the other 
task that needs it is the receiver or consumer. 

That type of local point-to-point communication can work when each task only needs to communicate with a small number 
of other tasks. - But if your tasks need to communicate with a larger audience, then you should consider other 
structures for sharing data between multiple tasks. You might have one task that broadcasts the same data out to all 
members of a group or collective, or it scatters different pieces of the data out to each of the members to process. 
Afterwards, that task can gather all of the individual results from the members of the group and combine them for a 
final output. 

When operations require this type of global communication, it's important to consider how it can grow and scale. 
Simply establishing point-to-point pairs may not be sufficient. If one task is acting as a centralized manager to 
coordinate operations with a group of distributed workers, as the number of workers grow, the communication workload 
of a central manager grows too, and may turn it into a bottleneck. 

This is where strategies like divide and conquer can be useful. in a way that reduces the burden on any one task. 
These are just a few high-level structures to serve as a starting point as you begin to plan the communications 
for a parallel program. 

A few other factors to consider include whether the communications will be synchronous or asynchronous. Synchronous 
communications are sometimes called blocking communications, because all tasks involved have to wait until the 
entire communication process is completed to continue doing other work. That can potentially result in tasks spending 
a lot of time waiting on communications instead of doing useful work. 

Asynchronous communications, on the other hand, are often referred to as non-blocking communications, because after 
a task sends an asynchronous message, it can begin doing other work immediately, regardless of when the receiving 
task actually gets that message. You should also consider the amount of processing overhead a communication strategy 
involves, because the computer cycles spent sending and receiving data are cycles not being spent processing it. 

Latency is another factor to consider, the time it takes for a message to travel from point A to B, expressed in 
units of time, like microseconds. And bandwidth, which is the amount data that can be communicated per unit of time, 
expressed in some unit of bytes per second. Now if you're just writing basic multi-threaded or multi-processed 
programs to run on a desktop computer, some of these factors like latency and bandwidth, probably aren't major 
concerns, because everything is running on the same physical system. 

But as you develop larger programs that distribute their processing across multiple physical systems, those 
inter-system communication factors can have a significant impact on the overall performance. can have a significant 
impact on the overall performance.
"""

"""
Agglomeration

In the first two stages of our parallel design process, we partitioned a problem into a set of separate tasks and 
established communication to provide those tasks with the data they needed. We looked at different ways to decompose 
the problem and focused on defining as many small tasks as possible. That approach helped us consider a wide range of 
opportunities for parallel execution. 

However, the solution it created is not very efficient, especially if there are way more tasks than there are 
processors on the target computer. - Now it's time to turn our thinking from abstract to something concrete and 
modify that design to execute more efficiently on a specific computer. 

In the third agglomeration stage, we'll revisit the decisions we made during the partitioning and communication 
stages to consider changes to make our program more efficient, combining some of those tasks and possibly replicating 
data or computations. 

As a parallel program executes, periods of time spent performing usable computations are usually separated by periods 
of communication and synchronization events. The concept of granularity gives us a qualitative measure of the time 
spent performing computation over the time spent on communication. 

Parallelism can be classified into two categories based on the amount of work performed by each task. 

With fine-grained parallelism, a program is broken down into a large number of small tasks. The benefit is that 
lots of small tasks can be more evenly distributed among processors to maximize their usage, a concept called 
load balancing. The downside is that having lots of tasks increases the overhead for communication and 
synchronization, so it has a lower computation-to-communication ratio. 

On the other end of the spectrum, coarse-grained parallelism splits the program into a small number of large tasks. 
The advantage is that it has a much lower communication overhead, so more time can be spent on computation. 
However, the larger chunks of work may produce a load imbalance, where certain tasks process the bulk of data, 
while others remain idle. 

Those are two extremes and the most efficient solution will be dependent on the algorithm and the hardware on 
which it runs. For most general purpose computers, that's usually in the middle with some form of medium-grained 
parallelism. 

A well-designed parallel program should adapt to changes in the number of processors, so keep flexibility in mind. 
Try not to incorporate unnecessary, hard-coded limits on the number of tasks in the program. If possible, use 
compiled time or run time parameters to control the granularity.
"""

"""
Mapping
The fourth and final stage of our parallel design process is mapping. And this is where we specify where each 
of the tasks we established will actually execute. Now this mapping stage does not apply if you're only using a 
single process or system because there's only one place to execute the program or if you're using a system with 
automated task scheduling. 

So if I'm just writing programs to run on a desktop computer, like the examples we've shown you throughout this 
course, mapping isn't even a consideration. The operating system handles scheduling threads to execute on specific
processor cores, so that's out of our hands. 

Mapping really becomes a factor if you're using a distributed system or specialized hardware with lots of parallel 
processors for large-scale problems, like in scientific computing applications. The usual goal of a mapping algorithm 
is to minimize the total execution time of the program, and there are two main strategies to achieve that goal. 
You can place tasks that are capable of executing concurrently on different processors to increase the overall 
concurrency, or you can focus on placing tasks that communicate with each other frequently on the same processor 
to increase locality by keeping them close together. 

In some situations, it might be possible to leverage both of those approaches, but more often, they'll conflict 
with each other, which means the design will have to make trade-offs. There's a variety of different load-balancing 
algorithms that use domain decomposition and agglomeration techniques to map task execution to processors. 

If the number of tasks or the amount of computation and communication per task changes as the program executes, 
that makes the problem more complex, and it may require dynamic load-balancing techniques that periodically 
determine a new mapping strategy. 

Designing a good mapping algorithm is highly dependent on both the program structure and the hardware it's running 
on, and that gets beyond the scope of this course. 


So to summarize the four-step parallel design process, we start by taking a problem and partitioning or decomposing 
it into a collection of tasks. Then we evaluate the communication necessary to synchronize and share data between 
those tasks. After that, we agglomerate or combine those tasks into groups to increase the program's efficiency with 
certain hardware in mind. And then finally, those tasks get mapped to specific processors to actually execute.
"""