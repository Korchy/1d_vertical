# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_vertical
#
# Version history:
#   1.0 (2018.02.01) - release
#   1.1 (2018.06.08) - improve - added Y and X axis
#   1.2 (2018.06.08) - improve - work in both object and edit mode
#   1.3 (2018.06.09) - improve - uv 90-deg rotation
#   1.4 (2018.06.09) - improve - rotate not selected uv polygons

bl_info = {
    'name': 'vertical',
    'category': 'Mesh',
    'author': 'Nikita Akimov',
    'version': (1, 4, 0),
    'blender': (2, 79, 0)
}

import bpy
import math


class Vertical(bpy.types.Operator):
    bl_idname = 'vertical.select'
    bl_label = 'Vertical: Select'
    bl_options = {'REGISTER', 'UNDO'}

    algorithm = bpy.props.IntProperty(name='algorithm', default=1)
    uv_rotation_angle = 90

    def execute(self, context):
        active = context.active_object
        mode = context.active_object.mode
        if context.active_object.mode == 'OBJECT':
            selection = context.selected_objects[:]
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            selection = [context.active_object]
        for obj in selection:
            self.selectVerticalPolygons(context, obj)
            if context.window_manager.interface_vars.rotate_uv:
                if context.window_manager.interface_vars.rotate_origin == '0':
                    UV.rotate_selection(obj, (0, 0), __class__.uv_rotation_angle)
                elif context.window_manager.interface_vars.rotate_origin == '1':
                    UV.rotate_selection(obj, UV.selection_center(obj), __class__.uv_rotation_angle)
        context.scene.objects.active = active
        bpy.ops.object.mode_set(mode=mode)
        return {'FINISHED'}

    def selectVerticalPolygons(self, context, obj):
        if obj:
            context.scene.objects.active = obj
            if context.active_object.mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(type='FACE')
            bpy.ops.object.mode_set(mode='OBJECT')
            activeobjectdata = obj.data
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
                # check vertical
                if context.window_manager.interface_vars.axis == 'Z' and mlz >= mlx and mlz >= mly:
                    polygon.select = True
                elif context.window_manager.interface_vars.axis == 'X' and mlx >= mlz and mlx >= mly:
                    polygon.select = True
                elif context.window_manager.interface_vars.axis == 'Y' and mly >= mlx and mly >= mlz:
                    polygon.select = True


class UV:
    @staticmethod
    def selection_center(obj=None):
        center = (0, 0)
        if obj:
            polygons_centers = []
            for polygon_index, polygon in enumerate(obj.data.polygons):
                if polygon.select:
                    x_list = [obj.data.uv_layers.active.data[loop_index].uv[0] for loop_index in polygon.loop_indices]
                    y_list = [obj.data.uv_layers.active.data[loop_index].uv[1] for loop_index in polygon.loop_indices]
                    length = len(polygon.loop_indices)
                    x = sum(x_list) / length
                    y = sum(y_list) / length
                    polygons_centers.append((x, y))
            x_list = [center[0] for center in polygons_centers]
            y_list = [center[1] for center in polygons_centers]
            length = len(polygons_centers)
            x = sum(x_list) / length
            y = sum(y_list) / length
            center = (x, y)
        return center

    @staticmethod
    def rotate_selection(obj, origin, angle):
        rot = __class__.make_rotation_transformation(math.radians(angle), origin)
        for polygon_index, polygon in enumerate(obj.data.polygons):
            if polygon.select != bpy.context.window_manager.interface_vars.rotate_uv_invert_selection:
                for i, loop_index in enumerate(polygon.loop_indices):
                    obj.data.uv_layers.active.data[loop_index].uv = rot(obj.data.uv_layers.active.data[loop_index].uv)

    @staticmethod
    def make_rotation_transformation(angle, origin=(0, 0)):
        cos_theta, sin_theta = math.cos(angle), math.sin(angle)
        x0, y0 = origin

        def xform(point):
            x, y = point[0] - x0, point[1] - y0
            return (x * cos_theta - y * sin_theta + x0,
                    x * sin_theta + y * cos_theta + y0)
        return xform


class InterfaceVars(bpy.types.PropertyGroup):
    axis = bpy.props.EnumProperty(
        items=[
            ('X', 'X', 'X', '', 0),
            ('Y', 'Y', 'Y', '', 1),
            ('Z', 'Z', 'Z', '', 2)
        ],
        default='Z'
    )
    rotate_uv = bpy.props.BoolProperty(
        name='UVRotate',
        description='Rotate UV of selected polygons to 90 deg',
        default=False
    )
    rotate_uv_invert_selection = bpy.props.BoolProperty(
        name='InvertSelection',
        description='Invert selection of rotating polygons',
        default=False
    )
    rotate_origin = bpy.props.EnumProperty(
        items=[
            ('0', '0,0', '0,0', '', 0),
            ('1', 'Selection center', 'Selection center', '', 1)
        ],
        default='0'
    )


class VerticalPanel(bpy.types.Panel):
    bl_idname = 'vertical.panel'
    bl_label = 'Vertical'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        button = self.layout.operator('vertical.select', text='Vertical 0')
        button.algorithm = 0
        button = self.layout.operator('vertical.select', text='Vertical 1')
        button.algorithm = 1
        row = self.layout.row()
        row.prop(context.window_manager.interface_vars, 'axis', expand=True)
        row = self.layout.row()
        row.prop(context.window_manager.interface_vars, 'rotate_uv')
        row.prop(context.window_manager.interface_vars, 'rotate_uv_invert_selection')
        row = self.layout.row()
        row.prop(context.window_manager.interface_vars, 'rotate_origin', expand=True)


def register():
    bpy.utils.register_class(Vertical)
    bpy.utils.register_class(VerticalPanel)
    bpy.utils.register_class(InterfaceVars)
    bpy.types.WindowManager.interface_vars = bpy.props.PointerProperty(type=InterfaceVars)


def unregister():
    del bpy.types.WindowManager.interface_vars
    bpy.utils.unregister_class(InterfaceVars)
    bpy.utils.unregister_class(VerticalPanel)
    bpy.utils.unregister_class(Vertical)


if __name__ == '__main__':
    register()
