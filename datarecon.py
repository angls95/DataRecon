import argparse
import sys
import os.path
import ipaddress
import modules.recon as recon
import modules.scan as scan
import modules.utils as utils
import validators

def val_num_args():
    return True if len(sys.argv) == 1 else False

def val_target(ip, ips):
    if validators.ipv4(ip):
        ips["valid"].append(ip)
    elif validators.domain(ip):
        ips["domains"].append(ip)
    else:
        ips["invalid"].append(ip)
    
    return ips

def get_content_file(fname, ips):
    with open(fname, 'r') as t_file:
        lines = t_file.readlines()
    
    for line in lines:
        val_target(line.rstrip(), ips)
    
    return ips

def is_file(target):
    return os.path.isfile(target)

def filter_targets(target):
    ips = {"valid":[], "invalid":[], "domains":[]}
    
    if is_file(target):
        return get_content_file(target, ips)
    else:
        return val_target(target, ips)

def print_list_values(list_values):
    [print(i) for i in list_values]

def valid_targets(list_targets):
    u_ips = utils.remove_repeted(list_targets['valid'])
    u_dom = utils.remove_repeted(list_targets['domains'])
    u_inv = utils.remove_repeted(list_targets['invalid'])
    valid = len(u_ips) + len(u_dom)
    print("Valid Targets: %i" % valid)
    print_list_values(u_ips)
    print_list_values(u_dom)
    print("\nInvalid Targets: %i" % len(u_inv))
    print_list_values(u_inv)

    return True if valid > 0 else False

def example_execution():
    print("\nExample of execution:")
    print("    python %s -t 192.168.1.10 -s" % os.path.basename(__file__))
    print("    python %s -t example.com -r" % os.path.basename(__file__))
    print("    python %s --target target_file.txt" % os.path.basename(__file__))

def main():
    parser = argparse.ArgumentParser(description="Easy tool to do recon.")
    parser.add_argument("-t", "--target", help="IP, domain or file with multiple targets")
    parser.add_argument("-r", "--recon", help="Module to execute recon module on domain", action="store_true")
    parser.add_argument("-s", "--scan", help="Module to execute scan module on IP Address", action="store_true")

    if val_num_args():
        parser.print_help(sys.stderr)
        example_execution()
        sys.exit(1)
    else:
        args = parser.parse_args()
        if is_file(args.target) and not args.recon and not args.scan:
            utils.separator("Target validation started", "")
            targets = filter_targets(args.target)
            
            if valid_targets(targets):
                u_ips = utils.remove_repeted(targets['valid'])
                u_dom = utils.remove_repeted(targets['domains'])
                recon.recon_domains(targets['domains'])
                scan.scan_ips(u_ips)
            else:
                print("\n[!] There is no valid targets")
        elif (args.recon or args.scan) and not is_file(args.target):
            utils.separator("Target validation started", "")
            targets = filter_targets(args.target)
            
            if valid_targets(targets):
                if args.recon and len(targets['domains']) > 0:
                    recon.recon_domains(targets['domains'])
                elif args.scan and len(targets['valid']) > 0:
                    scan.scan_ips(targets['valid'])
                else:
                    print("\n[!] No valid options chosen\n")
                    parser.print_help(sys.stderr)
                    example_execution()
            else:
                print("\n[!] There is no valid targets")
        else:
            parser.print_help(sys.stderr)
            example_execution()

if __name__ == "__main__":
    main()