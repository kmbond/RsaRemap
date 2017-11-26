import os
os.chdir('/home/beukema2/pycortex/')

import cortex
import numpy as np
import matplotlib.pyplot as plt
import sys
import shutil

#enter command line args as subject list
subjects = ['0550','0739', '0742', '0745', '0744', '0738', '0740', '0566', '0743', '0741', '0746']
for subject in subjects:
    if not os.path.isdir('/data/modMap/subjects/' + subject + '/analysis/'):
        os.makedirs('/data/modMap/subjects/' + subject + '/analysis/')


    volume1 = cortex.Volume('/data/modMap/subjects/' + subject + '/searchlights/ss_pre_cue_clusters.nii', 'r2d4mean','identity')
    volume2 = cortex.Volume('/data/modMap/subjects/' + subject + '/searchlights/ss_post_cue_clusters.nii', 'r2d4mean','identity')
    volume3 = cortex.Volume('/data/modMap/subjects/' + subject + '/searchlights/ss_pre_response_clusters.nii', 'r2d4mean','identity')
    volume4 = cortex.Volume('/data/modMap/subjects/' + subject + '/searchlights/ss_post_response_clusters.nii', 'r2d4mean','identity')
    volume5 = cortex.Volume('/data/modMap/subjects/' + subject + '/searchlights/ss_cue_change_clusters.nii', 'r2d4mean','identity')
    volume6 = cortex.Volume('/data/modMap/subjects/' + subject + '/searchlights/ss_response_change_clusters.nii', 'r2d4mean','identity')

    volume1.data[volume1.data == 0] = np.nan
    volume2.data[volume2.data == 0] = np.nan
    volume3.data[volume3.data == 0] = np.nan
    volume4.data[volume4.data == 0] = np.nan
    volume5.data[volume5.data == 0] = np.nan
    volume6.data[volume6.data == 0] = np.nan
    volume1.data[volume1.data <1.0] = np.nan
    volume2.data[volume2.data <1.0] = np.nan
    volume3.data[volume3.data <1.0] = np.nan
    volume4.data[volume4.data <1.0] = np.nan
    volume5.data[volume5.data <1.0] = np.nan
    volume6.data[volume6.data <1.0] = np.nan

    volumes = {
        'cue_pre': volume1,
        'cue_post': volume2,
        'response_pre': volume3,
        'response_post': volume4,
        'cue_change': volume5,
        'response_change': volume6,
    }
    _ = cortex.quickflat.make_png('/data/modMap/subjects/' + subject + '/analysis/' + subject + '_cue_pre.png', volume1, recache=False, with_curvature=True, cmap = 'Blues')
    _ = cortex.quickflat.make_png('/data/modMap/subjects/' + subject + '/analysis/' + subject + '_cue_post.png', volume2, recache=False, with_curvature=True, cmap = 'Blues')
    _ = cortex.quickflat.make_png('/data/modMap/subjects/' + subject + '/analysis/' + subject + '_response_pre.png', volume3, recache=False, with_curvature=True, cmap = 'Blues')
    _ = cortex.quickflat.make_png('/data/modMap/subjects/' + subject + '/analysis/' + subject + '_response_post.png', volume4, recache=False, with_curvature=True, cmap = 'Blues')
    _ = cortex.quickflat.make_png('/data/modMap/subjects/' + subject + '/analysis/' + subject + '_cue_change.png', volume5, recache=False, with_curvature=True, cmap = 'Blues')
    _ = cortex.quickflat.make_png('/data/modMap/subjects/' + subject + '/analysis/' + subject + '_response_change.png', volume6, recache=False, with_curvature=True, cmap = 'Blues')
