import os

def nmap_scan(target, uid):
    # Run nmap scan
    # Output into /ta
    outfile = "targets/{}/nmap.json".format(uid)
    # Remove http from target
    if target[:8] == "https://":
        target = target[8:]
    elif target[:7] == "http://":
        target = target[7:]

    command = 'nmap -sS -sV -p- -T4 --max-retries=2 --host-timeout=10s -oG {} "{}"'.format(outfile, target)
    print("running nmap")
    os.system(command)


def ffuf_scan(target, uid):
    outfile = "targets/{}/ffuf.json".format(uid)
    if target[-1] == '/':
        target = target[:-1]
    command = 'ffuf -w wordlists/ffuf.txt -o {} -u "{}/FUZZ"'.format(outfile,target)
    print("running ffuf")
    os.system(command)

