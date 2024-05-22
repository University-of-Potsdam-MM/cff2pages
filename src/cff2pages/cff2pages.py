import os
import logging
import shutil
from argparse import ArgumentParser, FileType
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
    output_dir = os.path.split(init_path)[0]
    path_assets = os.path.join(output_dir, 'assets')
    path_img = os.path.join(path_assets, 'img')
    path_css = os.path.join(path_assets, 'css')

    # create all needed folders
    for folder in [output_dir, path_assets, path_img, path_css]:
        if not os.path.exists(folder):
            os.mkdir(folder)

    # write index file
    with open(init_path, 'w', encoding='utf-8') as fh:
        fh.write(html_string)

    # cp image files
    orcid_logo = 'orcid_16x16.webp'
    github_logo = 'github-logo.png'
    gitlab_logo = 'gitlab-logo.png'

    copy_files_to(path_img, 'img', [orcid_logo, github_logo, gitlab_logo])

    # cp css file
    css_file = 'cff2pages.css'

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


def guess_format(filename, supported_formats):
    """
    extracts the file extension and raises a ValueError if the extension is not one of our supported formats.
    """
    extension = os.path.splitext(filename)[-1]
    if extension in supported_formats:
        return extension
    else:
        raise ValueError(f'Extension of given output file ({filename}) is not one of the supported formats. Formats currently supported: ({supported_formats}).')

def main_procedure(cff_path, init_path):
    """
    function to process all steps in the main method

    :param cff_path: path to cff file
    :param init_path: initial path in which the public folder should be placed

    """
    # extract extension of output filename
    supported_formats = ['.html', '.md'] # list of output file formats we currently support
    output_format = guess_format(init_path, supported_formats)

    print(init_path)
    env = Environment(
        loader=PackageLoader("cff2pages"),
        autoescape=select_autoescape()
    )
    index_templ = env.get_template('base.html')
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


def parse_command():
    '''
    Parses options from the command line.
    
    Returns: a tuple of the option values (input_file, output_file).
    '''
    parser = ArgumentParser(
        prog='cff2pages',
        description='Converts citation information in Citation File Format into HTML or Markdown'
    )
    parser.add_argument(
        '-i', '--input', 
        default='./CITATION.cff', 
        nargs='?', 
        help='path to the input CFF file'
    )
    parser.add_argument(
        '-o', '--output', 
        default='public/citation.html', 
        nargs='?', 
        help='path to the output file'
    )
    args = parser.parse_args()
    return args


def init_main():
    command_args = parse_command()
    main_procedure(command_args.input, command_args.output)


if __name__ == '__main__':
    init_main()
