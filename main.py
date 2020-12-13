import face_alignment
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import io
import collections
import numpy as np
import os
from tqdm import tqdm #this is actually not neccessary but people like progress bars i guess

print("This will take a long time, linearly propertional to the amount of keyframes and can vary between systems.")
print("Go and pick up those old bottles on your floor, tidy things up, organize your clothes, admit your feelings to your crush in the meanwhile.")
print()

if __name__ == "__main__":
    fa = face_alignment.FaceAlignment(
        face_alignment.LandmarksType._3D,
        device='cpu', flip_input=True
    )

    directory = "keyframes"
    filenames = os.listdir(directory)

    for filename in tqdm(filenames):
        try:
            input_img = io.imread(f"../{directory}/{filename}")
        except FileNotFoundError:
            input_img = io.imread(f"{directory}/{filename}")

        preds = fa.get_landmarks(input_img)[-1]

        with open(f"landmarks/{os.path.splitext(filename)[0]}.npy", "wb") as file:
            np.save(file, preds)