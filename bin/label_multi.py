#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It labels the candidate list of fusion genes generated by 'find_fusion_genes.py'.



Author: Daniel Nicorici, Daniel.Nicorici@gmail.com

Copyright (c) 2009-2017 Daniel Nicorici

This file is part of FusionCatcher.

FusionCatcher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FusionCatcher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FusionCatcher (see file 'COPYING.txt').  If not, see
<http://www.gnu.org/licenses/>.

By default, FusionCatcher is running BLAT aligner
<http://users.soe.ucsc.edu/~kent/src/> but it offers also the option to disable
all its scripts which make use of BLAT aligner if you choose explicitly to do so.
BLAT's license does not allow to be used for commercial activities. If BLAT
license does not allow to be used in your case then you may still use
FusionCatcher by forcing not use the BLAT aligner by specifying the option
'--skip-blat'. Fore more information regarding BLAT please see its license.

Please, note that FusionCatcher does not require BLAT in order to find
candidate fusion genes!

This file is not running/executing/using BLAT.

"""
import sys
import os
import optparse

if __name__ == '__main__':

    #command line parsing

    usage="%prog [options]"
    description="""It labels the candidate list of fusion genes generated by 'find_fusion_genes.py'."""
    version="%prog 0.10 beta"

    parser=optparse.OptionParser(usage=usage,description=description,version=version)

    parser.add_option("--input",
                      action="store",
                      type="string",
                      dest="input_fusion_genes_filename",
                      help="""The input file in text tab delimited format containing the fusion genes candidates produced by 'find_fusion_genes.py'. """)


    parser.add_option("--data",
                      action="store",
                      type="string",
                      dest="input_data_filename",
                      help="""It contains the list of fusion genes with offending reads.""")

    parser.add_option("--label",
                      action="store",
                      type="string",
                      dest="label",
                      help="""Label used to mark the candidate fusion genes which are founf in the filter.""")

    parser.add_option("--pairs",
                      action="store",
                      type="int",
                      dest="pairs",
                      help="""For fusion genes with striclty less than the number of supporting pairs, specified here, it is applied the second label. Default is %default.""")


    parser.add_option("--output",
                      action="store",
                      type="string",
                      dest="output_fusion_genes_filename",
                      help="""The output text tab-separated file containing the candidate fusion genes which are found in the filter. The format is as the input file and sorted by counts column.""")




    (options,args) = parser.parse_args()

    # validate options
    if not (options.input_fusion_genes_filename and
            options.output_fusion_genes_filename and
            options.label
            ):
        parser.print_help()
        parser.error("One of the options has not been specified.")
        sys.exit(1)

    final = [line.rstrip("\r\n").split("\t") for line in file(options.input_fusion_genes_filename,"r") if line.rstrip("\r\n")]
    
    temp =  [line.rstrip("\r\n").split("\t") for line in file(options.input_data_filename,"r") if line.rstrip("\r\n")]
    head = temp.pop(0)
    temp = dict([((e[0],e[1]),e[2]) for e in temp])
    
    head = final.pop(0)
    r = []
    label = options.label.split(",")
    nr = options.pairs
    
    for line in final:
        k = (line[0],line[1])
        v = temp.get(k,'0')
        d = int(line[2]) - int(v)
        if d != 0:
            sd = v
            if line[5]:
                line[5] = line[5] + ',' + label[0] + sd
            else:
                line[5] = label[0] + sd
            if int(v) < nr:
                line[5] = line[5] + ',' + label[1]
        r.append(line)
        
    r.insert(0,head)
    file(options.output_fusion_genes_filename,"w").writelines(['\t'.join(e)+'\n' for e in r])
