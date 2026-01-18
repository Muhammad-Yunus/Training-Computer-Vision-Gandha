import cv2
import numpy as np
import argparse

# ---------- Argument parsing ----------
parser = argparse.ArgumentParser(description="Interactive HoughCircles with trackbars")
parser.add_argument(
    "--filename",
    required=True,
    help="Path to input image"
)
args = parser.parse_args()

# ---------- Load image ----------
img_orig = cv2.imread(args.filename)
if img_orig is None:
    raise IOError(f"Cannot load image: {args.filename}")

gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (9, 9), 1.5)

# ---------- Window ----------
window_name = "HoughCircles Interactive"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# ---------- Dummy callback ----------
def nothing(x):
    pass

# ---------- Trackbars ----------
cv2.createTrackbar("dp x10", window_name, 1, 30, nothing)
cv2.createTrackbar("minDist", window_name, 50, 300, nothing)
cv2.createTrackbar("param1 (Canny)", window_name, 200, 300, nothing)
cv2.createTrackbar("param2 (vote)", window_name, 17, 150, nothing)
cv2.createTrackbar("minRadius", window_name, 10, 100, nothing)
cv2.createTrackbar("maxRadius", window_name, 200, 300, nothing)

# ---------- Main loop ----------
while True:
    img = img_orig.copy()

    # Read trackbar values
    dp = cv2.getTrackbarPos("dp x10", window_name) / 10.0
    minDist = cv2.getTrackbarPos("minDist", window_name)
    param1 = cv2.getTrackbarPos("param1 (Canny)", window_name)
    param2 = cv2.getTrackbarPos("param2 (vote)", window_name)
    minRadius = cv2.getTrackbarPos("minRadius", window_name)
    maxRadius = cv2.getTrackbarPos("maxRadius", window_name)

    # Enforce minimums
    dp = max(dp, 1.0)
    minDist = max(minDist, 1)
    param1 = max(param1, 1)
    param2 = max(param2, 1)

    if maxRadius > 0 and maxRadius < minRadius:
        maxRadius = minRadius + 1

    # HoughCircles
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp,
        minDist,
        param1=param1,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius
    )

    # Draw circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for x, y, r in circles[0]:
            cv2.circle(img, (x, y), r, (255, 0, 0), 2)
            cv2.circle(img, (x, y), 2, (0, 0, 255), 3)

    cv2.imshow(window_name, img)

    key = cv2.waitKey(30)
    if key != -1:
        break

cv2.destroyAllWindows()
