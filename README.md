# DataRecon  

## Tool Description  
DataRecon is a security tool designed to automate some tasks in the reconnaissance and enumeration phase in penetration testing exercises. It enables structured and fast information gathering, integrating port and service scanning, subdomain enumeration, and WHOIS queries.  

## Main Purpose  
The main goal of DataRecon is to automate some reconnaissance tasks into a single workflow to reduce time and provide information about the target. With this tool, users can execute multiple activities automatically and obtain organized results for further activities. This tool can:
- Execute WHOIS queries to domain names.
- Perform subdomain enumeration based on the domains provided.
- Perform a port scan to one or more IP Addresses.
- Automatically execute service scans on ports discovered on an IP address.
- Use a file with many IP Addresses and domains together.
    - The tool will be able to identify if the targets provided in the file are valid for the execution.
    - Any valid and invalid targets will be shown on the output command line.
- Store the output on files.
    - The files are saved in a folder named with the execution date in the logs directory.
    - The files are named with the target name and the activity performed.

## Requirements  
The following packages are required:  
- python3-nmap  
- python-whois  
- requests  
- validators  

Install dependencies with:  
```bash
pip install -r requirements.txt
```

NOTE: Tt is recommended to execute the tool on a virtual env.

## Download and Execution  
Clone the repository:  
```bash
git clone https://github.com/user/DataRecon.git
cd DataRecon
```

Install dependencies:  
```bash
pip install -r requirements.txt
```

Run the tool:  
```bash
python3 datarecon.py -t example.com
```  

## How to Use  
The tool is executed from the command line, taking an IP address or domain as a target.  

Example:  
```bash
python3 datarecon.py -t target 
```

Available parameters: 
```
-t, --target TARGET It can be an IP or a domain, and it is necessary to specify the module according to the target type.
    --target FILE   It can contain IPs and Domains together. The tool automatically performs both modules with this option.. 
-r, --recon         Module to execute recon module on domain (It only works with domains)
-s, --scan          Module to execute scan module on IP Address (It only works with IPs)
```
Example of execution:
```
# Execute the scan module on the IP provided by the user
python main.py -t 192.168.1.10 -s

# Execute the recon module on domain provided by the user
python main.py -t example.com -r

# Execute both modules on the targets specified in the file provided by the user
python main.py --target target_file.txt
```

NOTE: It is possible to modify the number of ports scanned and the maximum retries in the scan module. By default, the tool scans the top 1000 ports, but you can change this value to scan as many ports as you need. The max-retries option can also be modified; by default, it is set to 2. To make these changes in the module, update the values in lines 5 and 6.
```
SCAN_TP = 1000
MR = 2
```

## Output  
The results are stored in a folder named with the execution date (e.g., `2025-08-16`).  

Each file follows the format:  
```
target_activity
```

If a file with the same name already exists in the directory, DataRecon appends an incremental number at the end to prevent overwriting results.
```
target_activity
target_activity_1
target_activity_2
...
...
target_activity_n
```

Examples of output files:
```
logs
├── 2025-08-11
│   ├── 192.168.50.137_nmap_sS_tp_1000
│   ├── 192.168.50.137_nmap_sV
│   ├── google.com_subdomains_enumeration
│   └── google.com_whois
└── 2025-08-16
    ├── 192.168.50.137_nmap_sS_tp_1000
    ├── 192.168.50.137_nmap_sS_tp_1000_1
    ├── 192.168.50.137_nmap_sV
    ├── 192.168.50.137_nmap_sV_1
    ├── 192.168.50.3_nmap_sS_tp_1000
    ├── 192.168.50.3_nmap_sV
    ├── google.com_whois
    └── google.com_whois_1
```