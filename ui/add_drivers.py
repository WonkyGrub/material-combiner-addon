import bpy

from ..icons import get_icon_id
from ..type_annotations import Scene
# from extend_types import target_collection

bpy.types.Scene.target_collection = bpy.props.StringProperty(name="Target Collection")

class OBJECT_OT_add_drivers_to_collection(bpy.types.Operator):
    bl_idname = "object.add_drivers_to_collection"
    bl_label = "Add Drivers to Collection"

    def add_driver(self, obj, prop, index, expression):
        # Create a driver for the given property
        driver = obj.driver_add(prop, index).driver
        driver.type = 'SCRIPTED'
        driver.expression = expression
        driver.use_self = True

        # print(f"Driver added to {obj.name}.{prop}[{index}] with expression: {expression}")

    def execute(self, context):
        collection_name = context.scene.target_collection  # Access target_collection from context.scene
        collection = bpy.data.collections.get(collection_name)

        if collection:
            for obj in collection.objects:
                if obj.type == 'LIGHT':  # Check if the object is a light
                    # Add drivers to light object properties
                    self.add_driver(obj, 'rotation_euler', 0, 'self.data.color[0]')
                    self.add_driver(obj, 'rotation_euler', 1, 'self.data.color[1]')
                    self.add_driver(obj, 'rotation_euler', 2, 'self.data.color[2]')
                    self.add_driver(obj, 'scale', 0, 'self.data.shadow_soft_size')
                    self.add_driver(obj, 'scale', 1, 'self.data.shadow_soft_size')
                    self.add_driver(obj, 'scale', 2, 'self.data.energy')
        return {'FINISHED'}
class OBJECT_PT_add_drivers_to_collection(bpy.types.Panel):
    bl_label = "Add Drivers to Collection"
    bl_idname = "OBJECT_PT_add_drivers_to_collection"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MatCombiner'

    def draw(self, context):
        # print('Draw method called')
        scn = context.scene
        layout = self.layout
        col = layout.column(align=True)

        # print('Target Collection:', scn.target_collection)
        col.label(text='Target Collection:')
        layout.prop_search(context.scene, "target_collection", bpy.data, "collections")
        row = col.row()
        row.scale_y = 1.2
        row.operator("object.add_drivers_to_collection", icon_value=get_icon_id('null'))

# \/ turned off as we have a registration function in registration.py
# need to ensure that this file is properly referenced within that, as well as init, addon updater, addon updater ops, etc.
# bpy.utils.register_class(OBJECT_OT_add_drivers_to_collection)
