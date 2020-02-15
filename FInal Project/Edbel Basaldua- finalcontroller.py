# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
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
    self.macaddrtable={}

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    #print "Example code."
    #In this lab we need to identify two types of packets 
    # these packets are the ip and the icmp packets
    # the follwing uses the find method to track these pakcets
    ipv4= packet.find('ipv4')
    icmp= packet.find('icmp')
    # In order to make things more clear i stored the ip addr of each host 
    # wihtin a variable
    h1_ip='10.1.1.10'
    h2_ip='10.2.2.20'
    h3_ip='10.3.3.30'
    h4_ip='123.45.67.89'
    h5_ip='10.5.5.50'
    # if there is a non ip packet then we flood it 
    if ipv4 is NONE:
      msg= ofp_flow_mod()
      msg.actions.append(ofp_action_output(port= OFPP_FLOOD))
      msg.idle_timeout=75
      msg.hard_timeout=100
      msg.data= packet_in
      self.connection.send(msg)
    print "Flooding Current Packet"
    return

    # If the traffic is ip then condtions for the switches must be met 
    if switch_id == 1 :
        print "Test for switch 1"
        #Test if the packet is going to host 1
        if ipv4.dstip == h1_ip:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port= 8))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
        else:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port= 2))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
    if switch_id == 2 :
        print "Test for switch 2"
        #Test if the packet is going to host 1
        if ipv4.dstip == h2_ip:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port= 9))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
        else:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port= 2))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return    
    if switch_id == 3 :
        print "Test for switch 3"
        #Test if the packet is going to host 1
        if ipv4.dstip == h3_ip:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port=10))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
        else:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port= 2))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return 
    if switch_id == 5 :
        print "Test for switch 5"
        #Test if the packet is going to host 1
        if ipv4.dstip == h5_ip:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port=11))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
        else:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port= 2))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return 
    #Rules for switch 4 the untrusted Host
    if switch_id == 4 :
      #Instill the rules for the untrusted host
      if ipv4.srcip==h4_ip:
        #Block ip traffic from host 4 to host 5 the server
        if ipv4 is not NONE and ipv4.dstip==h5_ip:
          print " UNTRUSTED HOST 4 BLOCKED"
        if icmp is not NONE:
          print "Blocked icmp from Host 4"
          return
        if dstip== h1_ip:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port=4 ))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
        if dstip== h2_ip:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port= 3))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
        if dstip== h3_ip:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port= 2))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
        if dstip== h5_ip:
          msg = of.ofp_flow_mod()
          msg.actions.append(ofp_action_output(port=7 ))
          msg.idle_timeout=100
          msg.hard_timeout=100
          msg.data= packet_in
          self.connection.send(msg)
          return
      



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
