import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from matplotlib.patches import Circle

# Global
data = {}
global circle

def generate_random_points(center, num_points, distance_multiplier):
    # Generate random points around the center with a distance multiplier
    x = center[0] + (np.random.rand(num_points) * 2 - 1) * distance_multiplier
    y = center[1] + (np.random.rand(num_points) * 2 - 1) * distance_multiplier
    global max_dist
    max_dist = 0
    for i in range(num_points):
        point = np.array([x[i], y[i]])
        dist = np.linalg.norm(center - point)
        max_dist = max(max_dist, dist)
    return x, y

def update(val):
    # Update the plot when the slider is moved
    distance_multiplier = slider.val

    if len(data) == 0:
        random_x, random_y = generate_random_points(center_point, num_points, distance_multiplier)
        data['x'] = random_x
        data['y'] = random_y
    else:
        random_x = [x*distance_multiplier for x in data.get('x')]
        random_y = [x*distance_multiplier for x in data.get('y')]
    
    points.set_offsets(np.column_stack((random_x, random_y)))

    max_dist = 0
    for i in range(num_points):
        point = np.array([random_x[i], random_y[i]])
        dist = np.linalg.norm(center_point - point)
        max_dist = max(max_dist, dist)

    # Update circle
    circle.set_radius(max_dist)
    circle.set_center(center_point)
    

    fig.canvas.draw_idle()

# Get user input for the center point
center_x = 0
center_y = 0
center_point = (center_x, center_y)

# Generate and plot random points
num_points = 10
initial_distance_multiplier = 1.0

if len(data) == 0:
    random_x, random_y = generate_random_points(center_point, num_points, initial_distance_multiplier)
    data['x'] = random_x
    data['y'] = random_y
else:
    random_x = [x*initial_distance_multiplier for x in data.get('x')]
    random_y = [x*initial_distance_multiplier for x in data.get('y')]

fig, ax = plt.subplots()
points = ax.scatter(random_x, random_y, label='Prompt Output', color='red')
center_marker = ax.scatter(center_point[0], center_point[1], label='Center', color='blue', marker='x')

circle = Circle(center_point, max_dist, fill=False, edgecolor='green', linestyle='dashed')
ax.add_patch(circle)

ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Prompt outputs embeddings around imaginary center')
ax.legend()

# Add slider
ax_slider = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Spread', 0.0, 1, valinit=initial_distance_multiplier)
slider.on_changed(update)

plt.show()
