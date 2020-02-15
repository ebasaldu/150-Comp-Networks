# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley
# Edbel Basaldua
# ebasaldu@ucsc.edu
# lab 3 assignment

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
    # The following lines specify the 3 types of packets
    # that are required to be looked for
    # using the find method for strings to return index of first occurence
    # tried setting up in a binary way to check if respective string exists in packet or not
    tcp = packet.find('tcp')
    ipv4 = packet.find('ipv4')
    arp = packet.find('arp')
    #print "Example Code."
    
    #The following are conditonals that represrnt the 
    # rules that this firewall needs to abide by
    # these rules are given in the table 
    # Logic: if no respective string or (strings) occur then return accept  otherwise drop
  
    if tcp is not NONE and ipv4 is not NONE:
      return 'accept'
    elif arp is not NONE:
      return 'accept'
    else: 
      return 'drop'

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    #self.do_firewall(packet, packet_in)
    
    # The following block of code will be used to create an
    # an instance of a table which will serve as a means to record
    # and keep track of the packets that are coming through
    
    macaddytable= {} 
    # creates an instance of a hastable or dictionary for packets
    macaddytable[(event.connection,packet.src)]= event.port
    # create a list in the dictionary 
    # retrieve the source and destination addressess 
    srcmacaddy= macaddytable.get(event.connection,packet.src)
    dstmacaddy= macaddytable.get(event.connection,packet.dst)
    # declatative satements to keep the msg in the empty null state
    # basically a generic table entry
    # Our table from ex
    
    self.macToPort = {}
    # We want to hear PacketIn messages, so we listen
    # to the connection
    connection.addListeners(self)

    msg = of.ofp_flow_mod()
    msg.idle_timeout=0
    msg.hard_timeout=0
    msg.actions.append(of.ofp_action_output(port = OFPP_NONE))
    #Switch rules
    # broadcast to eiher all aka a general broadcast to all present hosts
    # or it broadcasts to one specific host given the port

    #General case broadcast to all ports except the source port
    # otherwise it will halt the process
    if dstmacaddy is NONE: 
      if self.do_firewall(packet,packet_in) == 'accept':
        msg.idle_timeout=0
        msg.hard_timeout=0
        msg = of.ofp_packet_out(data = packet_in)
        msg.actions.append(of.ofp_action_output(port = OFPP_ALL))
        event.connection.send(msg)
      else:
        event.halt = True
    # Case for a specific port 
    # if we know the source and the destination then send it to its destination
    # otherwise it will halt the process
    # all we have to use is event and self
    self.macToPort[packet.src] = event.port
    porty = self.macToPort[packet.dst]

    if srcmacaddy is not NONE and dstmacaddy is not NONE:
      if self.do_firewall(packet, packet_in)== 'accept':
        msg= of.ofp_packet_out(data = packet_in)

      # There should be a specified port here so we can send it from the
      # switch to its destination
        msg.actions.append(of.ofp_action_output(port = dstmacaddy))
        event.connection.send(msg)
      else:
        event.halt = True

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
