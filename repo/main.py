from repo.filedb import read_repodatas
from repo.repack import meta_from_repodata
from repo.utils import normalize_depends, meta_from_index


cnt_tot = cnt_depend = cnt_lic = cnt_dl = 0

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

    if depends1 != normalize_depends(meta2.get('depends', [])):
        cnt_depend += 1
        cnt_dl += 1

    lc = False
    for key in 'license', 'license_family':
        if meta1.get(key) != meta2.get(key):
            lc = True

    if lc:
        cnt_lic += 1
        cnt_dl += 1

for varname in 'cnt_tot', 'cnt_depend', 'cnt_lic', 'cnt_dl':
    print '%s: %d' % (varname, eval(varname))
