import pandas as pd
import numpy as np
from tqdm import tqdm


def _parse_cols(lines, verbose, return_attrib_dict=False):
    """
    Hidden function to parse the tabular part of the data
    :param lines: (list of strings) - the lines of the file
    :return: (pd.DataFrame) - columns = Seqid, Source, Type, Start, End, Score, Strand, Phase

    """
    attribs = []

    # spec from https://m.ensembl.org/info/website/upload/gff3.html
    data = {"Seqid": [],
            "Source": [],
            "Type": [],
            "Start": [],
            "End": [],
            "Score": [],
            "Strand": [],
            "Phase": []}


    for line in (tqdm(lines) if verbose else lines):
        if line[0] != '#':
            columns = line.split('\t')

            for i, key in enumerate(data):
                data[key].append(columns[i])

            attribs.append(columns[-1])


    df = pd.DataFrame(data).replace('.', np.nan)

    if return_attrib_dict:
        return df, attribs

    else:
        return df


def _parse_all(lines, verbose):

    if verbose:
        print('Building structured data...')
    df, attribs = _parse_cols(lines, verbose, return_attrib_dict=True)

    if verbose:
        print("Adding Supplemental Attribute table...")
    attrib_keys = _get_attrib_keys(attribs, verbose)
    supplement_table = _make_attrib_table(attribs, attrib_keys, verbose)
    new_df = pd.merge(df, supplement_table, how='left', left_index=True, right_index=True)
    return new_df


def _get_attrib_keys(attrib_col, verbose):
    if verbose:
        print("Finding unique attribute keys...")
    keys = set()
    for line in (tqdm(attrib_col) if verbose else attrib_col):
        key_val_arr = line.split(";")
        for key_val in key_val_arr:
            key, val = key_val.split("=")
            keys.add(key)

    return list(keys)


def _make_attrib_table(attribs, keys, verbose):

    if verbose:
        print("Making attribute table...")

    data = {}
    for key in keys:
        data[key] = []

    for string in (tqdm(attribs) if verbose else attribs):
        row_attrib_dict = _make_dict_from_attrib_list(string)

        for key in data:
            if key in row_attrib_dict:
                data[key].append(row_attrib_dict[key])

            else:
                data[key].append(np.nan)

    df = pd.DataFrame(data)
    return df


def _make_dict_from_attrib_list(string):
    keys = [x.split("=")[0] for x in string.split(";")]
    vals = [x.split("=")[1] for x in string.split(";")]

    data = {}
    for k, v in zip(keys, vals):
        data[k] = v

    return data


def parse_gff3(filepath, verbose=True, parse_attributes=False):
    """
    This is the only public function of this package and it just parses a gff3 file into a pandas dataframe.

    **Background**  - There are 8 columns (Seqid, Source, Type, Start, End, Score, Strand, Phase) that are in every gff3 file (required by the spec).
    The last column stores additional data called 'attributes' which are stored in the last column in a weird form that is similar to key value pair tuples.
    The logic of this function is that if parameter parse_attributes is true, this will collect all this data and add it to the dataframe by creating a column
    for every unique key in all the rows. Many of these keys are always included (of at lease often) but others not so much so you can end up with some
    sparse columns occasionally.

    :param filepath: (pathlike, str) - the path to a gff3 file
    :param verbose: (bool, default = True) - This function often takes a while to run so this function prints updates and progress bars to the screen
    :param parse_attributes: (bool, default = False) - Read background in the docstring. Provides additional information but increased runtime.
    :return: pd.DataFrame
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]


    if verbose:
        for line in lines[:20]:
            if line[0] == '#' and ":" in line:
                print(line.replace("#", ''))

    if parse_attributes:
        return _parse_all(lines, verbose)

    else:
        return _parse_cols(lines, verbose)
