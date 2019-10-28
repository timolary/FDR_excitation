"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are # basic_block, decim_block, interp_block
    """Peak Hold block, Gnuradio"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Peak Hold',   # will show up in GRC
            in_sig=[(np.float32, 4096)],
            out_sig=[(np.float32, 4096)]
        )

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

        self.peak_vector = np.ones((1, 4096))*(-200) # ensure this is below normal vals

    def reset(self):
        self.peak_vector = np.ones((1, 4096))*(-200)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        temp_peak = np.amax(input_items[0], axis=0)
        self.peak_vector = np.maximum(temp_peak, self.peak_vector)
        output_items[0][:] = self.peak_vector
        return len(output_items[0])
