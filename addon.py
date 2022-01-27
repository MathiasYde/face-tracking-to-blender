import bpy
from math import radians
from bpy.types import Operator

from bpy_extras.io_utils import (
  ImportHelper
)

from bpy.props import (
  StringProperty
)

import os
import json
from mathutils import Euler

bl_info = {
  "name": "load face alignment data",
  "author": "Mathias Yde",
  "description": "",
  "blender": (2, 80, 0),
  "version": (0, 0, 1),
  "category": "Import-Export"
}

class IMPORT_FACETRACKINGDATA(Operator, ImportHelper):
  bl_idname = "facetrackingdata.import"
  bl_label = "Import face tracking data"

  # This was a bit of a learning curve, but this is awesome
  filter_glob: StringProperty(
    default="*.json",
    options={'HIDDEN'}
  )

  def execute(self, context):
    directory = os.path.dirname(self.filepath)

    framepaths = sorted(os.listdir(f"{directory}\\frames"), key=len)

    # Set background images
    camera = bpy.context.scene.camera
    image = bpy.data.images.load(f"{directory}\\frames\\{framepaths[0]}")
    camera.data.show_background_images = True
    background = camera.data.background_images.new()
    background.image = image
    image.source = "SEQUENCE"

    background.image_user.frame_duration = len(framepaths)
    background.image_user.frame_start = 1
    background.image_user.frame_offset = int(os.path.splitext(framepaths[0])[0]) - 1

    # Set camera position
    camera.location = (0, -10, 0)
    camera.rotation_euler = (radians(90), 0, 0)

    with open(self.filepath, "r") as file:
      data = json.loads(file.read())

      midpoints = data["midpoints"]
      normals = data["normals"]

      origin = midpoints[list(midpoints)[0]]

      bpy.ops.object.add(
        type='EMPTY',
        location=(0, 0, 0),
        rotation=(0, 0, 0)
      )

      for midpoint, normal in zip(midpoints, normals):
        if midpoint != normal:
          self.report("WARNING", "Frame indices not aligned")
          continue
        
        obj = bpy.context.object
        obj.location = [k - j for k, j in zip(midpoints[midpoint], origin)]
        obj.rotation_euler = Euler(normals[normal], 'XYZ')

        obj.keyframe_insert(data_path="location", frame=int(midpoint))
        obj.keyframe_insert(data_path="rotation_euler", frame=int(normal))
      
    return {'FINISHED'}

def import_facetrackingdata_button(self, context):
  # Create button under the import menu

  self.layout.operator(
    IMPORT_FACETRACKINGDATA.bl_idname,
    text = IMPORT_FACETRACKINGDATA.bl_label,
    icon = "TEXTURE"
  )

def register():
  bpy.utils.register_class(IMPORT_FACETRACKINGDATA)
  bpy.types.TOPBAR_MT_file_import.append(import_facetrackingdata_button)

def unregister():
  bpy.utils.unregister_class(IMPORT_FACETRACKINGDATA)
  bpy.types.TOPBAR_MT_file_import.remove(import_facetrackingdata_button)

if __name__ == "__main__":
  unregister()
  register()
