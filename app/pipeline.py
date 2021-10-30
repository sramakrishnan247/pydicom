from pydicom import dcmread,uid
import dicom_input as input
import dicom_output as output
import filter, blur
from collections import defaultdict
import numpy as np
import os
import json
import argparse


def inference(src, configfile, dest):
    '''
    End to end inference pipeline
    Parameters
    ----------
    src : str
    configfile : str
    dest : str

    Returns
    -------

    '''
    #Read the configuration from the configuration file
    config = {}
    with open(configfile) as json_file:
        config = json.load(json_file)

    #Read DICOM files and process slices
    slices = input.compute_slices(src)

    #Filter slices based on input config
    filtered_slices = filter.filter_mapping(slices, config) 

    #Compute 3d volume by preprocessing the slices
    volume = input.compute_volume_from_slices(filtered_slices)

    #Processing on the pre-processed input
    processed_volume = blur.gaussian_blur3d(volume,None, None)

    #Post-processing and write to file
    output.update_volume_and_write(filtered_slices, processed_volume, dest)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--input-dicom", dest="infile", help="path to input DICOM directory")
    parser.add_argument("-c", "--config", dest="config", help="path to input Config file")
    parser.add_argument("-o", "--output-dicom", dest="outfile", required=True, help="path to output DICOM directory")
    # print(os.listdir('.'))
    # print(os.listdir('./dataset'))
    # print(os. getcwd())   
    # # Test sample    
    # sample = [  '-d', './dataset/test_sample/',
    #             '-c', './dataset/config.json',
    #             '-o','./dataset/test_output/']

    args = parser.parse_args()
    inference(args.infile, args.config, args.outfile)
    