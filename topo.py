#!/usr/bin/python
# -*- coding: utf-8 -*-
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController, OVSBridge
from mininet.cli import CLI
from mininet.link import TCLink
import json
import sys


class FVTopo(Topo):
    "Utility class to make network topology using provided json"

    def __init__(self, filePath):
        """filePath: json topology file path"""
        Topo.__init__(self)

        self.filePath = filePath
        self.data = None

        self.fileUtility()

        self.buildTopo()

    def fileUtility(self):
        with open(self.filePath) as f:
            self.data = json.load(f)

    def buildTopo(self):
        """Make topology based on provided json.
           returns: None"""
        self.addSwitches()
        self.addHosts()
        self.addLinks()

    def addHosts(self):
        """Add topology hosts.
           returns: None"""
        for host in self.data['hosts']:
            hostConfig = {}

            for opt in host:
                if opt == 'name':
                    continue
                hostConfig[opt] = host[opt]

            self.addHost(host['name'], **hostConfig)

    def addSwitches(self):
        """Add topology switches.
           returns: None"""
        for switch in self.data['switches']:
            switchConfig = {}

            for opt in switch:
                if opt == 'name' or opt == 'protocols':
                    continue
                if opt == 'cls' and switch[opt] == 'OVSBridge':
                    switchConfig[opt] = OVSBridge
                    continue
                switchConfig[opt] = switch[opt]

            self.addSwitch(switch['name'], protocols=switch['protocols'],
                         **switchConfig)

    def addLinks(self):
        """Add topology links.
           returns: None"""
        for link in self.data['links']:
            linkConfig = {}

            for opt in link:
                if opt == 'e1' or opt == 'e2':
                    continue
                linkConfig[opt] = link[opt]

            self.addLink(link['e1'], link['e2'], **linkConfig)


topos = {'fvtopo': lambda : FVTopo()}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 topo.py [topo.json path]')
        raise Exception('Invalid input')

    topo = FVTopo(sys.argv[1])

    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
        )

    controller = RemoteController('c1', ip='127.0.0.1', port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()
