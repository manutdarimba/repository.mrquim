#! /usr/bin/python
############################################################################
#
#  Copyright 2012 Lee Smith
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

import sys
import os
import time
from argparse import ArgumentParser, RawTextHelpFormatter
from urlparse import urlparse
import bz2
import logging

from resources.lib.funcs import size_fmt, add_deps_to_path
add_deps_to_path()

import requests

from resources.lib import libreelec, config, sources, builds, history, log, funcs

arch_default = None
if libreelec.OS_RELEASE['NAME'] != "LibreELEC":
    from resources.lib import mock
    mock.mock_libreelec()
    libreelec.UPDATE_DIR = os.path.expanduser('~')
    arch_default = 'RPi2.arm'

parser = ArgumentParser(description='LibreELEC Dev Updater CLI')
subparsers = parser.add_subparsers(title='commands')

def get_choice(items, suffix=lambda item: " ", reverse=False):
    num_width = len(str(len(items) - 1))

    if reverse:
        items_iter = reversed(list(enumerate(items)))
    else:
        items_iter = enumerate(items)

    for i, item in items_iter:
        print "[{num:{width}d}] {item:s}\t{suffix}".format(
            num=i, item=item, width=num_width, suffix=suffix(item))
    print '-' * 50

    choice = raw_input('Choose an item or "q" to quit: ')
    while choice != 'q':
        try:
            item = items[int(choice)]
            return item
        except ValueError:
            choice = raw_input('You entered a non-integer. Choice must be an'
                               ' integer or "q": ')
        except IndexError:
            choice = raw_input('You entered an invalid integer. Choice must be'
                               ' from above list or "q": ')
    sys.exit()

def read_chunk(f):
    return f.read(131072)

decompressor = bz2.BZ2Decompressor()
def decompress(f):
    data = read_chunk(f)
    return decompressor.decompress(data)

def process(fin, fout, size, read_func=read_chunk):
    start_time = time.time()
    done = 0
    while done < size:
        data = read_func(fin)
        done = fin.tell()
        fout.write(data)
        percent = int(done * 100 / size)
        bytes_per_second = done / (time.time() - start_time)
        print "\r {0:3d}%   ({1}/s)   ".format(percent, size_fmt(bytes_per_second)),
        sys.stdout.flush()
    print

def download(args):
    if args.arch:
        config.arch = args.arch

    installed_build = builds.get_installed_build()

    def build_suffix(build):
        if build > installed_build:
            symbol = '+'
        elif build < installed_build:
            symbol = '-'
        else:
            symbol = '='
        return symbol

    build_sources = sources.build_sources()

    if args.source:
        source_name = args.source
        try:
            build_source = build_sources[source_name]
        except KeyError:
            parsed = urlparse(source_name)
            if parsed.scheme in ('http', 'https') and parsed.netloc:
                if args.releases:
                    build_url = builds.BuildsURL(source_name,
                                                 extractor=builds.ReleaseLinkExtractor)
                else:
                    build_url = builds.BuildsURL(source_name)
            else:
                print ('"{}" is not in the list of available sources '
                       'and is not a valid HTTP URL').format(args.source)
                print 'Valid options are:\n\t{}'.format("\n\t".join(build_sources.keys()))
                sys.exit(1)
    else:
        source_name = get_choice(build_sources.keys())
        build_source = build_sources[source_name]

    print
    print "Arch: {}".format(config.arch)
    print "Installed build: {}".format(installed_build)

    try:
        links = build_source.builds()
    except requests.RequestException as e:
        print str(e)
    except builds.BuildURLError as e:
        print str(e)
    else:
        if links:
            build = get_choice(links, build_suffix, reverse=True)
            remote = build.remote_file()
            file_path = os.path.join(libreelec.UPDATE_DIR, build.filename)
            print
            print "Downloading {0} ...".format(build.url)
            try:
                with open(file_path, 'w') as out:
                    process(remote, out, build.size)
            except KeyboardInterrupt:
                os.remove(file_path)
                print
                print "Download cancelled"
                sys.exit()

            if build.compressed:
                tar_path = os.path.join(libreelec.UPDATE_DIR, build.tar_name)
                size = os.path.getsize(file_path)
                print
                print "Decompressing {0} ...".format(file_path)
                with open(file_path, 'r') as fin, open(tar_path, 'w') as fout:
                    process(fin, fout, size, decompress)
                os.remove(file_path)

            funcs.create_notify_file(source_name, build)

            print
            print "The update is ready to be installed. Please reboot."
        else:
            print
            print "No builds available"

def print_install_history(args):
    if args.logdebug:
        logging.getLogger().setLevel(logging.DEBUG)

    print history.BuildHistory(args.dbpath)


download_parser = subparsers.add_parser('download', help="Download an update")
download_parser.add_argument('-a', '--arch',
                             help='Set the build type (e.g. Generic.x86_64, RPi.arm)',
                             default=arch_default)
download_parser.add_argument('-s', '--source', help='Set the build source')
download_parser.add_argument('-r', '--releases', action='store_true',
                             help='Look for unofficial releases instead of development builds')
download_parser.set_defaults(func=download)

history_parser = subparsers.add_parser('history', help="Show the install history",
                                       formatter_class=RawTextHelpFormatter)
history_parser.add_argument(
    'dbpath', nargs='?',
    default="/storage/.kodi/userdata/addon_data/script.libreelec.devupdater/",
    help="path to the install history database \n (default: %(default)s)")

history_parser.add_argument(
    '--logdebug', action='store_true',
    help="log all debug messages to the log file ({})".format(log.log_path))
history_parser.set_defaults(func=print_install_history)

args = parser.parse_args()
args.func(args)
