# Nikita Akimov
# interplanety@interplanety.org

import bpy


class VerticalPanel(bpy.types.Panel):
    bl_idname = 'vertical.panel'
    bl_label = 'Vertical'
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Vertical"

    def draw(self, context):
        self.layout.operator("vertical.select", text="Vertical Test")


def register():
    bpy.utils.register_class(VerticalPanel)


def unregister():
    bpy.utils.unregister_class(VerticalPanel)
