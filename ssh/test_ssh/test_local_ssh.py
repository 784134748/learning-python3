import unittest
from ssh import local_ssh


class TestLocalSsh(unittest.TestCase):

    def test_execute_shell_return(self):
        cmd = "echo \"hello world!\""
        self.assertTrue(local_ssh.execute_shell_return(cmd, ""))


if __name__ == '__main__':
    unittest.main()
