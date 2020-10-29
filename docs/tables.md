## Tables
Tables are the most basic structure we store in the suzieq database.
A table is the data that is gathered by a service, for instance BGP 
is the BGP data
that the bgp service collects from routers. To see what information is collected for each table, you can use the ```table describe table=<table name>``` via suzieq-cli to get the details. To see the list of tables, you can type ```help``` in suzieq-cli or run ```suzieq-cli --help```.


|         | Cumulus Linux | Arista EOS | Linux | Cisco NXOS | Juniper JunOS | SONIC |
| :---------: | :---------------: | :------------: | :-------: | :------: | :-------: | :-------: |
| Arpnd   |    yes        |      yes   | yes   | yes  |  yes  | yes |
| BGP     | yes | yes | yes | yes | yes | yes |
| Device  | yes | yes | yes | yes | yes |  yes |
| EvpnVni         | yes | no | no | yes* | yes | yes |
| Filesystem (fs) | yes | yes | yes | yes | no | yes |
| IfCounters      | yes | yes | yes | no | no | yes |
| Interfaces  | yes | yes | yes| yes | yes | yes |
| LLDP | yes | yes | yes | yes | yes | yes |
| Macs |yes | yes | yes | yes | yes | yes |
| MLAG | yes | untested | no | partial | no | no |
| Ospf |yes | yes | yes | yes | yes | yes |
| Routes | yes | yes | yes | yes | yes | yes |
| sqPoller | yes | yes | yes | yes | yes | yes |
| Topcpu | yes | yes | yes | yes | no | yes |
| Topmem | yes | yes | yes | no | no | yes |
| VLAN | yes | yes | yes | no | no | yes |
\* - EVPN support for NXOS requires version 9.3.3 or above
