# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
# https://github.com/Korchy/1d_vertical

import bpy


class VerticalPanel(bpy.types.Panel):
    bl_idname = 'vertical.panel'
    bl_label = 'Vertical'
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Vertical"

    def draw(self, context):
        button = self.layout.operator("vertical.select", text="Vertical Test 0")
        button.algorithm = 0
        button = self.layout.operator("vertical.select", text="Vertical Test 1")
        button.algorithm = 1


def register():
    bpy.utils.register_class(VerticalPanel)


def unregister():
    bpy.utils.unregister_class(VerticalPanel)
