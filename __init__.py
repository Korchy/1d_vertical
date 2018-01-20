# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
# https://github.com/Korchy/1d_vertical

bl_info = {
    'name': 'vertical',
    'category': 'Mesh',
    'author': 'Nikita Akimov',
    'version': (0, 0, 0),
    'blender': (2, 79, 0)
}

from . import vertical
from . import vertical_panel


def register():
    vertical.register()
    vertical_panel.register()


def unregister():
    vertical.unregister()
    vertical_panel.unregister()


if __name__ == '__main__':
    register()
