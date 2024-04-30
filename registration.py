from typing import Dict
from typing import Union

import bpy

from . import addon_updater_ops
from . import extend_lists
from . import extend_types
from . import globs
from . import operators
from . import ui
from .icons import initialize_smc_icons
from .icons import unload_smc_icons
from .type_annotations import BlClasses

__bl_classes = [
    ui.credits_menu.CreditsMenu,
    ui.main_menu.MaterialMenu,
    # ui.main_menu.MaterialMenu.OBJECT_OT_add_drivers_to_collection,
    ui.property_menu.PropertyMenu,
    ui.update_menu.UpdateMenu,
    
    operators.combiner.Combiner,
    operators.combine_list.RefreshObData,
    operators.combine_list.CombineSwitch,
    operators.multicombine_list.MultiCombineColor,
    operators.multicombine_list.MultiCombineImageAdd,
    operators.multicombine_list.MultiCombineImageMove,
    operators.multicombine_list.MultiCombineImagePath,
    operators.multicombine_list.MultiCombineImageReset,
    operators.multicombine_list.MultiCombineImageRemove,
    operators.browser.OpenBrowser,
    operators.get_pillow.InstallPIL,

    extend_types.CombineList,
    extend_types.UpdatePreferences,

    extend_lists.SMC_UL_Combine_List,
]


def register_all(bl_info: Dict[str, Union[str, tuple]]) -> None:
    _register_classes()
    initialize_smc_icons()
    addon_updater_ops.register(bl_info)
    addon_updater_ops.check_for_update_background()
    extend_types.register()


def unregister_all() -> None:
    _unregister_classes()
    unload_smc_icons()
    addon_updater_ops.unregister()
    extend_types.unregister()


def _register_classes() -> None:
    count = 0
    for cls in __bl_classes:
        make_annotations(cls)
        try:
            bpy.utils.register_class(cls)
            count += 1
        except ValueError as e:
            print('Error:', cls, e)
    print('Registered', count, 'Material Combiner classes.')
    if count < len(__bl_classes):
        print('Skipped', len(__bl_classes) - count, 'Material Combiner classes.')


def _unregister_classes() -> None:
    count = 0
    for cls in reversed(__bl_classes):
        try:
            bpy.utils.unregister_class(cls)
            count += 1
        except (ValueError, RuntimeError) as e:
            print('Error:', cls, e)
    print('Unregistered', count, 'Material Combiner classes.')


def make_annotations(cls: BlClasses) -> BlClasses:
    if globs.is_blender_2_79_or_older:
        return cls

    if bpy.app.version >= (2, 93, 0):
        bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, bpy.props._PropertyDeferred)}
    else:
        bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}

    if bl_props:
        if '__annotations__' not in cls.__dict__:
            setattr(cls, '__annotations__', {})

        annotations = cls.__dict__['__annotations__']

        for k, v in bl_props.items():
            annotations[k] = v
            delattr(cls, k)

    return cls
