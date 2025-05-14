import cv2
import numpy as np

def detect_markers(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform binary thresholding
    _, thresholded = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_markers = []

    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the polygon is a quadrilateral (4 sides)
        if len(approx) == 4:
            # Check if the quadrilateral is convex and has a significant area
            area = cv2.contourArea(approx)
            if area > 1000 and cv2.isContourConvex(approx):
                # Add the marker (quadrilateral) to the detected list
                detected_markers.append(approx)

    return detected_markers

def main():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Detect markers in the frame
        markers = detect_markers(frame)

        # Draw the detected markers
        for marker in markers:
            cv2.polylines(frame, [marker], True, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Custom Marker Detection', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    main()
