#! /usr/bin/env python
# Copyright (c) 2011 LightKeeper LLC
# ANY REDISTRIBUTION OR COPYING OF THIS MATERIAL WITHOUT THE EXPRESS CONSENT
# OF LIGHTKEEPER IS PROHIBITED.
# All rights reserved.
"""
Downloads the required python installers from web sites of compiled binaries and adds them
to the local directory.  This script does not actually execute the installers it only
fetches the most recent for both 32bit and 64 bit libraries.  The list is ordered below
and the files are downloaded in order of install.
"""
PYTHON_PACKAGES = ['boost_python', 'pyzmq', 'cython', 'greenlet', 
                   'pywin32', 'py2exe', 'lxml', 'ipython', 'pil', 'numpy', 'numexpr',
                   'scipy', 'h5py', 'tables', 'matplotlib', 'reportlab', 'thrift', 'pandas']

PYTHON_VER = '2.7'
PYTHON_PACKAGES_URL = 'http://www.lfd.uci.edu/~gohlke/pythonlibs/'

import os
import urllib
import re
import optparse

BIT_32 = 'win32'
BIT_64 = 'amd64'
STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
STORAGE_DIR_32 = os.path.join(STORAGE_DIR, BIT_32, 'python')
STORAGE_DIR_64 = os.path.join(STORAGE_DIR, BIT_64, 'python')

packageGrab = re.compile("^.*?\[(.*)\], \"(.*)\"\)'>(.*?)&.*$")

class maskedDownloader(urllib.FancyURLopener):
    # IE6 string: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)
    # Firefox 2.0: 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    
def getDownloadURL(indexStr, dataStr):
    """
    The information for translating the url is in the java code at the top of the page.
    It is a two part lookup of indexing.
    """
    ml = [int(value) for value in indexStr.split(',')]
    dataStr = dataStr.replace('&lt;', '<')
    dataStr = dataStr.replace('&gt;','>')
    dataStr = dataStr.replace('&amd;', '&')
    
    download = ''.join([chr(ml[ord(c)-48]) for c in dataStr])
    return ''.join([PYTHON_PACKAGES_URL, download])

def getPythonPackages(packages=None):
    """
    Parses the page to get the download urls for the packages.  For some reason the page
    attempts to be rather crafty about the urls, so this code translates it.
    """
    masked = maskedDownloader()
    
    # get the python packages
    page = masked.open(PYTHON_PACKAGES_URL)
    data = page.read()
    downloads = {BIT_64:{},BIT_32:{}}
    for line in data.split('\n'):
        line = line.strip()
        if line.startswith("<li><a href='javascript:;'"):
            m = packageGrab.match(line)
            if m is None:
                continue
            indexStr = m.group(1)
            dataStr = m.group(2)
            package = m.group(3)
            pDetails = package.split('-')
            pName = pDetails[0].lower()
            pPyVersion = pDetails[-1]
            if pDetails[-2].endswith('amd64'):
                pBitSize = BIT_64
            else:
                pBitSize = BIT_32
            if pPyVersion.endswith(PYTHON_VER):
                downloads[pBitSize][pName] = (package, getDownloadURL(indexStr, dataStr))

    found = 0
    skipped = 0
    downloaded = 0
    for package in PYTHON_PACKAGES:
        if packages is None or package in packages:
            for bitSize, storeDir in [(BIT_64, STORAGE_DIR_64)]: #Ignoring 32bit (BIT_32, STORAGE_DIR_32)
                try:
                    data = downloads[bitSize][package]
                except KeyError:
                    continue
                found += 1
                localFile = os.path.join(storeDir, data[1].split('/')[-1])
                if not os.path.exists(localFile):
                    print('Downloading %-15s to %s' % (package, localFile))
                    masked.retrieve(data[1], localFile)
                    downloaded += 1
                else:
                    skipped += 1

    print('Found %d, Skipped %d, Downloaded %d of Total %d' % (found, skipped, downloaded, len(PYTHON_PACKAGES)))
    return found, skipped, downloaded 

if __name__ == "__main__":
    parser = optparse.OptionParser(usage="fetchInstallers <package list>")

    opts, args = parser.parse_args()
    packages = None
    if len(args) > 0:
        packages = {args[0].split(',')}
    getPythonPackages(packages)
    
