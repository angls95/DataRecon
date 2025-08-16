import nmap3
import time
import modules.utils as utils

SCAN_TP = 1000
MR = 2

def do_sV_scan(targets):
    nmap = nmap3.Nmap()
    
    for host,ports in targets.items():
        utils.separator("nmap version scan started", host)
        comand = f"-Pn -sS -sV -p {ports} --open --max-retries {MR}"
        results = nmap.scan_top_ports(host, args=comand)
        versions_found = list()
        print("Versions identified:\n")
        
        try:
            for j in results[host]['ports']:
                protocol = j['protocol']
                port = j['portid']
                service = j['service']
                name = service['name']
                
                if 'version' in service and 'product' in service:
                    product = service['product']
                    version = service['version']
                    output = f"{port}/{protocol} - {name} / {product} - {version}"
                elif 'version' in service:
                    version = service['version']
                    output = f"{port}/{protocol} - {name} {version}"
                elif 'product' in service:
                    product = service['product']
                    output = f"{port}/{protocol} - {name} / {product}"
                else:
                    output = f"{port}/{protocol} - {name}"
                versions_found.append(output)
                print("\t%s" % output)

            str_versions_found = "\n".join(versions_found)
            utils.create_log_file(host, str_versions_found, "nmap_sV")
        except Exception as e:
                print(f"[!] Error: {e}")

def do_syn_scan(ips, tp):
    nmap = nmap3.Nmap()
    targets = dict()
    
    for ip in ips:
        utils.separator("nmap scan started", ip)
        comand = f"-Pn -sS --open --top-ports {tp} --max-retries {MR}"
        results = nmap.scan_top_ports(ip, args=comand)
        ports_open = list()
        ports_sV = list()
        print("Ports identified:\n")
        
        try:
            for j in results[ip]['ports']:
                protocol = j['protocol']
                port = j['portid']
                if 'service' in j:
                    service = j['service']
                    name = service['name']
                    output = f"{port}/{protocol} - {name}"
                else:
                    output = f"{port}/{protocol}"
                ports_open.append(output)
                ports_sV.append(port)
                print("\t%s" % output)
            str_ports_open = "\n".join(ports_open)
            utils.create_log_file(ip, str_ports_open, "nmap_sS_tp_%s" % tp)
            targets[ip] = ",".join(ports_sV)
            
        except Exception as e:
            print(f"[!] No ports identified in host {e}")
    return targets

def scan_ips(ips):
    if len(ips) > 0:
        utils.separator("IP scan started", "")
        targets_sV = do_syn_scan(ips, SCAN_TP)
        do_sV_scan(targets_sV)
        utils.separator("IP scan finished", "")
    else:
        print("\n[!] No IPs provided")