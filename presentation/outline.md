- decide on the compression
- calculate how many nodes can be compressed w/n a message w/o fragmentation

Outline
=======

- send me your presentation slides no later than 10am on April 20
- aim for 15 minutes of presentation time 
- make sure you devote enough time to clearly defining your problem and
  motivating why the problem is interesting (e.g., spend as much as ~50% of
  your time on problem definition/background/motivation and the remaining 50%
  on your solution and results)



## Background and Motivation

people should be familiar with wireless sensor networks, but good to
go over the features
- low memory (64 kbits of ram)
- low bandwidth (250 kbits / sec on 802.15.4)
- duty cycled

We want to establish the traffic patterns and applications are for routing.
Then we want to talk about where these deployments maybe taking place. The
answer is in homes and rooms and buildings, not gigantic networks apanning
miles or acres. A great deal of wireless sensor Network research has focused on
creating and maintaining large A great deal of wireless internet work research
has focused on creating and maintaining large many hop large diameter networks.
However, this is not the common case.  

Given the power and the range of today's modern radios comma the common case of
mesh Networks in homes and buildings is 1 - 3 hop Networks. At these ranges in
density, awareness of the broadcast medium in the design of routing protocol is
important. Specifically, too much control traffic over head can make it
difficult for applications to find bandwidth to send data. Also, waking up more
often to send reduces the lifetime of a network.

Now's a good time to go over the RPL standard and talk about why it doesn't
meet these goals.  Through the context of RPL we also build up how a WSN
routing protocol works: discover mesh, prefix, stateless addressing, the kinds
of messages. 

Talk about all of the features that RPL offers: do we really need these? Lots
of control messages because you are paying the price for all of these features
even if you do not use them.

Furthermore, RPL was not designed specifically for WSNs. People use it for PLC.
Duplicates functionality that is already in standards: IPv6 ND. Question here
of how much we overlap with IP is Dead. Don't want to repeat too much.

Given this, what are

## Goals for Routing Protocol:
- control traffic should scale w/ size of network
- control traffic shouldd quiesce as the network converges to steady state
- want to support multiple border routers
- want to motes to incorporate power profile of neighbors in routing decisions

- **Control traffic should scale with the size of the network**: 
    - deployments that fit within a single link-local broadcast domain should
      not require any routing overhead. 
    - The complexity and number of control messages needed to maintain a
      multihop network should only grow as the network grows.

- **Control traffic should quiesce as the network converges to steady state**:
  - the existing RPL standard does not provide guidelines for how often control
    messages should be sent, leading to wasted bandwidth and unnecessary mote
    wakeups. 
  - We will likely use a Trickle~\cite{levis2011trickle} timer here which would
    provide a simple solution that is both energy efficient and scalable.

- **Support multiple border routers**: 
    - to maintain small diameters and increase reliability, the routing
      architecture should support the existence of multiple border routers.
      There is some discussion required here as to whether border routers
      should advertise different prefixes, advertise the same prefix and use
      external routing infrastructure for inbound traffic, or have each mote
      support multiple interfaces/addresses.
    - also explain the trade offs of different approaches of handling multiple
      border routers.
    - show a simple example of the border routers at work and the logic behind
      them

- **Make use of neighbors' power characteristics in routing**: 
  - since the nodes are duty-cycled, they should learn their neighbors'
    schedules and route through powered nodes when/if possible. 
  - This will leverage existing work like B-MAC~\cite{polastre2004versatile}
    and the new 802.15.4e standard.

## What Routing Needs To Do

Here we establish context for *why* we are doing the things we are doing.

1. Mote needs to discover its prefix:
    ipv6 addresses for lowpans divided up into: 
    `<64 bit shared prefix for mesh> : <48 bit MAC> : <16 bit ID>`
2. Build Upward routes:
    discover and decide upon a "preferred parent" for a default route
3. Build Downward routes:
    Construct a Neighbor Table of other motes w/n the same bcast domain
    Construct a table of motes reachable through those neighbors
4. Point to Point?
    in 1-3 hops, "triangle routing" is acceptable
5. Support multiple BRs:
    Helps maintain 1-3 hop
    Different prefixes? Same prefix? How to keep reachability information consistent?

