#!/usr/bin/env python3

"""
This script is a the samcut project, designed to process paired-end FASTQ files by fragmenting DNA sequences at specified restriction enzyme sites.

Copyright © 2024 Samir Bertache

SPDX-License-Identifier: AGPL-3.0-or-later

===============================================================================

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import logging
import re
import signal
import subprocess
import sys
from typing import Generator, List, Tuple
import os 
from Bio.Restriction import AllEnzymes, RestrictionBatch
from Bio.Seq import Seq
import shutil
import multiprocessing 

logging.basicConfig(level=logging.INFO)

import importlib.resources as pkg_resources

def find_pigz():
    try:
        # Vérifier si pigz est dans le PATH du système
        pigz_system_path = shutil.which("pigz")
        if pigz_system_path:
            return pigz_system_path
        # Si aucun pigz n'est trouvé
        print("\nError: pigz binary not found in package or system PATH : \n\n\tRetry manual installation here : https://zlib.net/pigz/ \n\n\tIf already done, try to add pigz to the path, you can take this tutorial : \n https://gist.github.com/nex3/c395b2f8fd4b02068be37c961301caa7 \n\t")
        sys.exit(0)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(0)
        
# Define signal handler
def signal_handler(sig, frame, outF, outR):
    print(f"\nReceived signal {sig}. Terminating gracefully...")
    outF.terminate()  # Terminate the pigz processes
    outR.terminate()
    logging.info("\nProcess termination requested by signal")
    sys.exit(0)


def FindLigaSite(List_Enzyme: List[str]) -> List[Tuple[str, int]]:
    """
    Find ligation sites for given enzymes and generate regex patterns for those sites.

    Parameters:
        List_Enzyme (List[str]): List of enzyme names.

    Returns:
        List[Tuple[str, int]]: A list of tuples where each tuple contains a regex pattern and an integer.

    Examples:
        >>> FindLigaSite(['EcoRI'])
        [('GAATTAATTC', 5)]
        >>> FindLigaSite(['HinfI'])
        [('GA.TA.TC', 4)]
    """
    restriction_batch = RestrictionBatch(List_Enzyme)

    give_list = []
    accept_list = []
    ligation_site_list = []

    # Iterates on the enzymes.
    for enz in restriction_batch:

        # Extract restriction sites and look for cut sites.
        site = enz.elucidate()
        fw_cut = site.find("^")
        rev_cut = site.find("_")

        # Process "give" site. Remove N on the left (useless).
        give_site = site[:rev_cut].replace("^", "")
        while give_site[0] == "N":
            give_site = give_site[1:]
        give_list.append(give_site)

        # Process "accept" site. Remove N on the rigth (useless).
        accept_site = site[fw_cut + 1 :].replace("_", "")
        while accept_site[-1] == "N":
            accept_site = accept_site[:-1]
        accept_list.append(accept_site)

    # Iterates on the two list to build all the possible HiC ligation sites.
    for give_site in give_list:
        for accept_site in accept_list:
            # Replace "N" by "." for regex searching of the sites
            LigationSite = (give_site + accept_site).replace("N", ".")
            ligation_site_list.append((LigationSite, len(give_site)))
            if str(LigationSite) != str(
                Seq(LigationSite).reverse_complement()
            ):
                ligation_site_list.append(
                    (
                        str(Seq(LigationSite).reverse_complement()),
                        len(accept_site),
                    )
                )
    return ligation_site_list


# Codification : Necéssaire au site de restriction non palindromique
# 0 correspond à un brin
# Et 1 au brin de sens inverse


def find_positions_for_one_site(
    text: str, Enzyme: Tuple[str, int]
) -> List[int]:
    """
    Find all positions of a specific pattern (RESite) in a given text using regular expressions.

    Parameters:
        text (str): The text to search in.
        Enzyme (Tuple[str, int, int, int]): The restriction enzyme site to search for, with the length of give_site or accept_site
        depend of the

    Examples:
        >>> find_positions_for_one_site("AAGAATTCAA", ('GAATTC', 5))
        [7]
        >>> find_positions_for_one_site("AAAAAGAATTCAAAAAGAATTCAAAAAGAATTC", ('GAATTC', 5))
        [10, 21, 32]
        >>> find_positions_for_one_site("777777GA7TA7TC1717GA7TA7TC", ('GA.TA.TC', 4))
        [10, 22]
    """
    return [
        int(match.start() + Enzyme[1])
        for match in re.finditer(Enzyme[0], text)
    ]


def find_all_pos(
    text: str, ligation_site_list: List[Tuple[str, int]]
) -> List[int]:
    """
    Examples:
        >>> find_all_pos("777777GA7TA7TC1717GAATTCFFFFFF", [('GAATTC', 5), ('GA.TA.TC', 4)])
        [10, 23]
    """
    AllSite = []
    for TupleRegex in ligation_site_list:
        AllSite += find_positions_for_one_site(text, TupleRegex)
    AllSite.sort()
    return AllSite


def index_list(
    Seq: List[str], ligation_site_list: List[Tuple[str, int]]
) -> List[List[int]]:
    """
    _summary_ : Find all positions of ligation sites in two sequences
    """
    IndexForward = find_all_pos(Seq[0], ligation_site_list)
    IndexReverse = find_all_pos(Seq[1], ligation_site_list)
    return [IndexForward, IndexReverse]


def fragmentation(Sequence: str, Index: List[int], seed_size) -> List[str]:
    if len(Index) != 0:
        Index = [0] + Index + [len(Sequence)]
        List_Fragment = [
            Sequence[Index[i] : Index[i + 1]]
            for i in range(len(Index) - 1)
            if (Index[i + 1] - Index[i]) > seed_size
        ]
        return List_Fragment
    else:
        return [Sequence]


def produce_fragments(
    Seq: List[str], Qual: List[str], Index: List[List[int]], seed_size: int
) -> Tuple[List[List[str]], List[List[str]]]:
    """
    Create all fragments of one sequence using the restriction enzyme sites.

    :param Seq: A list containing the forward and reverse sequences.
    :param Qual: A list containing the forward and reverse quality sequences.
    :param Index: A list containing the indices of restriction enzyme sites in the forward and reverse sequences.
    :param seed_size: The minimum length of fragments to keep.

    :return: A list containing the fragments of the forward and reverse sequences,
             and the corresponding quality sequences.
    """
    forward_seq, reverse_seq = Seq
    forward_indices, reverse_indices = Index
    forward_qual, reverse_qual = Qual

    # Work on the forward and reverse sequences
    F_Frag = fragmentation(forward_seq, forward_indices, seed_size)
    R_Frag = fragmentation(reverse_seq, reverse_indices, seed_size)

    # Work on the forward and reverse quality sequences
    F_Qual = fragmentation(forward_qual, forward_indices, seed_size)
    R_Qual = fragmentation(reverse_qual, reverse_indices, seed_size)

    return [F_Frag, R_Frag], [F_Qual, R_Qual]


def read_fastq_gzip_simultaneously_MyWay(
    fileA: str, fileB: str, num_threads: int,
    pigz_path,
) -> Generator[Tuple[List[str], List[str], List[str]], None, None]:
    # Use pigz to decompress the input files
    procA = subprocess.Popen(
        [pigz_path, "-dc", "-p", str(num_threads), fileA],
        stdout=subprocess.PIPE,
        text=True,
    )
    procB = subprocess.Popen(
        [pigz_path, "-dc", "-p", str(num_threads), fileB],
        stdout=subprocess.PIPE,
        text=True,
    )

    while True:
        NomA = procA.stdout.readline().rstrip()
        seqA = procA.stdout.readline().rstrip()
        procA.stdout.readline()  # Skip the '+'
        qualA = procA.stdout.readline().rstrip()

        NomB = procB.stdout.readline().rstrip()
        seqB = procB.stdout.readline().rstrip()
        procB.stdout.readline()  # Skip the '+'
        qualB = procB.stdout.readline().rstrip()

        if not seqA or not seqB:
            break

        yield [NomA, NomB], [seqA, seqB], [qualA, qualB]

    # Check for errors in subprocess
    stdoutA, stderrA = procA.communicate()
    if stderrA:
        raise Exception(f"Error in pigz command for file {fileA}: {stderrA}")

    stdoutB, stderrB = procB.communicate()
    if stderrB:
        raise Exception(f"Error in pigz command for file {fileB}: {stderrB}")


def create_ALL_pairs(
    fragments: List[List[str]], qual: List[List[str]]
) -> Generator[List[str], None, None]:
    """
    Generate all possible pairs of fragments from forward and reverse sequences.

    Parameters:
        fragments (List[List[str]]): All possible fragments from the forward and reverse sequences.
        qual (List[List[str]]): Associated quality

    Yields:
        Tuple[List[str, str, str, str, str]]: Pairs of forward and reverse fragments and their associated quality scores.
    """
    all_fragments = fragments[0] + fragments[1]
    all_quals = qual[0] + qual[1]

    for i, f_frag in enumerate(all_fragments):
        for j, r_frag in enumerate(all_fragments):
            if (
                j > i
            ):  # Ensure that a fragment is not paired with itself or repeat
                Num = str(i) + str(j)
                yield [Num, f_frag, r_frag, all_quals[i], all_quals[j]]


def create_FWD_REV_pairs(
    fragments: List[List[str]], qual: List[List[str]]
) -> Generator[List[str], None, None]:
    """
    Generate all possible pairs of fragments from forward and reverse sequences.

    Parameters:
        fragments (List[List[str]]): All possible fragments from the forward and reverse sequences.
        qual (List[List[str]]): Associated quality

    Yields:
        Tuple[List[str, str, str, str, str]]: Pairs of forward and reverse fragments and their associated quality scores.
    """
    forward_fragments = fragments[0]
    reverse_fragments = fragments[1]
    forward_quals = qual[0]
    reverse_quals = qual[1]

    for i, f_frag in enumerate(forward_fragments):
        for j, r_frag in enumerate(reverse_fragments):
            Num = str(i) + str(j)
            yield [Num, f_frag, r_frag, forward_quals[i], reverse_quals[j]]


def Partitionning(num_threads):
    """
    _summary_ : Partition the number of threads
    """
    TWrite = num_threads // 4
    TRead = num_threads // 8
    return TWrite, TRead


def SearchInDataBase(list_enzyme, borderless=False):
    """
    _summary_ : Search the ligation site in the database
    """
    if list_enzyme == "No restriction enzyme found":
        print(list_enzyme)
        sys.exit(0)
    else:
        if type(list_enzyme) == list:
            ligation_site_list = FindLigaSite(list_enzyme)
        else:
        	ligation_site_list = FindLigaSite(list_enzyme.split(","))
        print(f"Ligation sites: {ligation_site_list}", flush=True)
        if (borderless == True) and (len(ligation_site_list) > 1):
            print(
                "Warning : More than one enzyme isn't compatible with borderless mode",
                flush=True,
            )
        return ligation_site_list


def OpenOutPut(output_forward, output_reverse, TWrite, pigz_path):

    bufferF = []
    bufferR = []

    # Open output files for writing

    outF = subprocess.Popen(
        [pigz_path, "-c", "-p", str(TWrite)],
        stdin=subprocess.PIPE,
        stdout=open(output_forward, "wb"),
    )
    outR = subprocess.Popen(
        [pigz_path, "-c", "-p", str(TWrite)],
        stdin=subprocess.PIPE,
        stdout=open(output_reverse, "wb"),
    )

    # Register signal handlers
    signal.signal(
        signal.SIGINT,
        lambda sig, frame: signal_handler(sig, frame, outF, outR),
    )  # Ctrl+C
    signal.signal(
        signal.SIGTSTP,
        lambda sig, frame: signal_handler(sig, frame, outF, outR),
    )  # Ctrl+Z

    return outF, outR, bufferF, bufferR


def Processing(TSeq, TQual, ligation_site_list, seed_size):
    """
    _summary_ : Process the sequences
    """
    indices = index_list(TSeq, ligation_site_list)
    fragments, qualities = produce_fragments(TSeq, TQual, indices, seed_size)
    return fragments, qualities


def CheckingError(outF, outR, output_forward, output_reverse):
    # Check for errors in subprocess
    stdoutF, stderrF = outF.communicate()
    if stderrF:
        raise Exception(
            f"Error in pigz command for file {output_forward}: {stderrF}"
        )

    stdoutR, stderrR = outR.communicate()
    if stderrR:
        raise Exception(
            f"Error in pigz command for file {output_reverse}: {stderrR}"
        )


def Writing(outF, outR, bufferF, bufferR):
    """
    _summary_ : Write the buffer to the output
    """
    outF.stdin.write("".join(bufferF).encode("utf-8"))
    outR.stdin.write("".join(bufferR).encode("utf-8"))
    bufferF = []
    bufferR = []

    return bufferF, bufferR


def Communicate(
    mode, num_threads, ligation_site_list, output_forward, output_reverse
):
    print(f"\nMode : {mode}", flush=True)
    print(f"Number of threads : {num_threads}", flush=True)
    if int(num_threads)%4 != 0:
        print("\n\nThe number must be a multiple of 4 and greater than 4")
        sys.exit(0)
    if num_threads > multiprocessing.cpu_count():
        print("\nWarning !\nWarning : You chose too much thread, this can slow down the process !\nWarning !\n")
    print("Ligation sites : ", flush=True)
    for el in ligation_site_list:
        print(f"\tLigation site : {el[0]}", flush=True)
    print(
        f"Creating output files {output_forward} and {output_reverse}",
        flush=True,
    )
    


def cut(
    source_forward: str,
    source_reverse: str,
    output_forward: str,
    output_reverse: str,
    list_enzyme: List[str],
    seed_size,
    mode,
    buffer_size: int = 1000,
    num_threads: int = 8,
) -> None:


    # Find pgiz :
    pigz_path = find_pigz()
    
    # Get repartition of threads
    TWrite, TRead = Partitionning(num_threads)

    # Take the enzyme list and make the ligation site list
    ligation_site_list = SearchInDataBase(list_enzyme)

    # Use pigz to compress the output files
    outF, outR, bufferF, bufferR = OpenOutPut(
        output_forward, output_reverse, TWrite, pigz_path
    )

    Communicate(
        mode, num_threads, ligation_site_list, output_forward, output_reverse
    )

    try:
        for TNom, TSeq, TQual in read_fastq_gzip_simultaneously_MyWay(
            source_forward, source_reverse, TRead, pigz_path
        ):
            fragments, qualities = Processing(
                TSeq, TQual, ligation_site_list, seed_size
            )

            if mode == "all":
                Currents_Pairs = create_ALL_pairs(fragments, qualities)
            elif mode == "fr":
                Currents_Pairs = create_FWD_REV_pairs(fragments, qualities)
            else:
                raise ValueError(f"Invalid mode: {mode}")

            bufferF = []
            bufferR = []
            for Current_Pair in Currents_Pairs:
                NewName = (
                    str(TNom[0].split(" ")[0]) + ":" + str(Current_Pair[0])
                )
                bufferF.append(
                    f"{NewName}\n{Current_Pair[1]}\n+\n{Current_Pair[3]}\n"
                )
                bufferR.append(
                    f"{NewName}\n{Current_Pair[2]}\n+\n{Current_Pair[4]}\n"
                )

                # Write the data to the file once the buffer reaches the specified size
                if len(bufferF) >= buffer_size:
                    bufferF, bufferR = Writing(outF, outR, bufferF, bufferR)

            # Write any remaining data in the buffer to the file
            if bufferF:
                bufferF, bufferR = Writing(outF, outR, bufferF, bufferR)

        # Close the output files
        outF.stdin.close()
        outR.stdin.close()

        print("Processing done", flush=True)

    except Exception as e:
        # Close the output files
        outF.stdin.close()
        outR.stdin.close()
        raise e

    finally:
        # Check for errors in subprocess
        CheckingError(outF, outR, output_forward, output_reverse)


def parse_args():
    parser = argparse.ArgumentParser(
        description="""\
Cutsite script

Features:

    Find and Utilize Restriction Enzyme Sites: Automatically identify ligation sites from provided enzyme names and generate regex patterns to locate these sites in sequences.
    Fragmentation: Split sequences at restriction enzyme sites, creating smaller fragments.
    Multi-threading: Efficiently handle large datasets by utilizing multiple threads for decompression and compression.
    Custom Modes: Supports different pairing modes for sequence fragments.

Arguments:

    --source_forward (str): Input file path for forward reads. Default is ../data/A.fq.gz.
    --source_reverse (str): Input file path for reverse reads. Default is ../data/B.fq.gz.
    --output_forward (str): Output file path for processed forward reads. Default is ../data/output_forward_class.fq.gz.
    --output_reverse (str): Output file path for processed reverse reads. Default is ../data/output_reverse_class.fq.gz.
    --list_enzyme (str): Comma-separated list of restriction enzymes. Default is No restriction enzyme found.
    --mode (str): Mode of pairing fragments. Options are "all" or "fr". Default is "fr".
    --seed_size (int): Minimum length of fragments to keep. Default is 20.
    --num_threads (int): Number of threads to use for processing. Default is 8.
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--source_forward",
        type=str,
        default="input_data/R1.fq.gz",
        help="Input file for forward reads",
    )
    parser.add_argument(
        "--source_reverse",
        type=str,
        default="input_data/R2.fq.gz",
        help="Input file for reverse reads",
    )
    parser.add_argument(
        "--output_forward",
        type=str,
        default="output_data/output_R1.fq.gz",
        help="Output file for forward reads",
    )
    parser.add_argument(
        "--output_reverse",
        type=str,
        default="output_data/output_R2.fq.gz",
        help="Output file for reverse reads",
    )
    parser.add_argument(
        "--list_enzyme",
        default="No restriction enzyme found",
        type=str,
        help="Restriction Enzyme(s) used separated by comma",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="fr",
        help="Mode of modification only : all or fr",
    )
    parser.add_argument(
        "--seed_size",
        type=int,
        default=20,
        help="Minimum length of fragments to keep",
    )
    parser.add_argument(
        "--num_threads", 
        type=int, 
        default=8, 
        help="The number must be a multiple of 4 and greater than 4"
    )

    return parser.parse_args()

def main_cli():
    args = parse_args()
    cut(
        source_forward=args.source_forward,
        source_reverse=args.source_reverse,
        output_forward=args.output_forward,
        output_reverse=args.output_reverse,
        list_enzyme=args.list_enzyme,
        mode=args.mode,
        seed_size=args.seed_size,
        num_threads=args.num_threads,
    )

if __name__ == "__main__":
    main_cli()
