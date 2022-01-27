import pygame as pg
import os
from skimage import io
import time
import json

images = [pg.image.load(f"keyframes/{filename}") for filename in sorted(os.listdir("keyframes"), key=len)]
#images = [io.imread(f"keyframes/{filename}") for filename in os.listdir("keyframes")]

with open("data.json", "r") as file:
  data = json.loads(file.read())
  normals = list(data["normals"].values())
  midpoints = list(data["midpoints"].values())

scale_factor = 0.5

pg.init()
display = pg.display.set_mode([int(n * scale_factor) for n in images[0].get_rect().size])

index = 0

# scale images

images = [pg.transform.scale(image, [int(n * scale_factor) for n in image.get_rect().size]) for image in images]

running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
        running = False
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_LEFT:
          index -= 1
      if event.key == pg.K_RIGHT:
          index += 1

  # make sure image index is within the range
  index = max(0, min(index, len(images) - 1))

  pg.display.set_caption(f"{index}/{len(images) - 1}")

  midpoint = [int(n * scale_factor * 0.44) for n in midpoints[index][0:2]]

  length_factor = 50

  

  normal = [
    midpoint[0] + -normals[index][0] * length_factor,
    midpoint[1] + -normals[index][1] * length_factor
  ]

  display.blit(images[index], (0, 0))
  pg.draw.circle(display, (255, 0, 0), midpoint, 4)
  pg.draw.line(display, (0, 255, 0), midpoint, normal, 2)

  

  pg.display.update()