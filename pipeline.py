from pydicom import dcmread,uid
from dicomio import input, output
from utils import filter, blur
from collections import defaultdict
import numpy as np
import os
import json
import argparse


def inference(src, configfile, dest):

    config = {}
    with open(configfile) as json_file:
        config = json.load(json_file)

    slices = input.compute_slices(src)

    filtered_slices = filter.filter_mapping(slices, config) 

    volume = input.compute_volume_from_slices(filtered_slices)

    processed_volume = blur.gaussian_blur3d(volume,None, None)

    output.update_volume_and_write(filtered_slices, processed_volume, dest)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--input-dicom", dest="infile", help="path to input DICOM directory")
    parser.add_argument("-c", "--config", dest="config", help="path to input Config file")
    parser.add_argument("-o", "--output-dicom", dest="outfile", required=True, help="path to output DICOM directory")
    
    # Test sample    
    sample = [  '-d', './dataset/test_sample/',
                '-c', './dataset/config.json',
                '-o','./dataset/test_output/']

    args = parser.parse_args(sample)
    inference(args.infile, args.config, args.outfile)
    