from datetime import datetime
import face_recognition
import pandas as pd
import pickle
import time
import cv2
import os

def attendance_check():
    # Load encoded faces from pickle file 
    pickle_path = "misc_files/encodings.pickle"
    face_encodings = load_pickle(pickle_path)
    
    # Initialize the video capture stream
    video_stream = capture_video()

    # Create a dictionary to store the count and time of each recognized face
    recognized_counts = {}

    # Set the start time
    start_time = time.time()

    while True:
        # While loop will stop running after 15 seconds
        if time.time() - start_time > 15:
            break

        # Read a frame from the video stream
        ret, frame = video_stream.read()
        
        # Resize the frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the frame from BGR to RGB
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the frame
        print("Wait as we recognize faces...")
        face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")

        # Loop over the detected faces
        for face_location in face_locations:
            top, right, bottom, left = [i * 4 for i in face_location]  # Scale the face locations back up

            # Extract the face encoding for the current frame
            face_encoding = face_recognition.face_encodings(rgb_small_frame, [face_location])[0]

            # Perform face recognition by comparing the current face encoding with known encodings
            name = "Unknown"
            matches = face_recognition.compare_faces(face_encodings["encodings"], face_encoding)
            face_distances = face_recognition.face_distance(face_encodings["encodings"], face_encoding)

            if True in matches:
                best_match_index = matches.index(True)
                name = face_encodings["names"][best_match_index]

                str_date, str_time = get_date_time()

                # Increment the count for the recognized face and store the time
                if name in recognized_counts:
                    recognized_counts[name]['count'] += 1
                    recognized_counts[name]['times'].append(str_time)
                else:
                    recognized_counts[name] = {'count': 1, 'times': [str_time]}

            # Draw a rectangle around the face and display the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 10 if top - 10 > 10 else top + 10
            label = f"{name} ({min(face_distances):.2f})"
            cv2.putText(frame, label, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        # Display the frame with recognized faces
        cv2.imshow("Video", frame)

        # Exit the video loop by pressing the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    most_frequent_name = create_excel_record(recognized_counts, str_date)

    # Release the video capture and close the OpenCV windows
    video_stream.release()
    cv2.destroyAllWindows()
    
    return(f"{most_frequent_name} successfully logged on at {str_time}.")

def get_date_time():
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Parse the current_time string
    parsed_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

    # Get the date and time separately
    str_date = parsed_time.date()
    str_time = parsed_time.time()
    
    return (str_date, str_time)

def create_excel_record(recognized_counts, str_date):
    # Find the most frequently detected person's name and their associated times
    most_frequent_name = max(recognized_counts, key=lambda x: recognized_counts[x]['count'])
    most_frequent_times = recognized_counts[most_frequent_name]['times']

    last_name = most_frequent_name.split("_")[0]
    first_name = most_frequent_name.split("_")[1]
    
    # Create a list of dictionaries to store the recognized faces and times
    recognized_faces_data = []

    # Add the most frequently detected name and time to the list
    recognized_faces_data.append({'Last Name': last_name, 'First Name': first_name, 'Time': most_frequent_times[0]})

    # Create a DataFrame with the recognized faces and times
    recognized_faces = pd.DataFrame(recognized_faces_data)

    # Create a file path for the Excel file
    file_path = f"attendance_logs/{str_date}.xlsx"
    
    # Function that logs data in an excel file 
    save_to_excel(file_path, recognized_faces)
    
    return most_frequent_name
    
def save_to_excel(file_path, recognized_faces):
    # Check if the file already exists
    if os.path.isfile(file_path):
        # Load the existing Excel file
        existing_data = pd.read_excel(file_path)

        # Concatenate the existing data and the new data
        updated_data = pd.concat([existing_data, recognized_faces], ignore_index=True)

        # Save the updated data to the Excel file
        updated_data.to_excel(file_path, index=False)
    else:
        # Save the new data to a new Excel file
        recognized_faces.to_excel(file_path, index=False)
        # Save the DataFrame to an Excel file
        recognized_faces.to_excel(file_path, index=False)
    
def load_pickle(pickle_path):
    print("Loading encodings...")
    return pickle.loads(open(pickle_path, "rb").read())

def capture_video():
    return cv2.VideoCapture(0) 

    

