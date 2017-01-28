from repo.filedb import read_repodatas
from repo.repack import meta_from_repodata
from repo.utils import normalize_depends, meta_from_index


cnt_tot = 0
cnt_nodep = set()
cnt_depend = set()
cnt_lic = set()

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
        cnt_nodep.add(path)

    if depends1 != normalize_depends(meta2.get('depends', ['xyz'])):
        cnt_depend.add(path)

    for key in 'license', 'license_family':
        if meta1.get(key) != meta2.get(key):
            cnt_lic.add(path)

print cnt_tot
print 'no depends', len(cnt_nodep)
print 'depends', len(cnt_depend)
assert cnt_nodep <= cnt_depend
print 'license', len(cnt_lic)
print 'intersection', len(cnt_depend & cnt_lic)
print 'union', len(cnt_depend | cnt_lic)
print 'd - l', len(cnt_depend - cnt_lic)
print 'l - d', len(cnt_lic - cnt_depend)
