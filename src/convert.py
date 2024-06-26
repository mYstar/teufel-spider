import os
import shutil

from bs4 import BeautifulSoup


def update_links(input_file: str, output_file: str):
    """
    Update the links in the HTML file to point to the correct local files.
    """

    link_conversions = {
        '/wege': 'index.html',
        '/gipfel': 'index.html',
        '/gipfel/suche.php?gebietnr=': 'gebiet/',
        '/gipfel/details.php?gipfelnr=': 'gipfel/',
        '/wege/suche.php?gipfelnr=': 'wege/',
        'suche.php?gipfelnr=': 'wege/',
        '/wege/bewertungen/anzeige.php?wegnr=': 'comments/',
    }
    img_conversions = {
        '/img/symbole/': 'img/symbole/',
    }
    delete_elements = {
        'body > table:nth-child(2) > tr > td:nth-child(1)',
        'body > table:nth-child(1) > tr > td:nth-child(3) > div > font > a',
        'body > table:nth-child(4) > tr > td:nth-child(2)'
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
            a_tag.attrs.pop('target', None)

            original_link = a_tag['href']
            for needle, folder in link_conversions.items():
                if original_link.startswith(needle):
                    if '=' in original_link:
                        number = original_link.split('=')[-1]
                        new_link = folder + f'{number}.html'
                        a_tag['href'] = new_link
                    else:
                        a_tag['href'] = folder

        # correct image src
        for img_tag in soup.find_all('img', src=True):
            original_link = img_tag['src']
            for needle, folder in img_conversions.items():
                if original_link.startswith(needle):
                    filename = original_link.split('/')[-1]
                    new_link = folder + f'{filename}'
                    img_tag['src'] = new_link

        # delete unused elements
        for selector in delete_elements:
            list = soup.select(selector)
            for element in list:
                element.decompose()

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))


def walk_directory_and_convert(base_path: str):
    """
    Walk through the directory and convert each HTML file.
    """
    source_path = base_path + 'output/'
    for root, dirs, files in os.walk(source_path):
        for file in files:
            input_file_path = os.path.join(root, file)
            output_path_parts = input_file_path.split(os.sep)
            output_path_parts = ['converted' if part == 'output' else part for part in output_path_parts]
            output_file_path = os.sep.join(output_path_parts)
            if file.endswith('.html'):
                print(f'converting file: {input_file_path}')
                update_links(input_file_path, output_file_path)
            if file.endswith('.gif'):
                print(f'copying file: {input_file_path}')
                shutil.copy(input_file_path, output_file_path)


if __name__ == '__main__':
    base_path = '/home/est/src/teufel-spider/'
    walk_directory_and_convert(base_path)
