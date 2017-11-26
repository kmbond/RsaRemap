function mm_convert_dcms(sub, sess)
    cd(sprintf('/data/modMap/subjects/%s/%s', sub, sess));
    dcms = ls;
    out_path = pwd;
    files = dir('17*');
    for file_n = 1:length(files);
      out_path = pwd;
      coax_dicom_convert('4dnii',files(file_n).name,out_path);
    end
    %delete TrufiSag dir

    [status, message, messageid] = rmdir('TrufiSag', 's');
    
    %delete localizer dir
     [status, message, messageid] = rmdir('localizer', 's');
end
