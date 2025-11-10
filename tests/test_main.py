import subprocess
import unittest
from io import StringIO
from unittest.mock import patch

class TestMain(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_hello_world_output(self, mock_stdout):
        subprocess.run(['python', '-m', 'hello'])
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")

if __name__ == '__main__':
    unittest.main()