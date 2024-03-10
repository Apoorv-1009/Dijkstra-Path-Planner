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
clearance = 5
color = (0, 255, 255)

# Make an empty canvas
canvas = np.zeros((height, width, 3), dtype=np.uint8)
# Draw a white rectangle from (clearance, clearance) to (width-clearance, height-clearance) on the canvas for wall padding
cv2.rectangle(canvas, (clearance, clearance), (width-clearance, height-clearance), (255, 255, 255), -1)

# OBSTACLE 1
x1, x2 = 100-clearance, 175+clearance
y1, y2 = clearance, 400+clearance
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = color
x1, x2 = 100, 175
y1, y2 = 0, 400
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = 0

# OBSTACLE 2
x1, x2 = 275-clearance, 350+clearance
y1, y2 = 100-clearance, 500-clearance
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = color
x1, x2 = 275, 350
y1, y2 = 100, 500
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = 0

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
x1, x2 = width-300-clearance, width-100+clearance
y1, y2 = 50-clearance, 125+clearance
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = color
x1, x2 = width-180-clearance, width-100+clearance
y1, y2 = 50-clearance, height-50+clearance
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = color
x1, x2 = width-300-clearance, width-300+120+clearance
y1, y2 = 450-75-clearance, 450+clearance
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = color

x1, x2 = width-300, width-100
y1, y2 = 50, 125
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = 0
x1, x2 = width-180, width-100
y1, y2 = 50, height-50
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = 0
x1, x2 = width-300, width-300+120
y1, y2 = 450-75, 450
for x in range(x1, x2):
    for y in range(y1, y2):
        canvas[y, x] = 0
        
########## STEP 3: GENERATE THE GRAPH AND CHECK FOR GOAL NODE IN EACH ITERATION ##########

# Enter the start and goal nodes with bottom left as origin
# Take input from the user, till its not in the obstacle space
while True:
    x_start = int(input('Enter start x position (5-1194): '))
    y_start = int(input('Enter start y position (5-494): '))

    y_start = height-y_start-1
    try:
        if canvas[y_start, x_start, 0] == 255:
            break
    except:
        print('Invalid input, re-enter the start node position')

    else:
        print('The start node is in the obstacle space, re-enter the start node position')

while True:
    x_goal = int(input('Enter goal x position (5-1194): '))
    y_goal = int(input('Enter goal y position (5-494): '))

    y_goal = height-y_goal-1
    try:
        if canvas[y_goal, x_goal, 0] == 255:
            break
    except:
        print('Invalid input, re-enter the goal node position')
    else:
        print('The goal node is in the obstacle space, re-enter the goal node position')

print("Positions accepted! Calculating path...")

q = []
heapq.heappush(q, (0, x_start, y_start))

# Dictionary to store visited nodes
visited = {(x_start, y_start): 1}
# Dictionary to store the parent of each node
parent = {(x_start, y_start): (x_start, y_start)}
# Dictionary to store the cost of each node
cost_to_come = {(x_start, y_start): 0}

reached = False

while q:

    _, x, y = heapq.heappop(q)

    if x == x_goal and y == y_goal:
        print('Goal reached')
        reached = True
        break

    for dx, dy, cost in action_cost_set:
        x_new, y_new = x + dx, y + dy

        # If its between the boundaries and not an obstacle
        if 0 <= x_new < width and 0 <= y_new < height and canvas[y_new, x_new, 0] == 255:
            
            # If the node is not visited 
            if (x_new, y_new) not in visited:
                node_cost = cost_to_come[(x, y)] + cost #+ ((x_new-x_goal)**2 + (y_new-y_goal)**2)**0.5
                heapq.heappush(q, (node_cost, x_new, y_new))
                visited[(x_new, y_new)] = 1

                # Store the parent of the node
                parent[(x_new, y_new)] = (x, y)
                # Store the cost of the node
                cost_to_come[(x_new, y_new)] = node_cost

            # If the node is visited and the cost to come is less than the previous cost
            elif cost_to_come[(x_new, y_new)] > cost_to_come[(x, y)] + cost:
                cost_to_come[(x_new, y_new)] = cost_to_come[(x, y)] + cost
                # Store the parent of the node
                parent[(x_new, y_new)] = (x, y)
                
if not reached:
    print('Goal could not be reached')
    print("Exiting...")
    exit()

########## STEP 4: OPTIMAL PATH ##########
    
# Get the path from the parent dictionary
path = []
x, y = x_goal, y_goal   
while (x, y) != (x_start, y_start):
    path.append((x, y))
    x, y = parent[(x, y)]
path.append((x, y))
path.reverse()

########## STEP 5: REPRESENT THE OPTIMAL PATH ##########

# Draw the start and goal nodes on the canvas
cv2.circle(canvas, (x_start, y_start), 10, (0, 255, 0), -1)
cv2.circle(canvas, (x_goal, y_goal), 10, (0, 165, 255), -1)

# Start a video writer in mp4 format
dijkstra = cv2.VideoWriter('dijkstra.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 50, (width, height))

# Draw on every threshold frame
threshold = 200
counter = 0

# Draw the visited nodes on the canvas
for x, y in visited:
    counter+=1
    canvas[y, x] = [255, 0, 0]
    if(counter == threshold):
        cv2.imshow('Canvas', canvas)
        dijkstra.write(canvas)
        cv2.waitKey(1)  
        counter = 0

threshold = 5
counter = 0

# Draw the start and goal nodes on the canvas
cv2.circle(canvas, (x_start, y_start), 10, (0, 255, 0), -1)
cv2.circle(canvas, (x_goal, y_goal), 10, (0, 165, 255), -1)

# Draw the path on the canvas
for i in range(len(path) - 1):
    cv2.line(canvas, path[i], path[i + 1], (0, 0, 255), 2)
    counter+=1
    if(counter == threshold):
        cv2.imshow('Canvas', canvas)
        dijkstra.write(canvas)
        cv2.waitKey(1)  
        counter = 0

# Release VideoWriter
dijkstra.release()
cv2.waitKey(0)
cv2.destroyAllWindows()