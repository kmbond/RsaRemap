
function [h_avg,h_response,h_cue,h_cue_response, dhat] = modMap_rsa(beta_w, n_betas)

%function [p_value, G, H, d, distance, U, frobDist, frobP] = rsa_evalCorrectTrials(y_raw, SPM, plot_flag)
%
% This function returns the cross validated distance between the short seqs in the SPM file.
% Written by P. Beukema 04/21/17
%
% Inputs
% y_raw : raw time series
% SPM = full spm file
% plot_flag : plots distance matrix and CDS matrix
% fold_size =  LVOCC
%
% Outputs
% p_value =  P(H^_<0)
% G = cross validated estimate of G
% H = [Hhat(1), ...Hhat(m)] : average squared distance for each fold.
% d = d^2 = [d_1^2, ..., d^2_m] : all distances across every pairing of m
% distance = (sum(d,3)./size(d,3)) used for searchlight
% U = full model (P voxels by k conditions)



% Generate prewhitened betas from y_raw and SPM.mat

i=0;
for j=[1:n_betas:size(beta_w,1)];
    %First build matrix of U's which is k conditions, by P voxels by M # of U's
    i= i+1;
    %build matrix with normalized pattern.
    nU(:,:,i) = normr(beta_w(j:j+7,:));
end;

num_seqs = combnk(1:size(nU,3),2);
% Find the squared distance between each finger for each permutations
% This generates all distances across each fold
for pair = 1:size(num_seqs,1);
    for seq1 = 1:size(nU,1);
        for seq2 = 1:size(nU,1);
            x = num_seqs(pair,:);
            foldm = (nU(seq1,:,x(1)) - nU(seq2,:,x(1)));
            foldl = (nU(seq1,:,x(2)) - nU(seq2,:,x(2)));
            d(seq1,seq2,pair) = foldm*foldl';
        end
    end
end

%Return H
dhat = sum(d,3)./size(d,3);
K = length(dhat);
dhat(dhat==Inf)=NaN;
h_avg = nansum(dhat(:))/(K*(K-1));
resp_ind = [0 1 1 1 0 0 0 0; 0 0 1 1 0 0 0 0; 0 0 0 1 0 0 0 0; zeros(1,8);zeros(1,8);zeros(1,8);zeros(1,8);zeros(1,8)];
cue_ind = [zeros(1,8);zeros(1,8);zeros(1,8);zeros(1,8);zeros(1,8);0 0 0 0 0 1 1 1; 0 0 0 0 0 0 1 1; 0 0 0 0 0 0 0 1];
resp_cue_ind = [0 0 0 0 1 1 1 1; 0 0 0 0 1 1 1 1; 0 0 0 0 1 1 1 1; 0 0 0 0 1 1 1 1;zeros(1,8);zeros(1,8);zeros(1,8);zeros(1,8)];
h_response = nanmean(dhat(find(resp_ind)));
h_cue = nanmean(dhat(find(cue_ind)));
h_cue_response = nanmean(dhat(find(resp_cue_ind)));
