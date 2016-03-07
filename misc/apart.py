import datetime
from dateutil.parser import parse


now = datetime.datetime.now()
ilan = parse('Oct 29 1971')
andreas = parse('Dec 4 1971')
arvin = parse('Apr 19 1973')
heather = parse('May 14 1991')

print (heather - ilan).days
print (now - ilan).days
print (now - heather).days
