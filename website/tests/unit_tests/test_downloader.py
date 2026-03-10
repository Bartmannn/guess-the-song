import unittest

from website.downloader import remove_numbering


class DownloaderUtilsTestCase(unittest.TestCase):
    def test_remove_numbering(self) -> None:
        self.assertEqual(remove_numbering("aaa30", "30"), "aaa")


if __name__ == "__main__":
    unittest.main()
