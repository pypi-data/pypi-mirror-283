#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2024 Ye Chang yech1990@gmail.com
# Distributed under terms of the GNU license.
#
# Created: 2024-07-04 23:20


import numpy as np
from pyfamsa import Aligner, Sequence
from pysam import FastaFile
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

from .utils import load_annotation


def group_annot(annot):
    # annot is dict of dict of Transcript object
    gene_dict = {}
    for _, gene_info in annot.items():
        for _, transcript in gene_info.items():
            if not transcript.gene_name:
                continue
            gene_name = transcript.gene_name
            if gene_name not in gene_dict:
                gene_dict[gene_name] = []
            gene_dict[gene_name].append(transcript)
    return gene_dict


def run_msa(names, seqs):
    aligner = Aligner(guide_tree="upgma")
    seqs = [Sequence(n.encode(), s.encode()) for n, s in zip(names, seqs)]
    # tree = aligner.build_tree(seqs)
    # print(tree.dumps())
    msa = aligner.align(seqs)
    return msa


def show_msa(msa):
    for sequence in msa:
        print(sequence.sequence)


def msa_to_array(msa, mask_ratio=0.5):
    arr = np.array([list(sequence.sequence) for sequence in msa])
    return arr


def cluster_sequences(alignment_array, threshold=0.1):
    # Calculate pairwise Hamming distances using scipy's pdist function
    def hamming(u, v, **kwargs):
        # return np.sum(u != v) / len(u)
        # but do not calculate the distance of positions where both sequence is a gap
        return np.sum((u != v) & (u != 45) & (v != 45)) / np.sum((u != 45) | (v != 45))

    distance_matrix = pdist(alignment_array, metric=hamming)

    # Perform hierarchical clustering using the 'average' method
    Z = linkage(distance_matrix, method="average")

    # Form clusters with a maximum distance threshold
    raw_clusters = fcluster(Z, t=threshold, criterion="distance")

    # Use NumPy to count and sort clusters by size
    unique, counts = np.unique(raw_clusters, return_counts=True)
    sorted_clusters = unique[np.argsort(-counts)]

    # Map original cluster IDs to new ordered IDs
    cluster_map = {cluster_id: i + 1 for i, cluster_id in enumerate(sorted_clusters)}
    ordered_clusters = np.vectorize(cluster_map.get)(raw_clusters)

    return ordered_clusters


def consensus_sequence(arr):
    # find the most common character in each column, and join to get the consensus sequence
    consensus = ""
    for i in range(arr.shape[1]):
        col = arr[:, i]
        unique, counts = np.unique(col, return_counts=True)
        max_count_index = np.argmax(counts)
        consensus += chr(unique[max_count_index])
    return consensus


def get_position_mapping_from_aligned_array(aligned_array):
    def map_positions(aligned_sequence):
        gap_positions = np.where(aligned_sequence == 45)[0]  # Find positions of '-'
        all_positions = np.arange(len(aligned_sequence))
        non_gap_positions = np.setdiff1d(all_positions, gap_positions)

        original_positions = []
        aligned_positions = []

        if len(non_gap_positions) == 0:
            return original_positions, aligned_positions

        start_orig = 0
        start_aligned = non_gap_positions[0]

        for i in range(1, len(non_gap_positions)):
            if non_gap_positions[i] != non_gap_positions[i - 1] + 1:
                end_orig = start_orig + (non_gap_positions[i - 1] - start_aligned) + 1
                end_aligned = non_gap_positions[i - 1] + 1

                original_positions.append((start_orig, end_orig))
                aligned_positions.append((start_aligned, end_aligned))

                start_orig = end_orig
                start_aligned = non_gap_positions[i]

        end_orig = start_orig + (non_gap_positions[-1] - start_aligned) + 1
        end_aligned = non_gap_positions[-1] + 1

        original_positions.append((start_orig, end_orig))
        aligned_positions.append((start_aligned, end_aligned))

        return list(zip(original_positions, aligned_positions))

    for i in range(aligned_array.shape[0]):
        aligned_sequence = aligned_array[i]
        mappings = map_positions(aligned_sequence)
        yield mappings


def map_genome_to_gap_open(genome_span_list, gap_open_list):
    mapping = {}
    gap_counter = 0
    current_gap_start, current_gap_end = gap_open_list[gap_counter]
    for genome_span in genome_span_list:
        genome_start, genome_end = genome_span
        for i in range(genome_start, genome_end + 1):
            if current_gap_start <= current_gap_end:
                mapping[i + 1] = current_gap_start + 1
                current_gap_start += 1
            else:
                gap_counter += 1
                if gap_counter < len(gap_open_list):
                    current_gap_start, current_gap_end = gap_open_list[gap_counter]
                    mapping[i + 1] = current_gap_start + 1
                    current_gap_start += 1
                else:
                    # In case there are more genome positions than gap open positions
                    mapping[i + 1] = None

    return mapping


def group_genes(fa_file, annot_file, out_file=None):
    fasta = FastaFile(fa_file)
    # if out_file is None write to stdout
    if out_file:
        out = open(out_file, "w")
    else:
        import sys

        out = sys.stdout
    annot = load_annotation(annot_file)
    gene_dict = group_annot(annot)
    for gene_name, tx_list in gene_dict.items():
        names = [tx.gene_id for tx in tx_list]
        seqs = [tx.get_seq(fasta) for tx in tx_list]
        exon_spans_list = [tx.exons.values() for tx in tx_list]
        exon_chroms = [tx.chrom for tx in tx_list]
        if len(tx_list) < 2:
            cluster_ids = np.zeros(len(tx_list), dtype=int)
        else:
            msa = run_msa(names, seqs)
            aligned_array = msa_to_array(msa)
            cluster_ids = cluster_sequences(aligned_array)
        # loop the cluster ids and redo the msa for each sub-group
        for cluster_id in np.unique(cluster_ids):
            cluster_names = [
                name for name, cid in zip(names, cluster_ids) if cid == cluster_id
            ]
            cluster_seqs = [
                seq for seq, cid in zip(seqs, cluster_ids) if cid == cluster_id
            ]
            cluster_exon_spans_list = [
                spans
                for spans, cid in zip(exon_spans_list, cluster_ids)
                if cid == cluster_id
            ]
            cluster_exon_chroms_list = [
                chrom
                for chrom, cid in zip(exon_chroms, cluster_ids)
                if cid == cluster_id
            ]
            cluster_msa = run_msa(cluster_names, cluster_seqs)
            cluster_aligned_array = msa_to_array(cluster_msa)
            # show_msa(cluster_msa)
            # print(consensus_sequence(cluster_aligned_array))

            for i, mapping in enumerate(
                get_position_mapping_from_aligned_array(cluster_aligned_array)
            ):
                msa_spans = []
                for _, aligned_span in mapping:
                    msa_spans.append(aligned_span)
                # d = map_genome_to_gap_open(cluster_exon_spans_list[i], msa_spans)
                # d_str = ",".join([f"{k}:{v}" for k, v in d.items()])
                # out.write(f"{gene_name}\t{cluster_id}\t{cluster_names[i]}\t{d_str}\n")
                exon_spans_str = ",".join(
                    [
                        f"{start + 1}-{end + 1}"
                        for start, end in cluster_exon_spans_list[i]
                    ]
                )
                msa_spans_str = ",".join(
                    [
                        f"{start + 1}-{end + 1}"
                        for start, end in msa_spans
                        if start is not None and end is not None
                    ]
                )
                out.write(
                    f"{gene_name}\t{cluster_id}\t{cluster_names[i]}\t{cluster_exon_chroms_list[i]}\t{exon_spans_str}\t{msa_spans_str}\n"
                )


if __name__ == "__main__":
    group_genes("../demo/subset.fa", "../demo/subset.tsv")
