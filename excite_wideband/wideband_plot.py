import numpy as np
import matplotlib.pyplot as plt
import argparse
plt.style.use('nicelooking.mplstyle')


def main():
    parser = argparse.ArgumentParser(description='Plot FFTs')
    parser.add_argument('-f', '--filename', type=str, help='Filename', required=True)
    parser.add_argument('-s', '--start_freq', type=int, help='Start Frequency (MHz)', required=True)
    parser.add_argument('-e', '--end_freq', type=int, help='End Frequency (MHz)', required=True)
    args = parser.parse_args()

    filename = args.filename
    start_freq, end_freq = args.start_freq, args.end_freq
    fft = np.fromfile(filename, dtype=np.float32)
    freq = np.linspace(start_freq, end_freq, len(fft))
    plt.plot(freq, fft)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Power (dBm)')

    plt.show()


if __name__ == '__main__':
    main()
