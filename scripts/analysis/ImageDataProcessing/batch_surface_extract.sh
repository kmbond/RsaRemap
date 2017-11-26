#! /bin/bash

for subject in $1
do
  python /data/r2d4/surfing-master/python/prep_afni_surf.py -d /data/modMap/surfaces/${subject}/T1w/${subject}/surf/ -a /data/modMap/subjects/${subject}/Pre/t1/t1.nii -r /data/modMap/subjects/${subject}/Pre/surface_searchlight/
done
