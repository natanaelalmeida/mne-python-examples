# The Evoked data structure: evoked/averaged data
# Tutorial: https://martinos.org/mne/stable/auto_tutorials/plot_object_evoked.html

import os.path as op
import mne

data_path = mne.datasets.sample.data_path()
fname = op.join(data_path, 'MEG', 'sample', 'sample_audvis-ave.fif')
evokeds = mne.read_evokeds(fname, baseline=(None, 0), proj=True)
print(evokeds)

# Reader function returned a list of evoked instances
evoked = mne.read_evokeds(fname, condition='Left Auditory')
evoked.apply_baseline((None, 0)).apply_proj()
print(evoked)

print(evoked.info)
print(evoked.times)

# The evoked data structure also contains some new attributes easily accessible:
print(evoked.name) # Number of averaged epochs.
print(evoked.first) # First time sample.
print(evoked.last) # Last time sample.
print(evoked.comment) # Comment on dataset. Usually the condition.
print(evoked.kind) # Type of data, either average or standard_error.

# Access data
data = evoked.data
print(data.shape)

print('Data from channel {0}:'.format(evoked.ch_names[10]))
print(data[10])

# Import evoked data from some other system
evoked = mne.EvokedArray(data, evoked.info, tmin=evoked.times[0])
evoked.plot(time_unit='s')

# Save evoked dataset to a file
# mne.Evoked.save() or save multiple categories mne.write_evokeds()