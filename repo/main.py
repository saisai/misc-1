import re
from os.path import basename

from repo.filedb import read_repodatas
from repo.repack import meta_from_repodata
from repo.utils import normalize_depends, meta_from_index


cnt_tot = 0
set_nodep = set()
set_depend = set()
set_lic = set()

for path, unused_md5 in read_repodatas():
    meta2 = meta_from_index(path)
    if meta2 is None:
        continue
    if 'ctime' not in meta2:
        print path, 'NO ctime'
        continue
    if meta2['ctime'] < 1.3E9:
        print path, meta2['ctime']

    meta1 = meta_from_repodata(path)
    depends1 = meta1['depends']
    assert normalize_depends(depends1) == depends1

    cnt_tot += 1

    if 'depends' not in meta2:
        set_nodep.add(path)

    if depends1 != normalize_depends(meta2.get('depends', ['xyz'])):
        set_depend.add(path)
    for key in 'features', 'track_features':
        if meta1.get(key) != meta2.get(key):
            set_depend.add(path)

    for key in 'license', 'license_family':
        if meta1.get(key) != meta2.get(key):
            set_lic.add(path)

print cnt_tot
print 'no depends', len(set_nodep)
print 'depends', len(set_depend)
assert set_nodep <= set_depend
print 'license', len(set_lic)
print 'intersection', len(set_depend & set_lic)
print 'union', len(set_depend | set_lic)
print 'd - l', len(set_depend - set_lic)
print 'l - d', len(set_lic - set_depend)

with open('out.txt', 'w') as fo:
    pat = re.compile(r'anaconda\-\d\.\d')
    for f in sorted(set_depend):
        if pat.match(basename(f)):
            continue
        if '/linux-32/' in f:
            fo.write('%s\n' % f)
