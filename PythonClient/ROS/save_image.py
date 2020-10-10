import numpy as np
import airsim
import os
import cv2

def main():

    client = airsim.CarClient()
    client.confirmConnection()
    filename = '/home/aiotlab/Documents/Unreal-data/image/test'
    count = 0
    while(True):
        count += 1
        responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        response = responses[0]
        
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

        img_rgb = img1d.reshape(response.height, response.width, 3)

        image_rgb = np.flipud(img_rgb)

        # airsim.write_png(os.path.normpath(filename+ str(count) + '.png'), img_rgb)
        cv2.imshow('img', image_rgb)
        key=cv2.waitKey(1)
        if key==ord('q'):
            break

if __name__ == "__main__":
    main()