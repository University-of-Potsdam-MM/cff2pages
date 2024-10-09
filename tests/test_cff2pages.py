import os.path
import shutil
import tempfile
import unittest
import toml
from bs4 import BeautifulSoup
from cffconvert.cli.create_citation import create_citation

from src.cff2pages.cff2pages import main_procedure, get_unique_affiliations, guess_format


class MinimalCffTester(unittest.TestCase):
    """
    Tests to create a html based on a minimal cff documentation.
    """

    def setUp(self):
        """
        Creates a temporary directory with the minimal cff
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.minimal_filename = 'minimal.cff'
        test_file = os.path.join(os.path.dirname(__file__), self.minimal_filename)
        shutil.copy2(test_file, self.temp_dir.name)

    def tearDown(self):
        """
        Deletes temporary directories
        """
        self.temp_dir.cleanup()

    def test_generated_minimal_html_body(self):
        """
        Creates a HTML with the minimal cff and compares it with the expected HTML
        """
        with self.temp_dir as tmp_dir:
            output_path = f'{tmp_dir}/public/cff2pages.html'
            main_procedure(os.path.join(tmp_dir, self.minimal_filename), output_path)
            index_file = check_folders(self, tmp_dir)
            with open(index_file, 'r') as index_html:
                soup = BeautifulSoup(index_html.read(), 'html.parser')
                actual_body = soup.find('body')
                expected_body = BeautifulSoup(expected_minimal_body, 'html.parser')
                self.assertEqual(actual_body.prettify(), expected_body.prettify())

    def test_authors_affiliation(self):
        """
        Tests the method which takes and aggregates the authors affiliations
        """
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
            },
            {
                'given-names': 'Ba',
                'family-names': 'Je',
                'email': 'baje@pu.de',
            }
        ]
        unique_affiliation = get_unique_affiliations(authors)
        self.assertEqual(len(unique_affiliation), 2)
        self.assertEqual(0, unique_affiliation.index(authors[0]['affiliation']),
                         f'affiliation from {authors[0]["given-names"]} {authors[0]["family-names"]} should be placed at 0')
        self.assertEqual(0, unique_affiliation.index(authors[1]['affiliation']),
                         f'affiliation from {authors[1]["given-names"]} {authors[1]["family-names"]} should be placed at 0')
        self.assertEqual(1, unique_affiliation.index(authors[2]['affiliation']),
                         f'affiliation from {authors[2]["given-names"]} {authors[2]["family-names"]} should be placed at 1')


expected_minimal_body = """<body>
<div class="container">
    <div class="content">

        <h1 class="blog-title"> Test CFF</h1>


    <h2>
            Muster Mina<sup>1</sup>, 
            Minster Mana<sup>2</sup>, 
            Minster Mana
    </h2>
    <ul>
        <sup>1</sup> : up
        <sup>2</sup> : pu
    </ul>
</div>
        <div class="citation">
            <p><b>cite as (APA):</b></p>
            <p id="citationText">Mina M., Mana M., Mana M. Test CFF
</p>
            <button id="copyButton">copy citation</button>
            <div id="notification" class="notification">Copied!</div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function () {
                const copyButton = document.getElementById('copyButton');
                if (copyButton) {
                    copyButton.addEventListener('click', function () {
                        const citationText = document.getElementById('citationText').innerText;
                        navigator.clipboard.writeText(citationText)
                            .then(() => {
                                // Zeige die Benachrichtigung
                                const notification = document.getElementById('notification');
                                notification.style.opacity = '1';

                                // Verstecke die Benachrichtigung nach 3 Sekunden
                                setTimeout(() => {
                                    notification.style.opacity = '0';
                                }, 3000);
                            })
                            .catch(err => {
                                console.error('Errors in the copy process: ', err);
                            });
                    });
                }
            });
        </script>


</div>

<div class="footer-container">
    <footer class="footer">
        <p>Generated with <a href="https://github.com/University-of-Potsdam-MM/cff2pages"
                             target="_blank">cff2pages</a>.
        </p>
    </footer>
</div>

</body>"""  # noqa


class CurrentCffTester(unittest.TestCase):
    """
    Test class to test all features for creating pages
    """
    maxDiff = None

    def setUp(self):
        """
        Creates a temporary directory with the Current cff
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.current_filename = 'current.cff'
        test_file = os.path.join(os.path.dirname(__file__), self.current_filename)
        shutil.copy2(test_file, self.temp_dir.name)

    def tearDown(self):
        """
        Deletes the temporary directories
        """
        self.temp_dir.cleanup()

    def test_generated_current_html_body(self):
        """
        Tests if the generated HTML from current cff is correct. Compares it with the expected HTML
        """
        with self.temp_dir as tmp_dir:
            output_path = f'{tmp_dir}/public/cff2pages.html'
            main_procedure(os.path.join(tmp_dir, self.current_filename), output_path)
            index_file = check_folders(self, tmp_dir)
            with open(index_file, 'r', encoding='utf-8') as index_html:
                soup = BeautifulSoup(index_html.read(), 'html.parser')
                actual_body = soup.find('body')
                expected_body = BeautifulSoup(expected_current, 'html.parser')
                print(actual_body.prettify())
                self.assertEqual(actual_body.prettify(), expected_body.prettify(),
                                 msg="The generation of the current HTML is not correct.")


expected_current = """<body>

<div class="container">
    <div class="content">
        <h1 class="blog-title"> Test CFF</h1>
    <h2>
            Muster Mina<sup>1</sup>, 
            Minster Mana<sup>2</sup>, 
            Manster Mona
    </h2>
    <ul>
        <sup>1</sup> : up
        <sup>2</sup> : pu
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

        <div class="references-container">
            <h2>References</h2>
            <ul class="references-list">

                    <li class="reference-item">
                    <span class="reference-icon" title="type software">
                        💻
                    </span>
                        <span class="reference-title">Citation File Format</span>,
                        <span class="reference-author">
                        Stephan Druskat<a href="https://orcid.org/0000-0003-4925-7248"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>, 
                        Jurriaan H. Spaaks<a href="https://orcid.org/0000-0002-7064-4069"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>, 
                        Neil Chue Hong<a href="https://orcid.org/0000-0002-8876-7606"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>, 
                        Robert Haines<a href="https://orcid.org/0000-0002-9538-7919"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>, 
                        James Baker<a href="https://orcid.org/0000-0002-2682-6922"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>, 
                        Spencer Bliven<a href="https://orcid.org/0000-0002-1200-1698"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>, 
                        Egon Willighagen<a href="https://orcid.org/0000-0001-7542-0286"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>, 
                        David Pérez-Suárez<a href="https://orcid.org/0000-0003-0784-6909"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>, 
                        Olexandr Konovalov<a href="https://orcid.org/0000-0001-5299-3292"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>
                    </span>
                        <span class="reference-doi"><a href="https://doi.org/10.5281/zenodo.1003149"
                                                       target="_blank">10.5281/zenodo.1003149</a></span>
                    </li>

                    <li class="reference-item">
                    <span class="reference-icon" title="type article">
                        📖
                    </span>
                        <span class="reference-title">Ya2RO: A tool for creating Research Object from minimum metadata</span>,
                        <span class="reference-author">
                        Antonia Pavel, 
                        Daniel Garijo<a href="https://orcid.org/0000-0003-0454-7145"><img decoding="async" alt=""
                                                              src="./assets/img/orcid_16x16.webp"
                                                              style="width:16px; height:16px; margin:3px"/></a>
                    </span>
                        <span class="year">2023</span>,

                        <span class="reference-doi"><a href="https://doi.org/10.4126/FRL01-006444984"
                                                       target="_blank">10.4126/FRL01-006444984</a></span>
                    </li>

            </ul>
        </div>

    </div>
        <div class="citation">
            <p><b>cite as (APA):</b></p>
            <p id="citationText">Mina M., Mana M., Mona M. Test CFF (version 1.2.3). DOI: 10.1111/zenodo.111111 URL: https://github.com/organization/site
</p>
            <button id="copyButton">copy citation</button>
            <div id="notification" class="notification">Copied!</div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function () {
                const copyButton = document.getElementById('copyButton');
                if (copyButton) {
                    copyButton.addEventListener('click', function () {
                        const citationText = document.getElementById('citationText').innerText;
                        navigator.clipboard.writeText(citationText)
                            .then(() => {
                                // Zeige die Benachrichtigung
                                const notification = document.getElementById('notification');
                                notification.style.opacity = '1';

                                // Verstecke die Benachrichtigung nach 3 Sekunden
                                setTimeout(() => {
                                    notification.style.opacity = '0';
                                }, 3000);
                            })
                            .catch(err => {
                                console.error('Errors in the copy process: ', err);
                            });
                    });
                }
            });
        </script>
</div>

<div class="footer-container">
    <footer class="footer">
        <p>Generated with <a href="https://github.com/University-of-Potsdam-MM/cff2pages"
                             target="_blank">cff2pages</a>.
        </p>
    </footer>
</div>

</body>"""  # noqa


def check_folders(cls, tmp_dir):
    """
    Tests if the temp_dir was created and have the necessary files in it.

    :param cls: Test class which does the assertion process.
    :param tmp_dir: Directory where the files are stored.
    :return: Path to the html
    """
    public_path = os.path.join(tmp_dir, 'public')
    index_file = os.path.join(public_path, 'cff2pages.html')
    cls.assertTrue(os.path.exists(public_path))
    cls.assertTrue(os.path.exists(index_file))
    return index_file


class DiacriticsCffTester(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.diacritics_filename = 'diacritics.cff'
        test_file = os.path.join(os.path.dirname(__file__), self.diacritics_filename)
        shutil.copy2(test_file, self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generated_diacritics_html_body(self):
        """
        Tests if there are any diacritics in the generated HTML
        """
        with self.temp_dir as tmp_dir:
            output_path = f'{tmp_dir}/public/cff2pages.html'
            main_procedure(os.path.join(tmp_dir, self.diacritics_filename), output_path)
            index_file = check_folders(self, tmp_dir)
            with open(index_file, 'r') as index_html:
                soup = BeautifulSoup(index_html.read(), 'html.parser')
                actual_body = soup.find('body')
                expected_body = BeautifulSoup(expected_diacritics_body, 'html.parser')
                self.assertEqual(actual_body.prettify(), expected_body.prettify())


expected_diacritics_body = """<body>
<div class="container">
<div class="content">
<h1 class="blog-title"> Test minimal CFF with diacritics</h1>
<h2>
            Antonio Rüdiger<sup>1</sup>, 
            İlkay Gündoğan<sup>2</sup>, 
            Aleksandar Pavlović<sup>3</sup>, 
            Hasret Kayikçi<sup>4</sup>
</h2>
<ul>
<sup>1</sup> : Real Madrid
        <sup>2</sup> : Manchester City
        <sup>3</sup> : FC Bayern München
        <sup>4</sup> : SC Freiburg
        </ul>
</div>
<div class="citation">
<p><b>cite as (APA):</b></p>
<p id="citationText">Rüdiger A., Gündoğan İ., Pavlović A., Kayikçi H. Test minimal CFF with diacritics
</p>
<button id="copyButton">copy citation</button>
<div class="notification" id="notification">Copied!</div>
</div>
<script>
            document.addEventListener('DOMContentLoaded', function () {
                const copyButton = document.getElementById('copyButton');
                if (copyButton) {
                    copyButton.addEventListener('click', function () {
                        const citationText = document.getElementById('citationText').innerText;
                        navigator.clipboard.writeText(citationText)
                            .then(() => {
                                // Zeige die Benachrichtigung
                                const notification = document.getElementById('notification');
                                notification.style.opacity = '1';

                                // Verstecke die Benachrichtigung nach 3 Sekunden
                                setTimeout(() => {
                                    notification.style.opacity = '0';
                                }, 3000);
                            })
                            .catch(err => {
                                console.error('Errors in the copy process: ', err);
                            });
                    });
                }
            });
        </script>
</div>
<div class="footer-container">
<footer class="footer">
<p>Generated with <a href="https://github.com/University-of-Potsdam-MM/cff2pages" target="_blank">cff2pages</a>.
        </p>
</footer>
</div>
</body>""" # noqa


class CffTomlComparer(unittest.TestCase):
    """
    Testing class to verify that the various aspects between toml and cff are the same.
    """
    def test_version_cff_toml(self):
        """
        Compares cff and toml version
        """
        # Load and parse pyproject.toml
        with open('pyproject.toml', 'r') as f:
            pyproject_data = toml.load(f)
        citation = create_citation('CITATION.cff', None)
        self.assertEqual(pyproject_data['project']['version'], citation.cffobj['version'],
                         "The version of the CFF and toml are not the same.")

    def test_abstract_cff_toml(self):
        """
        Compares abstracts of cff and toml
        :return:
        """
        # Load and parse pyproject.toml
        with open('pyproject.toml', 'r') as f:
            pyproject_data = toml.load(f)
        citation = create_citation('CITATION.cff', None)
        print(pyproject_data['project']['version'])
        self.assertEqual(pyproject_data['project']['description'], citation.cffobj['abstract'],
                         "Descriptions of the toml and the abstract of the cff are not the same.")


class OutputFormatTester(unittest.TestCase):
    def test_guess_format(self):
        """
        tests if the output format like html or md were guessed correctly
        """
        supported_formats = ['.md', '.html']
        output_filename = 'citation.html'
        guessed_output_format = guess_format(output_filename, supported_formats)
        expected_output_format = '.html'
        self.assertEqual(guessed_output_format, expected_output_format, "Expected to have an HTML output format.")


if __name__ == '__main__':
    unittest.main()
