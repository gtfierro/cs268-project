Multiple Border Routers
=======================

One of the primary requirements of the routing protocol is to support multiple
border routers. Rather than spend time discussing the many ways of doing this,
we will explain the approach we are taking.

## Prefixes

A mesh has a single prefix. All border routers will advertise the same prefix.
This is very easy to do in the common case, where the partitioning/grouping of
nodes to a single border router is straight forward.  The complexity comes when
there is a node that straddles a point in a mesh where it could reach either
border router.

You likely wouldn't put two border routers *very* close together (although we
should provide for this case), but a node might be between two nodes that talk
to two different border routers, and it may switch between which "sub mesh" it
joins based on environmental conditions or hop count. This switching may happen
at varying rates: very often or very rarely.

If we advertise a different prefix from each of these border routers, then
external traffic must somehow learn what both of those prefixes are, and
there's going to be some update latency, probably resulting in many packet
drops until the sender learns the new address.

A good approach, I think, to mitigating this is to advertise a single prefix
for all border routers on the edge of a mesh. Then, we must introduce some
external infrastructure that maintains a mapping of which nodes are reachable
via which border routers and directs incoming traffic appropriately.

## Border Router Infrastructure

I believe this approach is similar to RIP/OSPF, but we will have to check.

Border routers numbered 1 through N are `BR1, BR2, ... BRN` .
Nodes numbered 1 through M are `N1, N2, ... NM`.

Here's what a single border router might look like

```
    ||  External
    ||  Global IP
    ||  NIC
+------------------+
| Border Router #1 |
| Pfx:             |
| 2001:470::/64    |
|                  |
| List of Nodes    |
| -------------    |
| 4001, 4002, 4003 |
| 4004, etc...     |
+------------------+
    ||  Mesh prefix
    ||  and NIC
--------------------------
the mesh network is
down here
```

The border router (`BR`) would advertise the mesh prefix so that packets
intended for nodes in its contained mesh are routed to it.

Here's multiple border routers:

```

+------+             +------+
| BR 1 |             | BR 2 |
+------+             +------+
   ||      air gap      ||
--------      |      -------
  N2          |       N5   N6
N1   N3       |     N7   N8
   N4         |       N9

```

Right now we are ignoring the case of a node that can decide between the two
meshes.

In this scenario, as nodes appear, their presence is propagated up the mesh
until it reaches the border router, which then makes a note in some data structure
that it has a downward route to that node. The question now is how to handle
ingress traffic: how does it know which border router to go to?

##Border Router Routing

There's two main ways to accomplish border routing; one that requires a coordinator and one that doesn't. The benefit of using a coordinator 

### Coordinator

```
         +-------------+
         | Coordinator |
         |             |
         | Table:      |
         | Node => BR  |
         |  N2 : BR 1  |
         |  N5 : BR 2  |
         |  etc...     |
         +-------------+
             ||             
    +-------------------+  
   //                   \\     BR informs coordinator
   ||                   ||     of which nodes it can access.
+------+             +------+  Coordinator routes between the BR.
| BR 1 |             | BR 2 |
+------+             +------+
   ||      air gap      ||
--------      |      -------
  N2          |       N5   N6
N1   N3       |     N7   N8
   N4         |       N9

```

So as node reachability information is propagated up to the border router for
that sub-mesh, the BR forwards that information to the central coordinator
node, which makes sure that all of the BRs have consistent information. This
should cleanly solve the case of a node switching between border routers,
because external senders will simply send to the coordinator and it will then
figure out which BR to forward to.

### No Coordinator
```
    +-------------------+  
   //                   \\     BR informs coordinator
   ||                   ||     of which nodes it can access.
+------+             +------+  Coordinator routes between the BR.
| BR 1 |             | BR 2 |
+------+             +------+
   ||      air gap      ||
--------      |      -------
  N2          |       N5   N6
N1   N3       |     N7   N8
   N4         |       N9

```

In this design, node reachability information is sent to neighboring border routers in a similar fashion as RIP, and this way every border router in the network is aware of how to get to every node. Inbound traffic is sent downwards to the node if that border router can reach it; if not, simply send the traffic to the border router that can best reach the node, and that border router will send it downwards to the node.

###Coordinator vs No Coordinator

There are definitely some tradeoffs here. Using a coordinator leads to a much simpler design as it's more centralized and contains routing information in a single location. The downside, however, is that a single coordinator could potentially be a bottleneck if there's a lot of traffic coming in. Without a coordinator, the design is more distributed, more complicated, and will take longer to converge to a stable state. However, the upside is that there's no need  for a coordinator and external sender can send to any border router advertising that prefix.


The question now is the details of how to maintain this consistent routing
information.

## Point to point routes

Because we are optimizing for the 1-3 hop case, triangle routing (going up to
the root and then back down) does not actually introduce a large amount of
routing stretch.
