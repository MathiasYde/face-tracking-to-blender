import numpy as np
import os
import math
import json

def cross_product(side1, side2):
  a1 = side1[0]
  a2 = side1[1]
  a3 = side1[2]

  b1 = side2[0]
  b2 = side2[1]
  b3 = side2[2]

  return [
    a2*b3-a3*b2,
    a3*b1-a1*b3,
    a1*b2-a2*b1
  ]

def normalize(v):
  length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

  return [
    v[0] / length,
    v[1] / length,
    v[2] / length
  ]

def calculate_midpoint(a, b, c):
  return [
    a[0] + b[0] + c[0] / 3,
    a[1] + b[1] + c[1] / 3,
    a[2] + b[2] + c[2] / 3
  ]

def calculate_normal(a, b, c):
  side1 = b - a
  side2 = c - a

  return normalize(cross_product(side1, side2))

if __name__ == "__main__":
  features = {
    'face': slice(0, 17),
    'eyebrow1': slice(17, 22),
    'eyebrow2': slice(22, 27),
    'nose': slice(27, 31),
    'nostril': slice(31, 36),
    'eye1': slice(36, 42),
    'eye2': slice(42, 48),
    'lips': slice(48, 60),
    'teeth': slice(60, 68)
  }

  landmark_directory = "landmarks"
  pixelspermeter = 300

  # Note there is 68 landmarks in total
  keylandmarks_indices = [
    (features["face"], 0),
    (features["face"], 9),
    (features["face"], 16)
  ]

  normals = {}
  midpoints = {}

  for index, filename in enumerate(os.listdir(landmark_directory)):
    frame_index = int(filename.split(".")[0])
    with open(f"{landmark_directory}/{filename}", 'rb') as file:
      landmark = np.load(file)

      points = []
      for keylandmarks_index in keylandmarks_indices:
        points.append(landmark[keylandmarks_index[0]][keylandmarks_index[1]])

      normals[frame_index] = calculate_normal(*points)
      midpoints[frame_index] = [v / pixelspermeter for v in calculate_midpoint(*points)]
    
  data = json.dumps({
    "ppm": pixelspermeter
    "midpoints": midpoints,
    "normals": normals,
  })

  with open("data.json", "w") as file:
    file.write(data)