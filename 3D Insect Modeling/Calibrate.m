%% Description:
% This function implements camera calibriaion based on the input dot partern images.

% A reference image is selected and the corresponding homography is 
% computed to convert all other images into this reference image. To 
% compute homography, we extract all the dot patterns from the images and 
% use their center of circles as target coordinates.

% Inputs: Target dot pattern images
% Outputs: n*3*3 homography matrices, where n is the number of images

clc;clear;clear all;close all;
%% loead image

Path = '2019_01_25\IMG_00';% the path where
% the dot images are stored, you need to change it to the local directory.

nim = 10;%total number of target images
n_dots = 35;%total number of dots
IMG = cell(1,nim);% a cell variable for storing raw images
IMGBW = cell(1,nim);% a cell variable for storing Black&White images
for i = 1:nim
    IMG{i} = imresize(imread(strcat(Path,num2str(20+i),'.JPG')),0.25);%read and resize the dot images
    IMGBW{i} = im2bw(IMG{i},0.3);% convert raw images into B&W
    disp(strcat('Loading completed. Image No.',num2str(i)));
end

ref_index = nim;%the last image in the stack is selected as the reference image
%% Crop target regions (optional)

%[~, region_of_interest] = imcrop(IMG{ref_index}); % select region of interest interactively
%save('Crop Region','region_of_interest');
% for i = 1:nim
%     disp(strcat('Cropping Image No.',num2str(i)));
%     IMGBW{i} = imcrop(IMGBW{i},region_of_interest);
% end
%% Detect dot parttern

circle_centers = cell(1,nim);
circle_radii = cell(1,nim);

for i =1:nim
    [centers, radii, metric] = imfindcircles(IMGBW{i},[10 35],'ObjectPolarity','dark','Sensitivity',0.99);
    % this imfindcircles() function detect dot patterns in the images. Note
    % that the radius of target dots are in the range of [25,70], and this
    % parameter may need to be change w.r.t. different target images.
    circle_centers{i} = centers;
    circle_radii{i} = radii;
    disp(strcat('Dot parttern detction completed. Image No.',num2str(i)));
end

%% Delete repeated detection
% there may be some repeated circles detected (several different circles 
% detected at same dot) and they need to be delected.
circle_center_cleaned = cell(1,nim);
circle_radii_cleaned = cell(1,nim);
for i = 1:nim %number of images
    j = 1;
    k = 1;
    circle_center_cleaned{i}(1,:) = [0 0];
    while k <= n_dots % 35 in our case
        % we compute the euclidean distance between detected circles and we
        % set a threshold of 100 pixels. if the distance between any two
        % circles are smaller than 100 pixels, we will delete the weaker
        % one of the circle pair.
        rep = repmat(circle_centers{i}(j,:),size(circle_center_cleaned{i},1),1);
        dist = sqrt((rep(:,1) - circle_center_cleaned{i}(:,1)).^2+(rep(:,2) - circle_center_cleaned{i}(:,2)).^2);
        if dist > 100                     
            circle_center_cleaned{i}(k,:) = circle_centers{i}(j,:);
            circle_radii_cleaned{i}(k,:) = circle_radii{i}(j,:);
            k = k + 1;
        end
        j = j+1;
    end
%     figure;
%     hold on;
%     imshow(IMGBW{i});
%     viscircles(circle_center_cleaned{i}(1:end,:), circle_radii_cleaned{i}(1:end,:),'Color','b');
%     hold off;
end
%% Order the detected dot points
% in this section, we try to group the detected circles w.r.t. the
% reference image, we compute the ralative distance between the dots and
% hence, we can find the coloset dots and they are grouped together.

circle_center_sorted = cell(1,nim);% a cell variable to store the grouped circles.
circle_radii_sorted = cell(1,nim);

for i = 1:nim
    if i ~= ref_index
        for j = 1:n_dots 
            rep = repmat(circle_center_cleaned{i}(j,:),n_dots,1);
            dist = sqrt((rep(:,1) - circle_center_cleaned{ref_index}(:,1)).^2+(rep(:,2) - circle_center_cleaned{ref_index}(:,2)).^2);
            
            [~,Index_sort] = min(dist);
            circle_center_sorted{i}(Index_sort,:) = circle_center_cleaned{i}(j,:);
            circle_radii_sorted{i}(Index_sort,:) = circle_radii_cleaned{i}(j,:);

        end
    else
            circle_center_sorted{i} = circle_center_cleaned{i};
            circle_radii_sorted{i} = circle_radii_cleaned{i};
    end
    figure;
    hold on;
    imshow(IMGBW{i});
    viscircles(circle_center_sorted{i}(1:end,:), circle_radii_sorted{i}(1:end,:),'Color','b');
    hold off;
end
%% Compute the transformation Homography matrix

Tform = cell(1,nim);
for i = 1:nim
        [tform,inlierPtsDistorted,inlierPtsOriginal] = ...
            estimateGeometricTransform(circle_center_sorted{i},circle_center_sorted{ref_index},...
            'projective','Confidence',99,'MaxNumTrials',1000,'MaxDistance',50);
        % compute the transformation between images, according to the
        % groupd/sorted dot patterns.
        Tform{i} = tform;
        
        figure;
        showMatchedFeatures(IMGBW{ref_index},IMGBW{i},...
        inlierPtsOriginal,inlierPtsDistorted);
        title('Matched inlier points');
end
%% Recover Image and Visual Check
% the images are registered and they are displayed one by one. By a visual
% comparison, all the images should have dot patterns aligned together.
figure;
for i = 1:nim
    outputView = imref2d(size(IMGBW{ref_index}));
    Ir = imwarp(IMGBW{i},Tform{i},'OutputView',outputView);
    imshow(Ir); 
    title('Recovered image');
end

save('tforms','Tform');