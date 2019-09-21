%% Description
% This function implements Image Stacking Algorithms (Finalised version). 

% we fist register all the images into the same perspective as the
% reference image.
% we compute the local saliency/sharpness of each registered image and then
% use a weighted-sum algorithm to blend all the image

% Inputs: Target Images; transformation matrix from calibrition; target images.
% Outpus: Stacked Image(EDOF image)

% for any question, please contact: u5629478@anu.edu.au or
% hengjiali0625@gmail.com

clc;
clear all;
close all;
%% load Target Images

Path = 'C:\Users\Ben\Desktop\Cannon EOS\2019_01_25\IMG_00';
% the path where the stacked images are stored, need to be changed to local
% directory
nim = 10;%total number of target images
ref_index = nim;% we use the last image of the stack as a reference image

IMG = cell(1,nim);% a cell variable to store all raw images
IMG_cropped = cell(1,nim);% a cell variable to store all cropped images
IMGBW = cell(1,nim);% a cell variable to store all binary images
for i = 1:nim
    IMG_cropped{i} = imresize(imread(strcat(Path,num2str(30+i),'.JPG')),0.5);
    % load and resize input images
    disp(strcat('Loading completed. Image No.',num2str(i)));
end
a1=IMG_cropped{4};
a2=IMG_cropped{8};
%% Crop Area of Interest
% crop the target region of the images (optional)

% load('Crop Region.mat');%Reference coordinates for cropping
% for i = 1:nim
%     disp(strcat('Cropping Image No.',num2str(i)));
%     IMG_cropped{i} = imcrop(IMG{i},region_of_interest);
% end
clearvars IMG
%% Load H Matrix & register Images
% this section load the transformation matrix (from calibration) and
% register the target input images
load('tforms.mat');
for i = 1:nim
    tform = Tform{i};
    IMG_cropped{i}=imwarp(IMG_cropped{i},tform,'OutputView',imref2d(size(IMG_cropped{ref_index})));
    disp(strcat('Warping Image No.',num2str(i)));
end
%% Build Laplace and Gauss Filters
% we build a LOG filter to detect the saliency and sharpeness of input
% images. the parameters of the filter can be tuned for different
% brightness.
filter_size = 15;
Laplace = ones(filter_size,filter_size);
Gauss = ones(filter_size,filter_size);

mid = ceil(filter_size/2);
CC = 2;% standard-deviation of the Gaussian filter
for i = 1:filter_size
    for j = 1:filter_size
        x = i - mid;
        y = j - mid;
        Laplace(i,j) = (-1/pi/CC/CC/CC/CC)*(1-(x^2+y^2)/2/CC/CC)*exp(-(x^2+y^2)/2/CC/CC);
        Gauss(i,j) = exp(-(((x^2)/2/CC/CC+(y^2)/2/CC/CC)));
    end
end
%% Edge Detection or Sharpness Detection

for i = 1:nim
    Temp = conv2(double(IMG_cropped{i}(:,:,1))+double(IMG_cropped{i}(:,:,2))+double(IMG_cropped{i}(:,:,3)),Gauss,'same');
    IMGBW{i} = conv2(Temp,Laplace,'same');% convolve the image with the filter
    B = size(IMGBW{i});
    IMGBW{i} = abs(IMGBW{i});
    
    % we add a dilation process to enhance the effect of the
    % saliency/sharpness detection
    
    dilateballsize = 11; 
    % Dilattion size, can be fine-tuned to obtained different effect. 
    if (dilateballsize > 0)
        MidBall = ceil(dilateballsize/2);
        se = strel('ball',dilateballsize,dilateballsize);
        IMGBW{i} = imdilate(IMGBW{i},se,'same');
        Dims = size(IMGBW{i});
    end
    %IMGBW{i}=imgaussfilt(IMGBW{i},11,'FilterSize',11);
    disp(strcat('Edge Detection Completed. Image No.',num2str(i)));

end
b1 = uint8(IMGBW{4});
b2 = uint8(IMGBW{8});
clearvars Temp
%% Create Image Stacks (Convert cell variabls to matrices)
% convert all the cell variables into arrays. meanwhile, the RGB images are
% splitted into R,G,B channels.

IMGRGB_stack = cell(1,3);
IMGBW_stack = [];
for i =1:nim
    IMGRGB_stack{1}(:,:,i) = IMG_cropped{i}(:,:,1);%R channel
    IMGRGB_stack{2}(:,:,i) = IMG_cropped{i}(:,:,2);%G channel
    IMGRGB_stack{3}(:,:,i) = IMG_cropped{i}(:,:,3);%B channel
    IMG_cropped{i} = [];
    IMGBW_stack(:,:,i) = IMGBW{i};%Edge images
    IMGBW{i}=[];%clear variable
    disp(strcat('RGB Seperation Completed. Image No.',num2str(i)));
end
clearvars IMGBW IMG_cropped
%% Stacking Images by Weighted Sum Method
% blend all registered images by a weighted sum algorithm.

stack_image = cell(1);% we store the blending result in a cell variable
stack_BW  =cell(1);% we store the B&W version of the blending result in another cell variable


p = 5;% 3 - 8
IMGBW_stack = (IMGBW_stack).^p;
mins = min(min(IMGBW_stack(:,:,:)));
% we compute a weight matrix for the weighted-sum algoirhtm.
weight = (IMGBW_stack(:,:,:)- mins)./sum(IMGBW_stack(:,:,:)-mins,3);
% the three chanels (RGB) are blended seperately, to reduce computational
% cost.
stack_image{1}(:,:,1) = sum(bsxfun(@times,double(IMGRGB_stack{1}(:,:,:)),weight),3);
stack_image{1}(:,:,2) = sum(bsxfun(@times,double(IMGRGB_stack{2}(:,:,:)),weight),3);
stack_image{1}(:,:,3) = sum(bsxfun(@times,double(IMGRGB_stack{3}(:,:,:)),weight),3);

disp(strcat('Stacking Completed !!!'));

%% Plot Result
% a = IMGRGB_stack{1};
% for i =1:nim
%     imshow(a(:,:,i))
%     pause(0.5)
% end
figure;
imshow(uint8(stack_image{1}))
title('Image Stacking Output Figure')
% d = uint8(stack_image{1});
% 
% figure;
% set(gcf,'color','white')
% subplot(2,2,1);
% imshow(a1)
% title('(A) Raw Image A')
% subplot(2,2,2);
% imshow(b1)
% title('(B) Local Sharpness A')
% subplot(2,2,3);
% imshow(a2)
% title('(C) Raw Image B')
% subplot(2,2,4);
% imshow(b2)
% title('(D) Local Sharpness B')
% 
% figure;
% set(gcf,'color','white')
% subplot(1,2,1);
% imshow(c)
% title('Stacked Sharpness')
% subplot(1,2,2);
% imshow(d)
% title('Stacked Image')