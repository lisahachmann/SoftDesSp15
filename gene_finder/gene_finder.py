# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: YOUR NAME HERE

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###

def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    if (nucleotide == 'A') or (nucleotide == 'a'):
        return 'T'
    if (nucleotide =='T') or (nucleotide == 't'):
        return 'A'
    if (nucleotide =='C') or (nucleotide == 'c'):
        return 'G'
    if (nucleotide =='G') or (nucleotide == 'g'):
        return 'C'
    else:
        return 'That is not a nucleotide'

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    dna = dna[::-1] #reverses the string of dna
    dnastring = ""
    for x in range(0, len(dna)):
        dnastring += get_complement(dna[x])
    return dnastring 

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'

    in DNA:
    TAG 
    TAA
    TGA 
    """
    stop_codons = ["TAG", "TAA", "TGA"] 
    rorf = "" 
    for x in range(0,len(dna)):
        if x %3 == 0:
            if dna[x:x+3] in stop_codons:
                return rorf
        rorf += dna[x] 
    return rorf

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
"""
    rorf = ''
    started = False
    ALLORFS = []
    startcodon = 'ATG'
    stop_codons = 'TAG', 'TAA', 'TGA'
    for x in range(0,len(dna)-2,3):
        if dna[x:x+3] in startcodon:
            started = True
            rorf += dna[x:x+3]
            #print "startcodon line: ", rorf
        elif (dna[x:x+3] in stop_codons) and started:
           # print "stopcodon line: ", rorf
            ALLORFS.append(rorf)
            rorf = ''
            started = False
        elif started:
            rorf += dna[x:x+3]
        else:
            pass
        #print "print continuous: ", rorf
    if rorf == '':
        pass
    else:
        ALLORFS.append(rorf)
    
    return ALLORFS


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    orfallframes = []
    for i in range(3):
        orfallframes += find_all_ORFs_oneframe(dna[i:])
#        for x in range(i, len(dna), 3):
#            if dna[x:x+3] == 'ATG': 
#                orfallframes += find_all_ORFs_oneframe(dna[x:])
    return orfallframes

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    rev_dna = get_reverse_complement(dna)
    both = find_all_ORFs(dna) + find_all_ORFs(rev_dna)
    return both

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    bothstrands = find_all_ORFs_both_strands(dna)
    longest = 0
    for x in range(len(bothstrands)):
        if len(bothstrands[x])>  len(bothstrands[x-1]) and len(bothstrands[x])> longest:
            longest =  len(bothstrands[x])
            longest_elim = x
    return bothstrands[longest_elim]

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    # TODO: implement this
    shuffledstring = []
    filtlist = []
    totallist = []
 #   mini = []
    count =0
    for x in range(num_trials-1): 
        dnalist = list(dna)
        #count += 1
        random.shuffle(dnalist)
        shuffledstring = "".join(dnalist)
        totallist.append(shuffledstring)
        filtlist.append(find_all_ORFs_both_strands(totallist[x])) 
        print filtlist
        if filtlist[x]:
            mini = filtlist[x][0]
            if len(mini) > count:
                count = len(mini)
        else:
            pass
    return count

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    # TODO: implement this
    pass

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    # TODO: implement this
    #threshold = longest_ORF_noncoding(dna, 1500
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()