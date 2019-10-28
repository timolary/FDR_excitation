#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: N Wideband Excite
# Generated: Thu Oct 24 16:04:03 2019
##################################################


from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from math import pi
from optparse import OptionParser
import argparse
import divide_by_n
import numpy as np
import osmosdr
import peak_hold
import threading
import time


class n_wideband_excite(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "N Wideband Excite")

        ##################################################
        # Variables
        ##################################################
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.tx_freq = tx_freq = 1.3e9
        self.samp_rate = samp_rate = 20e6
        self.rx_freq = rx_freq = 2.6e9
        self.fft_size = fft_size = 2**12

        ##################################################
        # Blocks
        ##################################################
        self.probe_peak = blocks.probe_signal_vf(fft_size)

        def _variable_function_probe_0_probe():
            while True:
                val = self.probe_peak.level()
                try:
                    self.set_variable_function_probe_0(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
        _variable_function_probe_0_thread.daemon = True
        _variable_function_probe_0_thread.start()

        self.peak_hold = peak_hold.blk()
        self.osmosdr_source_0_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'bladerf=0' )
        self.osmosdr_source_0_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0_0.set_center_freq(rx_freq, 0)
        self.osmosdr_source_0_0.set_freq_corr(0, 0)
        self.osmosdr_source_0_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0_0.set_gain_mode(False, 0)
        self.osmosdr_source_0_0.set_gain(10, 0)
        self.osmosdr_source_0_0.set_if_gain(20, 0)
        self.osmosdr_source_0_0.set_bb_gain(20, 0)
        self.osmosdr_source_0_0.set_antenna('', 0)
        self.osmosdr_source_0_0.set_bandwidth(0, 0)

        self.osmosdr_sink_0_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'bladerf=0' )
        self.osmosdr_sink_0_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0_0.set_center_freq(tx_freq, 0)
        self.osmosdr_sink_0_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0_0.set_gain(10, 0)
        self.osmosdr_sink_0_0.set_if_gain(20, 0)
        self.osmosdr_sink_0_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0_0.set_antenna('', 0)
        self.osmosdr_sink_0_0.set_bandwidth(0, 0)

        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, (window.blackmanharris(fft_size)), True, 2)
        self.divide_by_n = divide_by_n.blk(divisor=4096)
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, 2*pi*10e6, .3)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, fft_size, -30)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_size)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SAW_WAVE, .5, 1, -.5)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.divide_by_n, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.peak_hold, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.osmosdr_sink_0_0, 0))
        self.connect((self.divide_by_n, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.peak_hold, 0), (self.probe_peak, 0))

    def get_peak(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.osmosdr_sink_0_0.set_center_freq(self.tx_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0_0.set_sample_rate(self.samp_rate)
        self.osmosdr_sink_0_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.osmosdr_source_0_0.set_center_freq(self.rx_freq, 0)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size


def main(top_block_cls=n_wideband_excite, options=None):

    parser = argparse.ArgumentParser(description='FDR receive with BladeRF')
    parser.add_argument('-s', '--start_freq', type=float, help='Start frequency (Hz)')
    parser.add_argument('-e', '--end_freq', type=float, help='End frequency (Hz)')
    parser.add_argument('-t', '--dwell_time', required=False, default=0.5, type=float, help='Dwell time in seconds')
    args = parser.parse_args()

    start_freq = args.start_freq
    end_freq = args.end_freq
    dt = args.dwell_time
    step_freq = 20e6
    tune_freq = start_freq

    tb = top_block_cls()
    tb.start()
    f = open('peak_data.fft', 'wb')
    while tune_freq <= end_freq:
        tb.set_rx_freq(tune_freq)
        tb.set_tx_freq(tune_freq/2)
        tb.peak_hold.reset()
        print('Receiving data at {} MHz'.format(tb.get_rx_freq() / 1e6))
        tune_freq = tune_freq + step_freq
        time.sleep(dt)
        fft_vec = tb.get_peak()
        f.write(np.float32(fft_vec))
    f.close()
    tb.stop()


if __name__ == '__main__':
    main()
