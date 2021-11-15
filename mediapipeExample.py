import cv2
import mediapipe as mp
import time
import serial
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
PRECISION = 0.1
TIME_INTERVAL = 500000000
TARGET_OUTLINE = True

def open_glove():
    return serial.Serial('COM10')

def close_glove(ser):
    ser.close()


def buzz(ser, loc, lenms=500):
    '''Buzz given location for given duration in ms
    location codes:
    t, b, l, r, a'''
    loc_ar = {'t':'1000', 'r':'0100', 'b':'0010', 'l':'0001', 'a':'1111'}
    loc_code = loc_ar[loc]
    com = loc_code+'buzz'+str(lenms)+'.'
    ser.write(str.encode(com))

def spin(times):
    for i in range(times):
        buzz('t',50)
        buzz('r',50)
        buzz('b',50)
        buzz('l',50)

def guide(position, imageHeight, imageWidth, marginOfError, ser):
    """Will print guiding information to guide the user's hand to the middle of the screen
    position: tupple with the hand's location
    imageHeight: height of the image being processed
    imageWidth: width of the image being processed
    marginOfError: double representing how far from the middle point 
    ser: connection to the glove
    """
    halfX = imageWidth / 2
    halfY = imageHeight / 2
    # Check the x coordinate to guide to middle
    if position[0] > halfX * (1.0 - marginOfError) and not position[0] < halfX * (1.0 + marginOfError):
        print("Left")
        buzz(ser, "l")
    elif position[0] < halfX * (1.0 + marginOfError) and not position[0] > halfX * (1.0 - marginOfError):
        print("Right")
        buzz(ser, "r")
        # Check the y coordinate to guide to middle
    if position[1] > halfY * (1.0 - marginOfError) and not position[1] < halfY * (1.0 + marginOfError):
        print("Up")
        buzz(ser, "t")
    elif position[1] < halfY * (1.0 + marginOfError) and not position[1] > halfY * (1.0 - marginOfError):
        print("Down")
        buzz(ser, "b")

def drawTarget(image, imageHeight, imageWidth, marginOfError):
    """Roughly draws an outline of the target area
    image: image object to be drawn
    imageHeight: height of the image being processed
    imageWidth: width of the image being processed
    marginOfError: double representing how far from the middle point 
    """
    axesLength = (int(imageWidth * marginOfError), int(imageHeight * marginOfError))
    center = (imageWidth//2, imageHeight//2)
    # Red color in BGR
    color = (0, 0, 255)
    # Draw a ellipse with red line borders
    image = cv2.ellipse(image, center, axesLength,
            0, 0, 360, color, thickness = 1)
    return image


# For webcam input:
cap = cv2.VideoCapture(0)
# Open connection to glove
ser = open_glove()

with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    lastPrint = 0
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        imageHeight, imageWidth, _ = image.shape
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if TARGET_OUTLINE == True:
           image = drawTarget(image, imageHeight, imageWidth, PRECISION)

        if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for point in mp_hands.HandLandmark:
                        # Point 0 is the wrist
                        if point == 0:
                            normalizedLandmark = hand_landmarks.landmark[point]
                            pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                                normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)

                            # If there are coordinates for the wrist and time has elapsed since the last p
                            if pixelCoordinatesLandmark != None and (time.time_ns() - lastPrint) > TIME_INTERVAL:
                                guide(pixelCoordinatesLandmark,
                                    imageHeight, imageWidth, PRECISION, ser)
                                lastPrint = time.time_ns()

                    # Original Google example, draw hand annotations on the image
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
        cv2.imshow('MediaPipe Hands', image)

        # Close the program if q is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
cap.release()
close_glove(ser)
