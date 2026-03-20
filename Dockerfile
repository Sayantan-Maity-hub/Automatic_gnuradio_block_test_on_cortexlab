FROM ghcr.io/cortexlab/cxlb-gnuradio-3.10:1.5

WORKDIR /app

COPY benchmark_tx.py .
COPY benchmark_rx.py .
COPY check_output.py .

RUN chmod +x *.py

CMD ["bash"]