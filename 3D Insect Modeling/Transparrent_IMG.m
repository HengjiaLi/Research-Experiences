% Description:
% This script generates transparent PNG image, by adding the masks on the
% images (both obtained from scan) as a trasnparency layer. Please note
% that the output images are PNG format, and thus you may need a SFM
% software that can handle PNG images.

% Before running, please change the variables "fullfilename" (at the bottom
% of the script) and "Path1; Path2".
clc;
clear all;
close all;

mkdir Transparrent_IMG
%% load image
Path1 = 'E:\Cannon Images\2019_06_26\result\';% dir of color image
Path2 = 'E:\Cannon Images\2019_06_27\result\';% dir of mask image

contents1 = dir([Path1 '/*.jpg']);
contents2 = dir([Path2 '/*.jpg']);
num_of_files = numel(contents1);
sort_contents1 = natsortfiles({contents1.name});
% we use this function "natsortfiles()" to sort the contents in each folder
sort_contents2 = natsortfiles({contents2.name});
for i = 1:num_of_files
    
    filepath1 = strcat(Path1,sort_contents1{i});
    filepath2 = strcat(Path2,sort_contents2{i});
    
    IMG_color = im2double(imread(filepath1));
    IMG_mask = im2double(imread(filepath2));
    
    alphachannel = double(all(IMG_mask < 0.6,3));
    % we define a directory for storing the transparrent PNG images
    fullfilename = fullfile('E:\Cannon Images\2019_06_27','Transparrent_IMG',strcat('transparrent Image No.',num2str(i),'.png'));
    imwrite(IMG_color, fullfilename, 'Alpha', alphachannel);

end
    
    



