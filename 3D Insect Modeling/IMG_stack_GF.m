%% Description:

% This Script implements the Guided Filter approach to solve image stacking
% problems. for more details about the guided filter, please refer to the
% published paper: "Li, Shutao & Kang, Xudong & Hu, Jianwen. (2013). Image 
% Fusion With Guided Filtering. IEEE transactions on image processing : a 
% publication of the IEEE Signal Processing Society. 22.
% 10.1109/TIP.2013.2244222"

% input: transformation/homography matrix and input images
% output: stacked image



%% Load images
clear all;
close all;
clc;
tic

Path = '2019_01_25\IMG_00';% path of stored images, this should be changed for
% different local directory
nim = 10;% total number of images

IMG_cropped = cell(1,nim);% a cell varaible to store images
IMGBW = cell(1,nim);% a cell varaible to BW images
ref_index = nim;% we define the last image in the stack as the reference

for i = 1:nim
    % load and resize image
    IMG_cropped{i} = imresize(imread(strcat(Path,num2str(30+i),'.JPG')),0.25);
    disp(strcat('Loading completed. Image No.',num2str(i)));
end

%% Load H matrix and warp stack images
load('tforms.mat');
for i = 1:nim
    tform = Tform{i};
    %warp images to the same perspective as the reference image
    IMG_cropped{i}=imwarp(IMG_cropped{i},tform,'OutputView',imref2d(size(IMG_cropped{ref_index})));
    disp(strcat('Warping Image No.',num2str(i)));
end

for i = 1:nim
    % create grayscale images
    I(i,:,:,:) =  im2double(imresize(IMG_cropped{i},1));
    Ig(i,:,:) = rgb2gray(squeeze(I(i,:,:,:)));
end

% figure(1);
% imshow(squeeze(I(1,:,:,:)));
% 
% figure(2);
% imshow(squeeze(I(2,:,:,:)));
% 
% figure(21);
% imshow(squeeze(I(3,:,:,:)));

%% Choice of parameters of GF filter
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
% build LoG filter for sharpness/saliency measurement.the parameters of the
% filter should be adjusted for different brightness
filter_size = 15;
Laplace = ones(filter_size,filter_size);
mid = ceil(filter_size/2);
CC = 2;
for i = 1:filter_size
    for j = 1:filter_size
        x = i - mid;
        y = j - mid;
        Laplace(i,j) = (-1/pi/CC/CC/CC/CC)*(1-(x^2+y^2)/2/CC/CC)*exp(-(x^2+y^2)/2/CC/CC);
        %Gauss(i,j) = exp(-(((x^2)/2/CC/CC+(y^2)/2/CC/CC)));
    end
end
H = zeros(size(Ig));
S = zeros(size(Ig));
for i=1:size(I,1)
    % laplacian filtering
    H(i,:,:) = conv2(squeeze(Ig(i,:,:)), Laplace, 'same');
    % gaussian filtering
    S(i,:,:) = imgaussfilt(abs(squeeze(H(i,:,:))), 'FilterSize', 15)*10;
    disp(strcat('Edge Detection Completed. Image No.',num2str(i)));
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
    
    Bb = Bb + bsxfun(@times,repmat(squeeze(Wb(i,:,:)), [1 1 3]),squeeze(B(i,:,:,:)));
    Db = Db + bsxfun(@times,repmat(squeeze(Wd(i,:,:)), [1 1 3]),squeeze(D(i,:,:,:))); 
    disp(strcat('Fusion Completed. Image No.',num2str(i)));
%     figure;
%     imshow(Bb)
%     fn = strcat('GF_result_Base',num2str(i),'.jpg');
%     imwrite(Bb,fn)
    % imshow(Db)
%     fn = strcat('GF_result_Detail',num2str(i),'.jpg');
%     imwrite(Db*3,fn)
end

F = Bb + Db;
figure;
imshow(F);
%% plots
% 
% I1 = squeeze(I(5,:,:,:));
% I2 = squeeze(I(8,:,:,:));
% S1 = squeeze(S(5,:,:));
% S2 = squeeze(S(8,:,:));
% P1 = squeeze(P(5,:,:));
% P2 = squeeze(P(8,:,:));
% wb1 = squeeze(Wb(5,:,:));
% wb2 = squeeze(Wb(8,:,:));
% wd1 = squeeze(Wd(5,:,:));
% wd2 = squeeze(Wd(8,:,:));
% 
% figure;set(gcf,'color','white');
% subplot(5,2,1)
% imshow(I1)
% title('Source Image I1')
% 
% subplot(5,2,2)
% imshow(I2)
% title('Source Image I2')
% 
% subplot(5,2,3)
% imshow(S1*10)
% title('Saliency Image S1')
% 
% subplot(5,2,4)
% imshow(S2*10)
% title('Saliency Image S2')
% 
% subplot(5,2,5)
% imshow(P1)
% title('Weight Map P1')
% 
% subplot(5,2,6)
% imshow(P2)
% title('Weight Map P2')
% 
% subplot(5,2,7)
% imshow(wb1)
% title('Guided weight map Wb1')
% 
% subplot(5,2,8)
% imshow(wb2)
% title('Guided weight map Wb2')
% 
% subplot(5,2,9)
% imshow(wd1)
% title('Guided weight map Wd1')
% 
% subplot(5,2,10)
% imshow(wd2)
% title('Guided weight map Wd2')
% 
% 
% 

