# Written by Joshua Warren (josh@creatuity.com)
# Copyright (C) 2012 Creatuity Corp. (http://creatuity.com)
# Released under the terms of the GNU GPL v3 (http://www.gnu.org/licenses/gpl.html)
# Make sure you have pysnmp installed on your system
# Make sure to replace ups0 in the last line with the hostname or IP of the UPS you want to check
# This is written in the style of a Server Density plugin, but could be used for other uses


from pysnmp.entity.rfc3413.oneliner import cmdgen

def getCyberpowerStatus(hostname):
	cmdGen = cmdgen.CommandGenerator()
	
	errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
	    cmdgen.CommunityData('public', mpModel=0),
	    cmdgen.UdpTransportTarget((hostname, 161), timeout=30, retries=3),
	    cmdgen.MibVariable('.1.3.6.1.4.1.3808.1.1.1.2.2.1.0'), # battery capacity
	    cmdgen.MibVariable('.1.3.6.1.4.1.3808.1.1.1.3.2.2.0'), # input voltage
	    cmdgen.MibVariable('.1.3.6.1.4.1.3808.1.1.1.4.2.1.0'), # output voltage
	    cmdgen.MibVariable('.1.3.6.1.4.1.3808.1.1.1.2.2.4.0'), #  runtime remaining
	    cmdgen.MibVariable('.1.3.6.1.4.1.3808.1.1.1.3.2.4.0') # input frequency
	)
	
	# Check for errors and print out results
	if errorIndication:
	    print(errorIndication)
	else:
	    if errorStatus:
	        print('%s at %s' % (
	            errorStatus.prettyPrint(),
	            errorIndex and varBinds[int(errorIndex)-1] or '?'
	            )
	        )
	    else:
	    	return_data = {} 
	        for name, val in varBinds:
	            if name.prettyPrint() == '1.3.6.1.4.1.3808.1.1.1.3.2.2.0':
	                actualName = 'Input Voltage'
	                actualValue = val / 10
	            elif name.prettyPrint() == '1.3.6.1.4.1.3808.1.1.1.2.2.1.0':
	                actualName = 'Battery Capacity'	                
	                actualValue = val    
	            elif name.prettyPrint() == '1.3.6.1.4.1.3808.1.1.1.4.2.1.0':
	                actualName = 'Output Voltage'
	                actualValue = val / 10
	            elif name.prettyPrint() == '1.3.6.1.4.1.3808.1.1.1.2.2.4.0':
	                actualName = 'Runtime Remaining'
	                actualValue = val / 6000
	            elif name.prettyPrint() == '1.3.6.1.4.1.3808.1.1.1.3.2.4.0':
	                actualName = 'Input Frequency'
	                actualValue = val / 10
	            else:
	                actualName = name.prettyPrint()
	                actualValue = val
	            return_data[actualName] = actualValue.prettyPrint()    
	        return return_data
	        
class CyberpowerSNMP:
    def __init__(self, config, logger, raw_config):
        self.config = config
        self.logger = logger
        self.raw_config = raw_config

    def run(self):
        return getCyberpowerStatus('ups0')

