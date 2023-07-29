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
    path_public_folder = os.path.join(init_path, 'public')
    path_public_assets_folder = os.path.join(path_public_folder, 'assets')
    path_public_img_folder = os.path.join(path_public_assets_folder, 'img')

    # create all needed folders
    for folder in [path_public_folder, path_public_assets_folder, path_public_img_folder]:
        if not os.path.exists(folder):
            os.mkdir(folder)

    # write index file
    index_html_path = os.path.join(path_public_folder, 'index.html')
    with open(index_html_path, 'w', encoding='utf-8') as file:
        file.write(html_string)
    # cp image files
    orcid_logo = 'orcid_16x16.webp'
    github_logo = 'github-logo.png'
    gitlab_logo = 'gitlab-logo.png'

    for logo in [orcid_logo, github_logo, gitlab_logo]:
        image_path = Path(__file__).parent.joinpath('resources').joinpath(logo)
        shutil.copy2(image_path, os.path.join(path_public_img_folder, logo))


def get_unique_affiliations(authors):
    unique_affiliation = list()
    for author in authors:
        if unique_affiliation.count(author['affiliation']) == 0:
            unique_affiliation.append(author['affiliation'])
    unique_affiliation.sort()
    return unique_affiliation


def main_procedure(init_path):
    """
    function to process all steps in the main method

    :param init_path: initial path in which the public folder should be placed

    """

    print(init_path)
    env = Environment(
        loader=PackageLoader("cff2pages"),
        autoescape=select_autoescape()
    )
    index_templ = env.get_template('index.html')
    citation = create_citation('CITATION.cff', None)
    citation.validate()
    citation.cffobj['unique_affiliations'] = get_unique_affiliations((citation.cffobj['authors']))
    if 'repository-code' in citation.cffobj:
        citation.cffobj['repository'] = citation.cffobj['repository-code']
    else:
        logger.warning("No 'repository-code' found in CITATION.cff.")
    print(citation.cffobj)
    index_html = index_templ.render(citation.cffobj)
    write_to_pub_folder(init_path, index_html)


if __name__ == '__main__':
    main_procedure(os.getcwd())
