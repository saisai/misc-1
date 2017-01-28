from repo.filedb import read_repodatas
from repo.repack import meta_from_repodata
from repo.utils import normalize_depends, meta_from_index


cnt = 0
for path, unused_md5 in read_repodatas():
    meta2 = meta_from_index(path)
    if meta2 is None:
        continue
    meta1 = meta_from_repodata(path)

    depends1 = meta1['depends']
    assert normalize_depends(depends1) == depends1
    changes = bool(depends1 != normalize_depends(meta2.get('depends', [])))
    for key in 'license', 'license_family':
        changes = changes or (meta1.get(key) != meta2.get(key))
    #print '%-60s %s' % (path[17:], changes)
    cnt += int(bool(changes))

print cnt
