Below is a sample large-scale, well-segmented network environment for a midstream/downstream Oil & Gas company (Pipeline and Refinery), consistent with the Purdue reference model. It contains both Business/Enterprise IT systems and ICS/OT systems, with at least 50 nodes. Use this as a scenario for an incident response tabletop exercise.

⸻

Network Segments

Segment                                   Subnet

⸻

Enterprise LAN (Level 4)                  10.0.10.0/24
DMZ (Level 3.5)                           10.0.20.0/24
ICS Control Network (Level 3)             10.0.30.0/24
ICS Supervisory Network (Level 2)         10.0.40.0/24
ICS Basic Control Network (Level 1)       10.0.50.0/24
Remote Pipeline ICS Segment               10.0.60.0/24
SIS Network                               10.0.70.0/24

⸻

Devices

Below is a list of 52 devices distributed across these segments. (MAC Addresses are sample values.)

Hostname               Purpose                          MAC Address        IP Address       Subnet

⸻

Enterprise LAN (Level 4) – 10.0.10.0/24
	1.	CORP-DC1           Primary Domain Controller        00:50:56:AA:BB:01  10.0.10.10       10.0.10.0/24
	2.	CORP-DC2           Secondary Domain Controller      00:50:56:AA:BB:02  10.0.10.11       10.0.10.0/24
	3.	CORP-FILE1         File Server                      00:50:56:AA:BB:03  10.0.10.12       10.0.10.0/24
	4.	CORP-EXCH1         Email/Exchange Server            00:50:56:AA:BB:04  10.0.10.13       10.0.10.0/24
	5.	CORP-WIN10-01      Administrative Workstation       00:50:56:AA:BB:05  10.0.10.21       10.0.10.0/24
	6.	CORP-WIN10-02      HR Workstation                   00:50:56:AA:BB:06  10.0.10.22       10.0.10.0/24
	7.	CORP-WIN10-03      Finance Workstation              00:50:56:AA:BB:07  10.0.10.23       10.0.10.0/24
	8.	CORP-WIN10-04      General Workstation              00:50:56:AA:BB:08  10.0.10.24       10.0.10.0/24
	9.	CORP-WIN10-05      General Workstation              00:50:56:AA:BB:09  10.0.10.25       10.0.10.0/24
	10.	CORP-WIN10-06      General Workstation              00:50:56:AA:BB:0A  10.0.10.26       10.0.10.0/24
	11.	CORP-WIN10-07      General Workstation              00:50:56:AA:BB:0B  10.0.10.27       10.0.10.0/24
	12.	CORP-WIN10-08      General Workstation              00:50:56:AA:BB:0C  10.0.10.28       10.0.10.0/24
	13.	CORP-WIN10-09      General Workstation              00:50:56:AA:BB:0D  10.0.10.29       10.0.10.0/24
	14.	CORP-WIN10-10      General Workstation              00:50:56:AA:BB:0E  10.0.10.30       10.0.10.0/24
	15.	CORP-Backup1       Backup Server                    00:50:56:AA:BB:0F  10.0.10.40       10.0.10.0/24

DMZ (Level 3.5) – 10.0.20.0/24
	16.	DMZ-WEB1           External Web Server              00:50:56:AA:BB:10  10.0.20.10       10.0.20.0/24
	17.	DMZ-VPN1           VPN Gateway                      00:50:56:AA:BB:11  10.0.20.11       10.0.20.0/24
	18.	DMZ-EMAIL-REL      Email Relay (SMTP)               00:50:56:AA:BB:12  10.0.20.12       10.0.20.0/24
	19.	DMZ-SIEM1          SIEM Collector/Server            00:50:56:AA:BB:13  10.0.20.13       10.0.20.0/24
	20.	DMZ-JUMP1          Jump Host for ICS                00:50:56:AA:BB:14  10.0.20.14       10.0.20.0/24

ICS Control Network (Level 3) – 10.0.30.0/24
	21.	ICS-DC1            ICS Domain Controller            00:50:56:AA:BB:15  10.0.30.10       10.0.30.0/24
	22.	ICS-APP1           SCADA Application Server         00:50:56:AA:BB:16  10.0.30.11       10.0.30.0/24
	23.	ICS-APP2           SCADA Redundant Server           00:50:56:AA:BB:17  10.0.30.12       10.0.30.0/24
	24.	ICS-HIST1          Historian Server                 00:50:56:AA:BB:18  10.0.30.13       10.0.30.0/24
	25.	ICS-HIST2          Redundant Historian              00:50:56:AA:BB:19  10.0.30.14       10.0.30.0/24
	26.	ICS-FW1            Control Network Firewall         00:50:56:AA:BB:1A  10.0.30.1        10.0.30.0/24
	27.	ICS-AV-Server      ICS AntiVirus Server             00:50:56:AA:BB:1B  10.0.30.15       10.0.30.0/24
	28.	ICS-WSUS           ICS Update Server                00:50:56:AA:BB:1C  10.0.30.16       10.0.30.0/24

ICS Supervisory Network (Level 2) – 10.0.40.0/24
	29.	ICS-HMI1           HMI Workstation                  00:50:56:AA:BB:1D  10.0.40.10       10.0.40.0/24
	30.	ICS-HMI2           HMI Workstation                  00:50:56:AA:BB:1E  10.0.40.11       10.0.40.0/24
	31.	ICS-ENGR1          Engineering Workstation          00:50:56:AA:BB:1F  10.0.40.12       10.0.40.0/24
	32.	ICS-ENGR2          Engineering Workstation          00:50:56:AA:BB:20  10.0.40.13       10.0.40.0/24
	33.	ICS-SUP-WS1        Supervisory Ops Workstation      00:50:56:AA:BB:21  10.0.40.14       10.0.40.0/24

ICS Basic Control Network (Level 1) – 10.0.50.0/24
	34.	PLC-01             PLC for Refinery Process A       00:50:56:AA:BB:22  10.0.50.10       10.0.50.0/24
	35.	PLC-02             PLC for Refinery Process B       00:50:56:AA:BB:23  10.0.50.11       10.0.50.0/24
	36.	PLC-03             PLC for Refinery Process C       00:50:56:AA:BB:24  10.0.50.12       10.0.50.0/24
	37.	RTU-01             RTU #1 (Tank Farm)               00:50:56:AA:BB:25  10.0.50.13       10.0.50.0/24
	38.	RTU-02             RTU #2 (Tank Farm)               00:50:56:AA:BB:26  10.0.50.14       10.0.50.0/24
	39.	DRIVE-01           VFD Drive Controller             00:50:56:AA:BB:27  10.0.50.15       10.0.50.0/24
	40.	DRIVE-02           VFD Drive Controller             00:50:56:AA:BB:28  10.0.50.16       10.0.50.0/24
	41.	RIO-01             Remote I/O Unit                  00:50:56:AA:BB:29  10.0.50.17       10.0.50.0/24
	42.	RIO-02             Remote I/O Unit                  00:50:56:AA:BB:2A  10.0.50.18       10.0.50.0/24
	43.	GATE-01            Protocol Gateway                 00:50:56:AA:BB:2B  10.0.50.19       10.0.50.0/24

Remote Pipeline ICS Segment – 10.0.60.0/24
	44.	PIPE-PLC1          Pipeline PLC #1                  00:50:56:AA:BB:2C  10.0.60.10       10.0.60.0/24
	45.	PIPE-PLC2          Pipeline PLC #2                  00:50:56:AA:BB:2D  10.0.60.11       10.0.60.0/24
	46.	PIPE-RTU1          Pipeline RTU                     00:50:56:AA:BB:2E  10.0.60.12       10.0.60.0/24
	47.	PIPE-HMI1          Local HMI for Pipeline           00:50:56:AA:BB:2F  10.0.60.13       10.0.60.0/24
	48.	PIPE-WAP1          Wireless AP for Field Techs      00:50:56:AA:BB:30  10.0.60.14       10.0.60.0/24
	49.	PIPE-Sensor1       Flow Sensor                      00:50:56:AA:BB:31  10.0.60.15       10.0.60.0/24
	50.	PIPE-Sensor2       Pressure Sensor                  00:50:56:AA:BB:32  10.0.60.16       10.0.60.0/24

SIS Network – 10.0.70.0/24
	51.	SIS-PLC1           Safety PLC (High Integrity)      00:50:56:AA:BB:33  10.0.70.10       10.0.70.0/24
	52.	SIS-PLC2           Safety PLC (Backup)              00:50:56:AA:BB:34  10.0.70.11       10.0.70.0/24

⸻

Connections

Below are sample notable connections and communications flows (not exhaustive). Ports are representative of typical services/protocols:

Source Hostname - IP - Port                    Destination Hostname - IP - Port

⸻

	1.	CORP-DC1 (10.0.10.10:389)   –> CORP-DC2 (10.0.10.11:389)          (Active Directory replication)
	2.	CORP-WIN10-02 (10.0.10.22:445) –> CORP-FILE1 (10.0.10.12:445)     (SMB file sharing)
	3.	DMZ-WEB1 (10.0.20.10:443)   –> CORP-EXCH1 (10.0.10.13:443)        (HTTPS OWA publishing)
	4.	DMZ-JUMP1 (10.0.20.14:3389) –> ICS-HMI1 (10.0.40.10:3389)         (RDP from DMZ jump host to ICS HMI)
	5.	ICS-HMI1 (10.0.40.10:502)   –> PLC-01 (10.0.50.10:502)           (Modbus/TCP command/monitor)
	6.	ICS-APP1 (10.0.30.11:1433)  –> ICS-HIST1 (10.0.30.13:1433)        (SQL data logging)
	7.	ICS-ENGR1 (10.0.40.12:44818)–> PLC-02 (10.0.50.11:44818)          (EtherNet/IP programming)
	8.	PIPE-RTU1 (10.0.60.12:502)  –> ICS-HIST2 (10.0.30.14:502)         (Modbus data to historian)
	9.	PIPE-HMI1 (10.0.60.13:3389) –> ICS-SUP-WS1 (10.0.40.14:3389)      (Remote HMI view for pipeline)
	10.	SIS-PLC1 (10.0.70.10:2222) –> SIS-PLC2 (10.0.70.11:2222)         (Safety PLC synchronization)

