import whois
import requests
import json
import modules.utils as utils

def do_whois(domains):
    for domain in domains:
        utils.separator("whois started", domain)
        whois_data = whois.whois(domain)
        print(whois_data)
        json_string = json.dumps(dict(whois_data), indent=4, default=str)  
        utils.create_log_file(domain, json_string, "whois")

def do_subdomain_scan(domains):
    for domain in domains:
        utils.separator("Subdomains enumeration started", domain)
        url = f"https://crt.sh/?q={domain}&output=json"
        try:
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200:
                data = r.json()
                subs = {entry['name_value'] for entry in data}
                sorted_subdomains = utils.remove_repeted(subs)
                
                if len(sorted_subdomains) > 0:
                    print("Subdomains found for '%s':\n" % domain)
                    
                    for sub in sorted_subdomains:
                        print("\t%s" % sub)
                    str_sorted_subdomains = "\n".join(sorted_subdomains)
                    utils.create_log_file(domain, str_sorted_subdomains, "subdomains_enumeration")
                else:
                    print("The information for subdomain '%s' could not be obtained" % domain)
            else:
                print("The information for subdomain '%s' could not be obtained" % domain)
        except Exception as e:
            print("%s" % {"error": str(e)})
    

def recon_domains(domains):
    if len(domains) > 0:
        utils.separator("Domain Recon estarted", "")
        do_whois(domains)
        do_subdomain_scan(domains)
        utils.separator("Domain Recon finished", "")
    else:
        print("\n[!] No domains provided")