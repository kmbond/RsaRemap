# Copy files from fileserver2.sibr.cmu.edu
scp -P 33 -r pbeukema@fileserver2.sibr.cmu.edu:/home/pbeukema/coax_Images/$file_id/ /data/modMap/subjects/$sid/$session/
# ssh-keygen

# MUST USE MATLAB R2013 for this particular dataset 

#Directory structure4
# -modMap
#   -subjects
#     -sid
#       -Pre
#       -Post
#       -searchlights
#       -analysis

# Convert dcms to nifti
matlab -nodesktop -nosplash -r "mm_convert_dcms(${sid}, $sess)"

# Grab onsets from ~/Dropbox
python /data/modMap/bin/mm_onsets.py $sub $sesms

# Run GLM
matlab -nodesktop -nosplash -r "preprocess_and_glm(${sid}, $sess)"


# Make surfaces from t1/t2 if sess=Pre (start this process in new shell)
modmap_hcp.sh ${sid} && sh /data/modMap/bin/batch_surface_extract.sh ${sid}
cp -r /data/modMap/surfaces/${sidT1w/${sid} /usr/local/freesurfer/subjects/
matlab -nodesktop -nosplash -r "modMap_ss_voxel_extraction(${sid})"

# run mri_qc

# Transfer files to cluster
rsync -zavr -e ssh --delete --include '*/' --include='*urRER_Run*.nii' --include='mask.*' --in='surface_voxels.mat' --include='SPM.mat' --exclude='*' /data/modMap/subjects/${sid} --prune-empty-dirs pbeukema@psych-o.hpc1.cs.cmu.edu:/home/pbeukema/modMap/subjects

# write and submit a pbs job for this subject (this is run on the cluster)
qsub -v SID=${sid} mm_searchlight // mm_searchligh_simple

# copy files back from cluster to local computer
scp pbeukema@psych-o.hpc1.cs.cmu.edu:/home/pbeukema/modMap/subjects/${sid}/ss* /data/modMap/subjects/${sid}/searchlights/

# align individual volumes to freesurfer space with BB alignment then align to group surface with spherical registration
Smooth images in the volume
sh /data/modMap/bin/bb_and_surf2vol.sh ${sid}

# Generate figures with pycortex
# Run from within a jupyter notebook and the ~/pyCortex directory
pyCortex_show.sh

# make an average subject out of modMap
make_average_subject --s subs --out modMap
