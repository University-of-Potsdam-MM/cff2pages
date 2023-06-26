import os.path
import tempfile
import unittest

from src.cff2pages.cff2pages import main_procedure


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_creation_of_index_html(self):
        with self.temp_dir as tmp_dir:
            main_procedure(tmp_dir)
            public_path = os.path.join(tmp_dir, 'public')
            index_file = os.path.join(public_path, 'index.html')
            self.assertTrue(os.path.exists(public_path))
            self.assertTrue(os.path.exists(index_file))
            with open(index_file, 'r') as index_html:
                self.assertEqual(index_html.read(), """<!DOCTYPE html>
<html lang="de">
<head>
    <title>cff2pages</title>
</head>
<body>
<h1> cff2pages</h1>

<h2>
    Jan Bernoth: University of Potsdam
    <img decoding="async" alt="" src="./assets/img/orcid_16x16.webp"
         style="width:16px; height:16px; margin:3px">
    <a href="https://orcid.org/0000-0002-4127-0053"> https://orcid.org/0000-0002-4127-0053</a>
</h2>

</body>
</html>""")


if __name__ == '__main__':
    unittest.main()
