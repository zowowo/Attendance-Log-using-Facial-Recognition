
from imutils.video import VideoStream
from tkinter import filedialog
from imutils import paths
import face_recognition
import numpy as np
import imutils
import shutil
import pickle
import time
import cv2
import os

class NewStudent:
    def __init__(self, first_name, last_name):
        self.first_name = first_name.upper()
        self.last_name = last_name.upper()
        self.folder_path = f"dataset/{last_name}_{first_name}" 
        self.pickle_path = "misc_files/encodings.pickle"
        self.protoxt_path = "misc_files/deploy.prototxt.txt"
        self.caffemodel_path = "misc_files/res10_300x300_ssd_iter_140000.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(self.protoxt_path, self.caffemodel_path)
        
    def get_net(self):
        return cv2.dnn.readNetFromCaffe(self.protoxt_path, self.caffemodel_path)
    
    def capture_video(self):
        return VideoStream(src=0).start()
    
    def convert_frame_to_blob(self, frame):
        return cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
            
    def save_face_images(self):
        num_images = 30
        # load our serialized model from disk
        print("Loading the model...")
        net = self.get_net()

        # initialize the video stream and allow the cammera sensor to warmup
        print("Starting the video stream...")
        vs = self.capture_video()
        
        time.sleep(2.0)
        snapshot_counter = 0
        
        # loop over the frames from the video stream
        while snapshot_counter < num_images:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            # grab the frame dimensions and convert it to a blob
            (h, w) = frame.shape[:2]
            blob = self.convert_frame_to_blob(frame)

            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is 
                # greater than the minimum confidence
                if confidence < 0.90:
                    continue

                # compute the (x, y)-coordinates of the bounding box for the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the bounding box of the face along with the associated probability
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

                reminder_text = "Slowly rotate your face in a clockwise motion"
                cv2.putText(frame, reminder_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
                # Display the frame only if the confidence is above the threshold
                if confidence >= 0.90 and snapshot_counter < num_images:
                    face_roi = frame[startY:endY, startX:endX]
                    
                    timestamp = int(time.time() * 1000)  # current timestamp in milliseconds
                    filename = os.path.join(self.folder_path, f"snapshot_{timestamp}{snapshot_counter}.jpg")

                    cv2.imwrite(filename, face_roi)
                    snapshot_counter += 1

                    # Half a second of delay in between snapshots
                    time.sleep(0.50)

                    # Or save the snapshot if the 's' key is pressed
                    '''if key == ord("s"):
                        snapshot_name = os.path.join(output_folder, f"snapshot_{time.time()}.jpg")
                        cv2.imwrite(snapshot_name, frame)'''
                    
                if snapshot_counter >= num_images:
                    break

            # show the output frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        
    def get_uploaded_images_names(self):
        return filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    
    def upload_images(self):
        # Prompt the user to select multiple image files
        file_paths = self.get_uploaded_images_names()
        destination_folder = self.folder_path  

        # Process the selected files
        for file_path in file_paths:
            # Get the file name from the file path
            file_name = file_path.split("/")[-1]

            # Create the destination path by joining the destination folder and the file name
            destination_path = f"{destination_folder}/{file_name}"

            # Copy the file to the destination folder
            shutil.copy(file_path, destination_path)
            print("Image saved:", destination_path)
        
    def get_file_extension(self):
        file_name, file_extension = os.path.splitext(self.folder_path)
        return file_extension
    
    def read_image(self, filename):
        return cv2.imread(os.path.join(self.folder_path, filename))
    
    def img_crop_face(self):
        # Gets the list of files in the folder
        file_list = os.listdir(self.folder_path)
        
        if len(file_list) == 0:
            return ""
        
        # iterate through each file in the folder
        for filename in os.listdir(self.folder_path):
            # check if the file is an image
            if not filename.endswith((".jpg", ".jpeg", ".png", ".PNG")):
                continue
            
            # get the file extension for later 
            file_extension = self.get_file_extension()

            # read the image
            image = self.read_image(filename)
            (h, w) = image.shape[:2]
            blob = self.convert_frame_to_blob(image)

            # pass the binary large object through the network and obtain the detections and predictions
            print("Processing image:", filename)
            self.net.setInput(blob)
            detections = self.net.forward()

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
                if confidence <= 0.89:
                    continue

                # compute the (x, y)-coordinates of the bounding box for the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the bounding box of the face along with the associated probability
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

                face_roi = image[startY:endY, startX:endX]
                cv2.imwrite(f"{self.folder_path}/{filename}{file_extension}", face_roi)

            cv2.imshow("Output", image)
            cv2.waitKey(0)

        cv2.destroyAllWindows()
        return "Successfully cropped all images."
 
    def process_pickle_file(self, pickle_path):
        if os.path.exists(pickle_path):
            try:
                with open(pickle_path, "rb") as f:
                    existing_data = pickle.load(f)

                knownEncodings = existing_data.get("encodings", [])
                knownNames = existing_data.get("names", [])

                # Check if both lists are empty
                if not knownEncodings and not knownNames:
                    print("Pickle file is empty. Skipping further processing.")
                    return

            except EOFError:
                print("Error: The pickle file is empty or corrupt. Skipping further processing.")
                return
        else:
            print(f"Pickle file '{pickle_path}' does not exist. Creating an empty pickle file.")
            
            # Create an empty pickle file
            empty_data = {"encodings": [], "names": []}
            with open(pickle_path, "wb") as f:
                pickle.dump(empty_data, f)

            # Initialize empty lists
            knownEncodings = []
            knownNames = []
        return (knownEncodings, knownNames)        
    
    def encode_new_images(self):
        file_list = os.listdir(self.folder_path)
        
        if len(file_list) == 0:
            return ""
        
        # set the path to the input images in our dataset
        print("quantifying faces from dataset path...")
        imagePaths = list(paths.list_images("dataset"))
        processedFolders_path = "misc_files/processed_folders.txt"

        # load the existing processed folders from the text file to skip them during the encoding process
        processedFolders = set()
        if os.path.exists(processedFolders_path):
            with open(processedFolders_path, "r") as f:
                processedFolders = set(f.read().splitlines())

        if os.path.exists(self.pickle_path):
            with open(self.pickle_path, "rb") as f:
                existing_data = pickle.load(f)
            knownEncodings = existing_data["encodings"]
            knownNames = existing_data["names"]
        else:
            # initialize the list of known encodings and known names
            knownEncodings = []
            knownNames = []

        processedNames = set(knownNames)

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            name = imagePath.split(os.path.sep)[-2]

            # extract the person name from the image path
            print(f"\nCurrently processing: {name}\n")
            print("processing image {}/{}".format(i + 1, len(imagePaths)))

            # Skip the image if it has already been processed
            if name in processedFolders:
                continue

            # load the input image and convert it from RGB (OpenCV ordering) to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model="cnn")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and encodings
                knownEncodings.append(encoding)
                knownNames.append(name)

            processedFolders.add(name)

        # dump or save the facial encodings + names to disk
        print("serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        with open(self.pickle_path, "wb") as f:
            pickle.dump(data, f)

        # save the updated processed folders to the text file
        with open(processedFolders_path, "w") as f:
            f.write("\n".join(processedFolders))
            
        return "Successfully encoded new images."
    
    
