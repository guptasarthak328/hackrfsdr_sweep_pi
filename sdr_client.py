#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# GNU Radio version: 3.8.2.0 (Must be in 3.8 and match with GNURadio Version on Pi)

from gnuradio import blocks
import pmt
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, blocks
import osmosdr
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import socket

class feb23(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "hackrf_sweep_pi")

        ##################################################
        # Variables
        ##################################################

        self.vec_len = vec_len = 1024
        self.samp_rate = samp_rate = float(sys.argv[2])
        self.center_freq = center_freq = float(sys.argv[1])
        filename = 'YOUR FILE NAME' #Filename + Directory

        ##################################################
        # Blocks
        ##################################################

        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(100e6, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.fft_vxx_0 = fft.fft_vcc(1024, True, window.blackmanharris(1024), True, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_tags_strobe_0 = blocks.tags_strobe(gr.sizeof_gr_complex*1, pmt.intern("TEST"), vec_len, pmt.intern("strobe"))
        self.blocks_tag_share_0 = blocks.tag_share(gr.sizeof_gr_complex, gr.sizeof_gr_complex, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_len)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vec_len, 0)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/vec_len, vec_len)
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_float*vec_len, filename, samp_rate, 1, blocks.GR_FILE_FLOAT, False, vec_len, pmt.make_dict(), True)
        self.blocks_file_meta_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_len)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_file_meta_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_tag_share_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_tags_strobe_0, 0), (self.blocks_tag_share_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_tag_share_0, 0))


    def get_vec_len(self):
        return self.vec_len

    def set_vec_len(self, vec_len):
        self.vec_len = vec_len
        self.blocks_multiply_const_xx_0.set_k(1/self.vec_len)
        self.blocks_tags_strobe_0.set_nsamps(self.vec_len)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

def main(top_block_cls=feb23, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    Fs = float(sys.argv[2]) #Sample Rate
    center_freq = float(sys.argv[1]) #Center Frequency
    filename = 'YOUR FILE NAME' #Filename + Directory
    N = 1024 #Vector Length

    time.sleep(1)

    x = np.fromfile(open(filename), dtype=np.float32)

    f = np.arange(Fs/-2.0, Fs/2.0, Fs/N) 
    f += center_freq

    def update(length):
        i = 0
        while i < length:
            x_i = x[i*1024:(i+1)*1024]
            for j in range(len(f)):
                freq = f[j]
                dBm = x_i[j]
                msgclient = "Freq: {:.5g} Hz, dBm: {:.5g}".format(freq, dBm)
                
                msgFromClient       = msgclient

                bytesToSend         = str.encode(msgFromClient)

                serverAddressPort   = ("SEVER IP ADDRESS", SEVER PORT) #Server Ethernet IP and Port Number

                bufferSize          = 1024

                UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) # Create a UDP socket at client side

                UDPClientSocket.sendto(bytesToSend, serverAddressPort) # Send to server using created UDP socket

                msgFromServer = UDPClientSocket.recvfrom(bufferSize)

                msg = "Message from Server {}".format(msgFromServer[0])

                print(msg) 
            i += 1

    update(float('inf'))

    tb.wait()


if __name__ == '__main__':
    main()