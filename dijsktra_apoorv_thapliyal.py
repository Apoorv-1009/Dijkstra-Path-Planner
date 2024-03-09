import numpy as np
import cv2
import heapq

########## Step 1: Define the action cost set ##########

# Define the cost of each action
action_cost_set = {(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0,-1, 1), (1, 1, 1.4), (-1, 1, 1.4), (1,-1, 1.4), (-1,-1, 1.4)}

########## STEP 2: MATHEMATICAL REPRESENTATION OF FREE SPACE ##########

# Define the height and width of the canvas
height = 500
width = 1200

# Make an empty canvas
canvas = 255*np.ones((height, width, 3), dtype=np.uint8)

clearance = 5

color = (0, 255, 255)

# OBSTACLE 1
# Define the vertices of the obstacle clearance
vertices = np.array([[100-clearance, 0], [100-clearance, 400+clearance],
                     [175+clearance, 400+clearance], [175+clearance, 0]])
vertices = vertices.reshape((-1, 1, 2))
cv2.fillPoly(canvas, [vertices], color)
# Define the vertices of the obstacle 
vertices = np.array([[100, 0], [100, 400], [175, 400], [175, 0]])
vertices = vertices.reshape((-1, 1, 2))
cv2.fillPoly(canvas, [vertices], (0, 0, 0))

# OBSTACLE 2
# Define the vertices of the obstacle clearance
vertices = np.array([[275-clearance, 500], [275-clearance, 100-clearance],
                     [350+clearance, 100-clearance], [350+clearance, 500]])
vertices = vertices.reshape((-1, 1, 2))
cv2.fillPoly(canvas, [vertices], color)
# Define the vertices of the obstacle
vertices = np.array([[275, 500], [275, 100], [350, 100], [350, 500]])
vertices = vertices.reshape((-1, 1, 2))
cv2.fillPoly(canvas, [vertices], (0, 0, 0))

# OBSTACLE 3
# Define the center and side length of the hexagon with clearance
center = (650, height/2)
side_length = 150+clearance

# Calculate the coordinates of the vertices
vertices = []
for i in range(6):
    angle_deg = 60 * i
    angle_rad = np.deg2rad(angle_deg)
    x = int(center[0] + side_length * np.cos(angle_rad))
    y = int(center[1] + side_length * np.sin(angle_rad))
    vertices.append((x, y))

# Draw the hexagon by connecting the vertices
for i in range(6):
    cv2.line(canvas, vertices[i], vertices[(i + 1) % 6], (255, 255, 255), 2)

# Fill up the inside of the hexagon with a color
pts = np.array(vertices, np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.fillConvexPoly(canvas, pts, color)

# Define the center and side length of the hexagon without clearance
center = (650, height/2)
side_length = 150

# Calculate the coordinates of the vertices
vertices = []
for i in range(6):
    angle_deg = 60 * i
    angle_rad = np.deg2rad(angle_deg)
    x = int(center[0] + side_length * np.cos(angle_rad))
    y = int(center[1] + side_length * np.sin(angle_rad))
    vertices.append((x, y))

# Draw the hexagon by connecting the vertices
for i in range(6):
    cv2.line(canvas, vertices[i], vertices[(i + 1) % 6], (255, 255, 255), 2)

# Fill up the inside of the hexagon with a color
pts = np.array(vertices, np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.fillConvexPoly(canvas, pts, (0, 0, 0))

# OBSTACLE 4
vertices = np.array([[width-300-clearance, 50-clearance], [width-100+clearance, 50-clearance],
                     [width-100+clearance, 450+clearance], [width-300-clearance, 450+clearance],
                     [width-300-clearance, 450-75-clearance], [width-300+120-clearance, 450-75-clearance],
                     [width-180-clearance, 125+clearance], [width-180-120-clearance, 125+clearance]])
vertices = vertices.reshape((-1, 1, 2))
cv2.fillPoly(canvas, [vertices], color)
vertices = np.array([[width-300, 50], [width-100, 50],
                     [width-100, 450], [width-300, 450],
                     [width-300, 450-75], [width-300+120, 450-75],
                     [width-180, 125], [width-180-120, 125]])
vertices = vertices.reshape((-1, 1, 2))
cv2.fillPoly(canvas, [vertices], (0, 0, 0))