import os
import shutil
import pkg_resources

from jinja2 import Environment, PackageLoader, select_autoescape
from cffconvert.cli.create_citation import create_citation


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
    image_path = pkg_resources.resource_filename('cff2pages', os.path.join('resources', orcid_logo))
    shutil.copy2(image_path, os.path.join(path_public_img_folder, orcid_logo))


def main_procedure(init_path):
    """
    function to process all steps in the main method

    :param init_path: initial path in which the public folder should be placed

    """

    env = Environment(
        loader=PackageLoader("cff2pages"),
        autoescape=select_autoescape()
    )
    index_templ = env.get_template('index.html')
    dummy_data = {
        'title': 'This is the Test-title',
        'author': ' Jan Bernoth'
    }
    citation = create_citation('CITATION.cff', None)
    citation.validate()
    print(citation.cffobj['authors'])
    index_html = index_templ.render(citation.cffobj)
    write_to_pub_folder(init_path, index_html)


if __name__ == '__main__':
    main_procedure('.')
