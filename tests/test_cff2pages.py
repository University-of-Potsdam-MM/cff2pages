import os.path
import shutil
import tempfile
import unittest
import toml
from bs4 import BeautifulSoup
from cffconvert.cli.create_citation import create_citation

from src.cff2pages.cff2pages import main_procedure, get_unique_affiliations


class MinimalCffTester(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.minimal_filename = 'minimal.cff'
        test_file = os.path.join(os.path.dirname(__file__), self.minimal_filename)
        shutil.copy2(test_file, self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generated_minimal_html_body(self):
        with self.temp_dir as tmp_dir:
            main_procedure(tmp_dir, os.path.join(tmp_dir, self.minimal_filename))
            index_file = check_folders(self, tmp_dir)
            with open(index_file, 'r') as index_html:
                soup = BeautifulSoup(index_html.read(), 'html.parser')
                actual_body = soup.find('body')
                expected_body = BeautifulSoup(expected_minimal_body, 'html.parser')
                self.assertEqual(actual_body.prettify(), expected_body.prettify())

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


expected_minimal_body = """<body>
<div class="container">
<h1 class="blog-title"> Test CFF</h1>
<h2> Muster Mina <sup>2</sup>, 
            Minster Mana <sup>1</sup> </h2>
<ul> <sup>1</sup> : pu <sup>2</sup> : up </ul>
</div>

<div class="footer-container">
<footer class="footer">
<p>Generated with <a href="https://github.com/University-of-Potsdam-MM/cff2pages" target="_blank">cff2pages</a>. </p>
</footer>
</div>
</body>""" # noqa


class CurrentCffTester(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.current_filename = 'current.cff'
        test_file = os.path.join(os.path.dirname(__file__), self.current_filename)
        shutil.copy2(test_file, self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generated_current_html_body(self):
        with self.temp_dir as tmp_dir:
            main_procedure(tmp_dir, os.path.join(tmp_dir, self.current_filename))
            index_file = check_folders(self, tmp_dir)
            with open(index_file, 'r') as index_html:
                soup = BeautifulSoup(index_html.read(), 'html.parser')
                actual_body = soup.find('body')
                expected_body = BeautifulSoup(expected_current, 'html.parser')
                self.assertEqual(actual_body.prettify(), expected_body.prettify())


expected_current = """
<body>
<div class="container">
    
    <h1 class="blog-title"> Test CFF</h1>

    
    <h2>
            Muster Mina<sup>2</sup>, 
            Minster Mana<sup>1</sup>
    </h2>
    <ul>
        <sup>1</sup> : pu
        <sup>2</sup> : up
        </ul>

    <div class="keyword-container">
            <b>Keywords:</b>
            <ul class="keyword-list"><li class="keyword-item">
                        <a class="keyword">keyword1</a>
                    </li><li class="keyword-item">
                        <a class="keyword">keyword2</a>
                    </li><li class="keyword-item">
                        <a class="keyword">keyword3</a>
                    </li><li class="keyword-item">
                        <a class="keyword">keyword4</a>
                    </li>
            </ul>
        </div>
    
    
        <div class="badges"><a class="badge-item" href="https://github.com/organization/site" target="_blank">
                    <img src="./assets/img/github-logo.png" alt="Github Logo"></a>
            <a href="https://github.com/organization/site" target="_blank">Repository</a>
                    <a href="https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/organization/site">
                        <img src="https://archive.softwareheritage.org/badge/origin/https://github.com/organization/site"
                             alt="Archived | https://github.com/organization/site"/>
                    </a>
                
                <a href="https://doi.org/10.1111/zenodo.111111">
                    <img src="https://img.shields.io/badge/DOI_-10.1111/zenodo.111111-blue"
                         alt="DOI"/>
                </a>
    </div>

    
        <p class="licence"><b>License</b>: MIT</p>
    
        <p class="abstract"><b>Abstract</b>: This is a test abstract.</p>
</div>

<div class="footer-container">
    <footer class="footer">
        <p>Generated with <a href="https://github.com/University-of-Potsdam-MM/cff2pages"
                             target="_blank">cff2pages</a>.
        </p>
    </footer>
</div>

</body>
 """ # noqa


def check_folders(cls, tmp_dir):
    public_path = os.path.join(tmp_dir, 'public')
    index_file = os.path.join(public_path, 'index.html')
    cls.assertTrue(os.path.exists(public_path))
    cls.assertTrue(os.path.exists(index_file))
    return index_file


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
