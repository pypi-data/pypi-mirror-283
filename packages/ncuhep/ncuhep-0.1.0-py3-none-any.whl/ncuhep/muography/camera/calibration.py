import numpy as np
import cv2
import glob
import pickle


def calibrate(image_path, checkerboard_dim, save_path, visualize):
    objp = np.zeros((checkerboard_dim[0]*checkerboard_dim[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:checkerboard_dim[0],0:checkerboard_dim[1]].T.reshape(-1,2)
    
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.
    
    images = glob.glob(image_path)
    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        print(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, checkerboard_dim, None)
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
            if visualize:
                cv2.drawChessboardCorners(img, checkerboard_dim, corners, ret)
                cv2.imshow('img', img)
                cv2.waitKey(500)
    cv2.destroyAllWindows()
    
    img = cv2.imread(images[0])
    img_size = (img.shape[1], img.shape[0])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

    if save_path:
        with open(save_path, 'wb') as f:
            pickle.dump([mtx, dist], f)
    else:
        with open('camera_calibration.p', 'wb') as f:
            pickle.dump([mtx, dist], f)
            
    return mtx, dist
