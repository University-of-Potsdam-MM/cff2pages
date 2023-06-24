import os

from jinja2 import Environment, PackageLoader, select_autoescape


def write_to_pub_folder(init_path, html_string):
    """
    creates a public folder and creates an index file with the given content in  it

    :param init_path: initial path in which the public folder should be placed
    :param html_string: content for the index.hml
    """
    path_public_folder = os.path.join(init_path, 'public')
    if not os.path.exists(path_public_folder):
        os.mkdir(path_public_folder)
    index_html_path = os.path.join(path_public_folder, 'index.html')
    with open(index_html_path, 'w', encoding='utf-8') as file:
        file.write(html_string)


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
    index_html = index_templ.render(dummy_data)
    write_to_pub_folder(init_path, index_html)


if __name__ == '__main__':
    main_procedure('.')
