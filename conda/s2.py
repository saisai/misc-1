from pprint import pprint
from conda.connection import CondaSession


url = 'http://repo.continuum.io/pkgs/free/osx-64/repodata.json'
url = 'https://conda.anaconda.org/ilan/osx-64/repodata.json'


session = CondaSession()
resp = session.get(url,
                   headers={'If-None-Match': '"551f32ee-9b"'})
print resp.status_code
pprint(dict(resp.headers))
