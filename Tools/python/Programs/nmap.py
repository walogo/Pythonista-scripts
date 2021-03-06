from argparse import ArgumentParser
from json import dumps
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
from random import randint
import ipaddress

database = {'0': ['None', 'In programming APIs '], '1': ['TCP Port Service Multiplexer '], '5': ['Remote Job Entry'],
            '7': ['Echo Protocol'], '9': ['Discard Protocol', 'Wake-on-LAN'], '11': ['Active Users '],
            '13': ['Daytime Protocol'],
            '15': ['Previously netstat service'], '17': ['Quote of the Day '], '18': ['Message Send Protocol'],
            '19': ['Character Generator Protocol '],
            '20': ['File Transfer Protocol '], '21': ['File Transfer Protocol '], '22': ['Secure Shell '],
            '23': ['Telnet protocolâ€”unencrypted text communications'], '25': ['Simple Mail Transfer Protocol '],
            '37': ['Time Protocol'],
            '42': ['Host Name Server Protocol'], '43': ['WHOIS protocol'], '47': ['None'],
            '49': ['TACACS Login Host protocol.'],
            '51': ['Historically used for Interface Message Processor logical address management,'],
            '52': ['Xerox Network Systems '],
            '53': ['Domain Name System '], '54': ['Xerox Network Systems '], '56': ['Xerox Network Systems '],
            '58': ['Xerox Network Systems '],
            '61': ['Historically assigned to the NIFTP Based Mail protocol,'], '67': ['Bootstrap Protocol '],
            '68': ['Bootstrap Protocol '],
            '69': ['Trivial File Transfer Protocol '], '70': ['Gopher protocol'], '79': ['Finger protocol'],
            '80': ['Hypertext Transfer Protocol ', 'Quick UDP Internet Connections '], '81': ['TorPark onion routing'],
            '82': ['TorPark control'],
            '88': ['Kerberos'], '90': ['PointCast '], '101': ['NIC host name'],
            '102': ['ISO Transport Service Access Point '],
            '104': ['Digital Imaging and Communications in Medicine '], '105': ['CCSO Nameserver'],
            '107': ['Remote User Telnet Service '],
            '108': ['IBM Systems Network Architecture '],
            '109': ['Post Office Protocol, version 2 '],
            '110': ['Post Office Protocol, version 3 '],
            '111': ['Open Network Computing Remote Procedure Call '],
            '113': ['Ident, authentication service/identification protocol,', 'Authentication Service '],
            '115': ['Simple File Transfer Protocol'],
            '117': ['UUCP Mapping Project '], '118': ['Structured Query Language '],
            '119': ['Network News Transfer Protocol '],
            '123': ['Network Time Protocol '],
            '126': [
                "Formerly Unisys Unitary Login, renamed by Unisys to NXEdit. Used by Unisys Programmer's Workbench for Clearpath MCP, an IDE for Unisys MCP software development"],
            '135': ['DCE endpoint resolution', 'Microsoft EPMAP '],
            '137': ['NetBIOS Name Service, used for name registration and resolution'],
            '138': ['NetBIOS Datagram Service'],
            '139': ['NetBIOS Session Service'], '143': ['Internet Message Access Protocol '],
            '152': ['Background File Transfer Program '], '153': ['Simple Gateway Monitoring Protocol '],
            '156': ['Structured Query Language '], '158': ['Distributed Mail System Protocol '],
            '161': ['Simple Network Management Protocol '], '162': ['Simple Network Management Protocol Trap '],
            '170': ['Network PostScript print server'], '177': ['X Display Manager Control Protocol '],
            '179': ['Border Gateway Protocol '], '194': ['Internet Relay Chat '],
            '201': ['AppleTalk Routing Maintenance'], '209': ['Quick Mail Transfer Protocol'], '210': ['ANSI Z39.50'],
            '213': ['Internetwork Packet Exchange '], '218': ['Message posting protocol '],
            '220': ['Internet Message Access Protocol '], '259': ['Efficient Short Remote Operations '],
            '262': ['Arcisdms'], '264': ['Border Gateway Multicast Protocol '], '280': ['http mgmt'],
            '300': ['ThinLinc Web Access'], '308': ['Novastor Online Backup'], '311': ['Mac OS X Server Admin'],
            '318': ['PKIX Time Stamp Protocol '], '319': ['Precision Time Protocol '],
            '320': ['Precision Time Protocol '], '350': ['Mapping of Airline Traffic over Internet Protocol '],
            '351': ['MATIP type B'], '356': ['cloanto net 1 '], '366': ['On Demand Mail Relay '],
            '369': ['Rpc2portmap'], '370': ['codaauth2, Coda authentication server',
                                            "securecast1, outgoing packets to NAI's SecureCast servers"],
            '371': ['ClearCase albd'], '383': ['HP data alarm manager'], '384': ['A Remote Network Server System'],
            '387': ['AURP '], '388': ['Unidata LDM near real time data distribution protocol'],
            '389': ['Lightweight Directory Access Protocol '], '399': ['Digital Equipment Corporation DECnet '],
            '401': ['Uninterruptible power supply '], '427': ['Service Location Protocol '],
            '433': ['NNSP, part of Network News Transfer Protocol'], '434': ['Mobile IP Agent '],
            '443': ['Hypertext Transfer Protocol over TLS/SSL ', 'Quick UDP Internet Connections '],
            '444': ['Simple Network Paging Protocol '], '445': ['Microsoft DS ', 'Microsoft-DS '],
            '464': ['Kerberos Change/Set password'], '465': ['URL Rendezvous Directory for SSM ', 'Authenticated SMTP'],
            '475': ['tcpnethaspsrv, Aladdin Knowledge Systems Hasp services'],
            '491': ['GO Global remote access and application publishing software'], '497': ['Retrospect'],
            '500': ['Internet Security Association and Key Management Protocol '], '502': ['Modbus Protocol'],
            '504': ['Citadel, multiservice protocol for dedicated clients for the Citadel groupware system'],
            '510': ['FirstClass Protocol '], '512': ['Rexec, Remote Process Execution', 'comsat, together with biff'],
            '513': ['rlogin', 'Who'],
            '514': ['Remote Shell, used to execute non interactive commands on a remote system ', 'Syslog,'],
            '515': ['Line Printer Daemon '], '517': ['Talk'], '518': ['NTalk'],
            '520': ['efs, extended file name server', 'Routing Information Protocol '],
            '521': ['Routing Information Protocol Next Generation '], '524': ['NetWare Core Protocol '],
            '525': ['Timed, Timeserver'], '530': ['Remote procedure call '], '532': ['netnews'],
            '533': ['netwall, For Emergency Broadcasts'], '540': ['Unix to Unix Copy Protocol '], '542': ['commerce '],
            '543': ['klogin, Kerberos login'], '544': ['kshell, Kerberos Remote shell'], '546': ['DHCPv6 client'],
            '547': ['DHCPv6 server'], '548': ['Apple Filing Protocol '], '550': ['new rwho, new who'],
            '554': ['Real Time Streaming Protocol '], '556': ['Remotefs, RFS, rfs_server'],
            '560': ['rmonitor, Remote Monitor'], '561': ['monitor'], '563': ['NNTP over TLS/SSL '], '564': ['9P '],
            '585': ['Legacy use of Internet Message Access Protocol over TLS/SSL '],
            '587': ['email message submission'], '591': ['FileMaker 6.0 '], '593': [
        'HTTP RPC Ep Map, Remote procedure call over Hypertext Transfer Protocol, often used by Distributed Component Object Model services and Microsoft Exchange Server'],
            '601': ['Reliable Syslog Service â€” used for system logging'], '604': ['TUNNEL profile,'],
            '623': ['ASF Remote Management and Control Protocol '], '625': ['Open Directory Proxy '],
            '631': ['Internet Printing Protocol ', 'Common Unix Printing System '], '635': ['RLZ DBase'],
            '636': ['Lightweight Directory Access Protocol over TLS/SSL '],
            '639': ['MSDP, Multicast Source Discovery Protocol'], '641': ['SupportSoft Nexus Remote Command '],
            '643': ['SANity'], '646': ['Label Distribution Protocol '], '647': ['DHCP Failover protocol'],
            '648': ['Registry Registrar Protocol '], '651': ['IEEE MMS'], '653': ['SupportSoft Nexus Remote Command '],
            '654': ['Media Management System '], '655': ['Tinc VPN daemon'], '657': ['IBM RMC '],
            '660': ['Mac OS X Server administration,'], '666': ['Doom, first online first person shooter',
                                                                "airserv-ng, aircrack-ng's server for remote-controlling wireless devices"],
            '674': ['Application Configuration Access Protocol '], '688': ['REALM RUSD '],
            '690': ['Velneo Application Transfer Protocol '], '691': ['MS Exchange Routing'],
            '694': ['Linux HA high availability heartbeat'], '695': ['IEEE Media Management System over SSL '],
            '698': ['Optimized Link State Routing '], '700': ['Extensible Provisioning Protocol '],
            '701': ['Link Management Protocol '], '702': ['IRIS'], '706': ['Secure Internet Live Conferencing '],
            '711': ['Cisco Tag Distribution Protocol'],
            '712': ['Topology Broadcast based on Reverse Path Forwarding routing protocol '], '749': ['Kerberos '],
            '750': ['kerberos iv, Kerberos version IV'], '751': ['kerberos_master, Kerberos authentication'],
            '752': ['passwd_server, Kerberos password '],
            '753': ['Reverse Routing Header ', 'userreg_server, Kerberos userreg server'],
            '754': ['tell send', 'krb5_prop, Kerberos v5 slave propagation'], '760': ['krbupdate '],
            '782': ['Conserver serial console management server'], '783': ['SpamAssassin spamd daemon'],
            '800': ['mdbs daemon'], '808': ['Microsoft Net.TCP Port Sharing Service'],
            '829': ['Certificate Management Protocol'], '830': ['NETCONF over SSH'], '831': ['NETCONF over BEEP'],
            '832': ['NETCONF for SOAP over HTTPS'], '833': ['NETCONF for SOAP over BEEP'], '843': ['Adobe Flash'],
            '847': ['DHCP Failover protocol'], '848': ['Group Domain Of Interpretation '], '853': ['DNS over TLS '],
            '860': ['iSCSI '], '861': ['OWAMP control '], '862': ['TWAMP control '],
            '873': ['rsync file synchronization protocol'],
            '888': ['cddbp, CD DataBase ', 'IBM Endpoint Manager Remote Control'], '897': ['Brocade SMI S RPC'],
            '898': ['Brocade SMI S RPC SSL'], '902': ['VMware ESXi'], '903': ['VMware ESXi'],
            '953': ['BIND remote name daemon control '],
            '981': ['Remote HTTPS management for firewall devices running embedded Check Point VPN 1 software'],
            '987': ['Microsoft Remote Web Workplace, a feature of Windows Small Business Server'],
            '989': ['FTPS Protocol '], '990': ['FTPS Protocol '], '991': ['Netnews Administration System '],
            '992': ['Telnet protocol over TLS/SSL'], '993': ['Internet Message Access Protocol over TLS/SSL '],
            '994': ['None', 'Internet Relay Chat over TLS/SSL '], '995': ['Post Office Protocol 3 over TLS/SSL '],
            '1010': ['ThinLinc web based administration interface', 'Official', 'Reserved', 'Yes', 'Reserved', '1027',
                     'Official', 'Official'], '1028': ['Deprecated'], '1029': ['Microsoft DCOM services'],
            '1058': ['nim, IBM AIX Network Installation Manager '],
            '1059': ['nimreg, IBM AIX Network Installation Manager '], '1080': ['SOCKS proxy'], '1085': ['WebObjects'],
            '1098': ['rmiactivation, Java remote method invocation '],
            '1099': ['rmiregistry, Java remote method invocation '],
            '1109': ['Reserved â€“ IANA', 'Kerberos Post Office Protocol '],
            '1113': ['Licklider Transmission Protocol '],
            '1119': ["Battle.net chat/game protocol, used by Blizzard's games"], '1167': ['Cisco IP SLA '],
            '1194': ['OpenVPN'], '1198': ['The cajo project Free dynamic transparent distributed computing in Java'],
            '1214': ['Kazaa'], '1220': ['QuickTime Streaming Server administration'],
            '1234': ['Infoseek search agent', 'VLC media player default port for UDP/RTP stream'],
            '1241': ['Nessus Security Scanner'], '1270': ['Microsoft System Center Operations Manager '],
            '1293': ['Internet Protocol Security '], '1311': ['Windows RxMon.exe', 'Dell OpenManage HTTPS'],
            '1314': ['Festival Speech Synthesis System server'],
            '1337': ['neo4j-shell', 'Sails.js default port', 'WASTE Encrypted File Sharing Program'],
            '1341': ['Qubes '], '1344': ['Internet Content Adaptation Protocol'], '1352': ['IBM Lotus Notes/Domino '],
            '1360': ['Mimer SQL'], '1414': ['IBM WebSphere MQ '], '1417': ['Timbuktu Service 1 Port'],
            '1418': ['Timbuktu Service 2 Port'], '1419': ['Timbuktu Service 3 Port'],
            '1420': ['Timbuktu Service 4 Port'], '1431': ['Reverse Gossip Transport Protocol '],
            '1433': ['Microsoft SQL Server database management system '],
            '1434': ['Microsoft SQL Server database management system '],
            '1492': ["Sid Meier's CivNet, a multiplayer remake of the original Sid Meier's Civilization game"],
            '1494': ['Citrix Independent Computing Architecture '], '1500': ['IBM Tivoli Storage Manager server'],
            '1501': ['IBM Tivoli Storage Manager client scheduler'], '1503': ['Windows Live Messenger '],
            '1512': ["Microsoft's Windows Internet Name Service "], '1513': ['Garena game client'],
            '1521': ['nCUBE License Manager', 'Oracle database default listener, in future releases'],
            '1524': ['ingreslock, ingres'],
            '1527': ['Oracle Net Services, formerly known as SQL*Net', 'Apache Derby Network Server'],
            '1533': ['IBM Sametime Virtual Places Chat'], '1540': ['1C:Enterprise server agent '],
            '1541': ['1C:Enterprise master cluster manager '],
            '1542': ['1C:Enterprise configuration repository server '],
            '1545': ['1C:Enterprise cluster administration server '], '1547': ['Laplink'],
            '1550': ['1C:Enterprise debug server ', 'Gadu-Gadu '],
            '1581': ['MIL STD 2045-47001 VMF', 'IBM Tivoli Storage Manager web client', 'None', '?', '1589', 'Official',
                     'DarkComet remote administration tool '], '1626': ['iSketch'], '1627': ['iSketch'],
            '1628': ['LonTalk normal'], '1629': ['LonTalk urgent'], '1645': [
        'Early deployment of RADIUS before RFC standardization was done using UDP port number 1645. Enabled for compatibility reasons by default on Cisco'],
            '1646': ['Old radacct port,'], '1666': ['Perforce'],
            '1677': ['Novell GroupWise clients in client/server access mode'],
            '1688': ['Microsoft Key Management Service '],
            '1701': ['Layer 2 Forwarding Protocol ', 'Layer 2 Tunneling Protocol '],
            '1707': ['Windward Studios games ', 'L2TP/IPsec, for establish an initial connection'],
            '1716': ["America's Army, a massively multiplayer online game "],
            '1719': ['H.323 registration and alternate communication'], '1720': ['H.323 call signaling'],
            '1723': ['Point-to-Point Tunneling Protocol '], '1755': ['Microsoft Media Services '],
            '1761': ['Novell ZENworks'], '1783': ['Decomissioned '], '1801': ['Microsoft Message Queuing'],
            '1812': ['RADIUS authentication protocol, radius'], '1813': ['RADIUS accounting protocol, radius-acct'],
            '1863': ['Microsoft Notification Protocol '], '1880': ['Node-RED'], '1883': ['MQTT '],
            '1900': ['Simple Service Discovery Protocol '], '1935': [
        "Macromedia Flash Communications Server MX, the precursor to Adobe Flash Media Server before Macromedia's acquisition by Adobe on December 3, 2005",
        'Real Time Messaging Protocol '], '1967': ['Cisco IOS IP Service Level Agreements '],
            '1970': ['Netop Remote Control'], '1972': ['InterSystems CachÃ©'], '1984': ['Big Brother'],
            '1985': ['Cisco Hot Standby Router Protocol '], '1998': ['Cisco X.25 over TCP '],
            '2000': ['Cisco Skinny Client Control Protocol '], '2010': ['Artemis: Spaceship Bridge Simulator'],
            '2033': ['Civilization IV multiplayer'], '2049': ['Network File System '],
            '2056': ['Civilization IV multiplayer'], '2080': ['Autodesk NLM '], '2082': ['cPanel default'],
            '2083': ['Secure RADIUS Service ', 'cPanel default SSL'], '2086': ['GNUnet', 'WebHost Manager default'],
            '2087': ['WebHost Manager default SSL'], '2095': ['cPanel default web mail'],
            '2096': ['cPanel default SSL web mail'], '2100': ['Warzone 2100 multiplayer'],
            '2101': ['Networked Transport of RTCM via Internet Protocol '],
            '2102': ['Zephyr Notification Service server'], '2103': ['Zephyr Notification Service serv-hm connection'],
            '2104': ['Zephyr Notification Service hostmanager'], '2123': ['GTP control messages '], '2142': ['TDMoIP '],
            '2152': ['GTP user data messages '], '2159': ['GDB remote debug port'],
            '2181': ['EForward-document transport system', 'Apache ZooKeeper default client port'],
            '2195': ['Apple Push Notification Service'], '2196': ['Apple Push Notification Service, feedback service'],
            '2210': ['NOAAPORT Broadcast Network'], '2211': ['EMWIN'], '2221': ['ESET anti-virus updates'],
            '2222': ['EtherNet/IP implicit messaging for IO data', 'DirectAdmin Access', 'None', 'Yes', '2262',
                     'Official', 'ArmA multiplayer', 'Halo: Combat Evolved multiplayer host'],
            '2303': ['ArmA multiplayer ', 'Halo: Combat Evolved multiplayer listener'], '2305': ['ArmA multiplayer '],
            '2351': ['AIM game LAN network port'], '2368': ['Ghost '],
            '2369': ['Default for BMC Control-M/Server Configuration Agent'], '2370': [
        'Default for BMC Control-M/Server, to allow the Control-M/Enterprise Manager to connect to the Control-M/Server'],
            '2372': ['Default for K9 Web Protection/parental controls, content filtering agent'],
            '2375': ['Docker REST API '], '2376': ['Docker REST API '],
            '2377': ['Docker Swarm cluster management communications'],
            '2379': ['CoreOS etcd client communication', 'KGS Go Server'], '2380': ['CoreOS etcd server communication'],
            '2389': ['OpenView Session Mgr'], '2399': ['FileMaker Data Access Layer '],
            '2401': ['CVS version control system password-based server'], '2404': [
        'IEC 60870-5-104, used to send electric power telecontrol messages between two systems via directly connected data circuits'],
            '2424': ['OrientDB database listening for binary client connections'],
            '2427': ['Media Gateway Control Protocol '], '2447': ['ovwdbâ€”OpenView Network Node Manager '],
            '2480': ['OrientDB database listening for HTTP client connections'],
            '2483': ['Oracle database listening for insecure client connections to the listener, replaces port 1521'],
            '2484': ['Oracle database listening for SSL client connections to the listener'],
            '2535': ['Multicast Address Dynamic Client Allocation Protocol '],
            '2541': ['LonTalk/IP', 'Yes', 'Yes', '2598', 'Unofficial', 'Ultima Online servers'],
            '2638': ['SQL Anywhere database server'], '2710': ['XBT Tracker.'],
            '2727': ['Media Gateway Control Protocol '], '2775': ['Short Message Peer-to-Peer '],
            '2809': ['corbaloc:iiop URL, per the CORBA 3.0.3 specification'],
            '2811': ['gsi ftp, per the GridFTP specification'], '2827': ['I2P BOB Bridge'],
            '2944': ['Megaco text H.248'], '2945': ['Megaco binary '], '2947': ['gpsd, GPS daemon'],
            '2948': ['WAP push Multimedia Messaging Service '], '2949': ['WAP push secure '],
            '2967': ['Symantec System Center agent '],
            '3000': ['Cloud9 IDE server', 'Ruby on Rails development default', 'Meteor development default',
                     'Resilio Sync,', 'Distributed Interactive Simulation '], '3004': ['iSync'],
            '3020': ['Common Internet File System '], '3050': ['gds-db '], '3052': ['APC PowerChute Network'],
            '3074': ['Xbox LIVE and Games for Windows â€“ Live'],
            '3101': ['BlackBerry Enterprise Server communication protocol'], '3128': ['Squid caching web proxy'],
            '3225': ['Fibre Channel over IP '], '3233': ['WhiskerControl research control protocol'], '3260': ['iSCSI'],
            '3268': ['msft-gc, Microsoft Global Catalog '], '3269': ['msft-gc-ssl, Microsoft Global Catalog over SSL '],
            '3283': ['Net Assistant,', 'Apple Remote Desktop 2.0 or later'],
            '3290': ['Virtual Air Traffic Simulation '], '3305': ['Odette File Transfer Protocol '],
            '3306': ['MySQL database system'], '3313': ['Verisys file integrity monitoring software'],
            '3323': ['DECE GEODI Server'], '3332': ['Thundercloud DataPath Overlay Control'],
            '3333': ['Eggdrop, an IRC bot default port', 'Network Caller ID server', 'CruiseControl.rb'],
            '3351': ['Pervasive PSQL'], '3386': ["GTP' 3GPP GSM/UMTS CDR logging protocol"],
            '3389': ['Microsoft Terminal Server '], '3396': ['Novell NDPS Printer Agent'], '3412': ['xmlBlaster'],
            '3455': ['Resource Reservation Protocol '], '3423': ['Xware xTrm Communication Protocol'],
            '3424': ['Xware xTrm Communication Protocol over SSL'],
            '3478': ['STUN, a protocol for NAT traversal', 'TURN, a protocol for NAT traversal',
                     'STUN Behavior Discovery.'], '3479': ['PlayStation Network'], '3480': ['PlayStation Network'],
            '3483': ['Slim Devices discovery protocol', 'Slim Devices SlimProto protocol'],
            '3493': ['Network UPS Tools '], '3516': ['Smartcard Port'], '3527': ['Microsoft Message Queuing'],
            '3535': ['SMTP alternate'], '3544': ['Teredo tunneling'], '3632': ['Distcc, distributed compiler'],
            '3645': ['Cyc'], '3659': ['Apple SASL, used by Mac OS X Server Password Server', 'Battlefield 4'],
            '3667': ['Information Exchange'], '3689': ['Digital Audio Access Protocol '], '3690': ['Subversion '],
            '3702': ['Web Services Dynamic Discovery '],
            '3724': ['Some Blizzard games', 'Club Penguin Disney online game for kids'], '3725': ['Netia NA-ER Port'],
            '3768': ['RBLcheckd server daemon'], '3784': ['Bidirectional Forwarding Detection '],
            '3785': ['VoIP program used by Ventrilo'], '3799': ['RADIUS change of authorization'],
            '3804': ['Harman Professional HiQnet protocol'], '3825': ['RedSeal Networks client/server connection'],
            '3826': ['WarMUX game server', 'RedSeal Networks client/server connection'],
            '3835': ['RedSeal Networks client/server connection'],
            '3830': ['System Management Agent, developed and used by Cerner to monitor and manage solutions'],
            '3856': ['ERP Server Application used by F10 Software'], '3880': ['IGRS'],
            '3868': ['Diameter base protocol '], '3872': ['Oracle Enterprise Manager Remote Agent'],
            '3900': ['udt_os, IBM UniData UDT OS'], '3960': ['Warframe online interaction'],
            '3962': ['Warframe online interaction'], '3978': ['OpenTTD game '], '3979': ['OpenTTD game'],
            '3999': ['Norman distributed scanning service'], '4000': ['Diablo II game'],
            '4001': ['Microsoft Ants game', 'CoreOS etcd client communication'],
            '4018': ['Protocol information and warnings'],
            '4035': ['IBM Rational Developer for System z Remote System Explorer Daemon'],
            '4045': ['Solaris lockd NFS lock daemon/manager'], '4050': ['Mud Master Chat protocol '],
            '4069': ['Minger Email Address Verification Protocol'], '4070': ['Amazon Echo Dot '],
            '4089': ['OpenCORE Remote Control Service'], '4090': ['Kerio'],
            '4093': ['PxPlus Client server interface ProvideX'], '4096': ['Ascom Timeplex Bridge Relay Element '],
            '4105': ['Shofar '], '4111': ['Xgrid'], '4116': ['Smartcard-TLS'],
            '4125': ['Microsoft Remote Web Workplace administration'], '4172': ['Teradici PCoIP'],
            '4190': ['ManageSieve'], '4198': ['Couch Potato Android app'], '4201': ['TinyMUD and various derivatives'],
            '4222': ['NATS server default port'], '4226': ['Aleph One, a computer game'],
            '4242': ['Orthanc â€“ DICOM server', 'Quassel distributed IRC client'],
            '4243': ['Docker implementations, redistributions, and setups default', 'CrashPlan'], '4244': ['Viber'],
            '4303': ['Simple Railroad Command Protocol '],
            '4307': ['TrueConf Client - TrueConf Server media data exchange'], '4321': ['Referral Whois '],
            '4444': ['Oracle WebCenter Content: Content Serverâ€”Intradoc Socket port. ',
                     "Metasploit's default listener port", 'Xvfb X server virtual frame buffer service', 'None', 'Yes',
                     '4488', 'Official', 'IPSec NAT Traversal', 'None', 'Yes', '4534', 'Unofficial',
                     'default Log4j socketappender port'], '4567': ['Sinatra default server port in development mode '],
            '4569': ['Inter-Asterisk eXchange '], '4604': ['Identity Registration Protocol'],
            '4605': ['Direct End to End Secure Chat Protocol', 'None', 'Yes', 'Yes', '4664', 'Unofficial',
                     'Default for older versions of eMule'], '4711': ['eMule optional web interface'],
            '4713': ['PulseAudio sound server'], '4728': ['Computer Associates Desktop and Server Management '],
            '4730': ["Gearman's job server"], '4739': ['IP Flow Information Export'], '4747': ['Apprentice'],
            '4753': ['SIMON '], '4789': ['Virtual eXtensible Local Area Network '],
            '4840': ['OPC UA Connection Protocol '],
            '4843': ['OPC UA TCP Protocol over TLS/SSL for OPC Unified Architecture from OPC Foundation'],
            '4847': ['Web Fresh Communication, Quadrion Software & Odorless Entertainment'],
            '4848': ['Java, Glassfish Application Server administration default'], '4894': ['LysKOM Protocol A'],
            '4949': ['Munin Resource Monitoring Tool'], '4950': ['Cylon Controls UC32 Communications Port'],
            '5000': ['UPnPâ€”Windows network device interoperability', 'VTun, VPN Software', 'FlightGear multiplayer',
                     'Synology Inc. Management Console, File Station, Audio Station', 'Flask Development Webserver',
                     'Heroku console access', 'Docker Registry',
                     'AT&T U-verse public, educational, and government access ', 'High-Speed SECS Message Services',
                     'Yes', 'Yes', 'Yes', 'Yes', '5002', 'Unofficial', 'FileMaker â€“ name binding and transport'],
            '5004': ['Real-time Transport Protocol media data '],
            '5005': ['Real-time Transport Protocol control protocol '],
            '5010': ['Registered to: TelePath ', 'Yes', 'Yes', 'Yes', 'Yes', '5048', 'Official', 'Yahoo! Messenger'],
            '5051': ['ita-agent Symantec Intruder Alert'], '5060': ['Session Initiation Protocol '],
            '5061': ['Session Initiation Protocol '], '5062': ['Localisation access'],
            '5064': ['EPICS Channel Access server'], '5065': ['EPICS Channel Access repeater beacon'],
            '5070': ['Binary Floor Control Protocol '], '5084': ['EPCglobal Low Level Reader Protocol '],
            '5085': ['EPCglobal Low Level Reader Protocol '],
            '5093': ['SafeNet, Inc Sentinel LM, Sentinel RMS, License Manager, client-to-server'],
            '5099': ['SafeNet, Inc Sentinel LM, Sentinel RMS, License Manager, server-to-server'],
            '5104': ['IBM Tivoli Framework NetCOOL/Impact'], '5121': ['Neverwinter Nights'], '5124': ['TorgaNET '],
            '5125': ['TorgaNET '], '5150': ['ATMP Ascend Tunnel Management Protocol'],
            '5151': ['ESRI SDE Instance', 'ESRI SDE Remote Start'], '5154': ['BZFlag'],
            '5172': ['PC over IP Endpoint Management'], '5190': ['AOL Instant Messenger protocol.'],
            '5198': ['EchoLink VoIP Amateur Radio Software '], '5199': ['EchoLink VoIP Amateur Radio Software '],
            '5200': ['EchoLink VoIP Amateur Radio Software '], '5201': ['Iperf3 '],
            '5222': ['Extensible Messaging and Presence Protocol '],
            '5223': ['Apple Push Notification Service', 'Extensible Messaging and Presence Protocol '],
            '5228': ['HP Virtual Room Service',
                     'Google Play, Android Cloud to Device Messaging Service, Google Cloud Messaging'],
            '5242': ['Viber'], '5243': ['Viber'], '5246': ['Control And Provisioning of Wireless Access Points '],
            '5247': ['Control And Provisioning of Wireless Access Points '],
            '5269': ['Extensible Messaging and Presence Protocol '],
            '5280': ['Extensible Messaging and Presence Protocol '],
            '5281': ['Extensible Messaging and Presence Protocol '],
            '5298': ['Extensible Messaging and Presence Protocol '],
            '5310': ['Outlaws, a 1997 first-person shooter video game'], '5318': ['Certificate Management over CMS'],
            '5349': ['STUN over TLS/DTLS, a protocol for NAT traversal',
                     'TURN over TLS/DTLS, a protocol for NAT traversal', 'STUN Behavior Discovery over TLS.'], '5351': [
        'NAT Port Mapping Protocol and Port Control Protocolâ€”client-requested configuration for connections through network address translators and firewalls'],
            '5353': ['Multicast DNS '], '5355': ['Link-Local Multicast Name Resolution '],
            '5357': ['Web Services for Devices '], '5358': ['WSDAPI Applications to Use a Secure Channel '],
            '5394': ['Kega Fusion, a Sega multi-console emulator'], '5402': ['Multicast File Transfer Protocol '],
            '5405': ['NetSupport Manager'], '5412': ['IBM Rational Synergy '], '5413': ['Wonderware SuiteLink service'],
            '5417': ['SNS Agent'], '5421': ['NetSupport Manager'], '5432': ['PostgreSQL'],
            '5433': ['Bouwsoft file/webserver'], '5445': ['Cisco Unified Video Advantage'], '5480': ['VMware VAMI '],
            '5481': ["Schneider Electric's ClearSCADA "], '5495': ['IBM Cognos TM1 Admin server'],
            '5498': ['Hotline tracker server connection'], '5499': ['Hotline tracker server discovery'],
            '5500': ['Hotline control connection',
                     'VNC Remote Frame Buffer RFB protocolâ€”for incoming listening viewer'],
            '5501': ['Hotline file transfer connection'],
            '5517': ['Setiqueue Proxy server client for SETI@Home project'], '5550': ['Hewlett-Packard Data Protector'],
            '5554': ['Fastboot default wireless port'],
            '5555': ['Oracle WebCenter Content: Inbound Refineryâ€”Intradoc Socket port. ',
                     'Freeciv versions up to 2.0, Hewlett-Packard Data Protector, McAfee EndPoint Encryption Database Server, SAP, Default for Microsoft Dynamics CRM 4.0, Softether VPN default port'],
            '5556': ['Freeciv, Oracle WebLogic Server Node Manager'], '5568': ['Session Data Transport '],
            '5601': ['Kibana'], '5631': ['pcANYWHEREdata, Symantec pcAnywhere '],
            '5632': ['pcANYWHEREstat, Symantec pcAnywhere '], '5656': ['IBM Lotus Sametime p2p file transfer'],
            '5666': ['NRPE '], '5667': ['NSCA '],
            '5670': ['FILEMQ ZeroMQ File Message Queuing Protocol', 'ZRE-DISC ZeroMQ Realtime Exchange Protocol '],
            '5671': ['Advanced Message Queuing Protocol '], '5672': ['Advanced Message Queuing Protocol '],
            '5683': ['Constrained Application Protocol '], '5684': ['Constrained Application Protocol Secure '],
            '5693': ['Nagios Cross Platform Agent '], '5701': ['Hazelcast default communication port'],
            '5722': ['Microsoft RPC, DFSR '], '5718': ['Microsoft DPM Data Channel '],
            '5719': ['Microsoft DPM Data Channel '], '5723': ['System Center Operations Manager'],
            '5724': ['Operations Manager Console'], '5741': ['IDA Discover Port 1'], '5742': ['IDA Discover Port 2'],
            '5800': ['VNC Remote Frame Buffer RFB protocol over HTTP', 'ProjectWise Server'],
            '5900': ['Remote Frame Buffer protocol ', 'Virtual Network Computing '],
            '5931': ['AMMYY admin Remote Control'], '5938': ['TeamViewer remote desktop protocol'],
            '5984': ['CouchDB database server'], '5985': ['Windows PowerShell Default psSession Port'],
            '5986': ['Windows PowerShell Default psSession Port', 'None', 'Yes', 'None', 'Yes', '6050', 'Unofficial',
                     'Arcserve backup'], '6086': ['Peer Distributed Transfer Protocol '],
            '6100': ['Vizrt System', 'Ventrilo authentication for version 3'], '6101': ['Backup Exec Agent Browser'],
            '6110': ['softcm, HP Softbench CM'], '6111': ['spc, HP Softbench Sub-Process Control'],
            '6112': ['dtspcd, execute commands and launch applications remotely',
                     "Blizzard's Battle.net gaming service and some games,",
                     'Club Penguin Disney online game for kids'],
            '6113': ['Club Penguin Disney online game for kids, Used by some Blizzard games'],
            '6136': ['ObjectDB database server'], '6159': ['ARINC 840 EFB Application Control Interface'],
            '6200': ['Oracle WebCenter Content Portable: Content Server '],
            '6201': ['Oracle WebCenter Content Portable: Admin'],
            '6225': ['Oracle WebCenter Content Portable: Content Server Web UI'],
            '6227': ['Oracle WebCenter Content Portable: JavaDB'],
            '6240': ['Oracle WebCenter Content Portable: Capture'],
            '6244': ['Oracle WebCenter Content Portable: Content Serverâ€”Intradoc Socket port'],
            '6255': ['Oracle WebCenter Content Portable: Inbound Refineryâ€”Intradoc Socket port'], '6257': ['WinMX '],
            '6260': ['planet M.U.L.E.'], '6262': ['Sybase Advantage Database Server'],
            '6343': ['SFlow, sFlow traffic monitoring'], '6346': ['gnutella-svc, gnutella '],
            '6347': ['gnutella-rtr, Gnutella alternate'], '6350': ['App Discovery and Access Protocol'],
            '6379': ['Redis key-value data store'], '6389': ['EMC CLARiiON'],
            '6432': ['PgBouncerâ€”A connection pooler for PostgreSQL'], '6436': ['Leap Motion Websocket Server TLS'],
            '6437': ['Leap Motion Websocket Server'], '6444': ['Sun Grid Engine Qmaster Service'],
            '6445': ['Sun Grid Engine Execution Service', 'None', 'Yes', 'Yes', '6513', 'Official', 'Syslog over TLS'],
            '6515': ['Elipse RPC Protocol '], '6516': ['Windows Admin Center'],
            '6543': ['Pylons project#Pyramid Default Pylons Pyramid web service port'], '6556': ['Check MK Agent'],
            '6566': ['SANE ', 'None', 'None', '6600', 'Official', 'Unofficial',
                     'Microsoft Forefront Threat Management Gateway'], '6602': ['Microsoft Windows WSS Communication'],
            '6619': ['odette-ftps, Odette File Transfer Protocol '], '6622': ['Multicast FTP'],
            '6653': ['OpenFlow', 'None', 'Yes', '6679', 'Official', 'Unofficial', 'Synology Cloud station'],
            '6697': ['IRC SSL '], '6699': ['WinMX '], '6715': ['AberMUD and derivatives default port'],
            '6771': ['BitTorrent Local Peer Discovery', 'None', 'Yes', '6888', 'Official', 'Unofficial',
                     'BitTorrent part of full range of ports used most often', 'Yes', 'Yes', '6901', 'Unofficial',
                     'Unofficial', 'BitTorrent part of full range of ports used most often'],
            '6969': ['acmsoda', 'BitTorrent tracker', 'Yes', 'Yes', 'Yes', 'None', 'Yes', 'Yes', '7002', 'Unofficial',
                     'Default for BMC Software Control-M/Server and Control-M/Agent for Agent-to-Server, though often changed during installation'],
            '7006': [
                'Default for BMC Software Control-M/Server and Control-M/Agent for Server-to-Agent, though often changed during installation'],
            '7010': ['Default for Cisco AON AMC '], '7022': ['Database mirroring endpoints'],
            '7023': ['Bryan Wilcutt T2-NMCS Protocol for SatCom Modems'], '7025': ['Zimbra LMTP '],
            '7047': ['Zimbra conversion server'], '7070': ['Real Time Streaming Protocol '],
            '7133': ['Enemy Territory: Quake Wars'], '7144': ['Peercast'], '7145': ['Peercast'], '7171': ['Tibia'],
            '7262': ['CNAP '], '7272': ['WatchMe - WatchMe Monitoring'], '7306': ['Zimbra mysql '],
            '7307': ['Zimbra mysql '], '7312': ['Sibelius License Server'],
            '7396': ['Web control interface for Folding@home v7.3.6 and later'], '7400': ['RTPS '], '7401': ['RTPS '],
            '7402': ['RTPS '], '7471': ['Stateless Transport Tunneling '], '7473': ['Rise: The Vieneo Province'],
            '7474': ['Neo4J Server webadmin'], '7478': ['Default port used by Open iT Server.'],
            '7542': ['Saratoga file transfer protocol'], '7547': ['CPE WAN Management Protocol '],
            '7575': ['Populous: The Beginning server'], '7624': ['Instrument Neutral Distributed Interface'],
            '7631': ['ERLPhase'], '7634': ['hddtempâ€”Utility to monitor hard drive temperature', '7655', 'Unofficial',
                                           'BrettspielWelt BSW Boardgame Portal'], '7687': ['Bolt database connection'],
            '7717': ['Killing Floor'], '7777': ['iChat server file transfer proxy', 'Oracle Cluster File System 2',
                                                'Windows backdoor program tini.exe default',
                                                'Just Cause 2: Multiplayer Mod Server', 'Terraria default server',
                                                'San Andreas Multiplayer '],
            '7831': ['Default used by Smartlaunch Internet Cafe Administration'],
            '7880': ['PowerSchool Gradebook Server'],
            '7890': ['Default that will be used by the iControl Internet Cafe Suite Administration software'],
            '7915': ['Default for YSFlight server'],
            '7935': ['Fixed port used for Adobe Flash Debug Player to communicate with a debugger '],
            '7946': ['Docker Swarm communication among nodes'], '7990': ['Atlassian Bitbucket '],
            '8000': ['Commonly used for Internet radio streams such as SHOUTcast', 'DynamoDB Local',
                     'Django Development Webserver'], '8005': ['Tomcat remote shutdown'],
            '8006': ['Quest AppAssure 5 API'], '8007': ['Quest AppAssure 5 Engine'],
            '8008': ['Alternative port for HTTP. See also ports 80 and 8080.', 'IBM HTTP Server administration default',
                     'iCal, a calendar application by Apple'], '8009': ['Apache JServ Protocol '],
            '8010': ['Buildbot Web status page'], '8042': ['Orthanc â€“ REST API over HTTP'],
            '8069': ['OpenERP 5.0 XML-RPC protocol'], '8070': ['OpenERP 5.0 NET-RPC protocol'], '8074': ['Gadu-Gadu'],
            '8075': ['Killing Floor web administration interface'],
            '8080': ['Alternative port for HTTP. See also ports 80 and 8008.', 'Apache Tomcat',
                     'Atlassian JIRA applications'], '8088': ['Asterisk management access via HTTP'],
            '8089': ['Splunk daemon management', 'Fritz!Box automatic TR-069 configuration'],
            '8090': ['Atlassian Confluence', 'Coral Content Distribution Network '],
            '8091': ['CouchBase web administration'], '8092': ['CouchBase API'], '8111': ['JOSM Remote Control'],
            '8112': ['PAC Pacifica Coin'], '8116': ['Check Point Cluster Control Protocol'],
            '8118': ['Privoxyâ€”advertisement-filtering Web proxy'], '8123': ['Polipo Web proxy'], '8139': ['Puppet '],
            '8140': ['Puppet '], '8172': ['Microsoft Remote Administration for IIS Manager'],
            '8184': ['NCSA Brown Dog Data Access Proxy', '?', 'Yes', 'Yes', '8222', 'Unofficial',
                     'HTTPS listener for Apache Synapse'], '8245': ['Dynamic DNS for at least No-IP and DyDNS'],
            '8280': ['HTTP listener for Apache Synapse'], '8281': ['HTTP Listener for Gatecraft Plugin'], '8291': [
        'Winboxâ€”Default on a MikroTik RouterOS for a Windows application used to administer MikroTik RouterOS'],
            '8303': ['Teeworlds Server'], '8332': ['Bitcoin JSON-RPC server'],
            '8333': ['Bitcoin', 'VMware VI Web Access via HTTPS'],
            '8337': ['VisualSVN Distributed File System Service '], '8384': ['Syncthing web GUI'],
            '8388': ['Shadowsocks proxy server'],
            '8443': ['SW Soft Plesk Control Panel', 'Apache Tomcat SSL', 'Promise WebPAM SSL', 'iCal over SSL'],
            '8444': ['Bitmessage'], '8484': ['MapleStory Login Server'],
            '8500': ['Adobe ColdFusion built-in web server'], '8530': ['Windows Server Update Services over HTTP'],
            '8531': ['Windows Server Update Services over HTTPS'],
            '8580': ['Freegate, an Internet anonymizer and proxy tool'], '8629': ['Tibero database'],
            '8642': ['Lotus Notes Traveler auto synchronization for Windows Mobile and Nokia devices'], '8691': [
        'Ultra Fractal, a fractal generation and rendering software application â€“ distributed calculations over networked computers'],
            '8765': ['Default port of a local GUN relay peer that the Internet Archive'],
            '8767': ['Voice channel of TeamSpeak 2,'],
            '8834': ['Nessus, a vulnerability scanner â€“ remote XML-RPC web server'],
            '8840': ['Opera Unite, an extensible framework for web applications'],
            '8880': ['Alternate port of CDDB ', 'IBM WebSphere Application Server SOAP connector'],
            '8883': ['Secure MQTT '], '8887': ['HyperVM over HTTP'],
            '8888': ['HyperVM over HTTPS', 'Freenet web UI ', 'Default for IPython', 'MAMP'], '8889': ['MAMP'],
            '8983': ['Apache Solr'], '8997': ['Alternate port for I2P Monotone Proxy'], '8998': ['I2P Monotone Proxy'],
            '8999': ['Alternate port for I2P Monotone Proxy'],
            '9000': ['SonarQube Web Server', 'DBGp', 'SqueezeCenter web server & streaming', 'UDPCast',
                     'Play! Framework web server', 'Hadoop NameNode default port', 'PHP-FPM default port',
                     "QBittorrent's embedded torrent tracker default port"],
            '9001': ['ETL Service Manager', 'Microsoft SharePoint authoring environment',
                     'cisco-xremote router configuration', 'Tor network default', 'DBGp Proxy', 'HSQLDB default port'],
            '9002': ['Newforma Server comms'], '9006': ['De-Commissioned Port', 'Tomcat in standalone mode'],
            '9030': ['Tor often used'], '9042': ['Apache Cassandra native protocol clients'],
            '9043': ['WebSphere Application Server Administration Console secure', 'None', 'Yes', '9080', 'Official',
                     'Unofficial', 'Unofficial', 'Unofficial', 'Openfire Administration Console',
                     'SqueezeCenter control ', 'Cherokee Admin Panel'],
            '9091': ['Openfire Administration Console ', 'Transmission '],
            '9092': ['H2 ', 'Apache Kafka A Distributed Streaming Platform'],
            '9100': ['PDL Data Stream, used for printing to certain network printers'], '9101': ['Bacula Director'],
            '9102': ['Bacula File Daemon'], '9103': ['Bacula Storage Daemon'], '9119': ['MXit Instant Messenger'],
            '9150': ['Tor'], '9191': ['Sierra Wireless Airlink'], '9199': ['Avtex LLCâ€”qStats'],
            '9200': ['Elasticsearch'], '9217': ['iPass Platform Service'], '9293': ['Sony PlayStation RemotePlay'],
            '9300': ['IBM Cognos BI'], '9303': ['D-Link Shareport Share storage and MFP printers'],
            '9306': ['Sphinx Native API'], '9309': ['Sony PlayStation Vita Host Collaboration WiFi Data Transfer'],
            '9312': ['Sphinx SphinxQL'], '9332': ['Litecoin JSON-RPC server'], '9333': ['Litecoin'],
            '9339': ['Clash of Clans, a mobile freemium strategy video game'],
            '9389': ['adws, Microsoft AD DS Web Services, Powershell uses this port'],
            '9418': ['git, Git pack transfer service'],
            '9419': ['MooseFS distributed file system â€“ master control port'],
            '9420': ['MooseFS distributed file system â€“ master command port'],
            '9421': ['MooseFS distributed file system â€“ master client port'],
            '9422': ['MooseFS distributed file system â€“ Chunkservers'],
            '9425': ['MooseFS distributed file system â€“ CGI server'],
            '9443': ['VMware Websense Triton console ', 'NCSA Brown Dog Data Tilling Service'],
            '9535': ['mngsuite, LANDesk Management Suite Remote Control'],
            '9536': ['laes-bf, IP Fabrics Surveillance buffering function'],
            '9600': ['Factory Interface Network Service '], '9675': ['Spiceworks Desktop, IT Helpdesk Software'],
            '9676': ['Spiceworks Desktop, IT Helpdesk Software'], '9695': ['Content centric networking '],
            '9785': ['Viber'], '9800': ['WebDAV Source', 'WebCT e-learning portal'],
            '9875': ['Club Penguin Disney online game for kids'],
            '9898': ['Tripwireâ€”File Integrity Monitoring Software'], '9899': ['SCTP tunneling '],
            '9981': ['TVHeadend HTTP server '], '9982': ['TVHeadend HTSP server '],
            '9987': ['TeamSpeak 3 server default '], '9993': ['ZeroTier Default port for ZeroTier'],
            '9997': ['Splunk port for communication between the forwarders and indexers'],
            '9999': ['Urchin Web Analytics'], '10000': ['Network Data Management Protocol', 'BackupExec',
                                                        'Webmin, Web-based Unix/Linux system administration tool '],
            '10001': ['Ubiquiti UniFi access points broadcast to 255.255.255.255:10001 '],
            '10009': ['CrossFire, a multiplayer online First Person Shooter'], '10010': ['Open Object Rexx '],
            '10024': ['Zimbra smtp '], '10025': ['Zimbra smtp '], '10042': ['Mathoid server'],
            '10050': ['Zabbix agent'], '10051': ['Zabbix trapper'], '10080': ['Touhou fight games '],
            '10110': ['NMEA 0183 Navigational Data. Transport of NMEA 0183 sentences over TCP or UDP'],
            '10172': ['Intuit Quickbooks client'],
            '10200': ["FRISK Software International's fpscand virus scanning daemon for Unix platforms",
                      "FRISK Software International's f-protd virus scanning daemon for Unix platforms"],
            '10212': ['GE Intelligent Platforms Proficy HMI/SCADA â€“ CIMPLICITY WebView'],
            '10308': ['Lock On: Modern Air Combat'], '10480': ['SWAT 4 Dedicated Server'], '10505': ['BlueStacks '],
            '10514': ['TLS-enabled Rsyslog '], '10823': ['Farming Simulator 2011'], '10891': ['Jungle Disk '],
            '10933': ['Octopus Deploy Tentacle deployment agent'], '11001': ['metasys '],
            '11111': ['RiCcI, Remote Configuration Interface '],
            '11112': ['ACR/NEMA Digital Imaging and Communications in Medicine '], '11211': ['memcached'],
            '11214': ['memcached incoming SSL proxy'], '11215': ['memcached internal outgoing SSL proxy'],
            '11235': ['Savage: Battle for Newerth'], '11311': ['Robot Operating System master'],
            '11371': ['OpenPGP HTTP key server'], '11753': ['OpenRCT2 multiplayer'],
            '12012': ['Audition Online Dance Battle, Korea Serverâ€”Status/Version Check'],
            '12013': ['Audition Online Dance Battle, Korea Server'],
            '12035': ['Second Life, used for server UDP in-bound'],
            '12043': ['Second Life, used for LSL HTTPS in-bound'], '12046': ['Second Life, used for LSL HTTP in-bound'],
            '12201': ['Graylog Extended Log Format '], '12222': ['Light Weight Access Point Protocol '],
            '12223': ['Light Weight Access Point Protocol '],
            '12345': ['Cube World', 'Little Fighter 2', 'NetBus remote administration tool '],
            '12443': ['IBM HMC web browser management access over HTTPS instead of default port 443'],
            '12489': ['NSClient/NSClient++/NC_Net '], '12975': ['LogMeIn Hamachi '],
            '13008': ['CrossFire, a multiplayer online First Person Shooter'], '13075': ['Default'],
            '13720': ['Symantec NetBackupâ€”bprd '], '13721': ['Symantec NetBackupâ€”bpdbm '],
            '13724': ['Symantec Network Utilityâ€”vnetd '], '13782': ['Symantec NetBackupâ€”bpcd '],
            '13783': ['Symantec VOPIED protocol '], '13785': ['Symantec NetBackup Databaseâ€”nbdb '],
            '13786': ['Symantec nomdb '], '14550': ['MAVLink Ground Station Port'],
            '14567': ['Battlefield 1942 and mods'], '15000': ['psyBNC', 'Wesnoth', 'Kaspersky Network Agent'],
            '15441': ['ZeroNet fileserver'], '15567': ['Battlefield Vietnam and mods'], '15345': ['XPilot Contact'],
            '15672': ['RabbitMQ management plugin'], '16000': ['Oracle WebCenter Content: Imaging ', 'shroudBNC'],
            '16080': ['Mac OS X Server Web '], '16200': ['Oracle WebCenter Content: Content Server '],
            '16225': ['Oracle WebCenter Content: Content Server Web UI. Port though often changed during installation'],
            '16250': ['Oracle WebCenter Content: Inbound Refinery '], '16261': [
        'Project Zomboid multiplayer. Additional sequential ports used for each player connecting to server.'],
            '16300': ['Oracle WebCenter Content: Records Management '], '16384': ['CISCO Default RTP MIN'],
            '16400': ['Oracle WebCenter Content: Capture '], '16482': ['CISCO Default RTP MAX'],
            '16567': ['Battlefield 2 and mods'], '17011': ['Worms multiplayer'], '17500': ['Dropbox LanSync Protocol '],
            '18080': ['Monero P2P network communications'], '18081': ['Monero incoming RPC calls'],
            '18091': ['memcached Internal REST HTTPS for SSL'], '18092': ['memcached Internal CAPI HTTPS for SSL'],
            '18104': ['RAD PDF Service'],
            '18200': ['Audition Online Dance Battle, AsiaSoft Thailand Server status/version check'],
            '18201': ['Audition Online Dance Battle, AsiaSoft Thailand Server'],
            '18206': ['Audition Online Dance Battle, AsiaSoft Thailand Server FAM database'],
            '18300': ['Audition Online Dance Battle, AsiaSoft SEA Server status/version check'],
            '18301': ['Audition Online Dance Battle, AsiaSoft SEA Server'],
            '18306': ['Audition Online Dance Battle, AsiaSoft SEA Server FAM database'], '18333': ['Bitcoin testnet'],
            '18400': ['Audition Online Dance Battle, KAIZEN Brazil Server status/version check'],
            '18401': ['Audition Online Dance Battle, KAIZEN Brazil Server'],
            '18505': ['Audition Online Dance Battle R4p3 Server, Nexon Server status/version check'],
            '18506': ['Audition Online Dance Battle, Nexon Server'], '18605': ['X-BEAT status/version check'],
            '18606': ['X-BEAT'],
            '19000': ['Audition Online Dance Battle, G10/alaplaya Server status/version check', 'JACK sound server'],
            '19001': ['Audition Online Dance Battle, G10/alaplaya Server'],
            '19132': ['Minecraft: Bedrock Edition multiplayer server'],
            '19133': ['Minecraft: Bedrock Edition IPv6 multiplayer server'], '19150': ['Gkrellm Server'],
            '19226': ['Panda Software AdminSecure Communication Agent'],
            '19294': ['Google Talk Voice and Video connections'], '19295': ['Google Talk Voice and Video connections'],
            '19302': ['Google Talk Voice and Video connections'], '19812': ['4D database SQL Communication'],
            '19813': ['4D database Client Server Communication'], '19814': ['4D database DB4D Communication'],
            '19999': ['Distributed Network Protocolâ€”Secure '],
            '20000': ['Distributed Network Protocol ', 'Usermin, Web-based Unix/Linux user administration tool ',
                      'Used on VoIP networks for receiving and transmitting voice telephony traffic which includes Google Voice via the OBiTalk ATA devices as well as on the MagicJack and Vonage ATA network devices.'],
            '20560': ['Killing Floor'], '20595': ['0 A.D. Empires Ascendant'], '20808': ['Ableton Link'],
            '21025': ['Starbound Server '], '22000': ['Syncthing '], '22136': ['FLIR Systems Camera Resource Protocol'],
            '22222': ['Davis Instruments, WeatherLink IP'], '23073': ['Soldat Dedicated Server'],
            '23399': ['Skype default protocol'], '23513': ['Duke Nukem 3D source ports'],
            '24441': ['Pyzor spam detection network'], '24444': ['NetBeans integrated development environment'],
            '24465': ['Tonido Directory Server for Tonido which is a Personal Web App and P2P platform'],
            '24554': ['BINKP, Fidonet mail transfers over TCP/IP'],
            '24800': ['Synergy: keyboard/mouse sharing software'],
            '24842': ['StepMania: Online: Dance Dance Revolution Simulator'],
            '25565': ['Minecraft multiplayer server', 'Minecraft multiplayer server query'],
            '25575': ['Minecraft multiplayer server RCON'], '25826': ['collectd default port'],
            '26000': ["id Software's Quake server", 'EVE Online', 'Xonotic, an open-source arena shooter', 'None',
                      'Yes', '27000â€“27006', 'Unofficial', "FlexNet Publisher's License server ", 'Yes', 'No', '27016',
                      'Unofficial', 'MongoDB daemon process '], '27031': ['Steam '], '27036': ['Steam '],
            '27037': ['Steam '], '27374': ['Sub7 default.'], '27888': ['Kaillera server'],
            '27950': ['OpenArena outgoing'], '28001': ['Starsiege: Tribes'], '28015': ['Rust '],
            '28852': ['Killing Floor'], '28910': ['Nintendo Wi-Fi Connection'],
            '28960': ['Call of Duty; Call of Duty: United Offensive; Call of Duty 2; Call of Duty 4: Modern Warfare;'],
            '29000': ['Perfect World, an adventure and fantasy MMORPG'],
            '29070': ['Jedi Knight: Jedi Academy by Ravensoft'], '29920': ['Nintendo Wi-Fi Connection'],
            '30564': ['Multiplicity: keyboard/mouse/clipboard sharing software'],
            '31337': ['Back Orifice and Back Orifice 2000 remote administration tools'], '31416': ['BOINC RPC'],
            '31438': ['Rocket U2'], '31457': ['TetriNET'], '32137': ['Immunet Protect '],
            '32400': ['Plex Media Server'],
            '32764': ['A backdoor found on certain Linksys, Netgear and other wireless DSL modems/combination routers'],
            '32887': ['Ace of Spades, a multiplayer FPS video game'],
            '32976': ['LogMeIn Hamachi, a VPN application; also TCP port 12975 and SSL '], '33434': ['traceroute'],
            '33848': ['Jenkins, a continuous integration '], '34000': ['Infestation: Survivor Stories '],
            '34197': ['Factorio, a multiplayer survival and factory-building game'], '35357': ['OpenStack Identity '],
            '37008': ['TZSP intrusion detection'],
            '40000': ['SafetyNET p â€“ a real-time Industrial Ethernet protocol'],
            '43110': ['ZeroNet web UI default port'], '44405': ['Mu Online Connect Server'],
            '44818': ['EtherNet/IP explicit messaging'], '47001': ['Windows Remote Management Service '],
            '47808': ['BACnet Building Automation and Control Networks '], '49151': ['Reserved']}


# Corresponding to Target specification segment in "https://linux.die.net/man/1/nmap"
class TargetSpecification:
    def __init__(self):
        self.__targets = []

    # [target]
    def settargets(self, targets):
        self.__targets += targets

    # -iL inputfilename (Input from list)
    def inputfromlist(self, filename):
        self.__targets += [target.strip() for target in open(filename, 'r').readlines()]

    # --exclude host1[,host2[,...]] (Exclude hosts/networks)
    def exclude(self, targets):
        for host in targets:
            try:
                self.__targets.remove(host)
            except:
                pass

    # --excludefile exclude_file (Exclude list from file)
    def excludefile(self, filename):
        for host in [target.strip() for target in open(filename, 'r').readlines()]:
            try:
                self.__targets.remove(host)
            except:
                pass

    def gettargets(self):
        return list(set(self.__targets))


# Some kind of pind aproaching the ConnectionRefusedError exeption
class Ping:
    def __init__(self):
        # Only have this number of  threads active at the same time
        self.__max_number_of_threads = 500
        self.__active_threads = 0

        self.__alive_targets = []

    # Handler for thread each target
    def __ping_handler(self, target):
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(10)
        try:
            s.connect((target, 80))
            self.__alive_targets.append(target)
        except Exception as e:
            if type(e) == ConnectionRefusedError:
                self.__alive_targets.append(target)
        s.close()
        del s
        self.__active_threads -= 1
        exit(-1)

    # Only a ping function
    def ping(self, targets):
        for target in targets:
            while self.__active_threads >= self.__max_number_of_threads:
                pass
            self.__active_threads += 1
            Thread(target=self.__ping_handler, args=([target])).start()
        while self.__active_threads > 0:
            pass

    def getalive(self):
        return self.__alive_targets


# Port Scanner handler
class PortScanner:
    def __init__(self, family, protocol, port_range):
        # IP family
        self.__family = family
        # UDP or TCP
        self.__protocol = protocol
        # Port range
        self.__port_range = port_range

        self.__packet = b"bytes\n\r"
        self.__ports = {}
        self.__socket = None
        # Only have this number of  threads active at the same time
        self.__max_number_of_threads = 500
        self.__active_threads = 0

    # UDP  scanning by sending bytes to ort and  waiting for response
    def __udp_scan(self, address):
        # Use the created UDP Socket
        s = self.__socket
        try:
            s.sendto(self.__packet, address)
            for try_ in range(5):
                btes, recv_address = s.recvfrom(2048)
                if address[0] == recv_address[0]:
                    self.__ports[address[0]].append(address[1])
                    break
        except:
            pass
        self.__active_threads -= 1

    # Basic TCP scan
    def __tcp_scan(self, address):
        s = socket(self.__family, self.__protocol)
        s.settimeout(10)
        if not s.connect_ex(address):
            self.__ports[address[0]].append(address[1])
        s.close()
        del s
        self.__active_threads -= 1
        exit(-1)

    # Handler that decide which method is going to be used for each target
    def __target_handler(self, target, port):
        # Decide which method use to scan
        if self.__protocol == SOCK_STREAM:
            self.__tcp_scan((target, port))
        elif self.__protocol == SOCK_DGRAM:
            self.__udp_scan((target, port))
        else:
            pass

    # Scan all required ports of all targets
    def scan(self, targets):
        # Create a udp socket that can be used for any thread
        if self.__protocol == SOCK_DGRAM:
            self.__socket = socket(self.__family, self.__protocol)
            self.__socket.bind(('0.0.0.0', randint(0, 65535 + 1)))
            self.__socket.settimeout(10)
        # Start Scanning the targets
        for target in targets:
            self.__ports[target] = []
            for port in self.__port_range:
                while self.__active_threads >= self.__max_number_of_threads:
                    pass
                self.__active_threads += 1
                Thread(target=self.__target_handler, args=([target, port])).start()
        # Wait until all threads end
        while self.__active_threads > 0:
            pass
        # Finally close the UDP socket if it was created
        if self.__protocol == SOCK_DGRAM:
            self.__socket.close()
            del self.__socket

    def getports(self):
        return self.__ports


class Ports:
    def __init__(self):
        self.__ports = []

    # -p port ranges (Only scan specified ports)
    def portrange(self, ports):
        ranges = []
        for port in ports.split(','):
            if '-' in port:
                splited_port = port.split('-')
                ranges += list(range(int(splited_port[0]), int(splited_port[1]) + 1))
            else:
                ranges.append(int(port))
        self.__ports += ranges

    # -F (Fast (limited port) scan)
    def fast(self, n):
        self.__ports += [21, 22, 23, 80, 135, 139, 443, 445, 1000, 4444, 8080]

    def getports(self):
        return list(set(self.__ports))


class HostDiscovery:
    def __init__(self):
        self.__family = AF_INET
        self.__protocols = {}

        self.__ports = []
        self.__targets = []

        self.__results = {}

        self.__noports = False
        self.__noping = False

    # Calculate Subnet
    def __subnet(self, target):
        interface = ipaddress.IPv4Interface(target)
        network = interface.network
        for ip in network:
            yield str(ip)

    # Can be only one
    def settargets(self, targets):
        ts = []
        for target in targets:
            if "/" in target:
                ts.extend(list(self.__subnet(target)))
            else:
                ts.append(target)
        self.__targets += ts

    def setports(self, ports):
        self.__ports += ports

    # -sT (TCP connect scan)
    def enabletcp(self, n):
        if n == 0:
            if not self.__protocols.setdefault('SOCK_DGRAM', False):  # when no protocol was specified
                self.__protocols["SOCK_STREAM"] = SOCK_STREAM
        else:
            self.__protocols["SOCK_STREAM"] = SOCK_STREAM

    # -sU (UDP scans)
    def enableudp(self, n):
        if n:
            self.__protocols["SOCK_DGRAM"] = SOCK_DGRAM

    # -sn (No port scan)
    def noports(self, n):
        self.__noports = n

    # -Pn (No ping)
    def noping(self, n):
        self.__noping = n

    def scan(self):
        # Filter alive from down targets
        if not self.__noping:
            ping = Ping()
            ping.ping(self.__targets)
            self.__targets = ping.getalive()
            # When you only want to ping every target
            if self.__noports:
                return {tuple(self.__protocols.keys())[0]: {target: {} for target in self.__targets}}
        # Scan all the requested ports of the available targets
        if not self.__noports:
            for protocol in self.__protocols.keys():
                portscanner = PortScanner(self.__family, self.__protocols[protocol], self.__ports)
                portscanner.scan(self.__targets)
                self.__results[protocol] = portscanner.getports()
        return self.__results


class Processing:
    def __init__(self, results: dict, only_open):
        self.__results = results
        self.__only_open = only_open

    # Filter open ports of results
    def open_ports(self):
        if self.__only_open:
            results = {}
            for protocol in self.__results.keys():
                buffer = dict(filter(lambda element: len(element[1]), self.__results[protocol].items()))
                if len(buffer):
                    results[protocol] = buffer
            self.__results = results

    # terminal print
    def termprint(self):
        for protocol in self.__results:
            print('PROTOCOL: {}'.format(protocol))
            for target in self.__results[protocol]:
                print('\tTARGET: {}'.format(target))
                for port in self.__results[protocol][target]:
                    if database.setdefault(str(port), False):
                        print('\t\tPORT: {}; Pos_Protocols: {}'.format(port, ', '.join(database[str(port)])))
                    else:
                        print('\t\tPORT: {} {}'.format(port, 'UNKNOW'))

    # like nmap [host] > outfile.txt
    def normaloutput(self, filename):
        with open(filename, 'w') as output:
            for protocol in self.__results:
                output.write('PROTOCOL: {}\n'.format(protocol))
                for target in self.__results[protocol]:
                    output.write('\tTARGET: {}\n'.format(target))
                    for port in self.__results[protocol][target]:
                        if database.setdefault(str(port), False):
                            output.write('\t\tPORT: {} {} \n'.format(port, database[str(port)]))
                        else:
                            output.write('\t\tPORT: {} {}\n'.format(port, 'UNKNOW'))
            output.close()

    # -oJ filespec (XML output)
    def jsonoutput(self, filename):
        with open(filename, 'w') as output:
            output.write(dumps(self.__results))
            output.close()


def main(args=None):
    if not args:
        parser = ArgumentParser()

        # Target specification
        parser.add_argument('target[s]', help='Target[s] to scan', nargs='*')
        parser.add_argument('-iL', dest='inputfromlist', help='-iL filename; Get targets from file; one per line')
        parser.add_argument('--exclude', help='--exclude target,[target2]..; Remove this targets from targets',
                            nargs='*', type=list)
        parser.add_argument('--excludefile',
                            help='--excludefile filename; Exclude all the targets in a file; one per line')
        ## add new Target specification down here

        # Port specification
        parser.add_argument('-p', dest='portrange', help='-p port ranges (Only scan specified ports)', default='1-1000')
        parser.add_argument('-F', dest='fast', help='Fast port scanning', default=False, action='store_const',
                            const=True)
        ## add new port options down here

        # Options
        parser.add_argument('-sU', dest='enableudp', help='-sU (UDP scans)', default=False, action='store_const',
                            const=True)
        parser.add_argument('-sT', dest='enabletcp', help='-sT (TCP connect scan)', default=0, action='store_const',
                            const=True)  # IS a 0 because we need to difference went we want only UDP and wen we want both or only one of  them
        parser.add_argument('-Pn', dest='noping', help='Consider all targets as alive', default=False,
                            action='store_const', const=True)
        parser.add_argument('-sn', dest='noports', help='Do not scan ports', default=False, action='store_const',
                            const=True)
        ## add more options down here

        # Output options
        parser.add_argument('-oN', dest='normaloutput', help='Normal output like "nmap [host] > out.txt"')
        parser.add_argument('-oJ', dest='jsonoutput', help='Store in json file')
        parser.add_argument('--open', dest='open_ports', help='Show only the hosts with open ports', default=False,
                            action='store_const', const=True)

        args = vars(parser.parse_args())
    # Target processing handler
    ts = TargetSpecification()
    ts.settargets(args['target[s]'])
    # Port processing handler
    ps = Ports()

    keys_list = tuple(args.keys())
    first_port_option_index = None
    for number, key in enumerate(keys_list[1:]):
        if key == 'portrange':
            first_port_option_index = number + 1
            break
        if args[key]:
            getattr(ts, key)(args[key])
    first_option_index = None
    for number, key in enumerate(keys_list[first_port_option_index:]):
        if key == 'enableudp':
            first_option_index = number + first_port_option_index
            break
        if args[key]:
            getattr(ps, key)(args[key])

    targets = ts.gettargets()
    ports = ps.getports()
    # Host handler
    hs = HostDiscovery()
    hs.settargets(targets)
    hs.setports(ports)
    for key in keys_list[first_option_index:]:
        if key == 'normaloutput':
            break
        getattr(hs, key)(args[key])
    results = hs.scan()

    # Do something with the resulted scan
    processing = Processing(results, args["open_ports"])
    # Try to filter ports if theuser wants
    processing.open_ports()
    if args['jsonoutput']:
        processing.jsonoutput(args['jsonoutput'])
    elif args['normaloutput']:
        processing.normaloutput(args['normaloutput'])
    else:
        processing.termprint()


if __name__ == '__main__':
    main()
