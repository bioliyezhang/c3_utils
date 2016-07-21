# -*- coding: cp936 -*-
"""
The main purpose of this script is to convert Gene Symbol to CMap L1000 probe
IDs.

=============================
Usage: python ConvertGeneSymbol2L1000ID_obj_v0.0.py
-h help

-i files to processed                           *[No default value]
    (gene Symbol file)

-c Column of gene symbol                        [default value: 0]

-p parameter file               *[No default value]

-o prefix of output files                       [default:"output"]

-s suffix for the files to be processed         [default value "txt"]

-S output SUFFIX                                [default: "txt"]

-d sep_char within among columns                [default value '\t']

-j skip header lines                            [default value 0]
    if skip header lines = 0 indicates that there is no header line
    if skip header lines = n indicates that first n lines are header lines
    
-I input file path              [default: current folder]

-O output file path             [default: current folder]

-L unique_id length for the infile      [default value 2]

===================
input description:
input files:
1. Genelist file (the encoding should be UTF-8,the script fails when
    the encoding is UTF-16)

======================
output files:


============================

Python & Module requirement:
Versions 2.x : 2.4 or above 
Module: No additional Python Module is required.

============================
Library file requirement:

Not Standalone version, few library file is required.

============================

External Tools requirement:

============================
command line example:

============================
versions update

"""

##Copyright
##By Liye Zhang
##Contact: bioliyezhang@gmail.com
##Compatible Python Version:2.4 or above

###Code Framework

### Specific Functions definiation
    
def specific_function(infiles):
    import cmap.util.api_utils as apiu

    ##Section I: Generate the gene annotation dictionary
    
    cmd_records=record_command_line()  ##record the command line    
    ac = apiu.APIContainer(key=LINCS_API_KEY) ## this is my personal key
        
    for infile in infiles:
        print "Processing infile:", infile
        ##Set up infile object
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=infile_skip    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen()  ##create the file reader to process infile
        gene_list = []
        for row in infile_reader:
            gene = row[SYMBOL_COLUMN]
            gene_list.append(gene)

        ## perform the query
        genes = ac.geneinfo.find({'pr_gene_symbol' : {'$in' : gene_list}},
                         fields = ['pr_id', 'pr_gene_symbol', 'pr_gene_title'],
                         toDataFrame = True, limit= 1000)
        probe_list = list(genes["pr_id"])
        
        ##Setup output file
        outfile_name=infile_obj.outputfilename_gen(prefix,OUTPUT_SUFFIX) ##create output file
        outfile_path=OUTPUT_PATH+"/"+outfile_name
        outfile_obj=GeneralFile_class(outfile_path)              ##create output obj
        #outfile_obj.RECORD=cmd_records      
        outfile_sample_ID = infile_obj.generate_sample_id()                     
        outfile_obj.output_handle_gen()    ##generate output handle       
        outfile_obj.handle.write(outfile_sample_ID+'\t')
        outfile_obj.handle.write(outfile_sample_ID)
        for probe  in probe_list:
            if str(probe)!="nan":
                outfile_obj.handle.write('\t'+str(probe))
        outfile_obj.handle.write('\n')
        outfile_obj.handle.close()





if __name__ == "__main__":
    ###Python General Module Import 
    import sys, csv, getopt, re
    import os
    import math
    from itertools import ifilter
    
    ##Liye own common function,class loading
    #from Constant_Library import *
    #from General_Library import *
    #from File_Class import *  ###
    #from Sequencing_Library import *
    from c3_utils.general_class import *
    from c3_utils.general_functions import *
    
    OUTPUT_SEP_CHAR='\t'
    
    
            
                 
    #exit if not enough arguments
    if len(sys.argv) < 3:
        print __doc__
        sys.exit(0)
    
    ###set default value
    suffix="txt"
    infile=None
    infile_skip=0
    SYMBOL_COLUMN = 0
    sep_char='\t'
    sep_gene=','
    header_file=None
    unique_id_length=2
    parameter_file=None
    INPUT_PATH=os.getcwd()
    OUTPUT_PATH=os.getcwd()
    prefix="L1000-probe-IDs"
    OUTPUT_SUFFIX="gmt"
    LINCS_API_KEY = "cac40ffd57f8873d2d50976375e2d509"
    
    ###get arguments(parameters)
    optlist, cmd_list = getopt.getopt(sys.argv[1:], 'hi:s:S:r:c:d:D:j:I:t:p:L:o:O:z',["test="])
    for opt in optlist:
        if opt[0] == '-h':
            print __doc__; sys.exit(0)
        elif opt[0] == '-i': infile = opt[1]
        elif opt[0] == '-I': INPUT_PATH = opt[1]
        elif opt[0] == '-O': OUTPUT_PATH = opt[1]
        elif opt[0] == '-c': SYMBOL_COLUMN = int(opt[1])
        elif opt[0] == '-S': OUTPUT_SUFFIX = opt[1]
        elif opt[0] == '-s': suffix = opt[1]
        elif opt[0] == '-d': sep_char =opt[1]
        elif opt[0] == '-D': sep_gene =opt[1]
        elif opt[0] == '-j': infile_skip= int(opt[1])
        elif opt[0] == '-r': reference = opt[1]
        elif opt[0] == '-o': prefix = opt[1]
        elif opt[0] == '-L': unique_id_length = int(opt[1])
        elif opt[0] == '--test': long_input = opt[1]
    
    #print "Test long input", long_input
    if infile==None:
        infiles=CurrentFolder_to_Infiles(INPUT_PATH, suffix)
    else:
        infiles=[infile]

    ##perform specific functions
    specific_function(infiles)
    
    
    
