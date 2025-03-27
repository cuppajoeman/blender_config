bl_info = {
    "name": "Auto Rename Baked Actions",
    "blender": (3, 0, 0),
    "category": "Animation",
    "description": "Automatically renames baked actions with a '_baked' suffix",
}

import bpy

class OBJECT_OT_bake_and_rename(bpy.types.Operator):
    """Bake Action and Rename"""
    bl_idname = "pose.bake_and_rename"
    bl_label = "Bake and Rename Action"
    bl_options = {'REGISTER', 'UNDO'}

    frame_start: bpy.props.IntProperty(name="Start Frame", default=1)
    frame_end: bpy.props.IntProperty(name="End Frame", default=250)
    only_selected: bpy.props.BoolProperty(name="Only Selected", default=True)
    visual_keying: bpy.props.BoolProperty(name="Visual Keying", default=True)
    clear_constraints: bpy.props.BoolProperty(name="Clear Constraints", default=True)
    clear_parents: bpy.props.BoolProperty(name="Clear Parents", default=False)
    use_current_action: bpy.props.BoolProperty(name="Use Current Action", default=True)

    def execute(self, context):
        baked_actions = {}

        for obj in context.selected_objects:
            if obj.type == 'ARMATURE' and obj.animation_data and obj.animation_data.action:
                original_action = obj.animation_data.action
                original_name = original_action.name
                baked_name = f"{original_name}_baked"
                baked_actions[obj] = (original_name, baked_name)
                
                if original_action.frame_range:
                    self.frame_end = int(original_action.frame_range[1])

        bpy.ops.nla.bake(frame_start=self.frame_start, frame_end=self.frame_end, 
                          only_selected=self.only_selected, visual_keying=self.visual_keying, 
                          clear_constraints=self.clear_constraints, clear_parents=self.clear_parents, 
                          use_current_action=self.use_current_action, bake_types={'POSE'})
        
        for obj, (original_name, baked_name) in baked_actions.items():
            if obj.animation_data and obj.animation_data.action:
                baked_action = obj.animation_data.action
                if baked_action.name != original_name:
                    existing_action = bpy.data.actions.get(baked_name)
                    if existing_action:
                        bpy.data.actions.remove(existing_action)
                    baked_action.name = baked_name
        
        return {'FINISHED'}

    def invoke(self, context, event):
        for obj in context.selected_objects:
            if obj.type == 'ARMATURE' and obj.animation_data and obj.animation_data.action:
                self.frame_end = int(obj.animation_data.action.frame_range[1])
                break
        return context.window_manager.invoke_props_dialog(self)


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_bake_and_rename.bl_idname, text="Bake Action with Rename")


def register():
    bpy.utils.register_class(OBJECT_OT_bake_and_rename)
    bpy.types.VIEW3D_MT_pose.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_bake_and_rename)
    bpy.types.VIEW3D_MT_pose.remove(menu_func)


if __name__ == "__main__":
    register()
