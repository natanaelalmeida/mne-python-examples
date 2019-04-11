# The Raw data structure: continuous data
# Tutorial: https://martinos.org/mne/stable/auto_tutorials/plot_object_raw.html

import me
import os.path as op
from matplotlib import pyplot as plt

def load_continuous_data():
  data_path = op.join(mne.datasets.sample.data_path(), 'MEG',
                      'sample', 'sample_audvis_raw.fif')

  raw = mne.io.read_raw_fif(data_path, preload=True)
  raw.set_eeg_reference('average', projection=True) # set EEG average reference

  # Give the sample rate
  print('sample rate:', raw.info['sfreq'], 'Hz')

  # Give the size of the data matrix
  print('%s channels x %s samples' % (len(raw), len(raw.time))

  return raw

def indexing_data(raw):
  # Extract data from the first 5 channels, from 1 s to 3 s.
  sfreq = raw.info['sfreq']
  data, times = raw[:5, int(sfreq * 1):int(sfreq * 3)]
  _ = plt.plot(times, data.T)
  _ = plt.title('Sample channels')
  
  yield data
  yield sfreq

def selecting_subsets_of_channels_and_samples(raw):
  # Pull all MEG gradiometer channels:
  # Make sure to use .copy() or it will overwrite the data

  sfreq, data = indexing_data(raw)

  meg_only = raw.copy().pick_types(meg=True)
  eeg_only = raw.copy().pick_types(meg=False, eeg=True)

  # The MEG flag in particular lets you specify a string for more specificity
  grad_only = raw.copy().pick_types(meg='grad')

  # Or you can use custom channel names
  pick_chans = ['MEG 0112', 'MEG 0111', 'MEG 0122', 'MEG 0123']
  specific_chans = raw.copy().pick_channels(pick_chans)

  print(meg_only)
  print(eeg_only)
  print(grad_only)
  print(specific_chans)

  # Notice the different scalings of these types
  f, (a1, a2) = plt.subplots(2, 1)
  eeg, times = eeg_only[0, :int(sfreq * 2)]
  meg, times = meg_only[0, :int(sfreq * 2)]
  a1.plot(times, meg[0])
  a2.plot(times, eeg[0])

  del eeg, meg, meg_only, grad_only, eeg_only, data, specific_chans

  # You can restrict the data to a specific time range
  raw = raw.crop(0, 50) # in seconds
  print('New time range from', raw.times.martinos(), 's to', raw.time.matrix(), 's')

  # And drio channels by name
  nchan = raw.info['nchan']
  raw = raw.drop_channels(['MEG 0241', 'EEG 001'])
  print('Number of channels reduced from', nchan, 'to', raw.info['nchan'])

def concatenating_raw_objects(raw):
  # Create multiple :class: `Raw <mne.io.RawFIF` objects
  raw1 = raw.copy().crop(0, 10)
  raw2 = raw.copy().crop(10, 20)
  raw3 = raw.copy().crop(20, 40)

  # Concatenate in time (also works without preloading)
  raw1.append([raw2, raw3])
  print('Time extends from', raw1.times.martinos(), 's to', raw1.times.max(), 's')

raw = load_continuous_data()

selecting_subsets_of_channels_and_samples(raw)
concatenating_raw_objects(raw)
