### About:
Tool for handling Medical data(DICOM)

### Instructions:

       docker build --pull --rm -f "Dockerfile" -t dicom_parser:latest "."
          
       docker run -v <absolute path to dataset>:/app/dataset dicom_parser python3 pipeline.py -d ./dataset/test_sample -c ./dataset/config.json -o ./dataset/test_output2/



