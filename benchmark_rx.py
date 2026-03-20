from gnuradio import gr, blocks, uhd
import time

class RX(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        samp_rate = 2e6

        usrp = uhd.usrp_source("", uhd.stream_args(cpu_format="fc32"))
        usrp.set_samp_rate(samp_rate)
        usrp.set_center_freq(2.49e9)
        usrp.set_gain(20)

        sink = blocks.file_sink(8, "rx.dat")

        self.connect(usrp, sink)

if __name__ == "__main__":
    tb = RX()
    tb.start()
    print("RX started")
    time.sleep(20)
    tb.stop()
    tb.wait()