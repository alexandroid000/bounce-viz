import numpy as np 
import random 
import matplotlib.pyplot as plt

grid_size = 5
points_size = 30

def generate_points(grid_size, points_size):

  x_coords = 2*[random.randint(1, grid_size) for x in range(points_size)]
  y_coords = 2*[random.randint(1, grid_size) for x in range(points_size)]
  random.shuffle(x_coords)
  random.shuffle(y_coords)
  horizontal_dots = np.array(list(sorted(sorted(list(zip(x_coords, y_coords)), key = lambda x: x[1]), key = lambda x: x[0])))
  vertical_dots = np.array(list(sorted(sorted(list(zip(x_coords, y_coords)), key = lambda x: x[0]), key = lambda x: x[1])))
  h_dots = []
  v_dots = []
  i = 0
  flag = False
  while i <len(horizontal_dots)-1:
    if (horizontal_dots[i] == horizontal_dots[i+1]).all():
      i += 2
      flag = False
      continue
    h_dots.append(horizontal_dots[i])
    flag = True
    i += 1
  if flag:
    h_dots.append(horizontal_dots[-1])
  h_dots = np.array(h_dots)
  i = 0
  flag = False
  while i <len(vertical_dots)-1:
    if (vertical_dots[i] == vertical_dots[i+1]).all():
      i += 2
      flag = False
      continue
    v_dots.append(vertical_dots[i])
    flag = True
    i += 1
  if flag:
    v_dots.append(vertical_dots[-1])
  v_dots = np.array(v_dots)
  return h_dots, v_dots

horizontal_dots, vertical_dots = generate_points(grid_size, points_size)
current_x = horizontal_dots[0][0]
connect_flag = False
edges = []

i = 0
while i < len(horizontal_dots)-1:
  current_x = horizontal_dots[i][0]
  while i<len(horizontal_dots)-1 and horizontal_dots[i][0] == current_x:
    edges.extend([horizontal_dots[i], horizontal_dots[i+1], [np.nan, np.nan]])
    i += 2

i = 0
current_y = vertical_dots[0][1]
while i < len(vertical_dots)-1:
  current_y = vertical_dots[i][1]
  while i<len(vertical_dots)-1 and vertical_dots[i][1] == current_y:
    edges.extend([vertical_dots[i], vertical_dots[i+1], [np.nan, np.nan]])
    i += 2
edges = np.array(edges)
print(edges)

plt.figure()
ax = plt.gca()
ax.axis('equal')
ax.axis('off')
plt.plot(horizontal_dots[:, 0], horizontal_dots[:, 1], 'ko')
plt.plot(edges[:, 0], edges[:, 1], 'b-')
plt.show()