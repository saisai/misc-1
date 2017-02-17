import os
from os.path import isdir, isfile, join

from libconda.fetch import fetch_pkg, fetch_index

from ll.utils import human_bytes, md5_file
from repo.update_index import write_repodata
from repo.config import PKGS_DIR_PATH, MAJOR_SUBDIRS, full_arch



BASE_URL = 'https://conda.anaconda.org'


def sync_platform(channel_name, subdir='linux-64', verbose=True):
    dst_dir = join('/home/data/sync', channel_name, subdir)
    if not isdir(dst_dir):
        os.makedirs(dst_dir)
    assert not isfile(join(dst_dir, 'index.json')), dst_dir

    channel_urls = ('%s/%s/%s' % (BASE_URL, channel_name, subdir + '/'),)
    if verbose:
        print "Channel URLs", channel_urls

    index = fetch_index(tuple(channel_urls))

    files_tb = set(fn for fn in index.iterkeys() if
                   fn.startswith(('llvmlite-0.16.0-', 'numba-0.31.0-')))

    files_cr = set(fn for fn in os.listdir(dst_dir)
                   if fn.endswith('.tar.bz2'))

    for fn in sorted(files_cr):
        if fn in files_tb and md5_file(join(dst_dir, fn)) == index[fn]['md5']:
            continue
        if verbose:
            print 'Removing: %s/%s/%s' % (channel_name, subdir, fn)
        os.unlink(join(dst_dir, fn))
        files_cr.remove(fn)

    for fn in sorted(files_tb):
        if fn in files_cr:
            continue
        if verbose:
            print 'Downloading: %s/%s/%s  %s' % (
                   channel_name, subdir, fn, human_bytes(index[fn]['size']))
        fetch_pkg(index[fn], dst_dir=dst_dir)

    new_index = {}
    for fn in os.listdir(dst_dir):
        if fn.endswith('.part'): # cleanup partially downloaded files
            os.unlink(join(dst_dir, fn))
            continue
        if fn.endswith('.tar.bz2'):
            info = index[fn]
            for var_name in ('channel', 'binstar', 'home_page', 'machine',
                             'target-triplet', 'requires', 'operatingsystem'):
                try:
                    del info[var_name]
                except KeyError:
                    pass
            new_index[fn] = info

    platform, arch = subdir.split('-')
    repodata = {'packages': new_index,
                'info': {'platform': platform,
                         'arch': full_arch(arch)}}

    write_repodata(repodata, dst_dir)


for platform in 'win-32', 'win-64':
    sync_platform('numba', platform, verbose=1)
