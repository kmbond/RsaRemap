function mm_surface_searchlight(SID);
% h = waitbar(0,'Initializing waitbar...');
% function gen_searchlight(spm_file, mask_file, varargin);


matlabpool open
addpath('/home/pbeukema/r2d4/bin/');
addpath('/home/pbeukema/modMap/bin/');
addpath('/home/pbeukema/r2d4/subjects/');
addpath('/home/matlab/8.1/toolbox/spm/spm8');

SID = sprintf('0%s', num2str(SID));

% General searchlight routine. Built for RSA
plot_flag = 0; % don't plot on each run
outfname = 'ss';

which_session = {'Pre', 'Post'};
for session = 1:2;
    wdir = sprintf('/home/pbeukema/modMap/subjects/%s/%s/GLM/', SID, which_session{session});
    cd(wdir);
    load SPM
    if isempty(strfind(SPM.xY.VY(1,1).fname,'pbeukema'));
        %change filenames
        spm_changepath('SPM.mat','/data/modMap/subjects/','/home/pbeukema/modMap/subjects/');
    else
        %do nothing, filenames already overwritten
    end;
end
sprintf('/home/pbeukema/modMap/subjects/%s', SID);
cd(sprintf('/home/pbeukema/modMap/subjects/%s', SID));

% Load the SPM objects
spm_file1 = sprintf('/home/pbeukema/modMap/subjects/%s/Pre/GLM/SPM.mat', SID);
spm_file2 = sprintf('/home/pbeukema/modMap/subjects/%s/Post/GLM/SPM.mat', SID);
mask_file = sprintf('/home/pbeukema/modMap/subjects/%s/Pre/GLM/mask.hdr', SID);

SPM_pre = load(spm_file1);
SPM_post = load(spm_file2);
SPM_pre = SPM_pre.SPM;
SPM_post = SPM_post.SPM;

% Check if output directory exists and if not create it.
output_dir = sprintf('/home/pbeukema/modMap/subjects/%s/searchlights/', SID);
if ~exist(output_dir)
    mkdir(output_dir)
end


% Load the mask
Vmask = spm_vol(mask_file);
Ymask = spm_read_vols(Vmask);
voxels = load(sprintf('/home/pbeukema/modMap/subjects/%s/Pre/surface_searchlight/surface_voxels.mat', SID));

%Clear those serchlights that are empty:
vox_centers = voxels.centerindxs;
surface_voxels = voxels.n2v;
non_empty = find(~cellfun(@isempty,surface_voxels));
vox_centers = vox_centers(non_empty);

is_empty = find(cellfun(@isempty,surface_voxels));
surface_voxels(:,is_empty) = [];

% get only masked voxels as your seeds
index = find(Ymask(:));

% Setup a new output volumes

h_vol_pre_cue = NaN(size(Ymask));
h_vol_pre_response = NaN(size(Ymask));
h_vol_pre_both = NaN(size(Ymask));
h_vol_post_cue = NaN(size(Ymask));
h_vol_post_response = NaN(size(Ymask));
h_vol_post_both = NaN(size(Ymask));
h_vol_cue_change = NaN(size(Ymask));
h_vol_response_change = NaN(size(Ymask));
h_vol_both_change = NaN(size(Ymask));


n_betas = length(SPM_pre.Sess(1).col);

%Preallocate for parfor loop.
pre = [];
post = [];
change = [];


pre_cue = [];
pre_response = [];
pre_both = [];

post_cue = [];
post_response = [];
post_both = [];

cue_change = [];
response_change = [];
both_change = [];



parfor i = 1:length(vox_centers);

    %Select the center voxel and searchlight voxels
    this_center = vox_centers(i);
    this_searchlight = surface_voxels{i};

    [x, y, z] = ind2sub(size(Ymask),this_searchlight);
    coord = double([x;y;z]); %searchlight voxels

    % Extract data
    y_data_pre = spm_get_data(SPM_pre.xY.VY, coord);
    y_data_post = spm_get_data(SPM_post.xY.VY, coord);

    %Remove columns of zeros o/w matrix may not be positive semi definite:
    y_data_pre(:, find(sum(abs(y_data_pre)) == 0)) = [];
    y_data_post(:, find(sum(abs(y_data_post)) == 0)) = [];

    %Occasionaly grabs data outside mask - unclear why
    if numel(y_data_pre)==0;
        pre_cue(i) = NaN;
        pre_response(i) = NaN;
        pre_both(i) = NaN;

        post_cue(i) = NaN;
        post_response(i) = NaN;
        post_both(i) = NaN;

        cue_change(i) = NaN;
        response_change(i) = NaN;
        both_change(i) = NaN;
        continue
    end;

    % Orthogonalize y_data
    y_data_pre = grab95pca(y_data_pre);
    y_data_post = grab95pca(y_data_post);

    % Prewhiten the beta coefficients
    [beta_w_pre, beta_pre, resMS_pre] = mva_prewhiten_beta(y_data_pre, SPM_pre);
    [beta_w_post, beta_post, resMS_post] = mva_prewhiten_beta(y_data_post, SPM_post);

    % Run RSA to obtain distances between patterns
    [pre_b, pre_r, pre_c, ~, ~] = modMap_rsa(beta_w_pre, n_betas);
    [post_b, post_r, post_c, ~, ~] = modMap_rsa(beta_w_post, n_betas);

    %Compute the difference between pre and post
    pre_cue(i) = pre_c*100;
    pre_response(i) = pre_r*100;
    pre_both(i) = pre_b*100;

    post_cue(i) = post_c*100;
    post_response(i) = post_r*100;
    post_both(i) = post_b*100;

    cue_change(i) =  (post_c - pre_c)*100;
    response_change(i) =   (post_r - pre_r)*100;
    both_change(i) =  (post_b - pre_b)*100;

end;

h_vol_pre_cue(vox_centers) = pre_cue;
h_vol_pre_response(vox_centers) = pre_response;
h_vol_pre_both(vox_centers) = pre_both;

h_vol_post_cue(vox_centers) = post_cue;
h_vol_post_response(vox_centers) = post_response;
h_vol_post_both(vox_centers) = post_both;

h_vol_cue_change(vox_centers) = cue_change;
h_vol_response_change(vox_centers) = response_change;
h_vol_both_change(vox_centers) = both_change;

% Now save the output files to searchlight dir
fp = sprintf('/home/pbeukema/modMap/subjects/%s/searchlights/', SID);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_pre_cue.img', outfname));
spm_write_vol(Vh, h_vol_pre_cue);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_pre_response.img', outfname));
spm_write_vol(Vh, h_vol_pre_response);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_pre_both.img', outfname));
spm_write_vol(Vh, h_vol_pre_both);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_post_cue.img', outfname));
spm_write_vol(Vh, h_vol_post_cue);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_post_response.img', outfname));
spm_write_vol(Vh, h_vol_post_response);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_post_both.img', outfname));
spm_write_vol(Vh, h_vol_post_both);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_cue_change.img', outfname));
spm_write_vol(Vh, h_vol_cue_change);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_response_change.img', outfname));
spm_write_vol(Vh, h_vol_response_change);

Vh = Vmask;
Vh.dt(1)= 16;
Vh.fname = fullfile(fp,sprintf('%s_both_change.img', outfname));
spm_write_vol(Vh, h_vol_both_change);

matlabpool close;
exit;
