import cv2

class VideoCamera(object):
    def __init__(self):
        # Attempt to capture from device 0 (default webcam)
        self.video = cv2.VideoCapture(0)
        
        # Check if the video source is opened successfully
        if not self.video.isOpened():
            raise Exception("Could not open video source")
    
    def __del__(self):
        # Release the video when the object is destroyed
        if self.video.isOpened():
            self.video.release()
    
    def get_frame(self):
        # Read a frame from the video stream
        success, image = self.video.read()
        
        # If frame reading failed or frame is None
        if not success or image is None:
            raise Exception("Failed to capture image from video stream")
        
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the video stream.
        # ret, jpeg = cv2.imencode('.jpg', image)
        
        return image
