import cv2
import pickle


def read_calibration_data(calibration_file=None):
    if calibration_file is None:
        calibration_file = 'camera_calibration.p'
        
    with open(calibration_file, 'rb') as f:
        mtx, dist = pickle.load(f)
    
    return mtx, dist


def undistort(img, mtx, dist):
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    
    return dst


