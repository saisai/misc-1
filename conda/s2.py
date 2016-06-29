import time
import random
from pprint import pprint

from conda.connection import CondaSession


url = 'http://repo.continuum.io/pkgs/free/osx-64/repodata.json.bz2'
url = 'https://conda.anaconda.org/conda-forge/osx-64/repodata.json.bz2'

while 1:
    startTime = time.time()
    session = CondaSession()
    resp = session.get(url)
    timeTaken = time.time() - startTime
    print resp.status_code, timeTaken
    pprint(dict(resp.headers))
    time.sleep(random.random() * 5.0)
