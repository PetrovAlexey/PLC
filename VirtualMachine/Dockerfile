FROM python:3

WORKDIR /usr/src/app
RUN pip install numpy
COPY . .

CMD python ./assembler.py fibbonachi.asm data.bin && python ./virmach.py data.bin