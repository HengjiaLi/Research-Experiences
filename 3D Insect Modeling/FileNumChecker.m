% Description:
% This function checks the number of images in the folder, and return the
% top n images (n: number of images per stack). The returned
% images will be moved to another folder, named "finished" and thus, this
% fuction can follow a "first-in-first-out scheme"  to constantly deliver
% images for blending.

% input: directory of the image folder; number of images per stack N
% output: the top N imgaes in the target folder

function IMG = FileNumChecker(Path,Num_of_IMG_per_Stack)
    contents = dir([Path '/*.jpg']);
    num_of_files = numel(contents);
    IMG = cell(1,Num_of_IMG_per_Stack);
    if num_of_files < Num_of_IMG_per_Stack
        IMG{1} = 0;
        disp('Not Enough Images for Stacking');
    else
        for i = 1:Num_of_IMG_per_Stack
            
            filepath = strcat(Path,contents(i).name);
            filename = contents(i).name;
            IMG{i} = im2double(imresize(imread(filepath),0.25));
            disp(strcat('loading Image No.',num2str(i)))
            movefile(filename,'finished')
            %delete(filename)
        end
    end
end