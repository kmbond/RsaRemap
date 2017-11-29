function groovy_reslice(glob_ps, sub_ps)

% Get defaults
wdefs = glob_ps.reslice_opts.write;

% Flags to pass to routine to create resliced images
% (spm_reslice)
resFlags = struct(...
    'interp', wdefs.interp,...    % trilinear interpolation
    'wrap', wdefs.wrap,...        % wrapping info (ignore...)
    'mask', wdefs.mask,...        % masking (see spm_reslice)
    'which',wdefs.which, ...      % whether to write reslice time series
    'prefix',wdefs.prefix, ...    % Prefix to use for output
    'mean',1);           % do write mean image

clear imgs; 

% get the subdirectories in the main directory

for sb = 1:length(sub_ps) % for each subject
  this_sub = sub_ps(sb);
  imgs(1) = {glob_ps.reslice_target};
  r_filter = ['^' glob_ps.reslice_prefix this_sub.raw_filter '$'];

  for ss = 1:length(this_sub.sesses) % and session 
    dirn = fullfile(glob_ps.fdata_root, ...
		    this_sub.dir, this_sub.sesses(ss).dir);
    [P Pdir] = spm_select('List', dirn, r_filter);
    imgs(ss+1) = {[repmat([dirn filesep],size(P,1),1) P]};
    
    % For 4dnii files
    switch glob_ps.epi_format
        case '4dnii'
         vol = spm_vol(fullfile(dirn,P));

         try isfield(vol(1),'name');
             filename = vol(1).name;
         catch
             filename = vol(1).fname;
         end;

         for b = 1:length(vol);
             file_list{b}=fullfile(dirn,sprintf('%s, %d',filename,b));
         end;
         
         img(ss) = {strvcat(file_list)};
    end;

  end

  % Run the reslicing
  spm_reslice(imgs, resFlags);
end











