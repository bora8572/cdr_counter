#!/usr/bin/env python

# For TrunkGroup: cdr_counter.py InputFile "TG Name" [OutputFile]
# For all records: cdr_counter.py InputFile S [OutputFile]

from sys import argv  # filename_in, keyword, filename_out = argv[1:4] respectively

def time2time_s(time):  # Conversion hh:mm:ss format to seconds
  return 3600*int(time[:2]) + 60*int(time[3:5]) + int(time[6:])

In, Out = [], []

with open(argv[1], 'r') as fi:
  for line in fi:
    if line.count('|' + argv[2] + '|'):  # Pipes exists in cdr file
      index = line.find(':')  # Search ':' character in every record
      time_in = line[(index-2):(index+6)]  # Crop time start call from cdr
      time_out = line[(index+20):(index+28)]  # Crop time end call from cdr
      time_in_s = time2time_s(time_in)
      time_out_s = time2time_s(time_out)
      if time_out_s < time_in_s:  # When call ends next day
        time_out_s += 86400
      In.append(time_in_s)
      Out.append(time_out_s)

InT = [i-min(In) for i in In]  # Crop to the beginning of time (to 0)
OutT = [i-min(In) for i in Out]  # The same

conn = [0 for i in range(max(OutT)+1)]  # conn contains number of simultaneous calls
for i in range(len(InT)):
  conn[InT[i]] += 1
  conn[OutT[i]] -= 1
for i in range(len(conn)-1):
  if conn[i+1] != 0:
    conn[i+1] += conn[i]
  else:
    conn[i+1] = conn[i]

print('Max value: ' + str(max(conn)))

if len(argv) > 3:
  with open(argv[3], 'w') as fo:
    for i in conn:
      fo.write(str(i) + '\n')
