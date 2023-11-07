The basic principle of binocular vision is to simulate the human eye and use spatial geometric models to derive corresponding algorithms to solve practical problems. To put it more bluntly, the fundamental purpose of binocular vision is to extract the "points", "lines", and "surfaces" that interest us from the complex objective world, and then describe them with numbers to accurately understand and control them. This principle consists of three parts:

Firstly, extract interest points (feature detection). It is the segmentation of objects of interest to us. The characteristic of this application in feature point extraction is that it requires fewer feature points to be extracted and requires a higher extraction speed.

In this process, we must first extract the information of the object. People easily believe that we can install a camera to take photos of objects in front of us. However, if we use a camera, we can only obtain the plane information of the obstacle, namely the X and Y coordinate information. So we need to add another camera to capture this object from another angle. In this way, we can obtain two images that depict objects from different angles. Then, appropriate preprocessing algorithms (image processing) are added, such as binarization, edge extraction, feature point denoising (appropriate algorithms need to be selected based on specific scenes), to extract and segment the objects in the two images. This completes the extraction of feature points and lays the foundation for the next step of "precise numerical description".

Secondly, accurate numerical description (stereo matching, attitude measurement). This section refers to the need to use effective values to describe the feature points of the segmented obstacle. Of course, in a binocular vision system, it is described using three-dimensional coordinates. If both monocular camera calibration and binocular camera calibration are performed while installing a binocular camera, confirm the parameter matrices of the dual camera and lens, and obtain the translation vector and rotation matrix. Then, based on the principle of binocular stereo matching, the three-dimensional coordinate values of the obstacle can be obtained.

Combine the "stereo matching" algorithm with dual target determination. This algorithm calculates the basic matrix based on the coordinate points of feature points in the left and right images, and the coordinate points with the same name are left and right. The "translation vector" and "rotation matrix" used in this process are the parameters given in the next double objective determination.

Thirdly, dual goals. Binary positioning uses the correspondence between the known world coordinate system (calibration board) and the image coordinate system (image processing results on the calibration board) to calculate the parameter information of the binocular camera under the current position relationship. After calibration, three-dimensional information can be obtained when observing the unknown world coordinate system using a binocular system. In fact, before dual target calibration, it is necessary to perform a single camera calibration on each camera to determine its distortion coefficient and camera internal parameter matrix. The purpose of this is to enable the images obtained by the left and right cameras to be corrected to standard images before processing.

Firstly, I downloaded a pair of left and right camera images from the dataset, and in my code, I read these two images and converted them into grayscale images. Then I used three different algorithms to calculate the disparity between left and right images, namely BM algorithm, SGBM algorithm, and SAD algorithm. In the BM algorithm, I changed the window size for depth calculation by changing the blocksize, and printed seven different disparity maps. In the implementation code of the SGBM algorithm, three experiments were conducted by changing the blocksize, and three different depth images were printed.

When using three different algorithms to calculate disparity, the larger the window, the higher the chance that it contains useful texture features to provide good disparity estimation. The more windows contain depth discontinuity, which is caused by multiple objects at different depths causing image edges, where disparity can cause one image to contain occluded pixels in another image, And make the window contain multiple parallax values (in different sub regions). If the window is small, it is likely to contain smooth areas that do not provide meaningful information. When the window is too small, there is more noise in the disparity map; As the window increases, the view becomes smoother, but when the window is too large, the phenomenon of voids in the disparity map increases.

From the comparison in the above figure, it can be seen that when the window value is relatively small, image matching is particularly sensitive, and in some relatively flat and textureless areas, it is still very messy.

When calculating, using a large window is beneficial for solving problems such as texture, aperture, and duplicate textures; The use of small windows is beneficial for solving the problem of foreground enlargement, therefore, in the selection of windows, there is no worrisome window size that can perfectly solve all problems.

When calculating disparity maps, different similarity indicators and parameters will have different impacts on the results:

In the program, when using the BM method, the disparity is calculated by comparing small pixels between the left and right images.

It uses the similarity measure of the sum of square difference and absolute difference to find the best matching block.

The blockSize parameter controls the size of the blocks used for comparison. Smaller block sizes can capture more details but are more sensitive to noise, while larger block sizes can smooth out noise but may lose some details. This can be seen in the result graph of the program.

I tried different block sizes (9, 11, 13, etc.). Different block sizes can affect the details of disparity maps to varying degrees. A smaller block size may provide more details, but it may be more noisy.

In the SGBM algorithm, more complex cost functions are used, taking into account additional parameters such as uniqueness ratio and speckle filtering.

It usually produces a smoother and more accurate disparity map than BM.

In the program, I use parameters such as blockSize, minDisparity, and numDisparities to control the behavior of the SGBM algorithm. Change the block size to and set other parameters.

From the comparison of the result maps, it can be seen that the SGBM method produces more accurate disparity maps and is less sensitive to noise.
SAD measures the absolute pixel difference between the corresponding pixels in the left and right images.

I tried different window sizes (window_size) to define the comparison area.

A larger window size can provide a smoother disparity map, but may lose some details, while a smaller window size can capture more details but may be more noisy.

Parallax is calculated by finding the minimum SAD value for each pixel, which corresponds to the best match.

The calculated disparity map result depends on the selected window size and maximum disparity (max-Disparity).

Different similarity measures (such as SAD and SSD) and parameters (such as block size and window size) can significantly affect the quality and characteristics of disparity maps generated by stereo vision algorithms.

