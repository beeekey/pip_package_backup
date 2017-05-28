import pip
import requests, os, bs4
import unicodedata
from download import download_package

def get_installed_packages():
    installed_packages = pip.get_installed_distributions()
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    print(installed_packages_list)
    return installed_packages_list


if __name__ == '__main__':
    installed_packages_list = get_installed_packages()


    for package in installed_packages_list:
        # download all packages to an backup folder

        name = package[:package.find('=')]
        version = package[package.find('=')+2:]

        if 'dev' in version:
            version = version[:version.find('dev')]

        url = 'https://pypi.python.org/pypi/' + name + '/' + version
        print(url)
        download_package(url)



