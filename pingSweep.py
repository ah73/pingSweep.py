"""

Copyright (c) 2016 atticusmordecai

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


import os
import sys
import argparse

_start = raw_input('Enter starting 4th octet:')			# Ex 192.168.1.[x]
_stop = raw_input('Enter ending 4th octet')				# Ex 192.168.1.[x]

fhand = open('pingSweep.txt', 'w')
														
#built in range does not accept var as args; this is my solution
def my_Range(start, stop, step):
	index = start
	while index <= stop:
		yield index
		index += step

#loops through the range provided by user and uses ping command in bash to test for response
#TODO: limit to logical subnet inputes (ie 0-255); possibly account for subnet masks for approriate
#subnet limits. 

for index in my_Range(int(_start), int(_stop), 1):
	print "pinging", index
	ping = os.popen("ping -c 3 -W 100 10.251.19." + str(index)).read()

	#only writes out results of ping if there is a response
	if ping.find("100.0% packet loss") != -1:
		continue
	else:
		print ping
		fhand.write(ping)
	


print "end of list"