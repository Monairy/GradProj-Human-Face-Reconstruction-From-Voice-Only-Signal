
import tensorflow_addons as tfa
import cv2
from mlxtend.image import extract_face_landmarks
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image 
from image_align import align_image
def image_warping(src_img, src_landmarks, dest_landmarks):
	src_landmarks[:,[0,1]] = src_landmarks[:,[1,0]]
	dest_landmarks[:,[0,1]] = dest_landmarks[:,[1,0]]
	expanded_src_landmarks = np.expand_dims(np.float32(src_landmarks), axis=0)
	expanded_dest_landmarks = np.expand_dims(np.float32(dest_landmarks), axis=0)
	expanded_src_img = np.expand_dims(np.float32(src_img), axis=0)

	warped_img, dense_flows = tfa.image.sparse_image_warp(expanded_src_img,
						  expanded_src_landmarks,
						  expanded_dest_landmarks,
						  interpolation_order=1,
						  regularization_weight=0.1,
						  num_boundary_points=4,
						  name='sparse_image_warp')
   
	return (warped_img[0]).numpy().astype(np.uint8)

def showLandmarks(orig_img,img,landmarks):
	fig = plt.figure(figsize=(15, 5))
	ax = fig.add_subplot(1, 3, 1)
	ax.imshow(orig_img)
	ax = fig.add_subplot(1, 3, 2)
	ax.scatter(landmarks[:, 0], -landmarks[:, 1], alpha=0.8)
	ax = fig.add_subplot(1, 3, 3)
	img2 = img.copy()
	for p in landmarks:
		img2[p[1]-3:p[1]+3, p[0]-3:p[0]+3, :] = (255, 255, 255)
	# note that the values -3 and +3 will make the landmarks
	# overlayed on the image 6 pixels wide; depending on the
	# resolution of the face image, you may want to change
	# this value
	ax.imshow(img2)
	plt.show()

img1= cv2.imread('3ameed.png')
img2= cv2.imread('texture.png')

img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
landmark1 = extract_face_landmarks(img1)
landmark2 = extract_face_landmarks(img2)

align_image('3ameed.png','a_t1.png', landmark1, output_size=224)
align_image('texture.png','a_test.png', landmark2, output_size=224)

img1= cv2.imread('a_t1.png')
img2= cv2.imread('a_test.png')
img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)

warped_img = image_warping(img1,extract_face_landmarks(img1),extract_face_landmarks(img2))
showLandmarks(img1,warped_img,landmark1)

