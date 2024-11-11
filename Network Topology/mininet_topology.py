from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.link import TCLink


class DualSwitchTopo(Topo):
    def build(self):
        # Switches
        s1 = self.addSwitch("S1", dpid="1")
        s2 = self.addSwitch("S2", dpid="2")

        # Hosts
        h1 = self.addHost("Host1", ip="10.0.0.1/24", mac="00:00:00:00:00:01")
        h2 = self.addHost("Host2", ip="10.0.0.2/24", mac="00:00:00:00:00:02")
        h3 = self.addHost("Host3", ip="10.0.0.3/24", mac="00:00:00:00:00:03")
        h4 = self.addHost("Host4", ip="10.0.0.4/24", mac="00:00:00:00:00:04")

        # Switch to Hosts
        self.addLink(h1, s1, cls=TCLink, bw=10)
        self.addLink(h2, s1, cls=TCLink, bw=10)
        self.addLink(h3, s2, cls=TCLink, bw=10)
        self.addLink(h4, s2, cls=TCLink, bw=10)

        # Switch to Switch
        self.addLink(s1, s2, cls=TCLink, bw=10)


if __name__ == "__main__":
    setLogLevel("info")
    topo = DualSwitchTopo()
    controller = RemoteController("c1", ip="127.0.0.1")
    net = Mininet(topo, controller=controller)
    net.start()
    CLI(net)
    net.stop()
