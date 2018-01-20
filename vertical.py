# Nikita Akimov
# interplanety@interplanety.org

import bpy
import math


class Vertical(bpy.types.Operator):
    bl_idname = 'vertical.select'
    bl_label = 'Vertical: Select'
    bl_options = {'REGISTER', 'UNDO'}

    algorithm = bpy.props.IntProperty(name='algorithm', default=1)

    def execute(self, context):
        if context.active_object:
            if context.active_object.mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(type='FACE')
            bpy.ops.object.mode_set(mode='OBJECT')
            activeobjectdata = bpy.context.active_object.data
            for polygon in activeobjectdata.polygons:
                mlx = mly = mlz = None
                if self.algorithm == 0:
                    # сравнение максимальных длин проекций ребер на оси
                    for edge in polygon.edge_keys:
                        lx = math.fabs(activeobjectdata.vertices[edge[0]].co[0] - activeobjectdata.vertices[edge[1]].co[0])
                        mlx = lx if not mlx or lx > mlx else mlx
                        ly = math.fabs(activeobjectdata.vertices[edge[0]].co[1] - activeobjectdata.vertices[edge[1]].co[1])
                        mly = ly if not mly or ly > mly else mly
                        lz = math.fabs(activeobjectdata.vertices[edge[0]].co[2] - activeobjectdata.vertices[edge[1]].co[2])
                        mlz = lz if not mlz or lz > mlz else mlz
                elif self.algorithm == 1:
                    # сравнение максимальной проекции полигона на ось Z с максимальными проекциями ребер на оси
                    z_max = z_min = None
                    for vertex_id in polygon.vertices:
                        z_min = activeobjectdata.vertices[vertex_id].co[2] if not z_min or z_min > activeobjectdata.vertices[vertex_id].co[2] else z_min
                        z_max = activeobjectdata.vertices[vertex_id].co[2] if not z_max or z_max < activeobjectdata.vertices[vertex_id].co[2] else z_max
                    mlz = math.fabs(z_max - z_min)
                    for edge in polygon.edge_keys:
                        lx = math.fabs(activeobjectdata.vertices[edge[0]].co[0] - activeobjectdata.vertices[edge[1]].co[0])
                        mlx = lx if not mlx or lx > mlx else mlx
                        ly = math.fabs(activeobjectdata.vertices[edge[0]].co[1] - activeobjectdata.vertices[edge[1]].co[1])
                        mly = ly if not mly or ly > mly else mly
                if mlz >= mlx and mlz >= mly:
                    polygon.select = True
            bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

    # раскомментировать 3 след. строчки если нужна блокировка в объектном режиме
    # @classmethod
    # def poll(cls, context):
    #     return context.active_object.mode == 'EDIT'


def register():
    bpy.utils.register_class(Vertical)


def unregister():
    bpy.utils.unregister_class(Vertical)
