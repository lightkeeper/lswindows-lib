Windows Compiled Libraries
---------------------------

This module contains compiled libraries for windows which are required to run LightStation.  A developer should
not have to directly update this. It will be updated automatically from the git repository by local installers.

Updating managed libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The python file in this directory, fetchInstallers.py, attempts to automate much of the installer downloading
and maintenance by leveraging the great work of Christoph Gohlke.  He posts on his `website<http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_
a large number of the needed libraries for python.  A script will fetch the most recent files.  The version
numbers will need to be incorporated into StationControl to result in an update.  To run the script execute::

    ./fetchInstallers.py


Static Prebuilt Libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OpenSSL binaries obtained from `here <http://www.slproweb.com/products/Win32OpenSSL.html>`_ 

Internally Compiled Libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Some libraries must be compiled by hand to run on the platform.  Python 2.7 compatibility requires that these libraries
be compiled under Visual Studio 2008.  The process to handle various libraries is outlined below.

The generic handling on python when you have Visual Studio installed is to run::

   python setup.py build bdist_wininst --user-access-control=auto

This will build an install exe using VisualStudio 2008 automatically.

Gevent
++++++++

Latest version 1.0b2 does not require a seperate compile of libevent but instead bundles a build of libev.
It is important to make sure you grab the source tarball to build rather than source.  The tarball does not
require cython to build and works around many build issues (one being needing man gnu command line tools).
Download the tarball and run::

    python setup.py build bdist_wininst --user-access-control=auto

Pytables
++++++++
#. First read the `documentation on building from source <http://www.pytables.org/docs/manual/ch02.html#sourceInstallationDescr>`_.

#. From `the hdf5 downloads page <http://www.hdfgroup.org/HDF5/release/obtain5.html>`_, download and unpack the windows/x64 binaries for szip and zlib. Download and unpack the Windows 64 bit VS 2008 hdf5 binary build. Copy zlib1.dll and szlibdll.dll to C:\\Windows\\system (create directory if it does not exist)

#. Set an environment variable to tell the build about hdf5::

    set HDF5_DIR=C:\LightKeeper\Downloads\hdf5_183_xp64_vs2008_ivf101

#. lzo and bzip2 are optional and not covered.

#. Download and unpack the pytables source. Because of an error, you may need to edit setup.py and change the Windows section of the build, starting at line 101 in pytables 2.1.1 and append the last line to help pytables find the hdf5 dll::

    elif os.name == 'nt':
    default_header_dirs = []  # no default, must be given explicitly
    default_library_dirs = []  # no default, must be given explicitly
    default_runtime_dirs = [  # look for DLL files in ``%PATH%``
        _path for _path in os.environ['PATH'].split(';') ]
    # Add the \Windows\system to the runtime list (necessary for Vista)
    default_runtime_dirs.append('\\windows\\system')
    # Add the \path_to_python\DLLs and tables package to the list
    default_runtime_dirs.extend(
        [ os.path.join(sys.prefix, 'Lib\\site-packages\\tables') ]   )
    default_runtime_dirs.append( r'C:\LightKeeper\Downloads\hdf5_183_xp64_vs2008_ivf101\dll'    )

#. Build the installer from Visual Studio 2008 x64 Command prompt::

    python setup.py build bdist_wininst --user-access-control=auto

Lxml
++++
#. Download libxml, libxslt, libiconv and zlib from the `php libs <http://pecl2.php.net/downloads/php-windows-builds/php-libs/VC9/x64/>`_. Unzip them all to *the same directory*. This should create bin, include and lib dirs in that directory.

#. In the lib dir under your unzip directory, rename all libiconv* to iconv*. For example, libiconv.exp should be renamed to iconv.exp.

#. rename zlib1.lib to zlib.lib

#. Download and unzip the `lxml source <http://codespeak.net/lxml/index.html#download>`_.

#. In the lxml unzip directory, read doc/build.txt. It contains instructions on building with Windows. The relevant section of my edited setup.py looked like::

    STATIC_INCLUDE_DIRS = [r'C:\Newell\Downloads\lxml-build\include']
    STATIC_LIBRARY_DIRS = [r'C:\Newell\Downloads\lxml-build\lib']
    STATIC_CFLAGS = []
    STATIC_BINARIES = []

#. In your Visual Studio x64 build command prompt, build lxml::

    python setup.py build bdist_wininst --user-access-control=auto --static

Matplotlib
+++++++++++

#. Installation instructions can be found `here <http://matplotlib.sourceforge.net/users/installing.html>`__.

#. Download and unzip the latest `matplotlib's source .tar.gz <http://sourceforge.net/projects/matplotlib/files/>`_. Ignore the installers as they are compiled with something other than Visual Studio 2008 and do not work.

#. Navigate to the unzip directory and create a directory called win32_static. My path looked like ``C:\\Newell\\Downloads\\matplotlib-0.99.0\\win32_static``
#. From the `php libs <http://pecl2.php.net/downloads/php-windows-builds/php-libs/VC9/x64/>`_, download freetype, libpng and zlib. Unzip the contents of these to the win32_static directory you created.

#. Navigate to win32_static\\include. Move the files under libpng12 to the current directory.

#. Navigate to win32_static\\lib. Rename zlib_a.lib to z.lib. Rename libpng_a.lib to png.lib and libpng_a_debug.lib to png_debug.lib. Rename freetype_a.lib to freetype.lib.

#. In your Visual Studio x64 build command prompt, build matplotlib::

    python setup.py build bdist_wininst --user-access-control=auto


`Python Imaging Library (PIL) <http://www.pythonware.com/products/pil/>`_:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. From the `php libs <http://pecl2.php.net/downloads/php-windows-builds/php-libs/VC9/x64/>`_, download freetype, libjpeg and zlib. Unzip the contents of these to a common directory.

#. In your unzip directory, go to the lib directory. Rename freetype_a.lib to freetype.lib. Rename libjpeg_a.lib to libjpeg.lib.

#. Download and unzip the latest `PIL Source <http://www.pythonware.com/products/pil/>`_.

#. Navigate to your PIL Source unzip and edit setup.py, changing the ROOT sections to point to your unzip of the libs from the php site. Mine looked like::

    FREETYPE_ROOT = libinclude(r'C:\Newell\Downloads\imaging-build')
    JPEG_ROOT = libinclude(r'C:\Newell\Downloads\imaging-build')
    TIFF_ROOT = None
    ZLIB_ROOT = libinclude(r'C:\Newell\Downloads\imaging-build')
    TCL_ROOT = None

#. In your Visual Studio x64 build command prompt, build PIL::

    python setup.py build bdist_wininst --user-access-control=auto

Pygit2
++++++
#. Build libgit2

    #. Ensure cmake is installed and download libgit from github::

          git clone https://github.com/libgit2/libgit2.git

    #. Following `these<https://github.com/libgit2/libgit2sharp/wiki/How-to-build-x64-libgit2-and-LibGit2Sharp>`_ instructions to comment out errors in Visual Studio from GitBash::

           sed -i -s -e 's@SET(CMAKE_C_FLAGS "/W4 /nologo /Zi ${CMAKE_C_FLAGS}")@SET(CMAKE_C_FLAGS "/W4 /wd4244 /wd4267 /nologo /Zi ${CMAKE_C_FLAGS}")@' CMakeLists.txt

    #. Build from Visual Studio 2008 Command Prompt.
          mkdir buildx64
          cd buildx64
          cmake -G "Visual Studio 9 2008 Win64" ..
          cmake -- build .

    #.  Download pygit2 from github::

            git clone https://github.com/libgit2/pygit2.git

    #.  Copy zlib header and lib download downloaded from the `HDF5 precompiled binary <http://www.hdfgroup.org/HDF5/release/obtain5.html>`_ into include and lib.

    #.  Copy the headers and libs from the OpenSSL package installed above.

    #.  Copy the git includes and the compiled lib from the libgit package above ... including subdirectories.

    #.  Edit the setup.py file to point to the local include and lib directories created.  Edit the library names to be::

             libraries = ['git2', 'zlib', 'ssleasy32', 'libeay32']

    #.  This will build the distributable file, but the git2.dll will need to be installed into the same directory.

