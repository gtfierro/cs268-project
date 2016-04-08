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

