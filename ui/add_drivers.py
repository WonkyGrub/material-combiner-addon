import bpy

from ..icons import get_icon_id
from ..type_annotations import Scene
# from extend_types import target_collection

bpy.types.Scene.target_collection = bpy.props.StringProperty(name="Target Collection")

class OBJECT_OT_add_drivers_to_collection(bpy.types.Operator):
    bl_idname = "object.add_drivers_to_collection"
    bl_label = "Add Drivers to Collection"

    def add_driver(self, obj, prop, index, expression):
        # Ensure the object has animation data
        if not obj.animation_data:
            obj.animation_data_create()

        if prop in ['rotation_euler', 'scale']:
            driver = prop_group.driver_add('x').driver
            driver.expression = expression  # Set the expression for the driver
            driver.use_self = True  # Enable "Use Self"
            driver = prop_group.driver_add('y').driver
            driver.expression = expression  # Set the expression for the driver
            driver.use_self = True  # Enable "Use Self"
            driver = prop_group.driver_add('z').driver
            driver.expression = expression  # Set the expression for the driver
            driver.use_self = True  # Enable "Use Self"
        else:
            driver = prop_group.driver_add().driver
            driver.expression = expression  # Set the expression for the driver
            driver.use_self = True  # Enable "Use Self"

        print(f"Driver added to {obj.name}.{prop}[{index}] with expression: {expression}")  # Debug print statement

    def execute(self, context):
        collection_name = context.scene.target_collection  # Access target_collection from context.scene
        collection = bpy.data.collections.get(collection_name)

        if collection:
            for obj in collection.objects:
                if obj.type == 'LIGHT':  # Check if the object is a light
                    # Add drivers to light object properties
                    self.add_driver(obj, 'rotation_euler', 0, 'self.location.x')
                    self.add_driver(obj, 'rotation_euler', 1, 'self.location.y')
                    self.add_driver(obj, 'rotation_euler', 2, 'self.location.z')
                    self.add_driver(obj, 'scale', 0, 'self.scale.x')
                    self.add_driver(obj, 'scale', 1, 'self.scale.y')
                    self.add_driver(obj, 'scale', 2, 'self.scale.z')
        return {'FINISHED'}

class OBJECT_PT_add_drivers_to_collection(bpy.types.Panel):
    bl_label = "Add Drivers to Collection"
    bl_idname = "OBJECT_PT_add_drivers_to_collection"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MatCombiner'

    def draw(self, context):
        print('Draw method called')
        scn = context.scene
        layout = self.layout
        col = layout.column(align=True)

        print('Target Collection:', scn.target_collection)
        col.label(text='Target Collection:')
        col.prop(scn, "target_collection")  # Add a property UI element for scn.target_collection
        row = col.row()
        row.scale_y = 1.2
        row.operator("object.add_drivers_to_collection", icon_value=get_icon_id('null'))

# \/ turned off as we have a registration function in registration.py
# need to ensure that this file is properly referenced within that, as well as init, addon updater, addon updater ops, etc.
# bpy.utils.register_class(OBJECT_OT_add_drivers_to_collection)
