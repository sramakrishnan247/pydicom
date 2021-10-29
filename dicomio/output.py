from pydicom import dcmread,uid
from collections import defaultdict
import numpy as np
import os
import json
import argparse

def compute_slices(src):
    """    
    Reads input DICOM directory and computes slices.
    Sorts the slices by SliceLocation

    Parameters
    ----------
    src : str

    Returns
    -------
    slices : list
    """
    slices = [] 

    for dicom_file in os.listdir(src):
        if dicom_file.endswith('dcm'):
            fpath = os.path.join(src, dicom_file)
            with open(fpath, 'rb') as infile:
                ds = dcmread(infile)
                elem = ds.SliceLocation
                slices.append(ds)

    slices.sort(key = lambda s:s.SliceLocation)
    return slices 

def update_volume_and_write(slices, volume, output):
    """    
    Builds updated data by modifying pixel array and generating new ids.
    Rescales the volume numpy array before modification.

    Parameters
    ----------
    slices : list
    volume : np.array
    output : str

    Returns
    -------
    
    """

    if not os.path.isdir(output):
        os.makedirs(output)

    #perform rescaling
    volume = volume * 255 
    volume = np.asarray(volume, slices[0].pixel_array.dtype)

    idx = 0

    #retrieve old ids 
    SeriesInstanceUID = slices[0].SeriesInstanceUID
    SOPInstanceUID  = slices[0].SOPInstanceUID

    #compute new ids
    newSeriesInstanceUID  = uid.generate_uid()
    while newSeriesInstanceUID == SeriesInstanceUID:
        newSeriesInstanceUID  = uid.generate_uid() 
    
    newSOPInstanceUID = uid.generate_uid()
    while newSeriesInstanceUID == SOPInstanceUID:
        newSOPInstanceUID = uid.generate_uid()

    #Update data and metadata and write to file
    for slice in slices:
        slice.SeriesInstanceUID = newSeriesInstanceUID
        slice.SOPInstanceUID = newSOPInstanceUID
        np.copyto(slice.pixel_array,volume[idx])
        slice.PixelData = slice.pixel_array.tobytes()
        idx += 1

        #save new slice to destination directory
        filename = str(idx) + '.dcm'
        pathdir = os.path.join(output, filename)
        slice.save_as(pathdir)

def process(numpy_file=None, inputfile=None, outputfile=None):
    """    
    Runs pre-processing on input numpy file and DICOM directory
    Updates data and metadata in orginal dicom files.
    Writes copy to a new directory 

    Parameters
    ----------
    numpy_file : str
    inputfile : str
    outputfile : str

    Returns
    -------

    """
    mapping  = compute_slices(inputfile)
    arr = np.load(numpy_file) 


    update_volume_and_write(mapping, arr, outputfile)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--input-npy", dest="numpy_file", required=True, help="path to input numpy file")
    parser.add_argument("-d", "--input-dicom", dest="infile", help="path to input DICOM directory")
    parser.add_argument("-o", "--output-dicom", dest="outfile", required=True, help="path to output DICOM directory")
    
    # Test sample    
    sample = [ '-n', './pixel_numpy.npy',  
                '-d', './dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3',
                '-o','./dicom_copy/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3']

    args = parser.parse_args(sample)
    # args = parser.parse_args()
    process(args.numpy_file, args.infile, args.outfile)
    