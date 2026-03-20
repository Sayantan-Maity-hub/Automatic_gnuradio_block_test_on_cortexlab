from gnuradio import gr, analog, uhd
import time

class TX(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        samp_rate = 2e6

        src = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 1000, 0.5)

        usrp = uhd.usrp_sink("", uhd.stream_args(cpu_format="fc32"))
        usrp.set_samp_rate(samp_rate)
        usrp.set_center_freq(2.49e9)
        usrp.set_gain(20)

        self.connect(src, usrp)

if __name__ == "__main__":
    tb = TX()
    tb.start()
    print("TX started")
    time.sleep(20)
    tb.stop()
    tb.wait()