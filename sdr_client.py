from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import socket

if len(sys.argv) < 2:
    print("No command line arguments provided.")
else:
    if sys.argv[1] == '1':
        print("1 Hackrf SDR Mode Selected")
        class onesdr(gr.top_block):

            def __init__(self):
                gr.top_block.__init__(self, "HackRF Sweep Pi")

                ##################################################
                # Variables
                ##################################################
                self.vec_len = vec_len = int(sys.argv[5])
                self.samp_rate = samp_rate = float(sys.argv[6])
                self.center_freq = center_freq = float(sys.argv[7])
                filename = sys.argv[2] #Filename + Directory

                ##################################################
                # Blocks
                ##################################################
                self.osmosdr_source_0 = osmosdr.source(
                    args="numchan=" + str(1) + " " + 'hackrf=0'
                )
                self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
                self.osmosdr_source_0.set_sample_rate(samp_rate)
                self.osmosdr_source_0.set_center_freq(center_freq, 0)
                self.osmosdr_source_0.set_freq_corr(0, 0)
                self.osmosdr_source_0.set_dc_offset_mode(0, 0)
                self.osmosdr_source_0.set_iq_balance_mode(0, 0)
                self.osmosdr_source_0.set_gain_mode(False, 0)
                self.osmosdr_source_0.set_gain(10, 0)
                self.osmosdr_source_0.set_if_gain(20, 0)
                self.osmosdr_source_0.set_bb_gain(20, 0)
                self.osmosdr_source_0.set_antenna('', 0)
                self.osmosdr_source_0.set_bandwidth(0, 0)
                self.fft_vxx_0 = fft.fft_vcc(vec_len, True, window.blackmanharris(vec_len), True, 1)
                self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
                self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_len)
                self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vec_len, 0)
                self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/vec_len, vec_len)
                self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*vec_len, filename, False)
                self.blocks_file_sink_0.set_unbuffered(False)
                self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_len)



                ##################################################
                # Connections
                ##################################################
                self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
                self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
                self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_file_sink_0, 0))
                self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
                self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
                self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))
                self.connect((self.osmosdr_source_0, 0), (self.blocks_throttle_0, 0))


            def get_vec_len(self):
                return self.vec_len

            def set_vec_len(self, vec_len):
                self.vec_len = vec_len
                self.blocks_multiply_const_xx_0.set_k(1/self.vec_len)

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
                self.osmosdr_source_0.set_center_freq(self.center_freq, 0)





        def main(top_block_cls=onesdr, options=None):
            tb = top_block_cls()

            def sig_handler(sig=None, frame=None):
                tb.stop()
                tb.wait()

                sys.exit(0)

            signal.signal(signal.SIGINT, sig_handler)
            signal.signal(signal.SIGTERM, sig_handler)

            tb.start()


            Fs = float(sys.argv[6]) #Sample Rate
            center_freq = float(sys.argv[7]) #Center Frequency
            filename = sys.argv[2] #Filename + Directory
            N = int(sys.argv[5]) #Vector Length

            time.sleep(5)

            X = np.fromfile(open(filename), dtype=np.float32) #This part was found from here https://pysdr.org/content/sampling.html

            f = np.arange(Fs/-2.0, Fs/2.0, Fs/N) 
            f += center_freq

            def update(length):
                i = 0
                while i < length:
                    x_i = X[i*N:(i+1)*N]
                    for j in range(len(f)):
                        freq = f[j]
                        dBm = x_i[j]
                        msgclient = (f"Freq: {freq:} Hz, dBm: {dBm:}")

                        msgFromClient       = msgclient

                        bytesToSend         = str.encode(msgFromClient)

                        serverAddressPort   = (sys.argv[4], int(sys.argv[3])) #Client Ethernet IP and Port Number

                        bufferSize          = int(sys.argv[5])

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

    elif sys.argv[1] == '2':
        # do something else if the first argument is 2
        print("2 Hackrf SDR Mode Selected")
    
        class feb23(gr.top_block):

            def __init__(self):
                gr.top_block.__init__(self, "HackRF Sweep Pi")

                ##################################################
                # Variables
                ##################################################
                self.vec_len = vec_len = int(sys.argv[6])
                self.samp_rate = samp_rate = float(sys.argv[7])
                self.center_freq_2 = center_freq_2 = float(sys.argv[8])
                self.center_freq_1 = center_freq_1 = float(sys.argv[9])
                filename1 = sys.argv[2]
                filename2 = sys.argv[3]

                ##################################################
                # Blocks
                ##################################################
                self.osmosdr_source_0_0 = osmosdr.source(
                    args="numchan=" + str(1) + " " + 'hackrf=1'
                )
                self.osmosdr_source_0_0.set_time_unknown_pps(osmosdr.time_spec_t())
                self.osmosdr_source_0_0.set_sample_rate(samp_rate)
                self.osmosdr_source_0_0.set_center_freq(center_freq_2, 0)
                self.osmosdr_source_0_0.set_freq_corr(0, 0)
                self.osmosdr_source_0_0.set_dc_offset_mode(0, 0)
                self.osmosdr_source_0_0.set_iq_balance_mode(0, 0)
                self.osmosdr_source_0_0.set_gain_mode(False, 0)
                self.osmosdr_source_0_0.set_gain(10, 0)
                self.osmosdr_source_0_0.set_if_gain(20, 0)
                self.osmosdr_source_0_0.set_bb_gain(20, 0)
                self.osmosdr_source_0_0.set_antenna('', 0)
                self.osmosdr_source_0_0.set_bandwidth(0, 0)
                self.osmosdr_source_0 = osmosdr.source(
                    args="numchan=" + str(1) + " " + 'hackrf=0'
                )
                self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
                self.osmosdr_source_0.set_sample_rate(samp_rate)
                self.osmosdr_source_0.set_center_freq(center_freq_1, 0)
                self.osmosdr_source_0.set_freq_corr(0, 0)
                self.osmosdr_source_0.set_dc_offset_mode(0, 0)
                self.osmosdr_source_0.set_iq_balance_mode(0, 0)
                self.osmosdr_source_0.set_gain_mode(False, 0)
                self.osmosdr_source_0.set_gain(10, 0)
                self.osmosdr_source_0.set_if_gain(20, 0)
                self.osmosdr_source_0.set_bb_gain(20, 0)
                self.osmosdr_source_0.set_antenna('', 0)
                self.osmosdr_source_0.set_bandwidth(0, 0)
                self.fft_vxx_0_0 = fft.fft_vcc(vec_len, True, window.blackmanharris(vec_len), True, 1)
                self.fft_vxx_0 = fft.fft_vcc(vec_len, True, window.blackmanharris(vec_len), True, 1)
                self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
                self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
                self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_len)
                self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_len)
                self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, vec_len, 0)
                self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vec_len, 0)
                self.blocks_multiply_const_xx_0_0 = blocks.multiply_const_cc(1/vec_len, vec_len)
                self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/vec_len, vec_len)
                self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*vec_len, filename2, False)
                self.blocks_file_sink_0_0.set_unbuffered(False)
                self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*vec_len, filename1, False)
                self.blocks_file_sink_0.set_unbuffered(False)
                self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(vec_len)
                self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_len)



                ##################################################
                # Connections
                ##################################################
                self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
                self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
                self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
                self.connect((self.blocks_multiply_const_xx_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
                self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_file_sink_0, 0))
                self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_file_sink_0_0, 0))
                self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
                self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
                self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
                self.connect((self.blocks_throttle_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
                self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))
                self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_const_xx_0_0, 0))
                self.connect((self.osmosdr_source_0, 0), (self.blocks_throttle_0, 0))
                self.connect((self.osmosdr_source_0_0, 0), (self.blocks_throttle_0_0, 0))


            def get_vec_len(self):
                return self.vec_len

            def set_vec_len(self, vec_len):
                self.vec_len = vec_len
                self.blocks_multiply_const_xx_0.set_k(1/self.vec_len)
                self.blocks_multiply_const_xx_0_0.set_k(1/self.vec_len)

            def get_samp_rate(self):
                return self.samp_rate

            def set_samp_rate(self, samp_rate):
                self.samp_rate = samp_rate
                self.blocks_throttle_0.set_sample_rate(self.samp_rate)
                self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
                self.osmosdr_source_0.set_sample_rate(self.samp_rate)
                self.osmosdr_source_0_0.set_sample_rate(self.samp_rate)

            def get_center_freq_2(self):
                return self.center_freq_2

            def set_center_freq_2(self, center_freq_2):
                self.center_freq_2 = center_freq_2
                self.osmosdr_source_0_0.set_center_freq(self.center_freq_2, 0)

            def get_center_freq_1(self):
                return self.center_freq_1

            def set_center_freq_1(self, center_freq_1):
                self.center_freq_1 = center_freq_1
                self.osmosdr_source_0.set_center_freq(self.center_freq_1, 0)





        def main(top_block_cls=feb23, options=None):
            tb = top_block_cls()

            def sig_handler(sig=None, frame=None):
                tb.stop()
                tb.wait()

                sys.exit(0)

            signal.signal(signal.SIGINT, sig_handler)
            signal.signal(signal.SIGTERM, sig_handler)

            tb.start()


            Fs = float(sys.argv[7]) #Sample Rate
            center_freq1 = float(sys.argv[8])
            center_freq2 = float(sys.argv[9])
            filename1 = sys.argv[2] #Filename + Directory
            filename2 = sys.argv[3]
            N = int(sys.argv[6]) #Vector Length

            time.sleep(3)

            X = np.fromfile(open(filename1), dtype=np.float32)
            Y = np.fromfile(open(filename2), dtype=np.float32)

            f1 = np.arange(Fs/-2.0, Fs/2.0, Fs/N) 
            f1 += center_freq1

            f2 = np.arange(Fs/-2.0, Fs/2.0, Fs/N) 
            f2 += center_freq2

            def update(length):
                i = 0
                while i < length:
                    x_i = X[i*N:(i+1)*N]
                    y_i = Y[i*N:(i+1)*N]
                    for j in range(len(f1)):
                        freq1 = f1[j]
                        dBm1 = x_i[j]
                        msgclient1 = (f"Freq: {freq1:} Hz, dBm: {dBm1:}")
                        
                        msgFromClient       = msgclient1

                        bytesToSend         = str.encode(msgFromClient)

                        serverAddressPort   = (sys.argv[5], int(sys.argv[4])) #Server Ethernet IP and Port Number

                        bufferSize          = int(sys.argv[6])

                        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) # Create a UDP socket at client side

                        UDPClientSocket.sendto(bytesToSend, serverAddressPort) # Send to server using created UDP socket

                        msgFromServer = UDPClientSocket.recvfrom(bufferSize)

                        msg = "Message from Server {}".format(msgFromServer[0])

                        print(msg) 
                    for k in range(len(f2)):
                        freq2 = f2[k]
                        dBm2 = y_i[k]
                        msgclient2 = (f"Freq: {freq2:} Hz, dBm: {dBm2:}")

                        msgFromClient       = msgclient2

                        bytesToSend         = str.encode(msgFromClient)

                        serverAddressPort   = (sys.argv[5], int(sys.argv[4])) #Server Ethernet IP and Port Number

                        bufferSize          = int(sys.argv[6])

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
    else:
        # do something if the first argument is neither 1 nor 2
        print("First command line argument is not 1 or 2.")
