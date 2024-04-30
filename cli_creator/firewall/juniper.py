
import ipaddress

def network_address(ip_network_str):
    network = ipaddress.ip_network(ip_network_str, strict=False)
    return str(network.network_address) + '/' + str(network.prefixlen)

def j_creat_policy(policyname, fromiplist, toiplist, tcpport, udpport, fromzone, tozone, action):
#define application and policy
    command = ""
    if tcpport:
        for tcp in tcpport.split(','):
            if tcp == '':
                pass
            elif tcp =='any':
                command += "set security policies from-zone %s to-zone %s policy %s match application junos-tcp-any"%(fromzone,tozone,policyname) + '\n'
            else:
                command += "set applications application TCP-%s protocol tcp destination-port %s"%(tcp,tcp) + '\n'
                command += "set security policies from-zone %s to-zone %s policy %s match application TCP-%s"%(fromzone,tozone,policyname,tcp) + '\n'
    else:pass
    if udpport:
        for udp in udpport.split(','):
            if udp == '':
                pass
            elif udp == 'any':
                command += "set security policies from-zone %s to-zone %s policy %s match application junos-udp-any"%(fromzone,tozone,policyname) + '\n'
            else:
                command += "set applications application UDP-%s protocol udp destination-port %s"%(udp,udp) + '\n'
                command += "set security policies from-zone %s to-zone %s policy %s match application UDP-%s"%(fromzone,tozone,policyname,udp) + '\n'
    else:pass
    
    if fromiplist: 
        for fromip in fromiplist.split(','):
            if '-' in fromip:
                startip = fromip.split('-')[0]
                endip = fromip.split('-')[-1]
                startip_1 = startip.split('.')[0]
                startip_2 = startip.split('.')[1]
                startip_3 = startip.split('.')[2]
                startip_4 = startip.split('.')[-1]
                while True:
                    startip_4 = str(startip_4)
                    command += "set security address-book global address %s/32 %s/32"%((startip_1+'.'+startip_2+'.'+startip_3+'.'+startip_4),(startip_1+'.'+startip_2+'.'+startip_3+'.'+startip_4)) + '\n'
                    command +=  "set security policies from-zone %s to-zone %s policy %s match source-address %s/32"%(fromzone,tozone,policyname,(startip_1+'.'+startip_2+'.'+startip_3+'.'+startip_4)) + '\n'
                    startip_4 = int(startip_4)
                    startip_4 += 1
                    if int(startip_4) > int(endip.split('.')[-1]):
                        break
            elif fromip == 'any':
                command += "set security policies from-zone %s to-zone %s policy %s match source-address any"%(fromzone,tozone,policyname) + '\n'
            elif '/' in fromip:
                fromip = network_address(fromip)
                command += "set security address-book global address %s %s"%(fromip,fromip) + '\n'
                command += "set security policies from-zone %s to-zone %s policy %s match source-address %s"%(fromzone,tozone,policyname,fromip) + '\n'
            else:
                command += "set security address-book global address %s/32 %s/32"%(fromip,fromip) + '\n'
                command += "set security policies from-zone %s to-zone %s policy %s match source-address %s/32"%(fromzone,tozone,policyname,fromip) + '\n'
    else:pass
    
    if toiplist:
        for toip in toiplist.split(','):
            if '-' in toip:
                startip = toip.split('-')[0]
                endip = toip.split('-')[-1]
                startip_1 = startip.split('.')[0]
                startip_2 = startip.split('.')[1]
                startip_3 = startip.split('.')[2]
                startip_4 = startip.split('.')[-1]
                while True:
                    startip_4 = str(startip_4)
                    command += "set security address-book global address %s/32 %s/32"%((startip_1+'.'+startip_2+'.'+startip_3+'.'+startip_4),(startip_1+'.'+startip_2+'.'+startip_3+'.'+startip_4)) + '\n'
                    command += "set security policies from-zone %s to-zone %s policy %s match destination-address %s/32"%(fromzone,tozone,policyname,(startip_1+'.'+startip_2+'.'+startip_3+'.'+startip_4)) + '\n'
                    startip_4 = int(startip_4)
                    startip_4 += 1
                    if int(startip_4) > int(endip.split('.')[-1]):
                        break
            elif toip == 'any':
                command += "set security policies from-zone %s to-zone %s policy %s match destination-address any"%(fromzone,tozone,policyname) + '\n'
            elif '/' in toip:
                toip = network_address(toip)
                command += "set security address-book global address %s %s"%(toip,toip) + '\n'
                command += "set security policies from-zone %s to-zone %s policy %s match destination-address %s"%(fromzone,tozone,policyname,toip) + '\n'
            else:
                command += "set security address-book global address %s/32 %s/32"%(toip,toip) + '\n'
                command += "set security policies from-zone %s to-zone %s policy %s match destination-address %s/32"%(fromzone,tozone,policyname,toip) + '\n'
    else:pass
    try:
        if action:
                command += "set security policies from-zone %s to-zone %s policy %s then %s" %(fromzone, tozone, policyname, action)
    except:pass
    return command

if __name__ =='__main__':
    policyname = 'test'
    fromiplist = '192.168.1.1'
    toiplist = '223.5.5.5'
    tcpport = '53'
    udpport = '53'
    fromzone = 'trust'
    tozone = 'untrust'
    action = 'permit'
    command = j_creat_policy(policyname, fromiplist, toiplist, tcpport, udpport, fromzone, tozone, action)
    print(command)