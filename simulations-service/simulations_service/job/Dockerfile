FROM gcc:8.3

#WORKDIR /app/lbm_mrt

RUN apt-get update && apt-get install -y make

#RUN apt-get update && apt-get install -y emacs24
COPY app /app
WORKDIR /app/

RUN apt-get install python3-pip -y
RUN pip3 install boto3
RUN pip3 install botocore


ENTRYPOINT [ "./entrypoint.sh" ]

# CMD ["./a.out", "input_data", "output_data"]

