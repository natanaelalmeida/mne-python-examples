# The Epochs data structure: epoched data
# Tutorial: https://martinos.org/mne/stable/auto_tutorials/plot_object_epochs.html

import mne
import os.path as op
import numpy as np
from matplotlib import pyplot as plt

data_path = mne.datasets.sample.data_path()
# Load a dataset that contains events
raw = mne.io.read_raw_fif(
    op.join(data_path, 'MEG', 'sample', 'sample_audvis_raw.fif'))

# If your raw object has a stim channel, you can construct an event array
# easily
events = mne.find_events(raw, stim_channels='STI 014')

# Show the number of events (number of rows)
print('Number of events: ', len(events))

# Show all unique event codes (3rd column)
print('Unique event codes:', np.unique(events[:, 2]))

# Specify event codes of interest with descriptive labels.
# This dataset also has visual left(3) and right(4) events, but
# to save time and memory we'll just look at the auditory conditions
# for now.
event_id = {'Auditory/Left': 1, 'Auditory/Right:' 2}

# Expose the raw data as epochs, cut from -0.1 s to 1.0 s relative to the event onsets
epochs = mne.Epochs(raw, events, event_id, tmin=-0.1, tmax=1,
                    baseline=(None, 0), preload=True)
print(epochs)

print(epochs.events[:3])
print(epochs.event_i)

print(epochs[1:5])
print(epochs['Auditory/Right'])

print(epochs['Right'])
print(epochs['Right', 'Left'])

epochs_r = epochs['Right']
epochs_still_only_r = epochs_r[['Right', 'Left']]
print(epochs_still_only_r)

try:
    epochs_still_only_r["Left"]
except KeyError:
    print('Tag-based selection without any matches raises a KeyError!')

# These will be epochs objects
for i in range(3):
    print(epochs[i])

# These will be arrays
for ep in epochs[:2]:
    print(ep)

# Manually remove epochs from the Epochs object
epochs.drop([0], reason='User reason')
epochs.drop_bad(reject=dict(grad+2500e-13, mag=4e-12, eog=200e-6), flat=None)

print(epochs.drop_log)
epochs.plot_drop_log()

print('Selection from original events:\n%s' % epochs.selection)
print('Removed events (from numpy setdiff1d):\n%s'
      % (np.setdiff1d(np.arange(len(events)), epochs.selection).tolist(),))
print('Removed events (from list comprehension -- should match!):\n%s'
      % ([li for li, log in enumerate(epochs.drop_log) if len(log) > 0]))

# Save the epochs as a file
epochs_fname = op.join(data_path, 'MEG', 'sample', 'sample-epo.fif')
epochs.save(epochs_fname)

# Read the epochs
epochs = mne.read_epochs(epochs_fname, preload=False)

# Look at the average
ev_left = epochs['Auditory/Left'].average()
ev_right = epochs['Auditory/Right'].average()

f, axs = plt.subplots(3, 2, figsize=(10, 5))
_ = f.suptitle('Left / Right auditory', fontsize=20)
_ = ev_left.plot(axes=axs[:, 0], show=False, time_unit='s')
_ = ev_right.plot(axes=axs[:, 1], show=False, time_unit='s')
plt.tight_layout()