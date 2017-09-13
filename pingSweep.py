"""
Copyright (c) 2016 Andrew Hawkins
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import ipaddress
import sys
from os import popen
from texttable import texttable

assert sys.version_info >= (3, 3)

fhand = open('pingSweep.txt', 'w')

ifconfig = str(popen("ifconfig").read())

print("which interface?")

# break the ifconfig into interfaces.
ifconfig = ifconfig.replace("          ", "")
length = len(ifconfig)
blockEnd = ifconfig.find("\n\n")
blockStart = 0
blocks = []

while blockEnd != -1:
    blocks.append(str(ifconfig[blockStart:blockEnd].strip()))
    blockStart = blockEnd + 2
    blockEnd = ifconfig.find("\n\n", blockStart)

# blocks are done. need to extract all pernitent info (IPv4, IPv6, broadcast, etc)
table = texttable.Texttable()
details = [["number", "Interface name", "IPv4", "IPv6", "Hardware"]]
counter = 0
for i in blocks:
    intf = "none"
    intfStart = 0
    intfEnd = i.find("Link")
    intf = i[intfStart:intfEnd - 1].strip()


    v4Start = i.find("inet addr")
    if v4Start != -1:
        v4End = i.find("  ", v4Start)
        v4 = i[v4Start + 10:v4End]
    else:
        v4 = "none"

    v6Start = i.find("inet6 addr")
    if v6Start != -1:
        v6End = i.find("Scope")
        v6 = i[v6Start + 11:v6End - 1]
    else:
        v6 = "none"

    macStart = i.find("HWaddr")
    if macStart != -1:
        macEnd = i.find("\n")
        mac = i[macStart + 7:macEnd - 2]
    else:
        mac = "none"

    maskStart = i.find("Mask")
    if maskStart != -1:
        maskEnd = i.find("\n", maskStart)
        mask = i[maskStart + 5:maskEnd]
        cidr = "/" + str(sum([bin(int(x)).count("1") for x in mask.split(".")]))
    else:
        mask = "none"
        cidr = ""

    counter += 1
    details.append([counter, intf, str(v4) + str(cidr), v6, mac])

table.reset()
table.add_rows(details)
print(table.draw() + "\n")

while True:
    selection = int(input("number: "))
    try:
        row = details[selection]
    except:
        print("Invalid selection. please try again.")
        continue

    if row[2] == "none":
        print("that interface does not have an ipv4 address or is invalid. please choice another.")
        continue
    else:
        break

face = ipaddress.IPv4Interface(str(row[2]))

hosts = list(face.network.hosts())

# loops through the subnet the the interface the user selected resides on.


for address in hosts:
    address = str(address)
    print("pinging " + address)
    ping = popen("ping -c 3 " + address).read()

    # only writes out results of ping if there is a response
    if ping.find("100% packet loss") != -1 AND ping.find("Destination host") != -1:
        continue
    else:
        print(ping)
        fhand.write(ping)

print("end of list")
fhand.close()