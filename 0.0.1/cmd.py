#!/usr/bin/python3
import argparse
import cli
import re

parser = argparse.ArgumentParser(
    prog="Cisco",
    description="Cisco Command Interface",
)

parser.add_argument(
    "-c", nargs="+", action="store", dest="prompt", help="Command for device"
)
parser.add_argument("-d", action="store_true",
                    dest="device", help="Device info")
parser.add_argument("-i", action="store_true",
                    dest="inventory", help="Device info")
parser.add_argument("-a", type=str, dest="conf", help="Config apply")
args = parser.parse_args()
if args.conf:
    print(args.conf)
    commands = args.conf.split('%')
    formatted_commands = '; '.join(command.strip() for command in commands)
    cli.clip(formatted_commands)

if args.prompt:
    task = ""
    for word in args.prompt:
        task = task + word + " "
    print(cli.cli(task))

if args.device:
    output = cli.cli("show license udi")
    pattern = r'PID:([^,]+),\s*SN:([^,\n]+)'
    match = re.search(pattern, output)
    if match:
        pid = match.group(1)
        sn = match.group(2)
        sn = sn.replace('\n', '')

    pattern = re.compile(r"C([^-]+)-")
    match = pattern.search(pid)
    if match:
        platform = match.group(1)

    output = cli.cli("show version")
    if pid.startswith("N9K"):
        version_pattern = re.compile(r'^ *NXOS: version (\d+\.\d+\(\d+\))', re.MULTILINE)
    else:
        version_pattern = re.compile(
        r"Cisco IOS XE Software, Version\s+(\d+\.\d+\+?)", re.MULTILINE)
    # Search the Cisco output for the pattern
    match = version_pattern.search(output)
    # If a match is found, return the captured version number
    if match:
        swver = match.group(1)
    

    print(pid + "," + sn + "," + swver + "," + platform)

if args.inventory:
    data = cli.cli("show inventory")
    # Regular expression pattern to match PIDs with "C9" and containing "NM"
    pattern = r'PID: (.*(?:C9|NM)\S*)'

    # Extracting matching PIDs
    pids = re.findall(pattern, data)

    # Removing duplicates
    pids = list(set(pids))

    # Printing the extracted PIDs
    end = ""
    for pid in pids:
        end += pid+","
    end = end[:len(end)-1]
    print(end)
