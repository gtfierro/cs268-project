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
