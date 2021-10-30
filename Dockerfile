FROM python:3.8
RUN mkdir /app
WORKDIR /app

ADD ./app/. /app/

RUN pip install cycler==0.11.0
RUN pip install dicom==0.9.9.post1
RUN pip install kiwisolver==1.3.2
RUN pip install matplotlib==3.4.3
RUN pip install numpy==1.21.3
RUN pip install Pillow==8.4.0
RUN pip install pydicom==2.2.2
RUN pip install pyparsing==3.0.3
RUN pip install python-dateutil==2.8.2
RUN pip install six==1.16.0

# CMD [ "python", "./pipeline.py" ]