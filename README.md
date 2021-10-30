Setup the following directory structure
The dataset needs to be copied to the correct path

Directory structure:
    SubtleChallenge
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

docker build --pull --rm -f "Dockerfile" -t subtlemedicalsoftwareengcodingchallenge:latest "."


2. Run the Image

docker run -v <absolute path to dataset>:/app/dataset subtlemedicalsoftwareengcodingchallenge python3 pipeline.py -d ./dataset/test_sample -c ./dataset/config.json -o ./dataset/test_output2/

In my system its as follows:
docker run -v /Users/ram/Desktop/SubtleMedical_SoftwareEng_CodingChallenge/dataset:/app/dataset subtlemedicalsoftwareengcodingchallenge python3 pipeline.py -d ./dataset/test_sample -c ./dataset/config.json -o ./dataset/test_output2/



Current issues:
1. Gaussian Blur not implemented
2. Multiple directory support not implemented
3. Needs more testing