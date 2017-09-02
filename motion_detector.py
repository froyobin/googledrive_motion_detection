# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import os
import thread
from myGdrive.googledrive import MyGDrive


PREFIX_NAME = "MOTION_"
PIC_MAX = 500
class MMotivation:
    def __init__(self, args):
        # if  video argument is None, then we are reading from webcam
        if args.get("video", None) is None:
            self.camera = cv2.VideoCapture(0)
            time.sleep(0.25)
        # otherwise, we are reading from a video file
        else:
            self.camera = cv2.VideoCapture(args["video"])

        # initialize the first frame in the video stream
        self.firstFrame = None
        self.counter = 0
    def close_camera(self):
        # cleanup the camera and close any open windows
        self.camera.release()
        cv2.destroyAllWindows()

    def sensoring_loop(self):

        #loop over the frames of the video

        while True:
            time.sleep(0.5)
            # grab the current frame and initialize the occupied/unoccupied
            # text
            (grabbed, frame) = self.camera.read()
            text = "Unoccupied"

            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if not grabbed:
                break

            # resize the frame, convert it to grayscale, and blur it
            # frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if self.firstFrame is None:
                time.sleep(5)
                # frame = imutils.resize(frame, width=500)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                self.firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(self.firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < args["min_area"]:
                    continue

                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"

            # draw the text and timestamp on the frame
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame,
                        datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35,
                        (0, 0, 255), 1)

            # show the frame and record if the user presses a key
            cv2.imshow("Security Feed", frame)
            # cv2.imshow("Thresh", thresh)
            # cv2.imshow("Frame Delta", frameDelta)
            key = cv2.waitKey(1) & 0xFF
            if text == "Occupied":
                if self.counter == PIC_MAX:
                    self.counter = 0
                name = PREFIX_NAME + str(self.counter)
                path = "./tmp/"+name+".png"
                cv2.imwrite(path, frame)
                self.counter += 1
                self.firstFrame = gray
                time.sleep(0.3)
            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                break

def delete_file(this_driver, file_id):


    while True:
        files = os.listdir("./tmp")
        for each in files[:-1]:
            print "upload " + each
            PREFIX = "./tmp/"
            path = PREFIX + each
            this_drive.upload_file(file_id, each, path)
            os.remove(path)
        print "finish this round"
        time.sleep(5)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500,
                    help="minimum area size")
    args = vars(ap.parse_args())

    this_drive = MyGDrive()
    file_id = this_drive.get_file_id('video_camera')


    thread.start_new_thread(delete_file, (this_drive, file_id))
    this_monitor = MMotivation(args)
    this_monitor.sensoring_loop()
    thread.start_new_thread(delete_file, ("Thread-1", 2, ))

    this_monitor.close_camera()
