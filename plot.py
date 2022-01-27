    # 2D-Plot
import collections
from matplotlib import pyplot as plt
import sys
from skimage import io
import numpy as np

def main():
  landmark_directory = "landmarks"
  frame_directory = "frames"
  extension = "png"
  frame_prefix = ""

  try:
    _, identifier = sys.argv

    try:
      input_img = io.imread(f"../{frame_directory}/{frame_prefix}{identifier}.{extension}")
    except FileNotFoundError:
      input_img = io.imread(f"{frame_directory}/{frame_prefix}{identifier}.{extension}")

    try:
      with open(f"{landmark_directory}/{frame_prefix}{identifier}.npy", "rb") as file:
        preds = np.load(file)
    except:
      print("Couldn't find landmark data: ")


  except:
    print("filename not found")
    return

  plot_style = dict(marker='o',
                    markersize=4,
                    linestyle='-',
                    lw=2)

  pred_type = collections.namedtuple('prediction_type', ['slice', 'color'])
  pred_types = {
    'face': pred_type(slice(0, 17), (1.0, 0.0, 0.0, 1)),
    'eyebrow1': pred_type(slice(17, 22), (1.0, 0.498, 0.055, 0.4)),
    'eyebrow2': pred_type(slice(22, 27), (1.0, 0.498, 0.055, 0.4)),
    'nose': pred_type(slice(27, 31), (0.345, 0.239, 0.443, 0.4)),
    'nostril': pred_type(slice(31, 36), (0.345, 0.239, 0.443, 0.4)),
    'eye1': pred_type(slice(36, 42), (0.596, 0.875, 0.541, 0.3)),
    'eye2': pred_type(slice(42, 48), (0.596, 0.875, 0.541, 0.3)),
    'lips': pred_type(slice(48, 60), (0.596, 0.875, 0.541, 0.3)),
    'teeth': pred_type(slice(60, 68), (0.596, 0.875, 0.541, 0.4))
  }

  fig = plt.figure(figsize=plt.figaspect(.5))
  ax = fig.add_subplot(1, 2, 1)
  ax.imshow(input_img)

  for pred_type in pred_types.values():
    print(preds[pred_type.slice])
    ax.plot(
      preds[pred_type.slice, 0],
      preds[pred_type.slice, 1],
      color=pred_type.color,
      **plot_style
    )

  ax.axis('off')

  # 3D-Plot
  ax = fig.add_subplot(1, 2, 2, projection='3d')
  surf = ax.scatter(
    preds[:, 0] * 1.2,
    preds[:, 1],
    preds[:, 2],
    c='cyan',
    alpha=1.0,
    edgecolor='b'
  )

  for pred_type in pred_types.values():
      ax.plot3D(
        preds[pred_type.slice, 0] * 1.2,
        preds[pred_type.slice, 1],
        preds[pred_type.slice, 2],
        color='blue'
      )

  ax.view_init(elev=90., azim=90.)
  ax.set_xlim(ax.get_xlim()[::-1])
  plt.show()

if __name__ == "__main__":
  main()