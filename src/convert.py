import os
from bs4 import BeautifulSoup


def update_links(input_file: str, output_file: str):
    """
    Update the links in the HTML file to point to the correct local files.
    """

    link_conversions = {
        '/gipfel/suche.php?gebietnr=': 'gebiet/',
        '/gipfel/details.php?gipfelnr=': 'gipfel/',
        '/wege/suche.php?gipfelnr=': 'wege/',
        '/wege/bewertungen/anzeige.php?wegnr=': 'comments/',
    }
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        head = soup.find('head')
        if head and not input_file.endswith('index.html'):
            # Create a new <base> tag
            base_tag = soup.new_tag('base', href='..')

            # Insert the <base> tag at the beginning of the <head> section
            head.insert(0, base_tag)

        for a_tag in soup.find_all('a', href=True):
            original_link = a_tag['href']
            for needle, folder in link_conversions.items():
                if original_link.startswith(needle):
                    number = original_link.split('=')[-1]
                    new_link = folder + f'{number}.html'
                    a_tag['href'] = new_link

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))


def walk_directory_and_convert(base_path: str):
    """
    Walk through the directory and convert each HTML file.
    """
    source_path = base_path + 'output/'
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith('.html'):
                input_file_path = os.path.join(root, file)
                output_path_parts = input_file_path.split(os.sep)
                output_path_parts = ['converted' if part == 'output' else part for part in output_path_parts]
                output_file_path = os.sep.join(output_path_parts)
                print(f'converting file: {input_file_path}')
                update_links(input_file_path, output_file_path)


if __name__ == '__main__':
    base_path = '/home/est/src/teufel-spider/'
    walk_directory_and_convert(base_path)