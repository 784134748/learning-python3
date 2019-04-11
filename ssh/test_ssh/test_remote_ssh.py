import unittest
from ssh import remote_ssh


class TestRemoteSsh(unittest.TestCase):

    def test_ipv4_address_validation(self):
        addr1 = "128.0.0.x"
        self.assertFalse(remote_ssh.ipv4_address_validation(addr1))

        addr2 = "256.0.0.0"
        self.assertFalse(remote_ssh.ipv4_address_validation(addr2))

        addr3 = "128.0.0.1"
        self.assertTrue(remote_ssh.ipv4_address_validation(addr3))

        addr4 = "127.0.0.1"
        self.assertTrue(remote_ssh.ipv4_address_validation(addr4))

        addr5 = "mydefaultip"
        self.assertFalse(remote_ssh.ipv4_address_validation(addr5))

        addr6 = "localhost"
        self.assertFalse(remote_ssh.ipv4_address_validation(addr6))

        addr7 = "0.-1.0.0"
        self.assertFalse(remote_ssh.ipv4_address_validation(addr7))

        addr8 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        self.assertFalse(remote_ssh.ipv4_address_validation(addr8))

    def test_port_validation(self):
        port1 = 22
        self.assertTrue(remote_ssh.port_validation(port1))

        port2 = "232"
        self.assertTrue(remote_ssh.port_validation(port2))

        port3 = "12xxx"
        self.assertFalse(remote_ssh.port_validation(port3))

        port4 = "65536"
        self.assertFalse(remote_ssh.port_validation(port4))

        port5 = "-22"
        self.assertFalse(remote_ssh.port_validation(port5))

        port6 = 0
        self.assertTrue(remote_ssh.port_validation(port6))


if __name__ == '__main__':
    unittest.main()
