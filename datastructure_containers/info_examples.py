# The info data structure
# Tutorial: https://martinos.org/mne/stable/auto_tutorials/plot_info.html

import mne
import os.path as op

# Read the info object from an example recording
info = mne.io.read_info(
    op.join(mne.datasets.sample.data_path(), 'MEG', 'sample',
            'sample_audvis_raw.fif'), verbose=False)

print('Keys in info dictionary:\n', info.keys())

# Obtain the sampling rate of the data
print(info['sfreq'], 'Hz')

# List all information about the first data channel
print(info['chs'][0])

# Obtaining subsets of channels
# -------------------------------
channel_indices = mne.pick_channels(info['ch_names'], ['MEG 0312'], 'EEG 005')

channel_indices = mne.pick_channels_regexp(info['ch_names'], 'MEG *')