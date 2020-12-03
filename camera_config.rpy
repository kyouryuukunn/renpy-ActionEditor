init -1600 python:

    ##########################################################################
    # Camera functions
    _camera_focus = 1848.9 #default camera WD
    _camera_dof = 9999999 #default dof value
    _camera_blur_amount = 1.0 #The blur value where the distance from focus position is dof.
    _camera_blur_warper = "linear" #warper function name which is used for the distance from focus position and blur amount.
    _FOCAL_LENGTH = 147.40 #default focus position
    _LAYER_Z = 1848.9 #default z value of 3D layer

init -1600 python in _viewers:
    # If True, show rot default.
    default_rot = False
    # If True, set camera keymap FPS(wasd), otherwise vim(hjkl)
    fps_keymap = False
    default_warper = "linear"
