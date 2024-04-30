import bpy

class OBJECT_OT_add_drivers(bpy.types.Operator):
    bl_idname = "object.add_drivers"
    bl_label = "Add Custom Drivers"

    def execute(self, context):
        collection = context.collection  # Get the current collection
        for obj in collection.objects:
            # Add drivers to 'obj' here
            self.add_driver(obj, 'rotation_euler', 0, 'self.data.color[0]')
            self.add_driver(obj, 'rotation_euler', 1, 'self.data.color[1]')
            self.add_driver(obj, 'rotation_euler', 2, 'self.data.color[2]')
            self.add_driver(obj, 'scale', 0, 'self.data.shadow_soft_size')
            self.add_driver(obj, 'scale', 1, 'self.data.shadow_soft_size')
            self.add_driver(obj, 'scale', 2, 'self.data.energy')
        return {'FINISHED'}

    def add_driver(self, obj, prop, index, expression):
        # Get the property that the driver will be added to
        prop_group = eval('obj.' + prop)

        # Add the driver
        driver = prop_group.driver_add(index).driver
        driver.use_self = True
        driver.expression = expression