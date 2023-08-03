import os.path
import tempfile
import unittest
import toml
from cffconvert.cli.create_citation import create_citation
from unittest import skip

from src.cff2pages.cff2pages import main_procedure, get_unique_affiliations


class PagesTester(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    @skip
    def test_creation_of_index_html(self):
        with self.temp_dir as tmp_dir:
            main_procedure(tmp_dir)
            public_path = os.path.join(tmp_dir, 'public')
            index_file = os.path.join(public_path, 'index.html')
            self.assertTrue(os.path.exists(public_path))
            self.assertTrue(os.path.exists(index_file))
            with open(index_file, 'r') as index_html:
                self.assertEqual(index_html.read(), expected_html)

    def test_authors_affiliation(self):
        authors = [
            {
                'given-names': 'J',
                'family-names': 'B',
                'email': 'jb@up.de',
                'affiliation': 'UP',
                'orcid': 'https://orcid.org/0000-0000-0000-1234'
            },
            {
                'given-names': 'B',
                'family-names': 'J',
                'email': 'bj@up.de',
                'affiliation': 'UP',
                'orcid': 'https://orcid.org/0000-0000-0000-1235'
            },
            {
                'given-names': 'B',
                'family-names': 'J',
                'email': 'bj@pu.de',
                'affiliation': 'PU',
                'orcid': 'https://orcid.org/0000-0000-0000-1236'
            }]
        unique_affiliation = get_unique_affiliations(authors)
        self.assertEqual(len(unique_affiliation), 2)
        self.assertEqual(unique_affiliation.index(authors[0]['affiliation']), 1)
        self.assertEqual(unique_affiliation.index(authors[1]['affiliation']), 1)
        self.assertEqual(unique_affiliation.index(authors[2]['affiliation']), 0)


expected_html = """<!DOCTYPE html>
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
</html>"""


class VersionTester(unittest.TestCase):
    def test_version_cff_toml(self):
        # Load and parse pyproject.toml
        with open('pyproject.toml', 'r') as f:
            pyproject_data = toml.load(f)
        citation = create_citation('CITATION.cff', None)
        self.assertEqual(pyproject_data['project']['version'], citation.cffobj['version'])

    def test_abstract_cff_toml(self):
        # Load and parse pyproject.toml
        with open('pyproject.toml', 'r') as f:
            pyproject_data = toml.load(f)
        citation = create_citation('CITATION.cff', None)
        print(pyproject_data['project']['version'])
        self.assertEqual(pyproject_data['project']['description'], citation.cffobj['abstract'])


if __name__ == '__main__':
    unittest.main()
