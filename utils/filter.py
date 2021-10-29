from pydicom import dcmread,uid
from collections import defaultdict
from dicomio import input
import numpy as np
import os
import json
import argparse


def is_valid(slice, config):
    """    
    Checks if a slice has valid config paramters

    Parameters
    ----------
    slice : list
    config : dict

    Returns
    -------
    boolean
    """ 
    for key, val in config.items():
        if key not in slice:
            return False
        if slice[key].value != val:
            return False
    return True

def filter_mapping(slices, config):
    """    
    Filters slices by config 

    Parameters
    ----------
    slices: list
    config : dict

    Returns
    -------
    valid_slices : list 
    """ 
    valid_slices = []
    for i,slice in enumerate(slices):
        if is_valid(slice, config):
            valid_slices.append(slice)
    
    return valid_slices

def process(inputfile=None, configfile=None, outputfile=None):
    """   
    Filters DICOM directory by config provided.
    Returns filters slices. 
    Parameters
    ----------
    inputfile : str
    configfile : str
    outputfile : str

    Returns
    -------
    mapping : list
    """
    mapping  = input.compute_slices(inputfile)

    config = {}
    with open(configfile) as json_file:
        config = json.load(json_file)

    mapping = filter_mapping(mapping, config)

    return mapping



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--input-dicom", dest="infile", help="path to input DICOM directory")
    parser.add_argument("-c", "--config", dest="config", help="path to input Config file")
    # parser.add_argument("-o", "--output-dicom", dest="outfile", required=True, help="path to output DICOM directory")
    
    # Test sample    
    # sample = [  '-d', './dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3',
    #             '-c', './config.json'
    #             # '-o','./dicom_copy/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3']
    # ]
    sample = [  '-d', './test_sample',
                '-c', './config.json'
                # '-o','./dicom_copy/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3']
    ]
    args = parser.parse_args(sample)
    # args = parser.parse_args()
    filtered_slices = process(args.infile, args.config)