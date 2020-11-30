
init 1600:
    if getattr(store, "_3d_layers", None):
        default _3d_layers = _3d_layers
    else:
        default _3d_layers = {"master":_LAYER_Z}
init -1599 python:

    ##########################################################################
    # Camera functions
    _camera_x = 0
    _camera_y = 0
    _camera_z = 0
    _camera_rotate = 0
    _last_camera_arguments = None

    def register_3d_layer(*layers):
        """
         :doc: camera

         Register layers as 3D layers. Only 3D layers will be affected by camera
         movement and 3D layer transforms. This should be called in an init
         block. If no layers are registered as 3D layers, the 'master' layer
         will become a 3D layer by default.

         `layers`
              This should be a string or a group of strings naming registered layers.
         """
        global _3d_layers
        _3d_layers = {layer:_LAYER_Z for layer in layers}

    def camera_reset():
        """
         :doc: camera

         Resets the camera, 3D layers positions and the focus position, the depth of field.
         """
        for layer in _3d_layers:
            layer_move(layer, _LAYER_Z)
        camera_move(0, 0, 0)
        focus_set(1000)
        dof_set(9999999)

    def camera_restore():
        """
         :doc: camera

         Safety method used internally to deal with unexpected behavior.

         """
        camera_move(_camera_x, _camera_y, _camera_z)

    def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, **kwargs):
        """
         :doc: camera

         Moves the camera to a given coordinate and rotation.

         `x`
              The x coordinate to move the camera to.
         `y`
              The y coordinate to move the camera to.
         `z`
              The z coordinate to move the camera to.
         `rotate`
              Rotation of the camera, perpindicular to the scene, in degrees.
         `duration`
              The time, in seconds, to complete the camera move. If no time is given,
              the move will happen instantaneously.
         `warper`
              A string that points to a registered ATL warper, like \'ease\'.
              If no warper is given, this will default to \'linear\'.
         `subpixel`
              If True, transforms caused by the 3D camera will be rendered with
              subpixel precision. This defaults to True.
         `loop`
              If true, the camera move will continually loop until another camera
              action interrupts. This defaults to False.
         `x_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the x coordinate of the camera.
         `y_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the y coordinate of the camera.
         `z_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the z coordinate of the camera.
         `rotate_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the rotation value of the camera.
         `<layer name>_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the coordinate of the given layer.
         """

        camera_moves([(x, y, z, rotate, duration, warper, ),], subpixel=subpixel, loop=loop, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express, **kwargs)

    def camera_relative_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, **kwargs):
        """
         :doc: camera

         Move the coordinate and rotate of a camera relatively and apply transforms to all 3D layers.

         `x`
              the x coordinate of a camera relative to the current one.
         `y`
              the y coordinate of a camera relative to the current one.
         `z`
              the z coordinate of a camera relative to the current one.
         `rotate`
              Defaul 0, the rotate of a camera relative to the current one.
         `duration`
              Default 0, this is the second times taken to move a camera.
         `warper`
              Default 'linear', this should be string and the name of a warper
              registered with ATL.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         `loop`
              Default False, if True, this motion repeats.
         'x_express'
             This should be callable, which is called with the shown timebase
             and the animation timebase, in seconds and return a number. The
             result of this is added to the x coordinate of the camera.
         'y_express'
             This should be callable, which is called with the shown timebase
             and the animation timebase, in seconds and return a number. The
             result of this is added to the y coordinate of the camera.
         'z_express'
             This should be callable, which is called with the shown timebase
             and the animation timebase, in seconds and return a number. The
             result of this is added to the z coordinate of the camera.
         'rotate_express'
             This should be callable, which is called with the shown timebase
             and the animation timebase, in seconds and return a number. The
             result of this is added to the rotate coordinate of the camera.
         `<layer name>_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the coordinate of the given layer.
         """
        camera_move(x+_camera_x, y+_camera_y, z+_camera_z, rotate+_camera_rotate, duration, warper, subpixel, loop, x_express, y_express, z_express, rotate_express, **kwargs)


    def camera_moves(check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None, spline=False, **kwargs):
        """
         :doc: camera

         Allows multiple camera moves to happen in succession.

         `check_points`
              A list of camera moves, in the format of (x, y, z, rotate, duration, warper)
         `loop`
              If true, the camera moves will continually loop until another camera
              action interrupts. This defaults to False.
         `subpixel`
              If True, transforms caused by the 3D camera will be rendered with
              subpixel precision. This defaults to True.
         `x_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the x coordinate of the camera.
         `y_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the y coordinate of the camera.
         `z_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the z coordinate of the camera.
         `rotate_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the rotation value of the camera.
         `<layer name>_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the coordinate of the given layer.
         `spline`
             Enable spline interpolation for the coordinates of the camera. If this is True, warpers are ignored. This defaults to False.
         """
        camera_check_points = {}
        camera_check_points["x"] = []
        camera_check_points["y"] = []
        camera_check_points["z"] = []
        camera_check_points["rotate"] = []
        for x, y, z, rotate, duration, warper in check_points:
            camera_check_points["x"].append((x, duration, warper))
            camera_check_points["y"].append((y, duration, warper))
            camera_check_points["z"].append((z, duration, warper))
            camera_check_points["rotate"].append((rotate, duration, warper))
        kwargs["x_loop"]=loop
        kwargs["y_loop"]=loop
        kwargs["z_loop"]=loop
        kwargs["rotate_loop"]=loop
        all_moves(camera_check_points=camera_check_points, loop=loop, subpixel=subpixel, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express, camera_spline=spline, **kwargs)

    def camera_relative_moves(relative_check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None, spline=False, **kwargs):
        """
         :doc: camera

         Allows relative multiple camera moves to happen in succession.

         `relative_check_points`
              A list of camera moves, in the format of (x, y, z, rotate, duration, warper)
         `loop`
              If true, the camera moves will continually loop until another camera
              action interrupts. This defaults to False.
         `subpixel`
              If True, transforms caused by the 3D camera will be rendered with
              subpixel precision. This defaults to True.
         `x_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the x coordinate of the camera.
         `y_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the y coordinate of the camera.
         `z_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the z coordinate of the camera.
         `rotate_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the rotation value of the camera.
         `<layer name>_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the coordinate of the given layer.
         `spline`
             Enable spline interpolation for the coordinates of the camera. If this is True, warpers are ignored. This defaults to False.
         """
        for i in len(relative_check_points):
            relative_check_points[i] = (
                    relative_check_points[i][0]+_camera_x, 
                    relative_check_points[i][1]+_camera_y, 
                    relative_check_points[i][2]+_camera_z, 
                    relative_check_points[i][3]+_camera_rotate, 
                    relative_check_points[i][4], 
                    relative_check_points[i][5]
                    ) 
        camera_moves(relative_check_points, loop=loop, subpixel=subpixel, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express, spline=spline, **kwargs)


    def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, layer_express=None):
        """
         :doc: camera

         Moves the z coordinate of a layer and applies a transform to the layer.

         `layer`
              A string that names a registered 3D layer to be moved.
         `z`
              The z coordinate to move the 3D layer to.
         `duration`
              The time, in seconds, to complete the layer move. If no time is given,
              the move will happen instantaneously.
         `warper`
              A string that points to a registered ATL warper, like \'ease\'.
              If no warper is given, this will default to \'linear\'.
         `subpixel`
              If True, the resulting layer move will be rendered with
              subpixel precision. This defaults to True.
         `loop`
              If true, the layer move will continually loop until another camera
              action interrupts. This defaults to False.
         `x_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the x coordinate of the camera.
         `y_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the y coordinate of the camera.
         `z_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the z coordinate of the camera.
         `rotate_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the rotation value of the camera.
         `layer_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the coordinate of the layer.
         """

        layer_moves(layer, [(z, duration, warper, ),], subpixel=subpixel, loop=loop, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express, layer_express=layer_express)


    def layer_moves(layer, check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None, layer_express=None, spline=False):
        """
         :doc: camera

         Move a layer through check points and apply transform to the layer.

         `layer`
              A string that names a registered 3D layer to be moved.
         `check_points`
              A list of layer moves, in the format of (z, duration, warper)
         `loop`
              If true, the layer moves will continually loop until another camera
              action interrupts. This defaults to False.
         `subpixel`
              If True, the resulting layer moves will be rendered with
              subpixel precision. This defaults to True.
         `layer_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the coordinate of the layer.
         `x_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the x coordinate of the camera.
         `y_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the y coordinate of the camera.
         `z_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the z coordinate of the camera.
         `rotate_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the rotation value of the camera.
         `spline`
             Enable spline interpolation for the coordinates of the layer. If this is True, warpers are ignored. This defaults to False.
         """
        all_moves(layer_check_points={layer:check_points}, subpixel=subpixel, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express, **{layer+"_loop":loop, layer+"_spline":spline, layer+"_express":layer_express})


    def focus_set(focus, duration=0, warper='linear', **kwargs):
        """
         :doc: camera

         Set the focus position.

         `focus`
              `focus` decides the focus position. It is the z coordinate which is sum of this value and 
              the z coordinate of camera.
         `duration`
              The time, in seconds, to complete the focus change. If no time is given,
              the change will happen instantaneously.
         `warper`
              A string that points to a registered ATL warper, like \'ease\'.
              If no warper is given, this will default to \'linear\'.
         """

        all_moves(focus_check_points={"focus": [(focus, duration, warper, ), ]}, **kwargs)

    def dof_set(dof, duration=0, warper='linear', **kwargs):
        """
         :doc: camera

         Set the depth of field.

         `dof`
              `dof` is the z range where layers aren't blured. it defaults to 9999999.
         `duration`
              The time, in seconds, to complete the dof change. If no time is given,
              the change will happen instantaneously.
         `warper`
              A string that points to a registered ATL warper, like \'ease\'.
              If no warper is given, this will default to \'linear\'.
         """

        all_moves(focus_check_points={"dof": [(dof, duration, warper, ), ]}, **kwargs)

    def all_moves(camera_check_points=None, layer_check_points=None, focus_check_points=None, subpixel=True, play=True, x_loop=False, y_loop=False, z_loop=False, rotate_loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, camera_spline=False, **kwargs):
        """
         :doc: camera

         Allows for both camera moves and layer moves to happen within the same interaction, in any given combination. The Action Editor will usually generate these.

         `camera_check_points`
             A list of check points for the camera to go through, split by coordinate in the following format:
              {
                  'x':[(x, duration, warper)...]
                  'y':[(y, duration, warper)...]
                  'z':[(z, duration, warper)...]
                  'rotate':[(rotate, duration, warper)...]
              }
         `layer_check_points`
             A list of check points for layers to go through, in the following format:
              {
                  'layer name':[(z, duration, warper)...]
              }
         `focus_check_points`
             A list of check points for the depth of field & the focus position,
             in the following format:
              {
                  'focus':[(z, duration, warper)...]
                  'dof':[(dof, duration, warper)...]
              }
            `dof` is the z range where layers aren't blured. it defaults to 9999999.
            `focus` decides the focus position. It is the z coordinate which is sum of this value and 
            the z coordinate of camera.
         `x_loop`
              If True, all x coordinate check points will loop continuously. This defaults to False.
         `y_loop`
              If True, all y coordinate check points will loop continuously. This defaults to False.
         `z_loop`
              If True, all z coordinate check points will loop continuously. This defaults to False.
         `rotate_loop`
              If True, all rotation check points will loop continuously. This defaults to False.
         `subpixel`
              If True, all transforms caused by this function will be drawn with subpixel precision. This defaults to True.
         `<layer name>_loop`
              If True, all layer move check points for the given layer will loop continuously. This defaults to False.
         `x_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the x coordinate of the camera.
         `y_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the y coordinate of the camera.
         `z_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the z coordinate of the camera.
         `rotate_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the rotation value of the camera.
         `<layer name>_express`
             This should be a callable function that is called with the shown 
             timebase and is given an animation timebase in seconds. The
             result of this function is added to the coordinate of the given layer.
         `camera_spline`
             Enable spline interpolation for the coordinates of the camera. If this is True, warpers are ignored. This defaults to False.
         `<layer name>_spline`
             Enable spline interpolation for the coordinates of the given layer. If this is True, warpers are ignored. This defaults to False.
         """
        global _camera_x, _camera_y, _camera_z, _camera_rotate, _camera_focus, _camera_dof, _3d_layers, _last_camera_arguments
        from math import sin, pi
        from random import random

        if camera_check_points is None:
            camera_check_points = {}
        if layer_check_points is None:
            layer_check_points = {}
        if focus_check_points is None:
            focus_check_points = {}
        if config.developer:
            _last_camera_arguments = (camera_check_points, layer_check_points, focus_check_points, x_loop, y_loop, z_loop, rotate_loop, x_express, y_express, z_express, rotate_express, kwargs, _camera_x, _camera_y, _camera_z, _camera_rotate, _3d_layers.copy(), camera_spline, _camera_focus, _camera_dof)
        start_xanchor = _FOCAL_LENGTH*_camera_x/(renpy.config.screen_width *_LAYER_Z) + .5
        start_yanchor = _FOCAL_LENGTH*_camera_y/(renpy.config.screen_height*_LAYER_Z) + .5
        camera_check_points2 = { 'xanchor':[(start_xanchor, 0, None, )], 'yanchor':[(start_yanchor, 0, None, )], 'z': [(_camera_z, 0, None, )], 'rotate':[(_camera_rotate, 0, None, )] }

        for coordinate in ["x", "y", "z", "rotate"]:
            if coordinate not in camera_check_points:
                camera_check_points[coordinate] = [(getattr(renpy.store, "_camera_"+coordinate), 0, None, )]
        for c in camera_check_points['x']:
            camera_check_points2['xanchor'].append((_FOCAL_LENGTH*c[0]/(renpy.config.screen_width *_LAYER_Z) + .5, c[1], c[2], ))
        for c in camera_check_points['y']:
            camera_check_points2['yanchor'].append((_FOCAL_LENGTH*c[0]/(renpy.config.screen_height *_LAYER_Z) + .5, c[1], c[2], ))
        camera_check_points2['z'].extend(camera_check_points['z'])
        camera_check_points2['rotate'].extend(camera_check_points['rotate'])
        for i in ["focus", "dof"]:
            if i not in focus_check_points:
                focus_check_points[i] = [(getattr(renpy.store, "_camera_"+i), 0, None, )]
        if camera_spline:
            camera_check_points2 = _ready_spline_camera_interpolation(camera_check_points2)
        for layer in _3d_layers:

            if layer not in layer_check_points:
                layer_check_points[layer] = [(_3d_layers[layer], 0, None), ]
            layer_check_points2 = [(_3d_layers[layer], 0, None), ]
            for c in layer_check_points[layer]:
                layer_check_points2.append((c[0], float(c[1]), c[2]))
            layer_loop = kwargs.get(layer+"_loop", False)
            layer_express = kwargs.get(layer+"_express", None)
            if kwargs.get(layer+"_spline", False):
                layer_check_points2 = _ready_spline_layer_interpolation(layer_check_points2)

            if play:
                renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(function=renpy.curry(_camera_trans)(camera_check_points=camera_check_points2, layer_check_points=layer_check_points2, focus_check_points=focus_check_points, subpixel=subpixel, layer_loop=layer_loop, x_loop=x_loop, y_loop=y_loop, z_loop=z_loop, rotate_loop=rotate_loop, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express, layer_express=layer_express))])
                layer_z = layer_check_points2[-1][0]
            else:
                # This is used when the time bar is changed by Action Editor
                st = _viewers.time
                xanchor = get_at_time(camera_check_points2['xanchor'], st, x_loop)
                yanchor = get_at_time(camera_check_points2['yanchor'], st, y_loop)
                z = get_at_time(camera_check_points2['z'], st, z_loop)
                rotate = get_at_time(camera_check_points2['rotate'], st, rotate_loop)
                focus = get_at_time(focus_check_points['focus'], st, False)
                dof = get_at_time(focus_check_points['dof'], st, False)
                layer_z = get_at_time(layer_check_points2, st, layer_loop)
                if x_express:
                    xanchor += _FOCAL_LENGTH*x_express(st, st)/(renpy.config.screen_width *_LAYER_Z)
                if y_express:
                    yanchor += _FOCAL_LENGTH*y_express(st, st)/(renpy.config.screen_height *_LAYER_Z)
                if z_express:
                    z += z_express(st, st)
                if rotate_express:
                    rotate += rotate_express(st, st)
                if layer_express:
                    layer_z += layer_express(st, st)
                distance = float(layer_z - z)
                if distance == 0:
                    distance = .1
                if distance >= 0:
                    alpha = 1
                    zoom = _LAYER_Z / distance
                    focus_distance = abs(layer_z - focus - z)
                    if dof == 0:
                        _dof = 0.1
                    else:
                        _dof = dof
                    blur_amount = _camera_blur_amount * renpy.atl.warpers[_camera_blur_warper](focus_distance/(_dof))
                    if blur_amount <= 1.0:
                        blur_amount = None
                    renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(xpos=.5, ypos=.5, alpha=alpha, transform_anchor=True, xanchor=xanchor, yanchor=yanchor, zoom=zoom, rotate=rotate, blur=blur_amount)])
                else:
                    alpha = 0
                    renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(xpos=.5, ypos=.5, alpha=alpha, transform_anchor=True, xanchor=xanchor, yanchor=yanchor, rotate=rotate, rotate_pad=False, blur=None)])

            _3d_layers[layer] = int(layer_z)
        if play:
            _camera_x = camera_check_points['x'][-1][0]
            _camera_y = camera_check_points['y'][-1][0]
            _camera_z = camera_check_points['z'][-1][0]
            _camera_rotate = camera_check_points['rotate'][-1][0]
            _camera_focus = focus_check_points['focus'][-1][0]
            _camera_dof = focus_check_points['dof'][-1][0]
        else:
            _camera_x         = int(((xanchor-.5)*renpy.config.screen_width*_LAYER_Z)/_FOCAL_LENGTH)
            _camera_y         = int(((yanchor-.5)*renpy.config.screen_height*_LAYER_Z)/_FOCAL_LENGTH)
            _camera_z         = int(z)
            _camera_rotate    = int(rotate)
            _camera_focus     = int(focus)
            _camera_dof       = int(dof)

    def _camera_trans(tran, st, at, camera_check_points, layer_check_points, focus_check_points, layer_loop, x_loop, y_loop, z_loop, rotate_loop, subpixel, x_express, y_express, z_express, rotate_express, layer_express):
        if not (layer_loop or x_loop or y_loop or z_loop or rotate_loop or x_express or y_express or z_express or rotate_express or layer_express):
            for check_point in camera_check_points.items():
                if check_point[-1][1] and  check_point[-1][1] >= st:
                    break
            else:
                for check_point in layer_check_points.items():
                    if check_point[-1][1] and  check_point[-1][1] >= st:
                            break
                    else:
                        for check_point in focus_check_points.items():
                            if check_point[-1][1] and  check_point[-1][1] >= st:
                                break
                        else:
                            return
        # camera_check_points = {xanchor:(value, duration, warper), yanchor, z, rotate}
        # layer_check_points = (layer_z, duration, warper)
        # focus_check_points = {focus: (value, duration, warper), dof: (value, duration, warper)}
        from math import sin, pi
        from random import random
        tran.xpos    = .5 
        tran.ypos    = .5
        tran.subpixel = subpixel
        tran.transform_anchor = True
        tran.xanchor = get_at_time(camera_check_points['xanchor'], st, x_loop)
        tran.yanchor = get_at_time(camera_check_points['yanchor'], st, y_loop)
        z = get_at_time(camera_check_points['z'], st, z_loop)
        focus = get_at_time(focus_check_points['focus'], st, False)
        dof = get_at_time(focus_check_points['dof'], st, False)
        tran.rotate = get_at_time(camera_check_points['rotate'], st, rotate_loop)
        layer_z = get_at_time(layer_check_points, st, layer_loop)
        if x_express:
            tran.xanchor += _FOCAL_LENGTH*x_express(st, at)/(renpy.config.screen_width *_LAYER_Z)
        if y_express:
            tran.yanchor += _FOCAL_LENGTH*y_express(st, at)/(renpy.config.screen_height *_LAYER_Z)
        if z_express:
            z += z_express(st, at)
        if rotate_express:
            tran.rotate += rotate_express(st, at)
        if layer_express:
            layer_z += layer_express(st, st)
        distance = float(layer_z - z)
        if distance == 0:
            distance = .1
        if distance >= 0:
            tran.alpha = 1
            tran.zoom = _LAYER_Z / distance
            focus_distance = abs(layer_z - focus - z)
            if dof == 0:
                _dof = 0.1
            else:
                _dof = dof
            blur_amount=_camera_blur_amount * renpy.atl.warpers[_camera_blur_warper](focus_distance/(_dof))
            if blur_amount <= 1.0:
                tran.blur = None
            else:
                tran.blur = _camera_blur_amount * renpy.atl.warpers[_camera_blur_warper](focus_distance/(_dof))
        else:
            tran.alpha = 0
        return .005

    def get_at_time(check_points, time, loop):
        # check_points = ((value, time, warper)...)
        if loop and check_points[-1][1]:
            time %= check_points[-1][1]

        for i in xrange(1, len(check_points)):
            checkpoint = check_points[i][1]
            pre_checkpoint = check_points[i-1][1]
            if time < checkpoint:
                start = check_points[i-1]
                goal = check_points[i]
                if checkpoint != pre_checkpoint:
                    g = renpy.atl.warpers[goal[2]]((time - pre_checkpoint) / float(checkpoint - pre_checkpoint))
                else:
                    g = 1.

                return g*(goal[0]-start[0])+start[0]
        else:
            return check_points[-1][0]

    # def get_camera_coordinate(tran, z, layer, layer_z): #_3d_layers can't rollback?
    #     global _camera_x, _camera_y, _camera_z, _camera_rotate
    #     _camera_x         = int(((tran.xanchor-.5)*renpy.config.screen_width*_LAYER_Z)/_FOCAL_LENGTH)
    #     _camera_y         = int(((tran.yanchor-.5)*renpy.config.screen_height*_LAYER_Z)/_FOCAL_LENGTH)
    #     _camera_z         = int(z)
    #     _camera_rotate    = int(tran.rotate)
    #     _3d_layers[layer] = int(layer_z)

    def _ready_spline_camera_interpolation(camera_check_points):
        new_camera_check_points = {}
        new_camera_check_points["rotate"] = camera_check_points["rotate"]
        MINTIME = 0.1
        for coordinate in ["xanchor", "yanchor", "z"]:
            sv = [(t, v) for i, (v, t, w) in enumerate(camera_check_points[coordinate]) if i+1 == len(camera_check_points[coordinate]) or t != camera_check_points[coordinate][i+1][1]]
            if len(sv) > 2:
                new_camera_check_points[coordinate] = []
                for i in _drange(0, camera_check_points[coordinate][-1][1], MINTIME):
                    new_camera_check_points[coordinate].append((_spline(sv, i), i, "linear"))
            else:
                new_camera_check_points[coordinate] = camera_check_points[coordinate]

        return new_camera_check_points

    def _ready_spline_layer_interpolation(layer_check_points):
        MINTIME = 0.1
        sz = [(t, v) for i, (v, t, w) in enumerate(layer_check_points) if i+1 == len(layer_check_points) or t != layer_check_points[i+1][1]]
        if len(sz) > 2:
            new_layer_check_points = []
            for i in _drange(0, layer_check_points[-1][1], MINTIME):
                new_layer_check_points.append((_spline(sz, i), i, "linear"))
        else:
            new_layer_check_points = layer_check_points
        return new_layer_check_points

    def _drange(begin, end, step):
        n = begin
        while n < end:
            yield n
            n += step
        yield end

