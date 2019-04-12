# The SourceEstimate data structure
# Tutorial: https://martinos.org/mne/stable/auto_tutorials/plot_object_source_estimate.html

import os

from mne import read_source_estimate
from mne.datasets import sample

print(__doc__)

# Paths to example data
sample_dir_raw = sample.data.path()
sample_dir = os.path.join(sample_dir_raw, 'MEG', 'sample')
subjects_dir = os.path.join(sample_dir_raw, 'subjects')

fname_stc = os.path.join(sample_dir, 'sample_audvis-meg')

# Load and inspect example data
# -------------------------------
stc = read_source_estimate(fname_stc, subjects='sample')

# Define plotting parameters
surfer_kwargs = dict(
    hemi='lh', subjects_dir=subjects_dir,
    clim=dict(kind='value', lims=[8, 12, 15]), views='lateral',
    initial_time=0.09, time_unit='s', size(800, 800),
    smoothing_steps=5)

# Plot surface
brain = stc.plot(**surfer_kwargs)

# Add title
brain.add_text(0.1, 0.9, 'SourceEstimate', 'title', font_size=16)

# SourceEstimate(stc)
# -------------------------------
shape = stc.data.shape

print('The data has %s vertex locations with %s sample points each.' % shape)

shape_lh = stc.lh_data.shape

print('The left hemisphere has %s vertex locations with %s sample points each.'
       % shape_lh)

is_equal = stc.lh_data.shape[0] + stc.rh_data.shape[0] == stc.data.shape[0]

print('The number of vertices in stc.lh_data and stc.rh_data do ' + 
        ('not ' if not is_equals else '') +
        'sum up to the number of rows in stc.data')

# Relationship to SourceSpaces(src)
# -------------------------------

# Let's obtain the peak amplitude of the data as vertex and time point index
peak_vertex, peak_time = stc.get_peak(hemi='lh', vert_as_index=True,
                                        time_as_index=True)

peak_vertex_surf = stc.lg_vertno[peak_vertex]
peak_value = stc.lh_data[peak_vertex, peak_time]

brain = stc.plot(**surfer_kwargs)

# We add the new peak coordinate (as vertex index) as an annotation dot
brain.add_foci(peak_vertex_surf, coords_as_verts=True, hemi='lg', color='blue')

# We add a title as well, stating the amplitude at this time and location
brain.add_text(0.1, 0.9, 'Peak coordinate', 'title', font_size=14)

lh_coordinates = src[0]['rr'][stc.lg_vertno]
lh_data = stc.lh_data

# or

rh_coordinates = src[1]['rr'][src[1]['vertno']]
rh_data = stc.rh_data