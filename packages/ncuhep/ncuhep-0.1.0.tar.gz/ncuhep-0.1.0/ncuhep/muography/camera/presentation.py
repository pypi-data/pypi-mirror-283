import numpy as np
import cv2 


def square(img, fov, focal_length, pixel_size):
    h, w = img.shape[:2]
    sensor_size = 2 * np.tan(np.deg2rad(fov)/2) * focal_length
    pixel_density = 1/pixel_size
    pixel = int(sensor_size * pixel_density)
    cv2.rectangle(img, (int(w/2 - pixel/2), int(h/2 - pixel/2)), (int(w/2 + pixel/2), int(h/2 + pixel/2)), (0, 255, 0), 2)  
    
    return img


def divide(img, fov, focal_length, pixel_size, portions):
    h, w = img.shape[:2]
    sensor_size = 2 * np.tan(np.deg2rad(fov)/2) * focal_length
    pixel_density = 1/pixel_size
    pixel = int(sensor_size * pixel_density)
    for i in range(portions):
        for j in range(portions):
            cv2.rectangle(img, (int(w/2 - pixel/2 + i*pixel/portions), int(h/2 - pixel/2 + j*pixel/portions)), (int(w/2 - pixel/2 + (i+1)*pixel/portions), int(h/2 - pixel/2 + (j+1)*pixel/portions)), (0, 255, 0), 2)

    return img

