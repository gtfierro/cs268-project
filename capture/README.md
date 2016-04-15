Evaluation
==========

## Single Hop

Within the single hop domain, routing is not necessary -- devices should be
able to unicast to each other for the most part. Within a single hop domain,
the following metrics are important:

* how long does it take the routing to converge?
    * all nodes can report to BR
    * BR can report to all nodes
    * node to node is a rarer case
* how much control traffic overhead is there?
    * how many messages per second / how much bandwidth is used by the routing
      protocol to maintain this stable state?
    * does it elide completely? is there maintenance traffic?
* how resilient is this to failure?
    * 1 node fails -- what is repair time to steady state? what is control overhead of repair?
    * N nodes fails
    * border router fails

Want to run these tests both *without* traffic and with a set of traffic rates:

* 1 packet per second
* 1 packet per 2 seconds
* 1 packet per 5 seconds
* 1 packet per 10 seconds

Traffic patterns:

* nodes up to BR (probably to external server)
* BR down to nodes (probably from external server)
* node to node? maybe

Routing:
* with RPL
* with SERP
* with just unaltered ipv6 ND


## Packet Capture

Using ccsniffpiper

```
sudo python ccsniffpiper -c 22
```

Using tshark;

```
sudo tshark -i /tmp/ccsniffpiper -T "fields" -e list, of, fields

sudo tshark -t ud -i /tmp/ccsniffpiper -T "fields" -E separator=, -e frame.time -e ipv6.addr -e icmpv6.code -e icmpv6.opt.type
```

#### Code
ICMPv6.code is 0x00 for both RS and RA messages

#### Opt.Type

```c
enum {                                                                                                                                                                                                                                                                                                                        
  ND6_OPT_SLLAO = 1,                                                                                                                                                                                                                                                                                                          
  ND6_OPT_TLLAO = 2,                                                                                                                                                                                                                                                                                                          
  ND6_OPT_PREFIX = 3,                                                                                                                                                                                                                                                                                                         
  ND6_OPT_REDIRECT_HEADER = 4,                                                                                                                                                                                                                                                                                                
  ND6_OPT_MTU = 5,                                                                                                                                                                                                                                                                                                            
  ND6_SERP_MESH_INFO = 6,                                                                                                                                                                                                                                                                                                     
  ND6_SERP_MESH_ANN = 8                                                                                                                                                                                                                                                                                                       
}; 
```
