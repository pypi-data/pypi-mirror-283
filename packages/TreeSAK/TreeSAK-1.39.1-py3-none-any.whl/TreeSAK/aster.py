import os
import glob
import argparse
from ete3 import Tree
import multiprocessing as mp


aster_usage = '''
====================== aster example commands ======================

TreeSAK aster -i best10 -x fa -o best10_astral_tree -bmge -t 12 -f

====================================================================
'''


def aster(args):

    oma_op_fasta            = args['i']
    fasta_file_ext          = args['x']
    op_dir                  = args['o']
    trim_with_bmge          = args['bmge']
    trim_model              = args['bmge_m']
    entropy_score_cutoff    = args['bmge_esc']
    iqtree_model            = args['m']
    force_overwrite         = args['f']
    num_of_threads          = args['t']

    # specify path to BMGE.jar
    current_file_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    pwd_bmge_jar = '%s/BMGE.jar' % current_file_path

    fa_file_re   = '%s/*.%s' % (oma_op_fasta, fasta_file_ext)
    fa_file_list = ['.'.join(os.path.basename(i).split('.')[:-1]) for i in glob.glob(fa_file_re)]

    if len(fa_file_list) == 0:
        print('No file found in %s, progeam exited!' % oma_op_fasta)
        exit()

    ################################################################################

    # define file name
    cmd_1_mafft_txt         = '%s/cmd_1_mafft.txt'          % op_dir
    cmd_2_trim_txt          = '%s/cmd_2_trim.txt'           % op_dir
    cmd_3_iqtree_txt        = '%s/cmd_3_iqtree.txt'         % op_dir
    cmd_4_astral_txt        = '%s/cmd_4_astral.txt'         % op_dir
    aln_dir                 = '%s/dir_1_msa'                % op_dir
    trimmed_aln_dir         = '%s/dir_2_trimmed_msa'        % op_dir
    tree_dir                = '%s/dir_3_iqtree'             % op_dir
    combined_gene_tree_file = '%s/combined_trees.txt'       % op_dir
    astral_mapping_txt      = '%s/name_mapping.txt'         % op_dir
    consensus_tree_txt      = '%s/consensus_tree.treefile'  % op_dir

    ################################################################################

    # create output folder
    if os.path.isdir(op_dir) is True:
        if force_overwrite is True:
            os.system('rm -r %s' % op_dir)
        else:
            print('%s exist, program exited!' % op_dir)
            exit()
    os.mkdir(op_dir)

    ################################################################################

    cmd_list_mafft  = []
    cmd_list_trim   = []
    cmd_list_iqtree = []
    cmd_1_mafft_txt_handle = open(cmd_1_mafft_txt, 'w')
    cmd_2_trim_txt_handle = open(cmd_2_trim_txt, 'w')
    cmd_3_iqtree_txt_handle = open(cmd_3_iqtree_txt, 'w')
    for each_og in sorted(fa_file_list):

        # define file name
        og_fa          = '%s/%s.%s'             % (oma_op_fasta, each_og, fasta_file_ext)
        og_aln         = '%s/%s.aln'            % (aln_dir, each_og)
        og_aln_trimmed = '%s/%s_trimal.aln'     % (trimmed_aln_dir, each_og)
        if trim_with_bmge is True:
            og_aln_trimmed = '%s/%s_bmge.aln'   % (trimmed_aln_dir, each_og)

        # prepare commands
        mafft_cmd       = 'mafft-einsi --thread %s --quiet %s > %s'                                             % (1, og_fa, og_aln)
        trim_cmd        = 'trimal -in %s -out %s -automated1'                                                   % (og_aln, og_aln_trimmed)
        if trim_with_bmge is True:
            trim_cmd    = 'java -jar %s -i %s -m %s -t AA -h %s -of %s'                                         % (pwd_bmge_jar, og_aln, trim_model, entropy_score_cutoff, og_aln_trimmed)
        iqtree_cmd      = 'iqtree2 -s %s --seqtype AA -m %s -B 1000 --wbtl --bnni --prefix %s/%s -T %s --quiet' % (og_aln_trimmed, iqtree_model, tree_dir, each_og, num_of_threads)

        # add commands to list
        cmd_list_mafft.append(mafft_cmd)
        cmd_list_trim.append(trim_cmd)
        cmd_list_iqtree.append(iqtree_cmd)

        # write out commands
        cmd_1_mafft_txt_handle.write(mafft_cmd + '\n')
        cmd_2_trim_txt_handle.write(trim_cmd + '\n')
        cmd_3_iqtree_txt_handle.write(iqtree_cmd + '\n')

    cmd_1_mafft_txt_handle.close()
    cmd_2_trim_txt_handle.close()
    cmd_3_iqtree_txt_handle.close()

    # run mafft commands
    print('Running mafft with %s cores for %s OGs' % (num_of_threads, len(fa_file_list)))
    os.mkdir(aln_dir)
    pool = mp.Pool(processes=num_of_threads)
    pool.map(os.system, cmd_list_mafft)
    pool.close()
    pool.join()

    # run trim commands
    print('Trimming with %s cores for %s OGs' % (num_of_threads, len(fa_file_list)))
    os.mkdir(trimmed_aln_dir)
    pool = mp.Pool(processes=num_of_threads)
    pool.map(os.system, cmd_list_trim)
    pool.close()
    pool.join()

    # run iqtree commands
    print('Running iqtree with %s cores for %s OGs' % (num_of_threads, len(fa_file_list)))
    os.mkdir(tree_dir)
    for each_iqtree_cmd in sorted(cmd_list_iqtree):
        print(each_iqtree_cmd)
        os.system(each_iqtree_cmd)

    #################################################### run astral ####################################################

    # cat gene trees
    os.system('cat %s/*.treefile > %s' % (tree_dir, combined_gene_tree_file))

    gnm_to_gene_dict = dict()
    for each_tree in open(combined_gene_tree_file):
        tree_str = each_tree.strip()
        current_tree = Tree(tree_str, quoted_node_names=True, format=1)
        for node in current_tree.traverse():
            if node.is_leaf():
                leaf_name = node.name
                leaf_gnm = '_'.join(leaf_name.split('_')[:-1])
                if leaf_gnm not in gnm_to_gene_dict:
                    gnm_to_gene_dict[leaf_gnm] = {leaf_name}
                else:
                    gnm_to_gene_dict[leaf_gnm].add(leaf_name)

    # get the mapping file
    astral_mapping_txt_handle = open(astral_mapping_txt, 'w')
    for each_gnm in gnm_to_gene_dict:
        current_gene_set = gnm_to_gene_dict[each_gnm]
        for each_gene in current_gene_set:
            astral_mapping_txt_handle.write('%s\t%s\n' % (each_gene, each_gnm))
    astral_mapping_txt_handle.close()

    astral_cmd = 'astral -i %s -o %s -t %s -a %s' % (combined_gene_tree_file, consensus_tree_txt, num_of_threads, astral_mapping_txt)

    # write out command
    cmd_4_astral_txt_handle = open(cmd_4_astral_txt, 'w')
    cmd_4_astral_txt_handle.write(astral_cmd + '\n')
    cmd_4_astral_txt_handle.close()

    # run astral
    os.system(astral_cmd)

    ####################################################################################################################


if __name__ == '__main__':

    aster_parser = argparse.ArgumentParser()
    aster_parser.add_argument('-i',         required=True,                          help='orthologous gene sequence')
    aster_parser.add_argument('-x',         required=True,                          help='faa file extension')
    aster_parser.add_argument('-o',         required=True,                          help='output directory')
    aster_parser.add_argument('-bmge',      required=False, action="store_true",    help='trim with BMGE, default is trimal')
    aster_parser.add_argument('-bmge_m',    required=False, default='BLOSUM30',     help='trim model, default: BLOSUM30')
    aster_parser.add_argument('-bmge_esc',  required=False, default='0.55',         help='entropy score cutoff, default: 0.55')
    aster_parser.add_argument('-m',         required=False, default='LG+G+I',       help='iqtree_model, default: LG+G+I')
    aster_parser.add_argument('-f',         required=False, action="store_true",    help='force overwrite')
    aster_parser.add_argument('-t',         required=False, type=int, default=1,    help='num of threads, default: 1')
    args = vars(aster_parser.parse_args())
    aster(args)
