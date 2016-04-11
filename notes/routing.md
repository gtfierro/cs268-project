Proposed Routing Protocol
=========================

## Salient Features
* optimizing for low-hop networks, as this is the most common case
* optimizing for dense mesh deployments: want to summarize data so that we don't see
  explosions of control traffic
* support for multiple border routers, transparently handled by the infrastructure
* power-aware routing: use mains powered if we can

[[This is a rough sketch of my notes]]

Abbreviations:
* RS: Router Solicitation
* RA: Router Advertisement
* LL, L2: Link Layer
* NT: Neighbor Table
* FT: Forwarding Table
* Trickle timer

## Node Coming Online

* Node sends an RS on a trickle timer until one or more unicast RA are received
    * This is similar to the DIS message in RPL
    * **Question**: going to be receiving the unicast RAs at different times: do we delay
      processing until some point in the future eto see if we hear them all?
    * **Answer**: it is not up to the routing protocol to say what the wait time is for
      seeing how many RAs we hear, but the protocol should be resilient to processing
      both prematurely and making a more informed decision after hearing more RAs
* RA should contain:
    * prefix for the mesh -- if it does not contain a prefix, then the sensor is not
      part of a mesh. We should note it in our NT, but not establish a FT default route entry
    * hop count of the sender -- this will be missing if the heard node is not part of mesh
    * a hop count of 0 means border router
    * whether or not the node is powered (right now this might be a yes/no for mains/battery)
* Node processes the RA with the **lowest hop count**:
    * this is obviously contingent on how many RAs you hear, which depends on how
      long you listen for them after sending the initial RS
* For this lowest hop count (HC) RA:
    * `my_hop_count = RA.hop_count + 1`
    * `my_default_route = RA.src_addr`
    * Add an entry in the forwarding table for the default route
* In some "neighbor" data structure, we store for each `RA.src_addr`:
    * the hop count of the neighbor
    * the power state of that neighbor
    * the duty cycle schedule of that neighbor?
    * Also: add the LL addresses of these neighbors to the forwarding table

## Receiving an RS

First off, this RS should be a bcast by the node.

When we hear an RS, it means that a node wants to join the mesh. We increment a
counter C that keeps track of the number of outstanding RS we need to respond
to. C is never less than 0, and a value of 0 means that we think the mesh is in
a stable state.

We use a Trickle Timer to keep the routing information consistent. This means
that when we hear the RS, this is inconsistent information.  We first wait for
some period (`t/2`?) to see if the mote announces its routing decision (see
below for what to do on a received reachability message in an RA). If it does,
we decrement C by 1.

When this period expires, we wait a random backoff before sending a Mesh Info
RA (bcast).  At some point later, we should hear a Reachability RA message from
the node that sent the RS. This reachability RA contains, among other things,
which parent the new node has chosen. If the node has chosen us as its parent,
then we can then propagate this information upwards towards our BR.

When we are waiting this random backoff, if we hear another Mesh Info RA bcast, then
one of two things happens:
1. If the hop count it is advertising is better (e.g. lower) than ours, then we cancel our
   timer and don't send the Mesh Info RA. Decrement C by 1.
2. Else, if our own hop count is better, then we send our own Mesh Info RA bcast. Set C to 0.

A problem that might occur is that in the worst case scenario, nodes report their Mesh Info RA bcasts
in inverse order of their hop counts, so hop count N reports first, then N-1, then N-2, etc etc until
the minimum hop count finally is broadcasted.
TODO: should we wait some time proportional to our hop count? Then its more likely that a node will
hear the correct one first. E.g. wait hop count * 500ms +/- random jitter.

**For Now**: just have every node do this independently. What we are probably going to want to do
in a denser deployment is have this node summarize its neighbors and their hop count info so that
we don't get a ton of control traffic, but we can proceed w/o that for now.

### Messages

These messages are options attached to Router Advertisement messages.

**Mesh Info RA** contains the following
* our prefix (/64)
* our hop count
* our power profile

**Reachability Info RA** contains the following
* next hop parent (lower 64 bits of address)
* (compressed) list of nodes reachable from the node
* (compressed) list of hop counts for those nodes?

### Receiving an RS (Old)
* When we hear an RS, it means that a node wants to join the mesh.
* We send a unicast RA containing:
    * our prefix (/64)
    * our hop count
    * whether or not we are powered
    * this is similar to a DIO message in RPL
* Add the node that sent the RS to our neighbor table with its hop count which
  is 1 greater than our own (`self.hop_count + 1`)
* Add LL address of heard node to our forwarding table
* If we are part of a mesh, then we want to inform the rest of the mesh about this sensor:
    * Send a RA to default route with:
    * new neighbor address (lower 64 bits)
    * hop count of new neighbor (should be `self.hop_count+1`
    * whether or not the node is powered
* This RA should be forwarded up the network to the closest border router

Note:
* we will probably want to aggregate this notification?
* We do *not* want to fragment RA/RS messages, so we need to summarize the information
  somehow to keep it within a single frame
* maybe something like:
  http://www.stoimen.com/blog/2012/02/06/computer-algorithms-data-compression-with-prefix-encoding/

## Receiving an RA

This RA message is more like a DAO. This is differentiated from the the unicast RAs
above (more like the DIOs) because it is a different option attached to an RA message.

If we receive an RA w/ this sort of routing information, we should be a member of a mesh.
If we are not, then we should probably drop this message? Or otherwise try to repair the
mesh by telling the sender that we should not have received this (it probably means that
they have us as their default route).

* Received RA from `src` contains a list of mote destinations.
* For each of these destinations `dst` we add to FT that `dst` is reachable via `src`
  with some hop count `RA.hop_count`
* Change the `src` to self, forward to the next hop up to the border router

Note:
* We may want to augment the FT with the power profile of each of these? or does this
  belong only in NT?




## Questions

The basic sequence of routing messages for an "onboarding" process for a new mote is:
1. New mote sends RS messages on some timer
2. N motes hear and respond with a unicast RA
3. Mote decides on one of these as a parent.

What happens if each of those N motes sends up reachability information of that mote w/o knowing
which one of them it chose as a parent? It could reach two border routers
