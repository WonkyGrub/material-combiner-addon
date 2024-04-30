import bpy

from .. import globs
from ..icons import get_icon_id
from ..type_annotations import Scene

class MaterialMenu(bpy.types.Panel):
    bl_label = 'Main Menu'
    bl_idname = 'SMC_PT_Main_Menu'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if globs.is_blender_2_80_or_newer else 'TOOLS'
    bl_category = 'MatCombiner'

    def draw(self, context: bpy.types.Context) -> None:
        scn = context.scene
        layout = self.layout
        col = layout.column(align=True)
        if globs.pil_exist:
            self._materials_list(col, scn, layout)
        elif globs.smc_pi:
            col = col.box().column()
            col.label(text='Installation complete', icon_value=get_icon_id('done'))
            col.label(text='Please restart Blender', icon_value=get_icon_id('null'))
        else:
            self.pillow_installator(col)

    @staticmethod
    def _materials_list(col: bpy.types.UILayout, scn: Scene, layout: bpy.types.UIList) -> None:
        col.label(text='Materials to combine:')
        col.template_list('SMC_UL_Combine_List', 'combine_list', scn, 'smc_ob_data',
                          scn, 'smc_ob_data_id', rows=12, type='DEFAULT')
        col = col.column(align=True)
        col.scale_y = 1.2
        col.operator('smc.refresh_ob_data',
                     text='Update Material List' if scn.smc_ob_data else 'Generate Material List',
                     icon_value=get_icon_id('null'))
        col = layout.column()
        col.label(text='Properties:')
        box = col.box()
        box.scale_y = 1.2
        box.prop(scn, 'smc_size')
        if scn.smc_size in ['CUST', 'STRICTCUST']:
            box.prop(scn, 'smc_size_width')
            box.prop(scn, 'smc_size_height')
        box.scale_y = 1.2
        box.prop(scn, 'smc_crop')
        box.scale_y = 1.2
        box.prop(scn, 'smc_pixel_art')
        row = box.row()
        col = row.column()
        col.scale_y = 1.2
        col.label(text='Size of materials without image')
        col = row.column()
        col.scale_x = .75
        col.scale_y = 1.2
        col.alignment = 'RIGHT'
        col.prop(scn, 'smc_diffuse_size', text='')
        row = box.row()
        col = row.column()
        col.scale_y = 1.2
        col.label(text='Size of gaps between images')
        col = row.column()
        col.scale_x = .75
        col.scale_y = 1.2
        col.alignment = 'RIGHT'
        col.prop(scn, 'smc_gaps', text='')
        col = layout.column()
        col.scale_y = 1.5
        col.operator('smc.combiner', text='Save Atlas to..', icon_value=get_icon_id('null')).cats = False

    @staticmethod
    def pillow_installator(col: bpy.types.UILayout) -> None:
        discord = 'https://discordapp.com/users/275608234595713024'

        col.label(text='Python Imaging Library required to continue')
        col.separator()
        row = col.row()
        row.scale_y = 1.5
        row.operator('smc.get_pillow', text='Install Pillow', icon_value=get_icon_id('download'))
        col.separator()
        col.separator()
        col = col.box().column()
        col.label(text='If the installation process is repeated'
                       '\ntry to run Blender as Administrator'
                       '\nor check your Internet Connection.')
        col.separator()
        col.label(text='If the error persists, contact me on Discord for a manual installation:')
        col.operator('smc.browser', text='shotariya#4269', icon_value=get_icon_id('help')).link = discord

    class OBJECT_OT_add_drivers_to_collection(bpy.types.Operator):
        bl_idname = "object.add_drivers_to_collection"
        bl_label = "Add Drivers to Collection"

        def execute(self, context):
            collection_name = context.scene.target_collection
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

    class OBJECT_PT_add_drivers_to_collection(bpy.types.Panel):
        bl_label = "Add Drivers to Collection"
        bl_idname = "OBJECT_PT_add_drivers_to_collection"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Tool'

        def draw(self, context):
            layout = self.layout
            scene = context.scene

            layout.prop_search(scene, "target_collection", bpy.data, "collections")
            layout.operator("object.add_drivers_to_collection")

    bpy.types.Scene.target_collection = bpy.props.StringProperty(name="Target Collection")
    # del bpy.types.Scene.target_collection
