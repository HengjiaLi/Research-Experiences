
#mkdir opencv_install
cd opencv_install
#git clone https://github.com/opencv/opencv.git
#git clone https://github.com/opencv/opencv_contrib.git
#cd opencv; git checkout 3.4.1
#cd ../opencv_contrib; git checkout 3.4.1
#cd .. # in opencv_install


CONDA_ENV_PATH=$HOME/Softwares/anaconda3/envs
CONDA_ENV_NAME=opencv3
WHERE_OPENCV=../opencv
WHERE_OPENCV_CONTRIB=../opencv_contrib

#mkdir build # in opencv_install
#cd build
#
#sudo cmake -D CMAKE_BUILD_TYPE=RELEASE \
#	-D CMAKE_INSTALL_PREFIX=/usr/local/opencv3 \
#	-D PYTHON3_EXECUTABLE=$CONDA_ENV_PATH/$CONDA_ENV_NAME/bin/python \
#	-D INSTALL_C_EXAMPLES=ON \
#	-D INSTALL_PYTHON_EXAMPLES=ON \
#	-D OPENCV_EXTRA_MODULES_PATH=$WHERE_OPENCV_CONTRIB/modules \
#	-D BUILD_EXAMPLES=ON $WHERE_OPENCV
#
#sudo make -j4
#sudo make install
#sudo ldconfig

ln -s /usr/local/opencv3/lib/python3.6/site-packages/cv2.cpython-36m-x86_64-linux-gnu.so $CONDA_ENV_PATH/$CONDA_ENV_NAME/lib/python3.6/site-packages/cv2.so
