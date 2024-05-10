# <pep8 compliant>
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import bpy

# https://www.youtube.com/watch?v=mN3n9b98HMk was helpful, thanks!

# CHANGELOG
# v 1.0 May 2024 - Positive Cube
#   ☒ Initial Add-on, add positive and negative cube.


bl_info = {
    "name": "Add Positive Cube",
    "description": "Adds a cube with its origin at the corner.",
    "author": "Jeff Lange @jefftml",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh",
    "category": "Add Mesh",
}


class OBJECT_OT_add_positive_cube(bpy.types.Operator):
    """Adds a cube with its origin at the bottom left corner and exists""" \
    """ only in space positive to the 3D cursor"""
    bl_idname = "mesh.add_positive_cube"
    bl_label = "Add Positive Cube"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        verts = [
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (0, 1, 1)
        ]

        faces = [
            (3, 2, 1, 0),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
            (4, 5, 6, 7)
        ]

        edges = []

        mesh_data = bpy.data.meshes.new("positive_cube")
        mesh_data.from_pydata(verts, edges, faces)
        mesh_obj = bpy.data.objects.new("Positive Cube", mesh_data)
        bpy.context.collection.objects.link(mesh_obj)
        mesh_obj.select_set(True)
        mesh_obj.matrix_world = bpy.context.scene.cursor.matrix
        return {'FINISHED'}


class OBJECT_OT_add_negative_cube(bpy.types.Operator):
    """Adds a cube with its origin at the top right corner and exists""" \
    """ only in space negative to the 3D cursor"""
    bl_idname = "mesh.add_negative_cube"
    bl_label = "Add Negative Cube"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        verts = [
            (0, 0, 0),
            (-1, 0, 0),
            (-1, -1, 0),
            (0, -1, 0),
            (0, 0, -1),
            (-1, 0, -1),
            (-1, -1, -1),
            (0, -1, -1)
        ]

        faces = [
            (0, 1, 2, 3),
            (4, 5, 1, 0),
            (5, 6, 2, 1),
            (6, 7, 3, 2),
            (7, 4, 0, 3),
            (7, 6, 5, 4)
        ]

        edges = []

        mesh_data = bpy.data.meshes.new("negative_cube")
        mesh_data.from_pydata(verts, edges, faces)
        mesh_obj = bpy.data.objects.new("Negative Cube", mesh_data)
        bpy.context.collection.objects.link(mesh_obj)
        mesh_obj.select_set(True)
        mesh_obj.matrix_world = bpy.context.scene.cursor.matrix
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_add_positive_cube.bl_idname,
                         icon='MESH_CUBE')
    self.layout.operator(OBJECT_OT_add_negative_cube.bl_idname,
                         icon='CUBE')


def register():
    bpy.utils.register_class(OBJECT_OT_add_positive_cube)
    bpy.utils.register_class(OBJECT_OT_add_negative_cube)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_positive_cube)
    bpy.utils.unregister_class(OBJECT_OT_add_negative_cube)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
