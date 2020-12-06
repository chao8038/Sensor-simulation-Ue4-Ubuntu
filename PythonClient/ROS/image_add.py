import cv2
import numpy as np

# img1=cv2.imread(r'D:\CodeFile\PythonWorkspace\Sensor-simulation-Ue4-Ubuntu\output\test3\test34.png')
# img2=cv2.imread(r"C:\Users\chaoyu\Downloads\2020-11-26-21-09-45\img\frame34.jpg")
 
# res = cv2.add(img2,img1)

# gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# gray_three_channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

test = np.ones((720, 1280, 3), dtype='float32')
# test[:,:,2] = 1
# print(test)

# img = np.zeros([720,1280,3])

# img[:,:,0] = np.ones([720,1280])*64/255.0
# img[:,:,1] = np.ones([720,1280])*128/255.0
# img[:,:,2] = np.ones([720,1280])*192/255.0

# cv2.imwrite('color_img.jpg', img)
# cv2.imshow("image", img)
# cv2.waitKey()

cv2.imshow("Image", test)
cv2.waitKey(0)
cv2.destroyAllWindows()