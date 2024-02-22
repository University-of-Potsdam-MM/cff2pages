import os
import shutil
import logging
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from cffconvert.cli.create_citation import create_citation

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def write_to_pub_folder(init_path, html_string):
    """
    creates a public folder and creates an index file with the given content in  it

    :param init_path: initial path in which the public folder should be placed
    :param html_string: content for the index.hml
    """
    path_public = os.path.join(init_path, 'public')
    path_assets = os.path.join(path_public, 'assets')
    path_img = os.path.join(path_assets, 'img')
    path_css = os.path.join(path_assets, 'css')

    # create all needed folders
    for folder in [path_public, path_assets, path_img, path_css]:
        if not os.path.exists(folder):
            os.mkdir(folder)

    # write index file
    index_html_path = os.path.join(path_public, 'index.html')
    with open(index_html_path, 'w', encoding='utf-8') as file:
        file.write(html_string)

    # cp image files
    orcid_logo = 'orcid_16x16.webp'
    github_logo = 'github-logo.png'
    gitlab_logo = 'gitlab-logo.png'

    copy_files_to(path_img, 'img', [orcid_logo, github_logo, gitlab_logo])

    # cp css file
    css_file = 'default.css'

    copy_files_to(path_css, 'css', [css_file])


def copy_files_to(path_img, sub_folder, to_copy_files):
    for to_copy_file in to_copy_files:
        image_path = Path(__file__).parent.joinpath('resources').joinpath(sub_folder).joinpath(
            to_copy_file)
        shutil.copy2(image_path, os.path.join(path_img, to_copy_file))


def get_unique_affiliations(authors):
    unique_affiliation = list()
    for author in authors:
        if unique_affiliation.count(author['affiliation']) == 0:
            unique_affiliation.append(author['affiliation'])
    unique_affiliation.sort()
    return unique_affiliation


def main_procedure(init_path, cff_path):
    """
    function to process all steps in the main method

    :param cff_path: path to cff file
    :param init_path: initial path in which the public folder should be placed

    """

    print(init_path)
    env = Environment(
        loader=PackageLoader("cff2pages"),
        autoescape=select_autoescape()
    )
    index_templ = env.get_template('index.html')
    if cff_path is None:
        cff_file = 'CITATION.cff'
    else:
        cff_file = cff_path
    citation = create_citation(cff_file, None)
    citation.validate()
    citation.cffobj['unique_affiliations'] = get_unique_affiliations((citation.cffobj['authors']))
    if 'repository-code' in citation.cffobj:
        citation.cffobj['repository'] = citation.cffobj['repository-code']
    else:
        logger.warning("No 'repository-code' found in CITATION.cff.")
    citation.cffobj['citation'] = {}
    citation.cffobj['citation']['apa'] = str(citation.as_apalike())
    index_html = index_templ.render(citation.cffobj)
    write_to_pub_folder(init_path, index_html)


def init_main():
    main_procedure(os.getcwd(), None)


if __name__ == '__main__':
    init_main()
