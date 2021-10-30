Setup the following directory structure
The dataset needs to be copied to the correct path

Directory structure:
    Project 
        - app
            blur.py
            dicom_input.py
            dicom_output.py
            filter.py
            pipeline.py
        - dataset
            dicom_data/
                1.dcm
                2.dcm
                3.dcm
            config.json
        README.md
        requirements.txt
        Dockerfile

How to run?
1. Build Docker Image

docker build --pull --rm -f "Dockerfile" -t dicom_parser:latest "."


2. Run the Image

docker run -v <absolute path to dataset>:/app/dataset dicom_parser python3 pipeline.py -d ./dataset/test_sample -c ./dataset/config.json -o ./dataset/test_output2/
