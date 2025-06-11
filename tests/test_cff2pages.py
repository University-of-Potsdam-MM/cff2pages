import glob
import os.path
import shutil
import tempfile
import unittest
import toml
import markdown
import re
from pathlib import Path
from bs4 import BeautifulSoup
from cffconvert.cli.create_citation import create_citation

from src.cff2pages.cff2pages import main_procedure, get_unique_affiliations, guess_format

TEST_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(TEST_DIR, "fixtures")
EXPECTED_DIR = os.path.join(TEST_DIR, "expected")


def read_div_from_body(file_path, div_id=None, div_class=None):
    """
    Reads an HTML file, extracts the <body>, and retrieves a specific <div>.
    - div_id: Specific ID of the <div> to compare (optional).
    - div_class: Specific class of the <div> to compare (optional).
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        body = soup.body

        # Retrieve the specific <div> based on ID or class
        if div_id:
            return body.find('div', id=div_id)
        elif div_class:
            return body.find('div', class_=div_class)
        else:
            return body.find('div')  # Default to the first <div>


class MinimalCffTester(unittest.TestCase):
    """
    Tests to create a html based on a minimal cff documentation.
    """

    def setUp(self):
        """
        Creates a temporary directory with the minimal cff
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cff = 'minimal.cff'
        test_file = os.path.join(os.path.dirname(__file__), FIXTURES_DIR, self.cff)
        shutil.copy2(test_file, self.temp_dir.name)

    def tearDown(self):
        """
        Deletes temporary directories
        """
        self.temp_dir.cleanup()

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


def remove_script_tags(soup):
    """Removes all <script> tags from the given HTML content."""
    for script in soup.find_all("script"):
        script.decompose()
    return soup


def check_folders(cls, tmp_dir, file_format):
    """
    Tests if the temp_dir was created and have the necessary files in it.

    :param cls: Test class which does the assertion process.
    :param tmp_dir: Directory where the files are stored.
    :param file_format: The file format which was created.
    :return: Path to the file
    """

    public_path = os.path.join(tmp_dir, 'public')
    index_file = os.path.join(public_path, 'cff2pages.' + file_format)
    cls.assertTrue(os.path.exists(public_path))
    cls.assertTrue(os.path.exists(index_file), f'There is no file for the {file_format} format.')
    return index_file


class CffToHtmlTester(unittest.TestCase):
    """
    Test case for converting .cff files to HTML and comparing the output
    against expected HTML results.
    """

    def setUp(self):
        """
        Set up a temporary directory for processing files.
        """
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """
        Clean up the temporary directory after each test.
        """
        self.temp_dir.cleanup()

    def normalize_md(text):
        return "\n".join(line.strip() for line in text.strip().splitlines() if line.strip())

    def test_cff_files(self):
        """
        Iterate over all .cff files in the fixtures directory, convert them to HTML,
        and compare the generated output with the expected HTML files.
        """
        fixtures_path = os.path.join(os.path.dirname(__file__), FIXTURES_DIR, "*.cff")
        cff_files = glob.glob(fixtures_path)

        for cff_file in cff_files:
            file_name = os.path.basename(cff_file)
            tmp_dir = self.temp_dir.name
            shutil.copy2(cff_file, tmp_dir)
            input_path = os.path.join(tmp_dir, file_name)

            # Subtest for HTML conversion
            with self.subTest(cff_file=cff_file, format="html"):
                expected_file = os.path.join(os.path.dirname(__file__), EXPECTED_DIR,
                                             f"expected_{file_name.replace('.cff', '_body.html')}")

                if not os.path.exists(expected_file):
                    self.fail(f"Expected file missing: {expected_file}")
                output_path = os.path.join(tmp_dir, "public", "cff2pages.html")
                # Convert CFF to HTML
                main_procedure(input_path, output_path)
                index_file = check_folders(self, tmp_dir, "html")

                # Read the generated and expected HTML content
                actual_body = read_div_from_body(index_file, div_class="container")
                expected_body = read_div_from_body(expected_file, div_class="container")

                # Clean script tags before comparison
                actual_body_cleaned = remove_script_tags(actual_body)
                expected_body_cleaned = remove_script_tags(expected_body)

                # Compare the prettified HTML structures
                self.assertEqual(actual_body_cleaned.prettify(), expected_body_cleaned.prettify())

            # Subtest placeholder for Markdown conversion
            with self.subTest(cff_file=cff_file, format="md"):
                expected_file = os.path.join(os.path.dirname(__file__), EXPECTED_DIR,
                                            f"expected_{file_name.replace('.cff', '.md')}")
                output_path = os.path.join(tmp_dir, "public", "cff2pages.md")
                main_procedure(input_path, output_path)
                index_file = check_folders(self, tmp_dir, "md")
                with open(index_file, encoding="utf-8") as f:
                    actual_html =  markdown.markdown(f.read())
                with open(expected_file, encoding="utf-8") as f:
                    expected_html = markdown.markdown(f.read())

                self.assertEqual(actual_html, expected_html)



class CffTomlComparer(unittest.TestCase):
    """
    Testing class to verify that the various aspects between toml and cff are the same.
    """

    def test_version_from_code_matches_cff(self):
        """
        Ensures the __version__ in src/cff2pages/__init__.py matches the version in CITATION.cff
        """
        # Get version from __init__.py
        init_path = Path("src/cff2pages/__init__.py").read_text(encoding="utf-8")
        match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", init_path, re.MULTILINE)
        self.assertIsNotNone(match, "Could not find __version__ in __init__.py")
        code_version = match.group(1)

        # Get version from CITATION.cff
        citation = create_citation('CITATION.cff', None)
        cff_version = citation.cffobj["version"]

        # Compare
        self.assertEqual(code_version, cff_version, "Version mismatch between __init__.py and CITATION.cff")

    def test_abstract_cff_toml(self):
        """
        Compares abstracts of cff and toml
        :return:
        """
        # Load and parse pyproject.toml
        with open('pyproject.toml', 'r') as f:
            pyproject_data = toml.load(f)
        citation = create_citation('CITATION.cff', None)
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
