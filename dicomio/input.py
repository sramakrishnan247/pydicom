from pydicom import dcmread
from collections import defaultdict
import numpy as np
import os
import json
import argparse

def compute_volume(mapping):
    """    
    Builds a 3D volume by sorting against each file's Slice Location  
    DICOM tag in ascending order. 
    
    Normalizes the 3D volume to range between 0 and 1, 
    converting the data from the input data type to 32-bit float 
    data type.
    
    Parameters
    ----------
    mapping : dict

    Returns
    -------
    volume : np.array
    
    """
    volume = []
    for key in sorted(mapping.keys()):
        for ds in mapping[key]:
            arr = ds.pixel_array
            max_val = np.max(arr)
            min_val = np.min(arr)
            arr = (arr - min_val)/max_val
            volume.append(arr)
    volume = np.asarray(volume, dtype=np.float32)
    return volume

def compute_mapping(src):
    """    
    Reads a src DICOM directory and creates a dictionary to identify 
    each file by Slice Location.

    Stores the metadata of the directory during the first file.

    Parameters
    ----------
    src : str

    Returns
    -------
    mapping : dict
    metadata : dict
    """
    mapping = defaultdict(list)
    metadata = {}

    for dicom_file in os.listdir(src):
        if dicom_file.endswith('dcm'):
            fpath = os.path.join(src, dicom_file)
            with open(fpath, 'rb') as infile:
                ds = dcmread(infile)
                elem = ds.SliceLocation
                mapping[str(elem)].append(ds)

                if not metadata:
                    metadata['Modality'] = ds.Modality
                    metadata['PixelSpacing'] = (ds.PixelSpacing[0], ds.PixelSpacing[1])
                    metadata['SeriesDescription'] = ds.SeriesDescription
    return mapping, metadata

def process(src, numpy_file=None, json_file=None):

    """    
    Runs pre-processing on input DICOM directory
    Computes pixel data volume stores in numpy format.
    Computes metadata and stores in json format.

    Parameters
    ----------
    src : str
    numpy_file = str
    json_file = str

    Returns
    -------
    volume : np.array

    """
    mapping, metadata = compute_mapping(src)

    volume = compute_volume(mapping)

    with open(numpy_file, 'wb') as f:
        np.save(f,volume)
    
    with open(json_file, 'w') as outfile:
        json.dump(metadata, outfile)

    return volume


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-dicom", dest="src", help="path to input DICOM directory")
    parser.add_argument("-n", "--output-npy", dest="numpy_file", required=True, help="path to output numpy file")
    parser.add_argument("-j", "--output-json", dest="json_file", required=True, help="path to output json file")
    
    # Test sample    
    sample = [  '-i', 'dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3',
                '-n', 'pixel_numpy.npy',  
                '-j','output.json']

    args = parser.parse_args(sample)
    # args = parser.parse_args()
    arr = process(args.src, args.numpy_file, args.json_file)
    