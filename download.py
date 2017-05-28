#! python2
# download.py - Downloads every single installed pip package.

import requests, os, bs4
import unicodedata

def download_package(url='https://pypi.python.org/pypi/exchangelib/1.9.3'):

    if not os.path.exists('backup'):
        os.makedirs('backup')

    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    try:
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'lxml')

        if not 'Not Found' in soup.text:

            # Find the URL of the packages.
            tables = soup.findAll('table')

            files = []
            for table in tables:
                if 'File' in table.text and 'Type' in table.text and 'Py Version' in table.text:
                    print('found download table')
                    #print(table)
                    rows = table.findAll('tr')
                    for row in rows:
                        link = row.find('a')
                        if link:
                            print(link['href'])
                            files.append(link['href'])

            for f in files:
                print(f)

            if files:
                for f in files:
                    try:
                        urlforfilesystem = unicodedata.normalize('NFKD', u''+ f +'').encode('ascii', 'ignore')
                        urlforfilesystem = urlforfilesystem[:urlforfilesystem.find('#')]
                        # Download the file.
                        print('Downloading image %s...' % (urlforfilesystem))
                        res = requests.get(f)
                        res.raise_for_status()

                        # Save the file to ./backup.
                        BackupFile = open(os.path.join('backup', os.path.basename(urlforfilesystem)), 'wb')
                        for chunk in res.iter_content(100000):
                            BackupFile.write(chunk)
                        BackupFile.close()

                    except requests.exceptions.MissingSchema:
                        print('didnt found!')
                        continue


    except requests.exceptions.HTTPError as e:
        print('http error {}'.format(e))



