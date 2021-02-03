import scapy.all as scapy
import argparse
import sqlite3
import time
import uuid 

# Host Scanner
def scan(ip):
    arp_req_frame = scapy.ARP(pdst = ip)

    broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
    result = []
    for i in range(0,len(answered_list)):
        client_dict = {"ip" : answered_list[i][1].psrc, "mac" : answered_list[i][1].hwsrc}
        result.append(client_dict)

    return result

# Port Scanner
def syn_scan(target, ports):
	openPorts = []
	sport = scapy.RandShort()
	for port in ports:
		pkt = scapy.sr1(scapy.IP(dst=target)/scapy.TCP(sport=sport, dport=port, flags="S"), timeout=1, verbose=0)
		if pkt != None:
			if pkt.haslayer(scapy.TCP):
				if pkt[scapy.TCP].flags == 18:
					openPorts.append(port)
	return openPorts

def udp_scan(target, ports):
	openPorts = []
	for port in ports:
		pkt = scapy.sr1(scapy.IP(dst=target)/scapy.UDP(sport=port, dport=port), timeout=2, verbose=0)
		if pkt == None:
			openPorts.append(port)
		else:
			if pkt.haslayer(scapy.UDP):
				openPorts.append(port)
	return openPorts

def xmas_scan(target, ports):
	openPorts = []
	sport = scapy.RandShort()
	for port in ports:
		pkt = scapy.sr1(scapy.IP(dst=target)/scapy.TCP(sport=sport, dport=port, flags="FPU"), timeout=1, verbose=0)
		if pkt == None:
			openPorts.append(port)
	return openPorts

conn = sqlite3.connect('discovery.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS hosts(id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT NOT NULL, ip TEXT NOT NULL, mac TEXT UNIQUE NOT NULL, os TEXT, created INTEGER)')
c.execute('DROP TABLE IF EXISTS open_ports')
c.execute('CREATE TABLE open_ports(id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT NOT NULL, port INTEGER NOT NULL, created INTEGER)')
conn.commit()

targets = ["192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12"]
print("started host discovery")
for target in targets:
    scanned_output = scan(target)
    for i in scanned_output:
        osFingerprint = "X" 
        try:
            pack = scapy.IP(dst = i["ip"]) / scapy.ICMP()
            resp = scapy.sr1(pack, timeout = 2)
            if IP in resp:
                if resp.getlayer(IP).ttl < 65:
                    osFingerprint = "Linux"
                else:
                    osFingerprint = "Windows"
                # print("ttl value %d => %s " %(resp.getlayer(IP).ttl, os))
        except:
            print("An exception occurred") 
        tmp = [str(uuid.uuid1()), i["ip"], i["mac"], osFingerprint, int(time.time())]
        c.execute('INSERT OR IGNORE INTO hosts(uid, ip, mac, os, created) VALUES (?,?,?,?,?)', tmp)

print("finished host discovery")
conn.commit()

hostResults = c.execute("SELECT ip FROM hosts")
openPortsDictionary = dict()
print("started port discovery")
for hostResult in hostResults:
    openPorts = syn_scan(hostResult[0], range(1, 65535))
    openPortsDictionary[hostResult[0]] = openPorts
print("finished port discovery")

for tmpHost, tmpOpenPorts in openPortsDictionary.items():
    print(tmpHost)
    for tmpOpenPort in tmpOpenPorts:
        c.execute('INSERT INTO open_ports(ip, port, created) VALUES (?,?,?)', [tmpHost, tmpOpenPort, int(time.time())])
        print(tmpHost, ': ', tmpOpenPort)
        conn.commit()