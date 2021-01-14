import cv2
from mlxtend.image import extract_face_landmarks

landmarks = extract_face_landmarks(cv2.imread('picture-name.png')) # landmarks.shape ----> (68,2)   Representing (x,y) for 68 points circulating the detected face

''' 
################################ Landmarks visualization ###############################
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15, 5))
ax = fig.add_subplot(1, 3, 1)
ax.imshow(img)
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
'''
