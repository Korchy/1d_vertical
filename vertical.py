# Nikita Akimov
# interplanety@interplanety.org

import bpy
import math


class Vertical(bpy.types.Operator):
    bl_idname = 'vertical.select'
    bl_label = 'Vertical: Select'

    def execute(self, context):
        bpy.ops.mesh.select_all(action='DESELECT')

        activeobjectdata = bpy.context.active_object.data

        bpy.ops.object.mode_set(mode='OBJECT')

        for polygon in activeobjectdata.polygons:
            max_edge_len_x = 0
            max_edge_len_y = 0
            max_edge_len_z = 0
            for edge in polygon.edge_keys:
                edge_len_x = math.fabs(activeobjectdata.vertices[edge[0]].co[0] - activeobjectdata.vertices[edge[1]].co[0])
                max_edge_len_x = edge_len_x if edge_len_x > max_edge_len_x else max_edge_len_x
                edge_len_y = math.fabs(activeobjectdata.vertices[edge[0]].co[1] - activeobjectdata.vertices[edge[1]].co[1])
                max_edge_len_y = edge_len_y if edge_len_y > max_edge_len_y else max_edge_len_y
                edge_len_z = math.fabs(activeobjectdata.vertices[edge[0]].co[2] - activeobjectdata.vertices[edge[1]].co[2])
                max_edge_len_z = edge_len_z if edge_len_z > max_edge_len_z else max_edge_len_z

            if max_edge_len_z > max_edge_len_x and max_edge_len_z > max_edge_len_y:
                polygon.select = True

        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.active_object.mode == 'EDIT'


def register():
    bpy.utils.register_class(Vertical)


def unregister():
    bpy.utils.unregister_class(Vertical)
