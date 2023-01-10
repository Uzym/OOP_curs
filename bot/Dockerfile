FROM python:3.10.6
WORKDIR /home
COPY *.txt ./
COPY *.py ./
RUN pip3 install -U -r requirements.txt
RUN mkdir ./input
RUN mkdir ./output
ENTRYPOINT [ "python3", "app.py" ]
