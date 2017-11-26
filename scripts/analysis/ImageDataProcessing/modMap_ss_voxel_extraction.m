function modMap_ss_voxel_extraction(sid);

% This script selects the surface searchlight voxels in r2d4 subjects. It
% requres that prep_afni_surf.py has already been run on each subject. That
% script saves the aligned surfaces to /subjects/surface_searchlight. as
% written this script selects voxels in both hemispheres, using the
% freesurfer extracted pial and white matter surfaces. This script stores
% the saved voxels (n2v) in a mat file that should then be imported when running
% the MVPA searchlight. There are a number of options that can be set with
% the voxel_selector. This script uses the parameters that have been shown
% to be optimal in Ejaz and Wiestlers, and is specific for representations
% of finger movements in motor regions.

addpath('/usr/share/spm8');
addpath(genpath('/data/r2d4/'));
addpath(genpath('/data/r2d4/surfing-master/'));


radius =160; % constant number of voxels has been shown to be better than constant radius
radiusunit = 'vx'; % vx or mm
centercount = NaN ; % number of searchlight centers ; NaN for all
circledef =  [10 radius];

% input files ( ASCII freesurfer )
mask_file = sprintf('/data/modMap/subjects/%s/Pre/RER_Run1/urRER_Run1.nii', sid);
Vmask = spm_vol(mask_file);

% Dims
Vmask(1).mat;
Vmask(1).dim;

% Voldef
voldef.mat = Vmask(1).mat;
voldef.dim = Vmask(1).dim;

% Use high res surface for publications (128) - this is slower.
fns1 =sprintf('/data/modMap/subjects/%s/Pre/surface_searchlight/ico128_mh.pial_al.asc', sid); % freesurfer pial surface ( ascii format )
fns2 =sprintf('/data/modMap/subjects/%s/Pre/surface_searchlight/ico128_mh.smoothwm_al.asc', sid); % freesurfer white surface ( ascii format )
[c1 ,f]= freesurfer_asc_load(fns1);
[c2 , f_]= freesurfer_asc_load(fns2);

c1 =c1';
c2 =c2';
f=f';
nverts = size(c1,2);

% Show which voxels will be selected:
allcoords = surfing_nodeidxs2coords(c1,c2,1:length(c1),[5 0 1]);
alllinvoxidxs   = surfing_coords2linvoxelidxs(allcoords,Vmask(1));
unqlinvoxidxs   = surfing_uniqueidxsperrow(alllinvoxidxs);
[centerindxs] = unique(unqlinvoxidxs(~isnan(unqlinvoxidxs) & unqlinvoxidxs~=0));
ncenters        = numel(centerindxs);
inclMask        = Vmask(1);
inclMask.fname  = sprintf('/data/modMap/subjects/%s/Pre/surface_searchlight/surfMask.nii', sid);
inclMask.data   = NaN(inclMask.dim);
inclMask.data(centerindxs)  = 1;
spm_write_vol(inclMask,inclMask.data);


% Select those voxels
[n2v ,mn , mx , ds, centerindxs, node ]= surfing_voxelselectionv2(c1 ,c2 ,f, circledef , voldef);
fn = sprintf('/data/modMap/subjects/%s/Pre/surface_searchlight/surface_voxels.mat', sid);
save(fn,'n2v','mn', 'mx', 'ds', 'centerindxs','node');
