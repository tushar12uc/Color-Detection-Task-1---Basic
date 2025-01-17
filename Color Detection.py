# Importing required libraries
import cv2
import pandas as pd
import os

# Define the paths for the image and CSV file
img_path = r'C:\Users\HP\Desktop\Data Analytics Slash Mark\Task 1 Color Detection\pic3.jpg'
csv_path = r'C:\Users\HP\Desktop\Data Analytics Slash Mark\Task 1 Color Detection\colors.csv'

# Check if the image file exists
if not os.path.exists(img_path):
    print(f"Error: The image file '{img_path}' does not exist.")
    exit()

# Check if the CSV file exists
if not os.path.exists(csv_path):
    print(f"Error: The file '{csv_path}' does not exist.")
    exit()

# Reading the CSV file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Reading and resizing the image
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# Declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# Function to calculate the nearest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d < minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

# Function to get x, y coordinates on double-click
def draw_function(event, x, y, flags, params):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos, ypos = x, y
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)

# Creating a window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', img)
    if clicked:
        # Draw a rectangle with the detected color
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)

        # Display color name and RGB values
        text = get_color_name(r, g, b) + f' R={r} G={g} B={b}'
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # Change text color for light backgrounds
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    # Exit on pressing 'Esc'
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
