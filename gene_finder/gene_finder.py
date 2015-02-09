# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Lisa Joelle Hachmann

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq
dna = load_seq("./data/X73525.fa")

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
    for i in range(0, len(dna), 3):
        codon = dna[i:i+3]
        if codon in stop_codons:
            return dna[0:i]
    return dna

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
    allorf = []
    startcodon = 'ATG'
    x = 0
    while x < len(dna):
        codon = dna[x:x+3]
        if codon == startcodon:
            allorf.append(rest_of_ORF(dna[x:]))
            x += len(rest_of_ORF(dna[x:]))
        else:
            x+=3
    return allorf

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
        orfallframes.extend(find_all_ORFs_oneframe(dna[i:]))
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
        if len(bothstrands[x])>  longest: #len(bothstrands[x-1]) and len(bothstrands[x])> longest:
            longest =  len(bothstrands[x])
            longest_elim = x
    return bothstrands[longest_elim]

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """

    longlength = 0
    for x in range(num_trials):
        shufdna = shuffle_string(dna)
        if len(longest_ORF(shufdna)) > longlength:
            longlength = len(longest_ORF(shufdna))
    return longlength


    # shuffledstring = []
    # filtlist = []
    # totallist = []
    # count =0
    # for x in range(num_trials-1): 
    #     dnalist = list(dna)
    #     #count += 1
    #     random.shuffle(dnalist)
    #     shuffledstring = "".join(dnalist)
    #     totallist.append(shuffledstring)
    #     filtlist.append(find_all_ORFs_both_strands(totallist[x])) 
    #     print filtlist
    #     if filtlist[x]:
    #         mini = filtlist[x][0]
    #         if len(mini) > count:
    #             count = len(mini)
    #     else:
    #         pass
    # return count

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
    code = []
    translated = ''
    for i in range(0,len(dna)-2,3):
        my_codon = dna[i:i+3]
        for j in range(len(codons)):
            if my_codon in codons[j]:
                translated += aa[j]
    return translated

def gene_finder(dna):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified dna        
        threshold: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    """
    translate any code that comes out of orf both sides that is at the
    threshold
    """
    translated_orfs = []
    threshold = longest_ORF_noncoding(dna, 1500)
    print threshold
    dna_orfs = find_all_ORFs_both_strands(dna) 
    #print 'dna_orfs', dna_orfs 
    for x in range(len(dna_orfs)):
        if len(dna_orfs[x]) >= threshold:
            translated_orfs.append(coding_strand_to_AA(dna_orfs[x]))
    # print 'translated:', translated_orfs
    return translated_orfs

print gene_finder(dna)


if __name__ == "__main__":
    import doctest
    doctest.testmod()