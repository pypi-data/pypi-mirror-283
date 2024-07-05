import cv2


def save(image, path):
    cv2.imwrite(path, image)
    
    
def read(path):
    return cv2.imread(path)


def show(image, title='Image'):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    