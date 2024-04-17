class FirewallConfigurator:
    def __init__(self, name, src_if, des_if, src_address, des_address, tcp_port, udp_port, log):
        self.name = name
        self.src_if = src_if
        self.des_if = des_if
        self.src_address = src_address
        self.des_address = des_address
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.log = log
    def subnet_mask(self, prefix):
        """
        计算子网掩码
        :param prefix: 子网掩码的前缀长度，如 /24
     :return: 子网掩码字符串，如 '255.255.255.0'
        """
    # 先将前缀长度转换为整数
        prefix_length = int(prefix.strip('/'))

    # 计算子网掩码的四个字节
        mask = [0, 0, 0, 0]
        for i in range(prefix_length // 8):
            print(i)
            mask[i] = 255
            print(mask)
        remaining_bits = prefix_length % 8
        print(remaining_bits)
        if remaining_bits > 0:
            mask[prefix_length // 8] = 256 - (1 << (8 - remaining_bits))
            print(mask)
    # 将子网掩码转换为字符串形式
        mask_str = '.'.join(map(str, mask))

        return mask_str
    def configure_address(self):
        command = "config firewall address\n"
        for i in self.src_address.split(','):
            if i == "all":
                pass
            elif '/' in i:
                edit = "edit %s" % i
                subnet = "set subnet %s %s" % (i.split('/')[0],self.subnet_mask(i.split('/')[-1]))
                next = "next"
                command += edit + '\n' + subnet + '\n' + next + '\n'
            elif i =="":
                pass
            else:
                edit = "edit %s/32" % i
                subnet = "set subnet %s 255.255.255.255" % i
                next = "next"
                command += edit + '\n' + subnet + '\n' + next + '\n'
        for j in self.des_address.split(','):
            if j == 'all':
                pass
            elif '/' in j:
                edit = "edit %s" % j
                subnet = "set subnet %s %s" % (j.split('/')[0],self.subnet_mask(j.split('/')[-1]))
                next = "next"
                command += edit + '\n' + subnet + '\n' + next + '\n'
            elif j =="":
                pass
            else:
                edit = "edit %s/32" % j
                subnet = "set subnet %s 255.255.255.255" % j
                next = "next"
                command += edit + '\n' + subnet + '\n' + next + '\n'
        command += "end" + '\n'
        return command

    def configre_port(self):
        command = "config firewall service custom\n"
        for i in self.tcp_port.split(','):
            if i == "all" or i =="":
                pass
            else:
                edit = "edit TCP-%s" %i
                set = "set tcp-portrange %s" %i
                next = "next"
                command += edit + '\n' + set + '\n' + next + '\n'
        for j in self.udp_port.split(','):
            if j == "all" or j =="":
                pass
            else:
                edit = "edit UDP-%s" %j
                set = "set udp-portrange %s" %j
                next = "next"
                command += edit + '\n' + set + '\n' + next + '\n'
        command += "end" + '\n'
        return command

    def configure_policy(self):
        command = "config firewall policy\n" + "edit 0\n"
        src_address_str = ""
        des_address_str = ""
        tcp_port_str = ""
        udp_port_str = ""
        for i in self.src_address.split(','):
            if i == "all":
                src_address_str += "all"
            elif '/' in i:
                src_address_str += i + " "
            elif i =="":
                pass
            else:
                src_address_str += i + "/32 "
        for j in self.des_address.split(','):
            if j == "all":
                des_address_str += 'all'
            elif '/' in j:
                des_address_str += j + " "
            elif j == "":
                pass
            else:
                des_address_str += j + "/32 "
        for k in self.tcp_port.split(','):
            if k == "all":
                tcp_port_str += "ALL_TCP "
            elif k == "icmp":
                tcp_port_str += "ALL_ICMP "
            elif k == "":
                pass
            else:
                tcp_port_str += "TCP-%s " %k
        for l in self.udp_port.split(','):
            if l == "all":
                udp_port_str += "ALL_UDP "
            elif l == "":
                pass
            else:
                udp_port_str += "UDP-%s " %l
        name = "set name %s" % self.name
        srcintf = "set srcintf %s" % self.src_if
        dstintf = "set dstintf %s" % self.des_if
        srcaddr = "set srcaddr %s" % src_address_str
        dstaddr = "set dstaddr %s" % des_address_str
        schedule = "set schedule always"
        service = "set service %s" % (tcp_port_str + udp_port_str)
        logtraffic = "set logtraffic %s" % self.log
        action = "set action accept"
        status = "set status disable"
        end = "end"
        command += name + '\n' + srcintf + '\n' + dstintf + '\n' + srcaddr + '\n' + dstaddr + '\n' + schedule + '\n' + service + '\n' + logtraffic + '\n' + action + '\n' + status + '\n' + end
        return command
    
    def configure_policy_modify(self, policy_id, select):
        command = "end\nconfig firewall policy\n" + "edit %s\n"% policy_id
        src_address_str = ""
        des_address_str = ""
        tcp_port_str = ""
        udp_port_str = ""
        for i in self.src_address.split(','):
            if i == "all":
                src_address_str += "all"
            elif '/' in i:
                src_address_str += i + " "
            elif i =="":
                pass
            else:
                src_address_str += i + "/32 "
        for j in self.des_address.split(','):
            if j == "all":
                des_address_str += 'all'
            elif '/' in j:
                des_address_str += j + " "
            elif j == "":
                pass
            else:
                des_address_str += j + "/32 "
        for k in self.tcp_port.split(','):
            if k == "all":
                tcp_port_str += "ALL_TCP "
            elif k == "icmp":
                tcp_port_str += "ALL_ICMP "
            elif k == "":
                pass
            else:
                tcp_port_str += "TCP-%s " %k
        for l in self.udp_port.split(','):
            if l == "all":
                udp_port_str += "ALL_UDP "
            elif l == "":
                pass
            else:
                udp_port_str += "UDP-%s " %l
        if src_address_str != "":
            srcaddr = "%s srcaddr %s" % (select, src_address_str)
            command += srcaddr + '\n'
        else:
            pass
        if des_address_str != "":
            dstaddr = "%s dstaddr %s" % (select, des_address_str)
            command += dstaddr + '\n'
        else:
            pass
        if (tcp_port_str + udp_port_str) != "":
            service = "%s service %s" % (select, tcp_port_str + udp_port_str)
            command += service + '\n'
        else:
            pass
        end = "end" + '\n'
        command += end
        return command

if __name__ == '__main__':
    src_if = "x1"
    des_if = "x2"
    src_add = "2.2.2.1,2.2.2.4/25"
    des_add = "2.2.2.2,2.2.2.3"
    tcp_port = "55"
    udp_port = "56"
    log = "all"
    name_input = input("policy_name:")
    firewall = FirewallConfigurator(name_input,src_if,des_if,src_add,des_add,tcp_port,udp_port,log)
    print(firewall.configure_address())
    print(firewall.configre_port())
    print(firewall.configure_policy_modify('75','unselect'))