import cv2
import numpy as np
import argparse

# ---------- Argument parsing ----------
parser = argparse.ArgumentParser(description="Interactive HoughLines with trackbars")
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
edges = cv2.Canny(gray, 50, 200)

# ---------- Window ----------
window_name = "HoughLines Interactive"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# ---------- Dummy callback ----------
def nothing(x):
    pass

# ---------- Trackbars ----------
cv2.createTrackbar("rho", window_name, 1, 10, nothing)
cv2.createTrackbar("theta (deg)", window_name, 1, 180, nothing)
cv2.createTrackbar("threshold", window_name, 100, 300, nothing)
cv2.createTrackbar("srn", window_name, 0, 10, nothing)
cv2.createTrackbar("stn", window_name, 0, 10, nothing)

# ---------- Main loop ----------
while True:
    img = img_orig.copy()

    # Read trackbar values
    rho = cv2.getTrackbarPos("rho", window_name)
    theta_deg = cv2.getTrackbarPos("theta (deg)", window_name)
    threshold = cv2.getTrackbarPos("threshold", window_name)
    srn = cv2.getTrackbarPos("srn", window_name)
    stn = cv2.getTrackbarPos("stn", window_name)

    # Enforce minimums
    rho = max(rho, 1)
    theta_deg = max(theta_deg, 1)
    threshold = max(threshold, 1)

    theta = np.deg2rad(theta_deg)

    # HoughLines
    lines = cv2.HoughLines(
        edges,
        rho,
        theta,
        threshold,
        None,
        srn,
        stn
    )

    # Draw lines
    if lines is not None:
        for i, line in enumerate(lines):

            rho, theta = line[0]

            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho

            extend = 1000
            x1 = int(x0 + extend * -b)
            y1 = int(y0 + extend * a)
            x2 = int(x0 - extend * -b)
            y2 = int(y0 - extend * a)

            cv2.line(img, (x1, y1), (x2, y2),
                     (255, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow(window_name, img)

    key = cv2.waitKey(30)
    if key != -1:
        break

cv2.destroyAllWindows()
