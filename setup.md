3 Border Routers

Shared Prefix: 2001:470:1:1::/64

## BR 1

NodeID: 4037
Full IP: 2001:470:1:1:212:6d02::4037
Channel: 16
Nic: enp2s0
(Tunnel)
Nic local address: 10.4.10.3
BR remote address: 10.4.10.2

```bash
# config for border router
cat <<EOF >> config1.ini
[main]
mesh-ip6-prefix=2001:470:1:1::
remote-tunnel-addr=10.4.10.3
local-tunnel-addr=10.4.10.2
local-netmask=255.255.255.0
local-gateway-addr=10.4.10.1
EOF

# setup mote
sload flash ethshield_channel16.sdb
sload borderconfig -configfile config1.ini


# setup tunnel
sudo ip tunnel del tunnel2
ip tunnel add tunnel1 mode sit remote 10.4.10.2
ip link set tunnel1 up
ip addr add 2001:470:2:2::5/64 dev tunnel1
#ip route add 2001:470:1:1::/64 dev tunnel1
ip route add 2001:470:1:1:212:6d02::4037/128 dev tunnel1
ip route add 2001:470:1:1:212:6d02::4035/128 dev tunnel1
ip route add 10.4.10.2/32 dev enp2s0
```

## BR 2

NodeID: 310b
Full IP: 2001:470:1:1:212:6d02::310b
Channel: 18
Nic: ens1
(Tunnel)
Nic local address: 10.4.10.4
BR remote address: 10.4.10.5

```bash
# config for border router
cat <<EOF >> config2.ini
[main]
mesh-ip6-prefix=2001:470:1:1::
remote-tunnel-addr=10.4.10.4
local-tunnel-addr=10.4.10.5
local-netmask=255.255.255.0
local-gateway-addr=10.4.10.1
EOF

# setup mote
sload flash ethshield_channel18.sdb
sload borderconfig -configfile config2.ini

# setup tunnel
sudo ip tunnel del tunnel2
ip tunnel add tunnel2 mode sit remote 10.4.10.5
ip link set tunnel2 up
ip addr add 2001:470:2:2::6/64 dev tunnel2
#ip route add 2001:470:1:1::/64 dev tunnel2
ip route add 2001:470:1:1:212:6d02::310b/128 dev tunnel2
ip route add 2001:470:1:1:212:6d02::3024/128 dev tunnel2
ip route add 10.4.10.5/32 dev ens1
```
