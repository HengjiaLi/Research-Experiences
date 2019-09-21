%% Description:

% This script applies the function "FileNumChecker.m" on top of the guided
% filtering appraoch of image fusion. Thus, it can constantly detect the
% scaned image and perform image blending along with the scan. The used
% stack images will be stored in the folder "finished" and the blending
% results will be stored in the folder "result".

% Three important parameters need to be defined before running: "Path" (the
% directory that image stackes are stored);"Num_of_IMG_per_stack"(the 
% number of images per stack); and "fullfilename"(at the bottom of the script,
% it indicates a directory to save the blended result). 
%% Load images

clear all;
close all;
clc;

% create two folders to store images
mkdir finished %stores the images processed
mkdir result% srores the result images blended

k = 1;
Path = 'finished\';%the directory of raw source images
Num_of_IMG_per_Stack = 20;
while 1
    %clc
    % read the top N images in the target folder
    IMG = FileNumChecker(Path,Num_of_IMG_per_Stack);
    
    if IMG{1} == 0%if there is no image, wait for 2sec for scanning
        pause(2)
        continue
    else% if there are enough images, start blending
        nim = Num_of_IMG_per_Stack;
        ref_index = 1;

        %% Crop Area of Interest (optional)

        I = zeros([nim,size(IMG{1})]);

        %% Load H Matrix & Warp Images

        load('tforms_for_test.mat');
        for i = 1:nim
            tform = Tform{i};
            I(i,:,:,:)=imwarp(IMG{i},tform,'OutputView',imref2d(size(IMG{ref_index})));
            Ig(i,:,:) = rgb2gray(squeeze(I(i,:,:,:)));
            disp(strcat('Warping Image No.',num2str(i)));
        end
        clearvars IMG IMG_cropped


        %% Choice of parameters
        r1 = 45;
        eps1 = 0.3;
        r2 = 7;
        eps2 = 10^-6;

        %% step A : two-scale image decomposition
        % B1 and B2: blured images
        % D1 and D2: detailed images

        average_filter = 1/(31*31)*ones(31,31);

        B = zeros(size(Ig));
        D = zeros(size(I));
        for i=1:size(I,1)
            B(i,:,:) = conv2(squeeze(Ig(i,:,:)), average_filter, 'same');
            D(i,:,:,:) = squeeze(I(i,:,:,:) - B(i,:,:));
        end

        %% step B weight map construction

        %laplacian_filter = [[0 -1 0]; [-1 4 -1]; [0 -1 0]];
        filter_size = 15;
        laplacian_filter = ones(filter_size,filter_size);
        mid = ceil(filter_size/2);
        CC = 2;
        for i = 1:filter_size
            for j = 1:filter_size
                x = i - mid;
                y = j - mid;
                laplacian_filter(i,j) = (-1/pi/CC/CC/CC/CC)*(1-(x^2+y^2)/2/CC/CC)*exp(-(x^2+y^2)/2/CC/CC);
                
            end
        end
        H = zeros(size(Ig));
        S = zeros(size(Ig));
        for i=1:size(I,1)
            % laplacian filtering
            H(i,:,:) = conv2( squeeze(Ig(i,:,:)), laplacian_filter, 'same');
            % gaussian filtering
            S(i,:,:) = imgaussfilt(abs(squeeze(H(i,:,:))), 'FilterSize', 15);
        end




        % maybe reshape P1 and P2
        P = zeros(size(S));
        for i=1:size(I,1)
            P(i,:,:) = (S(i,:,:) == max(S));
        end

        % r1, eps1, r2 and eps2 are not related to the index of I1, P1, I2, P2, etc
        Wb = zeros(size(P));
        Wd = zeros(size(P));
        s1 = r1/4;
        s2 = r2/4;
        for i=1:size(I,1)
            Wb(i,:,:) = fastguidedfilter(squeeze(Ig(i,:,:)), squeeze(P(i,:,:)), r1, eps1,s1);
            Wd(i,:,:) = fastguidedfilter(squeeze(Ig(i,:,:)), squeeze(P(i,:,:)), r2, eps2,s2);
        end

        % normalizing weights
        Sumb = sum(Wb,1);
        Sumd = sum(Wd,1);
        Wb = Wb./Sumb;
        Wd = Wd./Sumd;


        %% step C: two-scale image reconstruction

        Bb = zeros(size(squeeze(I(1,:,:,:))));
        Db = zeros(size(squeeze(I(1,:,:,:))));
        for i=1:size(I,1)
            Bb = Bb + repmat(squeeze(Wb(i,:,:)), [1 1 3]) .* squeeze(B(i,:,:,:)); 
            Db = Db + repmat(squeeze(Wd(i,:,:)), [1 1 3]) .* squeeze(D(i,:,:,:)); 
        end

        F = Bb + Db;
        fullfilename = fullfile('E:\Cannon Images\2019_06_27','result',strcat('Stacked Image No.',num2str(k),'.JPG'));
        
        imwrite(F,fullfilename)
        disp(strcat('Stacking Completed Image No.',num2str(k)));
        k = k+1;
    end
end