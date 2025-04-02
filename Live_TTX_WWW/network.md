Network Segments

Segment                                   Subnet

⸻

Level 4 - Enterprise (Business)           192.168.100.0/24
Level 3.5 - DMZ                           192.168.200.0/24
Level 3 - ICS Management                  192.168.210.0/24
Level 2 - SCADA / Control                 192.168.220.0/24
Level 1 - PLC / RTUs                      192.168.230.0/24
Level 0 - Field Devices                   192.168.240.0/24

Devices

Hostname                Purpose                       Mac Address           IP Address         Subnet

⸻

BizFW-01            Enterprise Firewall           00:50:56:AB:00:01     192.168.100.1      192.168.100.0/24
Router-01           Core Router                   00:50:56:AB:00:02     192.168.100.2      192.168.100.0/24
DC01                Domain Controller             00:50:56:AB:00:03     192.168.100.10     192.168.100.0/24
FS01                File Server                   00:50:56:AB:00:04     192.168.100.11     192.168.100.0/24
Win10-Office01      Office Workstation            00:50:56:AB:00:05     192.168.100.21     192.168.100.0/24
Win10-Office02      Office Workstation            00:50:56:AB:00:06     192.168.100.22     192.168.100.0/24

DMZ-FW-01           DMZ Firewall                  00:50:56:AB:00:07     192.168.200.1      192.168.200.0/24
DMZ-Proxy-01        Web Proxy / Filtering         00:50:56:AB:00:08     192.168.200.10     192.168.200.0/24
DMZ-VPN-01          VPN Gateway                   00:50:56:AB:00:09     192.168.200.11     192.168.200.0/24
DMZ-WSUS-01         Patch Management Server       00:50:56:AB:00:0A     192.168.200.12     192.168.200.0/24
DMZ-EmailRelay-01   Email Relay                   00:50:56:AB:00:0B     192.168.200.13     192.168.200.0/24

ICS-FW-01           ICS Firewall (Mgmt Ingress)   00:50:56:AB:00:0C     192.168.210.1      192.168.210.0/24
ICS-EngStation-01   Engineering Workstation       00:50:56:AB:00:0D     192.168.210.10     192.168.210.0/24
ICS-EngStation-02   Engineering Workstation       00:50:56:AB:00:0E     192.168.210.11     192.168.210.0/24
ICS-AD-01           ICS Domain Controller         00:50:56:AB:00:0F     192.168.210.12     192.168.210.0/24

ICS-FW-02           ICS Firewall (SCADA Ingress)  00:50:56:AB:00:10     192.168.220.1      192.168.220.0/24
ICS-SCADA-01        SCADA Server                  00:50:56:AB:00:11     192.168.220.10     192.168.220.0/24
ICS-HMI-01          Operator HMI Station          00:50:56:AB:00:12     192.168.220.11     192.168.220.0/24
ICS-Historian-01    ICS Historian                 00:50:56:AB:00:13     192.168.220.12     192.168.220.0/24

ICS-PLC-01          PLC for Main Pump Control     00:50:56:AB:00:14     192.168.230.10     192.168.230.0/24
ICS-PLC-02          PLC for Disinfection System   00:50:56:AB:00:15     192.168.230.11     192.168.230.0/24
ICS-RTU-01          Remote Terminal Unit          00:50:56:AB:00:16     192.168.230.12     192.168.230.0/24

ICS-Sensor-Flow01   Flow Sensor                   00:50:56:AB:00:17     192.168.240.10     192.168.240.0/24
ICS-Sensor-Pressure01 Pressure Sensor             00:50:56:AB:00:18     192.168.240.11     192.168.240.0/24
ICS-Actuator-Valve01 Valve Actuator               00:50:56:AB:00:19     192.168.240.12     192.168.240.0/24
ICS-Actuator-Pump01  Pump Actuator                00:50:56:AB:00:1A     192.168.240.13     192.168.240.0/24
ICS-Sensor-Level01   Level Sensor                 00:50:56:AB:00:1B     192.168.240.14     192.168.240.0/24

Connections

Source Hostname-IP-Port                                        Destination Hostname-IP-Port

⸻

Win10-Office01 - 192.168.100.21:53                              DC01 - 192.168.100.10:53
Win10-Office01 - 192.168.100.21:443                             FS01 - 192.168.100.11:443
Win10-Office01 - 192.168.100.21:80                              DMZ-Proxy-01 - 192.168.200.10:80
ICS-SCADA-01 - 192.168.220.10:502                               ICS-PLC-01 - 192.168.230.10:502
ICS-SCADA-01 - 192.168.220.10:502                               ICS-PLC-02 - 192.168.230.11:502
ICS-HMI-01 - 192.168.220.11:44818                               ICS-PLC-01 - 192.168.230.10:44818
ICS-HMI-01 - 192.168.220.11:44818                               ICS-PLC-02 - 192.168.230.11:44818
ICS-RTU-01 - 192.168.230.12:502                                 ICS-Sensor-Flow01 - 192.168.240.10:502
ICS-RTU-01 - 192.168.230.12:502                                 ICS-Actuator-Valve01 - 192.168.240.12:502
ICS-Historian-01 - 192.168.220.12:1433                          ICS-EngStation-01 - 192.168.210.10:1433
ICS-EngStation-01 - 192.168.210.10:3389                         ICS-SCADA-01 - 192.168.220.10:3389
DMZ-VPN-01 - 192.168.200.11:443                                 ICS-FW-01 - 192.168.210.1:443
DC01 - 192.168.100.10:389                                       ICS-AD-01 - 192.168.210.12:389
ICS-EngStation-02 - 192.168.210.11:8080                         ICS-HMI-01 - 192.168.220.11:8080
ICS-SCADA-01 - 192.168.220.10:502                               ICS-RTU-01 - 192.168.230.12:502