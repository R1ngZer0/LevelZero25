Below is an **updated** Death Star network environment description, now **including Turbo Laser systems**. These changes expand the ICS Control (Level 2) and ICS Field/IO (Level 1) segments to account for the Turbo Laser batteries that protect the Death Star. Use this updated design for your Incident Response tabletop exercises.

---

## Network Segments

Segment                        | Subnet
------------------------------ | ----------------
Enterprise Network (Level 4-5)| 10.0.1.0/24
ICS DMZ (Level 3.5)           | 10.0.2.0/24
ICS Supervisory (Level 3)     | 10.0.3.0/24
ICS Control (Level 2)         | 10.0.4.0/24
ICS Field/IO (Level 1)        | 10.0.5.0/24

---

## Devices

> **Note**: MAC addresses are examples only. Replace or randomize as needed.

### **Enterprise Network (10.0.1.0/24 – Level 4-5)**

Hostname    | Purpose                       | MAC Address       | IP Address    | Subnet
----------- | ----------------------------- | ----------------- | ------------- | -------------
DS-DC01     | Primary Domain Controller     | 00:50:56:AA:01:01 | 10.0.1.10     | 10.0.1.0/24
DS-DC02     | Backup Domain Controller      | 00:50:56:AA:01:02 | 10.0.1.11     | 10.0.1.0/24
DS-FS01     | File Server                   | 00:50:56:AA:01:03 | 10.0.1.12     | 10.0.1.0/24
DS-ES01     | Email Server                  | 00:50:56:AA:01:04 | 10.0.1.13     | 10.0.1.0/24
DS-PS01     | Print Server                  | 00:50:56:AA:01:05 | 10.0.1.14     | 10.0.1.0/24
DS-SWS01    | Staff Workstation #1          | 00:50:56:AA:01:06 | 10.0.1.15     | 10.0.1.0/24
DS-SWS02    | Staff Workstation #2          | 00:50:56:AA:01:07 | 10.0.1.16     | 10.0.1.0/24
DS-SWS03    | Staff Workstation #3          | 00:50:56:AA:01:08 | 10.0.1.17     | 10.0.1.0/24
DS-IT01     | IT Admin Workstation          | 00:50:56:AA:01:09 | 10.0.1.18     | 10.0.1.0/24
DS-MGMT01   | Management Workstation        | 00:50:56:AA:01:0A | 10.0.1.19     | 10.0.1.0/24

---

### **ICS DMZ (10.0.2.0/24 – Level 3.5)**

Hostname      | Purpose                                | MAC Address       | IP Address    | Subnet
------------- | -------------------------------------- | ----------------- | ------------- | -------------
DS-FW01       | Perimeter Firewall                     | 00:50:56:AA:02:01 | 10.0.2.10     | 10.0.2.0/24
DS-REVPROXY01 | Reverse Proxy Server                   | 00:50:56:AA:02:02 | 10.0.2.11     | 10.0.2.0/24
DS-WEB01      | External Web Server                    | 00:50:56:AA:02:03 | 10.0.2.12     | 10.0.2.0/24
DS-JUMP01     | Jump Host for ICS                      | 00:50:56:AA:02:04 | 10.0.2.13     | 10.0.2.0/24
DS-DNS01      | DNS Server                             | 00:50:56:AA:02:05 | 10.0.2.14     | 10.0.2.0/24
DS-FTP01      | FTP Server                             | 00:50:56:AA:02:06 | 10.0.2.15     | 10.0.2.0/24
DS-AVUP01     | AntiVirus Update Server                | 00:50:56:AA:02:07 | 10.0.2.16     | 10.0.2.0/24
DS-SIEM01     | Security Info & Event Management       | 00:50:56:AA:02:08 | 10.0.2.17     | 10.0.2.0/24
DS-VPN01      | VPN Gateway                            | 00:50:56:AA:02:09 | 10.0.2.18     | 10.0.2.0/24
DS-IDS01      | Intrusion Detection System             | 00:50:56:AA:02:0A | 10.0.2.19     | 10.0.2.0/24

---

### **ICS Supervisory (10.0.3.0/24 – Level 3)**

Hostname           | Purpose                            | MAC Address       | IP Address    | Subnet
------------------ | ---------------------------------- | ----------------- | ------------- | -------------
DS-HMI-SUPERLASER1 | HMI for Superlaser Control         | 00:50:56:AA:03:01 | 10.0.3.10     | 10.0.3.0/24
DS-HMI-SUPERLASER2 | Backup HMI for Superlaser Control  | 00:50:56:AA:03:02 | 10.0.3.11     | 10.0.3.0/24
DS-HMI-TRACTOR1    | HMI for Tractor Beam Control       | 00:50:56:AA:03:03 | 10.0.3.12     | 10.0.3.0/24
DS-HISTORIAN01     | ICS Data Historian                 | 00:50:56:AA:03:04 | 10.0.3.13     | 10.0.3.0/24
DS-ENG-WS01        | Engineering Workstation #1         | 00:50:56:AA:03:05 | 10.0.3.14     | 10.0.3.0/24
DS-ENG-WS02        | Engineering Workstation #2         | 00:50:56:AA:03:06 | 10.0.3.15     | 10.0.3.0/24
DS-ICS-DC01        | Domain Controller for ICS          | 00:50:56:AA:03:07 | 10.0.3.16     | 10.0.3.0/24
DS-ICS-FW01        | ICS Firewall                       | 00:50:56:AA:03:08 | 10.0.3.17     | 10.0.3.0/24
DS-SCADA01         | SCADA Server                       | 00:50:56:AA:03:09 | 10.0.3.18     | 10.0.3.0/24
DS-SCADA-BACKUP01  | Backup SCADA Server                | 00:50:56:AA:03:0A | 10.0.3.19     | 10.0.3.0/24

---

### **ICS Control (10.0.4.0/24 – Level 2)**

Hostname               | Purpose                                  | MAC Address       | IP Address    | Subnet
---------------------- | ---------------------------------------- | ----------------- | ------------- | -------------
DS-PLC-SUPERLASER1     | Superlaser Main PLC                      | 00:50:56:AA:04:01 | 10.0.4.10     | 10.0.4.0/24
DS-PLC-SUPERLASER2     | Superlaser Redundant PLC                 | 00:50:56:AA:04:02 | 10.0.4.11     | 10.0.4.0/24
DS-PLC-TRACTOR1        | Tractor Beam Main PLC                    | 00:50:56:AA:04:03 | 10.0.4.12     | 10.0.4.0/24
DS-PLC-REACTOR1        | Main Reactor PLC                         | 00:50:56:AA:04:04 | 10.0.4.13     | 10.0.4.0/24
DS-PLC-SHIELD1         | Shield Generator PLC                     | 00:50:56:AA:04:05 | 10.0.4.14     | 10.0.4.0/24
DS-PLC-EXHAUST1        | Thermal Exhaust Port PLC                 | 00:50:56:AA:04:06 | 10.0.4.15     | 10.0.4.0/24
DS-PLC-TURBOLIFT1      | TurboLift Control PLC                    | 00:50:56:AA:04:07 | 10.0.4.16     | 10.0.4.0/24
DS-PLC-HYPERDRIVE1     | Auxiliary Hyperdrive PLC                 | 00:50:56:AA:04:08 | 10.0.4.17     | 10.0.4.0/24
DS-RTU-SECURITY1       | Security Systems RTU                     | 00:50:56:AA:04:09 | 10.0.4.18     | 10.0.4.0/24
DS-RTU-ENV1            | Environmental Control RTU                | 00:50:56:AA:04:0A | 10.0.4.19     | 10.0.4.0/24
**DS-PLC-TURBOLASER1** | Turbo Laser Battery #1 Control PLC       | 00:50:56:AA:04:0B | 10.0.4.20     | 10.0.4.0/24
**DS-PLC-TURBOLASER2** | Turbo Laser Battery #2 Control PLC       | 00:50:56:AA:04:0C | 10.0.4.21     | 10.0.4.0/24

---

### **ICS Field/IO (10.0.5.0/24 – Level 1)**

Hostname                     | Purpose                                         | MAC Address       | IP Address    | Subnet
---------------------------- | ----------------------------------------------- | ----------------- | ------------- | -------------
DS-SENSOR-LASERTEMP1         | Superlaser Temperature Sensor #1               | 00:50:56:AA:05:01 | 10.0.5.10     | 10.0.5.0/24
DS-SENSOR-LASERPRESS1        | Superlaser Pressure Sensor #1                  | 00:50:56:AA:05:02 | 10.0.5.11     | 10.0.5.0/24
DS-SENSOR-TRACTORTORQUE1     | Tractor Beam Torque Sensor #1                  | 00:50:56:AA:05:03 | 10.0.5.12     | 10.0.5.0/24
DS-SENSOR-REACTORFUEL1       | Reactor Fuel Level Sensor #1                   | 00:50:56:AA:05:04 | 10.0.5.13     | 10.0.5.0/24
DS-SENSOR-SHIELDINT1         | Shield Integrity Sensor #1                     | 00:50:56:AA:05:05 | 10.0.5.14     | 10.0.5.0/24
DS-SENSOR-EXHAUSTFLOW1       | Thermal Exhaust Flow Sensor #1                 | 00:50:56:AA:05:06 | 10.0.5.15     | 10.0.5.0/24
DS-SENSOR-TURBOLIFTPOS1      | TurboLift Position Sensor #1                   | 00:50:56:AA:05:07 | 10.0.5.16     | 10.0.5.0/24
DS-SENSOR-HYPERDRIVEENG1     | Hyperdrive Engaged Sensor                      | 00:50:56:AA:05:08 | 10.0.5.17     | 10.0.5.0/24
DS-VALVE-EXHAUST1            | Thermal Exhaust Valve Actuator #1              | 00:50:56:AA:05:09 | 10.0.5.18     | 10.0.5.0/24
DS-VALVE-COOLANT1            | Reactor Coolant Valve Actuator #1              | 00:50:56:AA:05:0A | 10.0.5.19     | 10.0.5.0/24
**DS-SENSOR-TURBOLASERPOWER1**| Turbo Laser Battery #1 Power Sensor            | 00:50:56:AA:05:0B | 10.0.5.20     | 10.0.5.0/24
**DS-SENSOR-TURBOLASERTEMP1** | Turbo Laser Battery #1 Temperature Sensor      | 00:50:56:AA:05:0C | 10.0.5.21     | 10.0.5.0/24
**DS-SENSOR-TURBOLASERPOWER2**| Turbo Laser Battery #2 Power Sensor            | 00:50:56:AA:05:0D | 10.0.5.22     | 10.0.5.0/24
**DS-SENSOR-TURBOLASERTEMP2** | Turbo Laser Battery #2 Temperature Sensor      | 00:50:56:AA:05:0E | 10.0.5.23     | 10.0.5.0/24

---

## Connections

Sample communication paths across the Death Star network, including new Turbo Laser devices. Add or adjust as needed for your scenarios.

Source Hostname - IP : Port              | Destination Hostname - IP : Port
---------------------------------------- | --------------------------------
DS-SWS01 - 10.0.1.15:443                 | DS-WEB01 - 10.0.2.12:443
DS-IT01 - 10.0.1.18:3389                 | DS-JUMP01 - 10.0.2.13:3389
DS-DC01 - 10.0.1.10:53                   | DS-DNS01 - 10.0.2.14:53
DS-SCADA01 - 10.0.3.18:502               | DS-PLC-SUPERLASER1 - 10.0.4.10:502
DS-PLC-TRACTOR1 - 10.0.4.12:502          | DS-SENSOR-TRACTORTORQUE1 - 10.0.5.12:502
DS-PLC-REACTOR1 - 10.0.4.13:502          | DS-SENSOR-REACTORFUEL1 - 10.0.5.13:502
DS-HISTORIAN01 - 10.0.3.13:1433          | DS-SCADA01 - 10.0.3.18:1433
DS-ENG-WS01 - 10.0.3.14:3389             | DS-JUMP01 - 10.0.2.13:3389
DS-SWS02 - 10.0.1.16:445                 | DS-FS01 - 10.0.1.12:445
DS-SIEM01 - 10.0.2.17:514                | DS-IDS01 - 10.0.2.19:514
**DS-SCADA01 - 10.0.3.18:502             | DS-PLC-TURBOLASER1 - 10.0.4.20:502**
**DS-PLC-TURBOLASER1 - 10.0.4.20:502     | DS-SENSOR-TURBOLASERPOWER1 - 10.0.5.20:502**
**DS-PLC-TURBOLASER2 - 10.0.4.21:502     | DS-SENSOR-TURBOLASERTEMP2 - 10.0.5.23:502**

---

### How to Use

1. **Identify Critical Assets**: The Superlaser and Turbo Laser control PLCs are key ICS assets.  
2. **Simulate Threats**: Consider potential infiltration from the Enterprise network (Level 4-5) through the ICS DMZ (Level 3.5) into Level 2 or 1 ICS devices.  
3. **Plan IR Scenarios**: Evaluate detection, containment, and recovery strategies for system compromise—especially focusing on the ICS domain and the newly added Turbo Laser control systems.  
4. **Test Communication Paths**: Review newly introduced connections for the Turbo Laser systems to ensure you have proper monitoring, logging, and segmentation.  

Use this updated environment to include Turbo Laser system defenses in your tabletop exercise, ensuring your IR processes account for the unique operational requirements of these critical defensive batteries.