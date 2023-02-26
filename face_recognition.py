import cv2
import os
import numpy as np

# Function to read images from a directory and convert to grayscale


def read_images(directory, size=(200, 200)):
    X = []
    y = []
    label_dict = {}  # dictionary to map directory names to integer labels
    label_counter = 0  # counter to assign unique integer label to each person
    img_name = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                if file.endswith("jpg") or file.endswith("png"):
                    path = os.path.join(root, file)
                    label = os.path.basename(path).split(" ")[0]
                    if label not in label_dict:
                        label_dict[label] = label_counter
                        label_counter += 1
                    img = cv2.imread(path, 0)
                    # resize the image to the desired size
                    img = cv2.resize(img, size)
                    X.append(np.asarray(img, dtype=np.uint8))
                    y.append(label_dict[label])
            except Exception as e:
                print(f"Error processing file {file}: {e}")
    return [X, y, label_dict]


def capture_images(label, count=20, size=(200, 200)):
    cap = cv2.VideoCapture(0)  # initialize video capture from camera
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Create directory for new person if it doesn't exist
    directory = os.path.join("base_pictures", label)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Capture 'count' images of new person's face
    i = 0
    while i < count:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

        # Iterate over detected faces
        for (x, y, w, h) in faces:
            # Crop face from the frame
            face = gray[y:y+h, x:x+w]

            # Resize face for saving (should be same size as training images)
            face = cv2.resize(face, size)

            # Save face image to file
            filename = os.path.join(directory, f"{label}_{i}.jpg")
            cv2.imwrite(filename, face)

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            i += 1
            if i >= count:
                break

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Exit if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture and close window
    cap.release()
    cv2.destroyAllWindows()


try:

    known_person_color = (0, 255, 0)  # green for known people
    unknown_person_color = (0, 0, 255)  # red for unknown people

    # Train face recognizer
    base_pictures, labels, label_dict = read_images(
        "base_pictures", size=(200, 200))

    face_recognizer = cv2.face.EigenFaceRecognizer_create()
    face_recognizer.train(base_pictures, np.array(labels, dtype=np.int32))

    # Initialize video capture from camera
    cap = cv2.VideoCapture(0)

    # Face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

        # Iterate over detected faces
        for (x, y, w, h) in faces:

            # Crop face from the frame
            face = gray[y:y+h, x:x+w]

            # Resize face for recognition (should be same size as training images)
            face = cv2.resize(face, (200, 200))

            # Recognize face using face recognizer
            label, confidence = face_recognizer.predict(face)

            print(label)
            # Get the name from the label_dict dictionary, or indicate that the person is not recognized
            if label in label_dict:
                name = label_dict[label]
                text = "{} ({:.2f}%) {}".format(label, confidence, name)
                color = known_person_color
            else:
                name = "Person not recognized"
                text = name
                color = unknown_person_color
            # Get the name from the label_dict dictionary
            name = list(label_dict.keys())[
                list(label_dict.values()).index(label)]

            # Draw label and confidence on the frame with the name
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

            # Train new face person if 't' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('t'):
                name = input("Enter the name of the new person: ")
                capture_images(name)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Exit if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture and close window
    cap.release()
    cv2.destroyAllWindows()
except Exception as e:
    print(f"Error: {e}")
