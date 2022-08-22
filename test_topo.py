import unittest
from topo import FVTopo

class TestFVTopo(unittest.TestCase):

    def setUp(self):
        self.topo = FVTopo('./testdata/topo.json')

    def test_addSwitches(self):
        switches = self.topo.switches()

        self.assertEqual(len(switches), 2)
        self.assertEqual(switches[0], 's1')
        self.assertEqual(switches[1], 's2')

        s1Info = self.topo.nodeInfo('s1')

        self.assertEqual(s1Info['protocols'], 'OpenFlow10')
        self.assertEqual(s1Info['dpid'], '1')
    
    def test_addHosts(self):
        hosts = self.topo.hosts()

        self.assertEqual(len(hosts), 1)
        self.assertEqual(hosts[0], 'h1')

        h1Info = self.topo.nodeInfo('h1')

        self.assertEqual(h1Info['cpu'], 0.5)


    def test_addLinks(self):
        links = self.topo.links(withInfo=True)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][0], 'h1')
        self.assertEqual(links[0][1], 's1')
        self.assertEqual(links[0][2]['delay'], '100ms')
        self.assertEqual(links[0][2]['bw'], 10)

if __name__ == '__main__':
    unittest.main()