#! /bin/bash

for subject in  0550 0566 0738 0739 0740 0741 0742 0743 0744 0745 0746 0747 0748 0749 0750 0751 0752 0753 0754 0755
do
  #scp /data/modMap/subjects/${subject}/Pre/RER_Run1/urRER_Run1.nii /data/modMap/subjects/${subject}/searchlights/urRER_Run1.nii
  # BB registration

  #bbregister --s $subject --mov /data/modMap/subjects/${subject}/searchlights/urRER_Run1.nii --init-spm --bold --reg /usr/local/freesurfer/subjects/${subject}/bb_mm.dat

  for image in ss_pre_cue  ss_pre_finger

  do
    for hemi in lh rh
    do
      #This guy will put the searchlights into freesurfer surface space.
      mri_vol2surf --src /data/modMap/subjects/${subject}/searchlights/first_finger/s_${image}.img --projfrac-avg 0 1 0.2 --out /usr/local/freesurfer/subjects/${subject}/s_${hemi}${image}.nii --trgsubject $subject --out_type paint --srcreg  /usr/local/freesurfer/subjects/${subject}/bb_mm.dat  --hemi ${hemi}

      # This guy must use the spherical registration
      mri_surf2surf --srcsubject ${subject} --srcsurfval /usr/local/freesurfer/subjects/${subject}/s_${hemi}${image}.nii  --trgsubject modmap --trgsurfval /usr/local/freesurfer/subjects/${subject}/s_${hemi}${image}.nii --hemi  ${hemi}

      #For random effects analysis
      cp /usr/local/freesurfer/subjects/${subject}/s_${hemi}${image}.nii /usr/local/freesurfer/subjects/${subject}/s_${hemi}${image}_surf.nii

      #mri_surfcluster --in /usr/local/freesurfer/subjects/${subject}/${hemi}${image}.nii --subject r2d4mean --hemi ${hemi} --annot aparc --sign pos --minarea 40 --sum area25.pos.cluster.summary --o /usr/local/freesurfer/subjects/${subject}/${hemi}${image}_clusters.nii --thmin 1mm

      #mri_surf2vol --surfval /usr/local/freesurfer/subjects/${subject}/${hemi}${image}_clusters.nii --hemi ${hemi} --outvol /data/modMap/subjects/${subject}/searchlights/${hemi}${image}_clusters.nii --volregidentity r2d4mean --template /usr/local/freesurfer/subjects/r2d4mean/mri/orig.mgz  --fill-projfrac 0 1 0.1

    done
    #mris_calc -o /data/modMap/subjects/${subject}/searchlights/${image}_clusters.nii /data/modMap/subjects/${subject}/searchlights/lh${image}_clusters.nii add /data/modMap/subjects/${subject}/searchlights/rh${image}_clusters.nii
  done

done
