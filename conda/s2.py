from pprint import pprint
from conda.connection import CondaSession


url = 'http://repo.continuum.io/pkgs/free/osx-64/repodata.json.bz2'
url = 'https://conda.anaconda.org/conda-forge/osx-64/repodata.json.bz2'

session = CondaSession()
resp = session.get(url,
                   headers={'If-None-Match': '"576d9600-461a7"'})
print resp.status_code
pprint(dict(resp.headers))
