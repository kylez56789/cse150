
# Kyle Zhang
# kmzhang
# kmzhang@ucsc.edu
# 1669388
# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)

    arp = packet.find('arp')
    icmp = packet.find('icmp')

    msg.idle_timeout = 10
    msg.hard_timeout = 100

    if icmp is not None or arp is not None:
      # accepting ICMP traffic
      if isICMP is not None:
        msg.data = packet_in
        msg.nw_proto = 6
        action = of.ofp_action_output(port=of.OFPP_FLOOD)
        msg.actions.append(action)
        self.connection.send(msg)

      # accepting ARP traffic
      elif isARP is not None:
        msg.data = packet_in
        msg.match.dl_type = 0x0806
        action = of.ofp_action_output(port=of.OFPP_FLOOD)
        msg.actions.append(action)
        self.connection.send(msg)

    else:
      self.connection.send(msg)

    print "Example Code."

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
