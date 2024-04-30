import bpy

from ..icons import get_icon_id
from ..type_annotations import Scene
from .extend_types import target_collection

bpy.types.Scene.target_collection = bpy.props.StringProperty(name="Target Collection")

class OBJECT_OT_add_drivers_to_collection(bpy.types.Operator):
    bl_idname = "object.add_drivers_to_collection"
    bl_label = "Add Drivers to Collection"

    def add_driver(self, obj, prop, index, expression):
        # Rest of the code...
        print(f"Driver added to {prop}[{index}] with expression: {expression}")  # Debug print statementdef add_driver(self, obj, prop, index, expression):
        # Get the property that the driver will be added to
        prop_group = eval('obj.' + prop)

        # Add the driver
        driver = prop_group.driver_add(index).driver
        driver.expression = expression  # Set the expression for the driver
        driver.use_self = True  # Enable "Use Self"

        print(f"Driver added to {prop}[{index}] with expression: {expression}")  # Debug print statement
    # Register the operator

    def execute(self, context):
        collection_name = target_collection
        collection = bpy.data.collections.get(collection_name)
        if collection is not None:
            for obj in collection.objects:
                # Add drivers to 'obj' here
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
        print('Draw method called')
        scn = context.scene
        layout = self.layout
        col = layout.column(align=True)
    
        print('Target Collection:', scn.target_collection)
        col.label(text='Target Collection:')
        col.prop_search(scn, "target_collection", bpy.data, "collections")
        row = col.row()
        row.scale_y = 1.2
        row.operator("object.add_drivers_to_collection", icon_value=get_icon_id('null'))

# \/ turned off as we have a registration function in registration.py
# need to ensure that this file is properly referenced within that, as well as init, addon updater, addon updater ops, etc.
# bpy.utils.register_class(OBJECT_OT_add_drivers_to_collection)
