#!/usr/bin/env python3

# Script to find artificial Nuclear integration Site options (aNSo)

from Bio import SeqIO
import pandas as pd
import re
import os


def main():


    # Get gene start and end indices for genome
    indices = []


    with open('UTEX2973_genome_with_TSS.gbk') as f:

        for line in f:

            if line.startswith("     gene"):
                tmp = line.split("gene")[-1].strip()

                if tmp.startswith("complement"):

                    try:
                        tmp = tuple(int(x) for x in tmp.split("(")[-1].rstrip(")").split(".."))
                        indices.append(tmp)

                    except ValueError:
                        continue

                else:

                    tmp = tuple(int(x) for x in tmp.split(".."))
                    indices.append(tmp)

            elif line.startswith("//"):
                break
    #number
    print("FOUND: {} genes".format(len(indices)))




    # Get intergenic regions that show >= 500 bp
    eligible_sites = []

    for i in range(len(indices)):

        try:
            diff = indices[i+1][0] - indices[i][1]

            if diff >= 500:
                eligible_sites.append((indices[i], indices[i+1], diff))

        except IndexError:
            break

    print("FOUND:   {} eligible sites showing the right length".format(len(eligible_sites)))




    # Get sequences for intergenic regions.
    # Get the whole intergenic region, if it's bigger than 2500 bp
    # or get the whole intergenic region and add bp to the left and to the right up to 2500 bp, if the intergenic region itself is shorter than 2500 bp
    eligible_sequences = []

    for record in SeqIO.parse('GCA_000817325.1_ASM81732v1_genomic.fna', "fasta"):

        if record.id == "CP006471.1":

            for i in range(len(eligible_sites)):

                if eligible_sites[i][2] >= 2500:

                    eligible_sequences.append([eligible_sites[i][0][0], eligible_sites[i][0][1], eligible_sites[i][1][0], eligible_sites[i][1][1], eligible_sites[i][2], str(record.seq[eligible_sites[i][0][1]:eligible_sites[i][1][0]])])

                else:

                    missing_nucleotides = round((2500 - eligible_sites[i][2])/2)
                    eligible_sequences.append([eligible_sites[i][0][0], eligible_sites[i][0][1], eligible_sites[i][1][0], eligible_sites[i][1][1], eligible_sites[i][2], str(record.seq[eligible_sites[i][0][1]-missing_nucleotides:eligible_sites[i][1][0]+missing_nucleotides])])




    # Get only sequences that don't include restriction sites for BsmBI
    without_bsmb1 = []

    for i in range(len(eligible_sequences)):

        if not eligible_sequences[i][5].__contains__("CGTCTC") and not eligible_sequences[i][5].__contains__("GAGACG"):

            without_bsmb1.append(eligible_sequences[i])

    print("FOUND:   {} eligible sites showing the right length and without BsmBI restriction site".format(len(without_bsmb1)))




    # Get only sequences that don't include BsmBI and BsaI
    without_bsmb1_bsa1 = []

    for i in range(len(without_bsmb1)):

        if not without_bsmb1[i][5].__contains__("GGTCTC") and not without_bsmb1[i][5].__contains__("GAGACC"):

            without_bsmb1_bsa1.append(without_bsmb1[i])

    print("FOUND:   {} eligible sites showing the right length and without BsmBI and BsaI restriction sites".format(len(without_bsmb1_bsa1)))




    # Find transcription start sites
    tss =[]

    with open('UTEX2973_genome_with_TSS.gbk') as f:
        for line in f:

            if re.match("     .TSS", line):

                tmp = line.split("TSS")[-1].strip()

                if tmp.startswith("complement"):

                    try:
                        tmp = int(tmp.split("complement(")[-1].strip(")"))
                        tss.append(tmp)

                    except ValueError:
                        continue

                else:

                    tmp = int(tmp)
                    tss.append(tmp)


    print("FOUND: {} transcriptional start sites".format(len(tss)))




    # Find TSS in intergenic regions and exclude sequences, that inherit a TSS
    with_tss = []

    for i in range(len(without_bsmb1_bsa1)):

        for j in range(len(tss)):


            if tss[j] in range(int(without_bsmb1_bsa1[i][1]), int(without_bsmb1_bsa1[i][2])):

                with_tss.append(i)
                break


    with_tss = set(with_tss)


    print("FOUND: {} eligible sites with TSS".format(len(with_tss)))


    # Number of candidates without transcriptomic data
    number_of_candidates = set(range(len(without_bsmb1_bsa1)))


    # Candidate indices without BsmBI, BsaI and TSS
    final_candidates = number_of_candidates - with_tss


    # Find final candidates
    without_bsmb1_bsa1_tss = []

    for x in final_candidates:

        without_bsmb1_bsa1_tss.append(without_bsmb1_bsa1[x])


    print("FOUND: {} final candidates fullfilling all criteria".format(len(without_bsmb1_bsa1_tss)))

    os.mkdir('aNSo_results')

    without_bsmb1_bsa1_tss_df = pd.DataFrame(without_bsmb1_bsa1_tss, columns=["Gene_1_start", "Gene_1_end", "Gene_2_start", "Gene_2_end", "Intergenic_region_length", "Sequence_of_aNSo_5'_to_3'_(at_least_2500_nt)"])
    without_bsmb1_bsa1_tss_df.to_csv('aNSo_results/aNSo_without_bsmbi_bsai_tss.csv')


    # Write a fasta file with final candidate sequences
    with open('aNSo_results/aNSo_without_bsmbi_bsai_tss.fna',
              mode='a') as fasta:

        for i in range(len(without_bsmb1_bsa1_tss)):
            fasta.write(">{0}|{1}|{2}|{3}|{4}\n".format(without_bsmb1_bsa1_tss[i][0], without_bsmb1_bsa1_tss[i][1], without_bsmb1_bsa1_tss[i][2], without_bsmb1_bsa1_tss[i][3], without_bsmb1_bsa1_tss[i][4]))
            fasta.write(without_bsmb1_bsa1_tss[i][5] + "\n")









if __name__ == '__main__':
    main()
