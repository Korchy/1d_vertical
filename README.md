# 1D Vertical

Blender add-on to search and select the vertical polygons of the mesh.

Installation
-
User Preferences - Add-ons - Install Add-on from File - select downloaded archive

Usage
-

Two buttons - different algorithms:
- Vertical 0 - checks the length of the maximum projection of the edge of the polygon on the Z axis
- Vertical 1 - checks the maximum projection of the whole polygon on the Z axis

Location
-
3D_View window - T-tab - "Vertical" panel

Including
-
You need the module vertical.py

Register this module in your add-on (with calling the "register" function)

Use it by calling the operator:

    bpy.ops.vertical.select()

The default algorithm is number 1. To call the operator with the second algorithm, specify it in the operator parameters:

    bpy.ops.vertical.select(algorithm=0)

Version history:
-
1.0.0
- Integrated to the NA 1D Tools

0.0.0
- Dev start