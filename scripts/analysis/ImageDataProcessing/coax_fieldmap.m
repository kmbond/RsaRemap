function coax_fieldmap(sub, session)
% FORMAT coax_fieldmap(exp_dir, sub)
%
% Create voxel displacement map and apply to EPIs
% Written by    K. Jarbo on 19 Apr 2016 like a boss
% vdmFlags = struct('te1', 5.00, 'te2', 7.46, 'epifm', 0, 'tert', 30.39,...
%     'kdir', -1, 'mask', 0, 'match', 1);

% Edited for modmap by George on 29 May 2017
% This function generates two vdms from two distinct fieldmaps that were collected on separate days.
% fieldmap 1 is used to undistort Runs 1-4 that were collected on the first day
% fieldmap 2 is used to undistort Runs 5-8 that were colected on the second day
% The fieldmaps are registered to the first scan (Pre scan) which all of the functional volumes have also been registered to from groovy_realign
% this process takes timIe because were are using the highest quality available registration algorithms.


addpath(genpath('/usr/share/spm8'));
pm_defaults_verio;
pm_defs.match_vdm=1; %this is not auto-loaded for some reason

for mapping_to_runs = [1,2];

    switch mapping_to_runs;
        case 1;
            run_start = 1;
            run_end = 4;
        case 2;
            run_start = 5;
            run_end = 8;
    end

    exp_dir = '/data/modMap/subjects';
    % Apply VDM
    job.roptions.rinterp = 7;
    job.roptions.wrap = [0 0 0];
    job.roptions.mask = 1;
    job.roptions.which = [2 1];
    job.roptions.prefix = 'u';
    job.roptions.pedir = 2;

    % Create fieldmap images and apply VDM
    % Set variables and paths
    epi_dir = fullfile(exp_dir,sub, session);
    fmap_dir = fullfile(exp_dir,sub,session,sprintf('fieldmap_runs%s_%s_01', int2str(run_start), int2str(run_end)));

    % Scale the phase image to radians (From pm_scale_phase in FieldMap toolbox)
    phase_img = dir(fullfile(fmap_dir,sprintf('fieldmap_runs%s_%s_01.nii', int2str(run_start), int2str(run_end))));

    tmp_vol = spm_vol(fullfile(fmap_dir,phase_img.name));
    vol = spm_read_vols(tmp_vol);
    mn = min(vol(:));
    mx = max(vol(:));
    sc_vol = -pi + (vol - mn) * 2 * pi / (mx - mn);
    out_img = struct('fname', spm_file(tmp_vol.fname,'prefix','sc'),...
        'dim',tmp_vol.dim(1:3),'dt',[4 spm_platform('bigend')],...
        'mat',tmp_vol.mat,'descrip','Scaled phase');
    spm_write_vol(out_img,sc_vol);

    % Define phase and magnitude images
    mag_dir = fullfile(exp_dir,sub,session,sprintf('fieldmap_runs%s_%s', int2str(run_start), int2str(run_end)));
    fm_imgs = char(spm_select('FPList',fmap_dir,sprintf('^sc.*fieldmap_runs%s_%s_01.nii', int2str(run_start), int2str(run_end))),...
        spm_select('FPList',mag_dir,sprintf('fieldmap_runs%s_%s.nii', int2str(run_start), int2str(run_end))));


    % Create VDM
    reg_dir = fullfile(epi_dir,sprintf('RER_Run%d',run_start));
    % if this is session Post:

    switch session
        case 'Post'
        reg_dir = strrep(reg_dir, 'Post', 'Pre'); %find the Pre file if this is a post
        epi_img_for_registration = cellstr(spm_select('ExtFPList',reg_dir,sprintf('^urRER_Run%d.nii',run_start),1));
        case 'Pre'

        epi_img_for_registration = cellstr(spm_select('ExtFPList',reg_dir,sprintf('^rRER_Run%d.nii',run_start),1));
    end

    [tmp_VDM,tmp_IP] = FieldMap_create(fm_imgs,epi_img_for_registration,pm_defs);
    vdm_file = sprintf('vdm5_scfieldmap_runs%s_%s_01.nii', int2str(run_start), int2str(run_end));

    for n = run_start:run_end;
        fprintf('\n Processing run %d... \n',n);
        tmp_dir = fullfile(epi_dir,sprintf('RER_Run%d',n));
        file_regex = sprintf('^rRER_Run%s.nii', num2str(n));
        epi_img = cellstr(spm_select('ExtFPList',tmp_dir,file_regex, 1:241));
        job.data.scans = epi_img;
        job.data.vdmfile = cellstr(spm_select('FPList',fmap_dir,vdm_file));
        FieldMap_applyvdm(job);
        fprintf('\n Run %d EPI unwarping complete. \n',n);
    end;

end;

fprintf('\n EPI unwarping complete for subject %s\n',sub);
