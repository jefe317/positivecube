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
# v 1.1 March 2026
#   ☒ Simplified, condensed code
#   ☒ Changed selection functionality to deselect all before adding geometry

bl_info = {
    "name": "Add Positive Cube",
    "description": "Adds a cube with its origin at the corner.",
    "author": "Jeff Lange @jefftml",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh",
    "category": "Add Mesh",
}

FACES = [(3, 2, 1, 0), (0, 1, 5, 4), (1, 2, 6, 5),
         (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7)]

VERTS = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
         (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]


def add_corner_cube(context, s=1):
    v = [(s * x, s * y, s * z) for x, y, z in VERTS]
    faces = [f[::-1] for f in FACES] if s < 0 else FACES
    mesh = bpy.data.meshes.new("cube")
    mesh.from_pydata(v, [], faces)
    obj = bpy.data.objects.new(
        ("Positive" if s > 0 else "Negative") + " Cube", mesh)
    context.collection.objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT')
    context.view_layer.objects.active = obj
    obj.select_set(True)
    obj.matrix_world = context.scene.cursor.matrix
    return {'FINISHED'}


def make_op(label, idname, s):
    class Op(bpy.types.Operator):
        bl_idname, bl_label, bl_options = idname, label, {'REGISTER', 'UNDO'}
        def execute(self, ctx): return add_corner_cube(ctx, s)
    Op.__name__ = idname.split('.')[1]
    return Op


CLASSES = [make_op("Positive Cube", "mesh.positive_cube", 1),
           make_op("Negative Cube", "mesh.negative_cube", -1)]


def menu_func(self, context):
    self.layout.operator(CLASSES[0].bl_idname, icon='MESH_CUBE')
    self.layout.operator(CLASSES[1].bl_idname, icon='CUBE')


def register():
    [bpy.utils.register_class(c) for c in CLASSES]
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    [bpy.utils.unregister_class(c) for c in CLASSES]
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
