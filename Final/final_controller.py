# Final Skeleton
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
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

  def do_final(self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    msg = of.ofp_flow_mod()
    h1 = '10.0.1.10'
    h2 = '10.0.1.20'
    h3 = '10.0.1.30'
    h4 = '10.0.1.40'
    h5 = '10.0.1.50'
    h6 = '10.0.1.60'
    h7 = '10.0.1.70'
    h8 = '10.0.1.80'
    untrusted = '10.0.10.10'
    server = '10.0.9.10'

    msg.hard_timeout = 30
    msg.idle_timeout = 30
    msg.match = of.ofp_match.from_packet(packet)
    
    ICMP = packet.find('icmp')
    IPV4 = packet.find('ipv4')
    
    if not IPV4:
      msg.data = packet_in
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      self.connection.send(msg)
    elif (ICMP or IPV4.dstip == server) and IPV4.dstip == untrusted:
         self.connection.send(msg)
    elif IPV4:
      if switch_id == 1: # S1
        msg.data = packet_in
        if IPV4.dstip == h1:
          msg.actions.append(of.ofp_action_output(port=1))
        elif IPV4.dstip == h2:
          msg.actions.append(of.ofp_action_output(port=2))
        else:
          msg.actions.append(of.ofp_action_output(port=3))
      elif switch_id == 2:  # S2
        msg.data = packet_in
        if IPV4.dstip == h3:
          msg.actions.append(of.ofp_action_output(port=1))
        elif IPV4.dstip == h4:
          msg.actions.append(of.ofp_action_output(port=2))
        else:
          msg.actions.append(of.ofp_action_output(port=3))
      elif switch_id == 3:  # S3
        msg.data = packet_in
        if IPV4.dstip == h5:
          msg.actions.append(of.ofp_action_output(port=1))
        elif IPV4.dstip == h6:
          msg.actions.append(of.ofp_action_output(port=2))
        else:
          msg.actions.append(of.ofp_action_output(port=3))
      elif switch_id == 4:  # S4
        msg.data = packet_in
        if IPV4.dstip == h7:
          msg.actions.append(of.ofp_action_output(port=1))
        elif IPV4.dstip == h8:
          msg.actions.append(of.ofp_action_output(port=2))
        else:
          msg.actions.append(of.ofp_action_output(port=3))
      elif switch_id == 5:  # core
	if ICMP == None or IPV4.srcip != untrusted:
        	msg.data = packet_in
        	if IPV4.dstip == untrusted:
          		msg.actions.append(of.ofp_action_output(port=5))
        	elif IPV4.dstip == h1 or IPV4.dstip == h2:
          		msg.actions.append(of.ofp_action_output(port=1))
        	elif IPV4.dstip == h3 or IPV4.dstip == h4:
          		msg.actions.append(of.ofp_action_output(port=2))
        	elif IPV4.dstip == h5 or IPV4.dstip == h6:
          		msg.actions.append(of.ofp_action_output(port=3))
        	elif IPV4.dstip == h7 or IPV4.dstip == h8:
          		msg.actions.append(of.ofp_action_output(port=4))
        	elif IPV4.dstip == server and IPV4.srcip != untrusted:
          		msg.actions.append(of.ofp_action_output(port=6))
      elif switch_id == 6:  # data center
        msg.data = packet_in
        if IPV4.dstip == server:
          msg.actions.append(of.ofp_action_output(port=1))
        else:
          msg.actions.append(of.ofp_action_output(port=2))
      self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)


