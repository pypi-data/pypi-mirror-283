import unittest
from webapppacker import WebAppPacker

class TestWebAppPacker(unittest.TestCase):
    def test_pack(self):
        packer = WebAppPacker("TestApp", "com.example.testapp", "1", "1.0")
        apk_path = packer.pack("examples/simple_app")
        self.assertTrue(os.path.exists(apk_path))

if __name__ == '__main__':
    unittest.main()