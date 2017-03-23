'''\
Austin, TX
  576 8h36
El Paso, TX
  305 4h58
Santa Fe, NM
  412 6h17
Sedona, AZ
  426 6h33
San Bernadino
   60 1h00
Los Angeles
  347 5h41
Big Sur
  147 2h28
San Francisco
   12 0h20
Oakland, CA
  357 5h43
Medford, OR
  273 4h34
Portland, OR
  173 2h43
Seattle, WA
   89 1h29
Bellingham
  577 9h23
Boise, ID
  621 9h35
Grand Junction, CO
  684 11h25
Lubbock
  373 5h53
Austin
'''

tot_miles = 0
for line in __doc__.splitlines():
    line = line.strip()
    if line[0].isdigit():
        miles, hrs = line.split()
        tot_miles += int(miles)
print tot_miles
