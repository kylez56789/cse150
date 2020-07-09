#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    h1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.1.10', defaultRoute="h1-eth0")
    h2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.1.20', defaultRoute="h2-eth0")
    h3 = self.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.1.30', defaultRoute="h3-eth0")
    h4 = self.addHost('h4', mac='00:00:00:00:00:04', ip='10.0.1.40', defaultRoute="h4-eth0")
    h5 = self.addHost('h5', mac='00:00:00:00:00:05', ip='10.0.1.50', defaultRoute="h5-eth0")
    h6 = self.addHost('h6', mac='00:00:00:00:00:06', ip='10.0.1.60', defaultRoute="h6-eth0")
    h7 = self.addHost('h7', mac='00:00:00:00:00:07', ip='10.0.1.70', defaultRoute="h7-eth0")
    h8 = self.addHost('h8', mac='00:00:00:00:00:08', ip='10.0.1.80', defaultRoute="h8-eth0")
    server = self.addHost('server1', mac='00:00:00:00:00:09', ip='10.0.9.10',
                          defaultRoute='server-eth0')
    untrusted = self.addHost('untrusted1', mac='00:00:00:00:00:10', ip='10.0.10.10',
                             defaultRoute='trusted-eth0')

    # Create a switch. No changes here from Lab 1.
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')
    s4 = self.addSwitch('s4')
    core = self.addSwitch('s5')
    data = self.addSwitch('s6')

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    self.addLink(s1, h1, port1=1, port2=1)
    self.addLink(s1, h2, port1=2, port2=1)
    self.addLink(s2, h3, port1=1, port2=1)
    self.addLink(s2, h4, port1=2, port2=1)
    self.addLink(s3, h5, port1=1, port2=1)
    self.addLink(s3, h6, port1=2, port2=1)
    self.addLink(s4, h7, port1=1, port2=1)
    self.addLink(s4, h8, port1=2, port2=1)
    self.addLink(data, server, port1=1, port2=1)
    self.addLink(core, untrusted, port1=5, port2=1)
    self.addLink(s1, core, port1=3, port2=1)
    self.addLink(s2, core, port1=3, port2=2)
    self.addLink(s3, core, port1=3, port2=3)
    self.addLink(s4, core, port1=3, port2=4)
    self.addLink(data, core, port1=2, port2=6)

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()


