import random
import dendropy
import argparse
from ete3 import Tree


tree_file_in     = '/Users/songweizhi/Desktop/ar53_r220.tree'
interested_taxon = 'o__Nitrososphaerales'
tree_file_out    = '/Users/songweizhi/Desktop/ar53_r220_subset.tree'


input_tree = Tree(tree_file_in, quoted_node_names=True, format=1)

for node in input_tree.traverse():
    if (node.name == interested_taxon) or (interested_taxon in node.name):
        leaf_list = [i.name for i in node.get_leaves()]
        print('%s\t%s' % (node.name, ','.join(leaf_list)))
        node.write(outfile=tree_file_out)

