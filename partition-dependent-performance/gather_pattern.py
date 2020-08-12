import argparse
import csv
import numpy as np
#import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='plot csv ghost gather data')
parser.add_argument('files', nargs='*')

args = parser.parse_args()

data_dict = {}
contiguous = []
count = 0

for filename in args.files:

  with open(filename, 'rb') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in rows:
      print row
      try:
        node = int(row[0])
        shared_node = int(row[1])
        index = int(row[2])

        if not data_dict.has_key(node):
            data_dict[node] = {}
        if not data_dict[node].has_key(shared_node):
            data_dict[node][shared_node] = {}
            data_dict[node][shared_node]["count"] = 0
            data_dict[node][shared_node]["contiguous"] = []
            data_dict[node][shared_node]["contiguous_index"] = -1
            data_dict[node][shared_node]["last_index"] = index
 
        data_dict[node][shared_node]["count"] += 1

        if index - data_dict[node][shared_node]["last_index"] == 1:
          data_dict[node][shared_node]["contiguous"][data_dict[node][shared_node]["contiguous_index"]] += 1
        else:
          data_dict[node][shared_node]["contiguous"].append(1)
          data_dict[node][shared_node]["contiguous_index"] += 1

        data_dict[node][shared_node]["last_index"] = index

      except ValueError:
        print " ".join(row)

for node in data_dict:
  for shared_node in data_dict[node]:
    contiguous.extend(data_dict[node][shared_node]["contiguous"])
    count += data_dict[node][shared_node]["count"]

print
total_ghost = np.sum(contiguous)
print 'total ghost(shared) cells', total_ghost
print 'min contiguous cells', np.min(contiguous)
print 'max contiguous cells', np.max(contiguous)
print

distribution = {}
for group in contiguous:
  if not distribution.has_key( group ):
    distribution[group] = 0
  distribution[group] += group
  
max_bin = 500

print
print 'threshold cells with counts above', max_bin
print

n_in_bin = np.zeros(max_bin+1)

for group in distribution:
  if group <= max_bin:
    n_in_bin[int(group)] += distribution[group]
  else:
    n_in_bin[max_bin] += distribution[group]

percent_in_bin = n_in_bin / total_ghost * 100
bins = np.arange(0,max_bin+1)

fig1, ax1 = plt.subplots()
plt.bar(bins, np.log10(percent_in_bin), width=2, color='blue')
ax1.set_yticks([-3, -2, -1, 0, 1, 2])
ax1.set_yticklabels(["0.001","0.01","0.1","1","10","100"])
plt.title('Thresholded at '+str(max_bin))
plt.xlim([0,max_bin+5])
plt.ylim([-3,2])
plt.xlabel('contiguous cells')
plt.ylabel('cell count (%)')
plt.show()

for i in range(len(n_in_bin)):
  if n_in_bin[i] > 0:
    print
    print int(n_in_bin[i]), "cells in contiguous clumps of",bins[i],
print "or more"
print

for node in data_dict:
  print "ghost node", node
  for shared_node in data_dict[node]:
    print
    print "  shared node", shared_node, "total shared cells", data_dict[node][shared_node]["count"]
    print "    contiguous cell counts", data_dict[node][shared_node]["contiguous"]
    print "    total cells verification", np.sum(data_dict[node][shared_node]["contiguous"])
    print
