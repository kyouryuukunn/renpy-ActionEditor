init 1600 python:
    if not _3d_layers:
        register_3d_layer('master')

init -1600 python:

    ##########################################################################
    # Camera functions

    # value of _3d_layers isn't included in rollback.
    # so I copy it many times.
    _3d_layers = {}
    _camera_x = 0
    _camera_y = 0
    _camera_z = 0
    _camera_rotate = 0
    _focal_length = 147.40
    _layer_z = 1848.9

    def register_3d_layer(*layers):
        """
         :doc: camera

         Register layers as 3D layers. 3D layers are applied transforms to by
         positions of a camera and 3D layers. This should be called in init
         block. If anything isn't registered as 3D layers, this script
         register 'master' layer as 3D layers

         `layers`
              This should be the string or strings of a layer name.
         """
        global _3d_layers
        _3d_layers = {layer:_layer_z for layer in layers}

    def camera_reset():
        """
         :doc: camera

         Reset a camera and 3D layers positions. Please call this at least once
         when the game has started. If this doesn't called, The position of 3D
         layers don't be saved.
         """
        global _3d_layers
        _3d_layers = _3d_layers.copy()
        for layer in _3d_layers:
            layer_move(layer, _layer_z)
        camera_move(0, 0, 0)

    def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None):
        """
         :doc: camera

         Move the coordinate and rotate of a camera and apply transforms to all 3D layers.

         `x`
              the x coordinate of a camera
         `y`
              the y coordinate of a camera
         `z`
              the z coordinate of a camera
         `rotate`
              Defaul 0, the rotate of a camera
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
         """

        camera_moves(((x, y, z, rotate, duration, warper), ), subpixel=subpixel, loop=loop, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express)

    def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None):
        """
         :doc: camera

         Move the z coordinate of a layer and apply transform to the layer.

         `layer`
              the string of a layer name to be moved
         `z`
              the z coordinate of a layer
         `duration`
              Default 0, this is the second times taken to move a camera.
         `warper`
              Default 'linear', this should be the string of the name of a
              warper registered with ATL.
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
         """

        layer_moves(layer, ((z, duration, warper), ), subpixel=subpixel, loop=loop, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express)

    def camera_moves(check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None):
        """
         :doc: camera

         Move a camera through check points and apply transforms to all 3D
         layers.

         `check_points`
              A tuple of (x, y, z, rotate, duration, warper)
         `loop`
              Default False, if True, this sequence of motions repeats.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
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
        kwargs = {coordinate+"_loop":loop for coordinate in ["x", "y", "z", "rotate"]}
        all_moves(camera_check_points=camera_check_points, loop=loop, subpixel=subpixel, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express, **kwargs)

    def layer_moves(layer, check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None):
        """
         :doc: camera

         Move a layer through check points and apply transform to the layer.

         `layer`
              the string of a layer name to be moved
         `check_points`
              A tuple of (z, duration, warper)
         `loop`
              Default False, if True, this sequence of motions repeats.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
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
         """
        all_moves(layer_check_points={layer:check_points}, subpixel=subpixel, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express, **{layer+"_loop":loop})

    def all_moves(camera_check_points=None, layer_check_points=None, subpixel=True, play=True, x_loop=False, y_loop=False, z_loop=False, rotate_loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, **kwargs):
        """
         :doc: camera

         Move a layer and camera through check points and apply transform to the layer.

         `camera_check_points`
              {
                  'x':[(x, duration, warper)...]
                  'y':[(y, duration, warper)...]
                  'z':[(z, duration, warper)...]
                  'rotate':[(rotate, duration, warper)...]
              }
         `layer_check_points`
              {
                  'layer name':[(z, duration, warper)...]
              }
         `loop_x`
              Default False, if True, this sequence of motions repeats.
         `loop_y`
              Default False, if True, this sequence of motions repeats.
         `loop_z`
              Default False, if True, this sequence of motions repeats.
         `loop_rotate`
              Default False, if True, this sequence of motions repeats.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         '<layer name>_loop'
              Default False, if True, this sequence of motions repeats.
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
         """
        global _camera_x, _camera_y, _camera_z, _camera_rotate, _3d_layers
        from math import sin, pi
        from random import random

        if camera_check_points is None:
            camera_check_points = {}
        if layer_check_points is None:
            layer_check_points = {}
        rotate_loop = kwargs.get("rotate_loop", False)
        start_xanchor = _focal_length*_camera_x/(renpy.config.screen_width *_layer_z) + .5
        start_yanchor = _focal_length*_camera_y/(renpy.config.screen_height*_layer_z) + .5
        camera_check_points2 = { 'xanchor':[(start_xanchor, 0, None, )], 'yanchor':[(start_yanchor, 0, None, )], 'z': [(_camera_z, 0, None, )], 'rotate':[(_camera_rotate, 0, None, )] }

        for coordinate in ["x", "y", "z", "rotate"]:
            if coordinate not in camera_check_points:
                camera_check_points[coordinate] = [(getattr(renpy.store, "_camera_"+coordinate), 0, None, )]
        for c in camera_check_points['x']:
            camera_check_points2['xanchor'].append((_focal_length*c[0]/(renpy.config.screen_width *_layer_z) + .5, c[1], c[2], ))
        for c in camera_check_points['y']:
            camera_check_points2['yanchor'].append((_focal_length*c[0]/(renpy.config.screen_height *_layer_z) + .5, c[1], c[2], ))
        camera_check_points2['z'].extend(camera_check_points['z'])
        camera_check_points2['rotate'].extend(camera_check_points['rotate'])
        for layer in _3d_layers:

            if layer not in layer_check_points:
                layer_check_points[layer] = ((_3d_layers[layer], 0, None), )
            layer_check_points2 = [(_3d_layers[layer], 0, None), ]
            for c in layer_check_points[layer]:
                layer_check_points2.append((c[0], float(c[1]), c[2]))
            layer_loop = kwargs.get(layer+"_loop", False)

            if play:
                renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(function=renpy.curry(_camera_trans)(camera_check_points=camera_check_points2, layer_check_points=layer_check_points2, subpixel=subpixel, layer=layer, layer_loop=layer_loop, x_loop=x_loop, y_loop=y_loop, z_loop=z_loop, rotate_loop=rotate_loop, x_express=x_express, y_express=y_express, z_express=z_express, rotate_express=rotate_express))])
                layer_z = layer_check_points2[-1][0]
            else:
                # This is used when the time bar is changed by Action Editor
                st = _viewers.time
                xanchor = get_at_time(camera_check_points2['xanchor'], st, x_loop)
                yanchor = get_at_time(camera_check_points2['yanchor'], st, y_loop)
                z = get_at_time(camera_check_points2['z'], st, z_loop)
                rotate = get_at_time(camera_check_points2['rotate'], st, rotate_loop)
                layer_z = get_at_time(layer_check_points2, st, layer_loop)
                distance = float(layer_z - z)
                if distance == 0:
                    distance = .1
                if distance >= 0:
                    alpha = 1
                    zoom = _layer_z / distance
                    renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(xpos=.5, ypos=.5, alpha=alpha, transform_anchor=True, xanchor=xanchor, yanchor=yanchor, zoom=zoom, rotate=rotate)])
                else:
                    alpha = 0
                    renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(xpos=.5, ypos=.5, alpha=alpha, transform_anchor=True, xanchor=xanchor, yanchor=yanchor, rotate=rotate)])

            _3d_layers[layer] = int(layer_z)
        if play:
            _camera_x = camera_check_points['x'][-1][0]
            _camera_y = camera_check_points['y'][-1][0]
            _camera_z = camera_check_points['z'][-1][0]
            _camera_rotate = camera_check_points['rotate'][-1][0]
        else:
            _camera_x         = int(((xanchor-.5)*renpy.config.screen_width*_layer_z)/_focal_length)
            _camera_y         = int(((yanchor-.5)*renpy.config.screen_height*_layer_z)/_focal_length)
            _camera_z         = int(z)
            _camera_rotate    = int(rotate)

    def _camera_trans(tran, st, at, camera_check_points, layer_check_points, layer_loop, x_loop, y_loop, z_loop, rotate_loop, subpixel, layer, x_express, y_express, z_express, rotate_express):
        # camera_check_points = (z, r, xanchor, yanchor, duration, warper)
        # layer_check_points = (layer_z, duration, warper)
        from math import sin, pi
        from random import random
        tran.xpos    = .5 
        tran.ypos    = .5
        tran.subpixel = subpixel
        tran.transform_anchor = True
        tran.xanchor = get_at_time(camera_check_points['xanchor'], st, x_loop)
        tran.yanchor = get_at_time(camera_check_points['yanchor'], st, y_loop)
        z = get_at_time(camera_check_points['z'], st, z_loop)
        tran.rotate = get_at_time(camera_check_points['rotate'], st, rotate_loop)
        layer_z = get_at_time(layer_check_points, st, layer_loop)
        if x_express:
            tran.xanchor += _focal_length*x_express(st, at)/(renpy.config.screen_width *_layer_z)
        if y_express:
            tran.yanchor += _focal_length*y_express(st, at)/(renpy.config.screen_height *_layer_z)
        if z_express:
            z += z_express(st, at)
        if rotate_express:
            tran.rotate += rotate_express(st, at)
        distance = float(layer_z - z)
        if distance == 0:
            distance = .1
        if distance >= 0:
            tran.alpha = 1
            tran.zoom = _layer_z / distance
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
    #     _camera_x         = int(((tran.xanchor-.5)*renpy.config.screen_width*_layer_z)/_focal_length)
    #     _camera_y         = int(((tran.yanchor-.5)*renpy.config.screen_height*_layer_z)/_focal_length)
    #     _camera_z         = int(z)
    #     _camera_rotate    = int(tran.rotate)
    #     _3d_layers[layer] = int(layer_z)

screen _rot(): #show rule of thirds
    for i in range(1, 3):
        add Solid("#F00", xsize=config.screen_width, ysize=1, ypos=config.screen_height*i/3) 
        add Solid("#F00", xsize=1, ysize=config.screen_height, xpos=config.screen_width*i/3)

transform _delay_show(time):
    alpha 0
    pause time
    alpha 1

screen _action_editor(tab="images", layer="master", tag="", time=0):
    if time:
        timer time+1 action Function(_viewers.change_time, _viewers.time)
    $state={k: v for dic in [_viewers.transform_viewer.state_org[layer], _viewers.transform_viewer.state[layer]] for k, v in dic.items()}
    key "game_menu" action Return()
    zorder 10
    key "rollback"    action _viewers.rollback
    key "rollforward" action _viewers.rollforward

    frame:
        background "#0006"
        if time:
            at _delay_show(time + 1)
        xfill True
        vbox:

            hbox:
                textbutton _("time: [_viewers.time:>.2f] s") action Function(_viewers.edit_time)
                textbutton _("<") action Function(_viewers.prev_time)
                textbutton _(">") action Function(_viewers.next_time)
                bar adjustment ui.adjustment(range=7.0, value=_viewers.time, changed=_viewers.change_time) xalign 1.
            hbox:
                xfill True
                hbox:
                    textbutton _("clear anchor") action [SensitiveIf(_viewers.sorted_anchor_points), Function(_viewers.clear_anchor_points), renpy.restart_interaction]
                    textbutton _("remove anchor") action [SensitiveIf(_viewers.time in _viewers.sorted_anchor_points), Function(_viewers.remove_anchor_point, _viewers.time), renpy.restart_interaction]
                    textbutton _("warper") action _viewers.select_time_warper
                    textbutton _("ROT") action [SelectedIf(renpy.get_screen("_rot")), If(renpy.get_screen("_rot"), true=Hide("_rot"), false=Show("_rot"))]
                    if _viewers.sorted_anchor_points:
                        # if _viewers.time in _viewers.sorted_anchor_points:
                        #     textbutton _("remove anchor") action [Function(_viewers.remove_anchor_point, _viewers.time), renpy.restart_interaction]
                        # else:
                        #     textbutton _("add    anchor") action [_viewers.set_anchor_point, renpy.restart_interaction]
                        textbutton _("play") action [SensitiveIf(_viewers.sorted_anchor_points), Function(_viewers.camera_viewer.play, play=True), Function(_viewers.transform_viewer.play, play=True), Hide("_action_editor"), Show("_action_editor", tab=tab, layer=layer, tag=tag, time=_viewers.sorted_anchor_points[-1]), renpy.restart_interaction]
                    else:
                        # textbutton _("add    anchor") action [_viewers.set_anchor_point, renpy.restart_interaction]
                        textbutton _("play") action [SensitiveIf(_viewers.sorted_anchor_points), Function(_viewers.camera_viewer.play, play=True), Function(_viewers.transform_viewer.play, play=True), Hide("_action_editor"), Show("_action_editor", tab=tab, layer=layer, tag=tag), renpy.restart_interaction]
                    textbutton _("clipboard") action Function(_viewers.put_clipboard)
                hbox:
                    xalign 1.
                    textbutton _("close") action Return()

            null height 10
            hbox:
                style_group "action_editor"
                xfill False
                textbutton _("Images") action [SelectedIf(tab == "images"), Show("_action_editor", tab="images")]
                textbutton _("2D Camera") action [SensitiveIf(_3d_layers.keys() == ["master"]), SelectedIf(tab == "2D Camera"), Show("_action_editor", tab="2D Camera")]
                textbutton _("3D Layers") action [SelectedIf(tab == "3D Layers"), Show("_action_editor", tab="3D Layers")]
                textbutton _("3D Camera") action [SelectedIf(tab == "3D Camera"), Show("_action_editor", tab="3D Camera")]
            if tab == "images":
                hbox:
                    style_group "action_editor"
                    xfill False
                    label _("layers")
                    for l in config.layers:
                        if l not in ["screens", "transient", "overlay"]:
                            textbutton "[l]" action [SelectedIf(l == layer), Show("_action_editor", tab=tab, layer=l)]
                hbox:
                    style_group "action_editor"
                    xfill False
                    label _("images")
                    for t in state:
                        textbutton "[t]" action [SelectedIf(t == tag), Show("_action_editor", tab=tab, layer=layer, tag=t)]

                if tag in state:
                    for p, d in _viewers.transform_viewer.props:
                        $prop = _viewers.transform_viewer.get_property(layer, tag, p)
                        $ f = _viewers.transform_viewer.generate_changed(layer, tag, p)
                        if p not in _viewers.transform_viewer.force_float and ((state[tag][p] is None and isinstance(d, int)) or isinstance(state[tag][p], int)):
                            hbox:
                                style_group "action_editor"
                                textbutton "[p]" action Function(_viewers.transform_viewer.put_prop_clipboard, p, prop)
                                textbutton _("loop") action ToggleDict(_viewers.loops, tag+"_"+layer+"_"+p+"_loop")
                                textbutton "[prop]" action Function(_viewers.transform_viewer.edit_value, f, True, default=prop)
                                bar adjustment ui.adjustment(range=_viewers.transform_viewer.int_range*2, value=prop+_viewers.transform_viewer.int_range, page=1, changed=f) xalign 1.
                        else:
                            hbox:
                                style_group "action_editor"
                                textbutton "[p]" action Function(_viewers.transform_viewer.put_prop_clipboard, p, prop)
                                textbutton _("loop") action ToggleDict(_viewers.loops, tag+"_"+layer+"_"+p+"_loop")
                                textbutton "[prop:>.2f]" action Function(_viewers.transform_viewer.edit_value, f, False, default=prop)
                                bar adjustment ui.adjustment(range=_viewers.transform_viewer.float_range*2, value=prop+_viewers.transform_viewer.float_range, page=.05, changed=f) xalign 1.
            elif tab == "3D Camera" or tab == "2D Camera":
                if _3d_layers.keys() == ["master"] and tab == "3D Camera":
                    label _("Please regist 3D layers")
                else:
                    hbox:
                        style_group "action_editor"
                        label "x"
                        textbutton _("loop") action ToggleDict(_viewers.loops, "_camera_x_loop")
                        textbutton "[_camera_x: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.x_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_x)
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_x+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.x_changed) xalign 1.
                    hbox:
                        style_group "action_editor"
                        label "y"
                        textbutton _("loop") action ToggleDict(_viewers.loops, "_camera_y_loop")
                        textbutton "[_camera_y: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.y_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_y)
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_y+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.y_changed) xalign 1.
                    hbox:
                        style_group "action_editor"
                        label "z"
                        textbutton _("loop") action ToggleDict(_viewers.loops, "_camera_z_loop")
                        textbutton "[_camera_z: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.z_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_z)
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_z+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.z_changed) xalign 1.
                    hbox:
                        style_group "action_editor"
                        label "rotate"
                        textbutton _("loop") action ToggleDict(_viewers.loops, "_camera_rotate_loop")
                        textbutton "[_camera_rotate: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.r_changed, _viewers.camera_viewer.range_rotate, default=_camera_rotate)
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_rotate*2, value=_camera_rotate+_viewers.camera_viewer.range_rotate, page=1, changed=_viewers.camera_viewer.r_changed) xalign 1.
            elif tab == "3D Layers":
                if _3d_layers.keys() == ["master"]:
                    label _("Please regist 3D layers")
                else:
                    for layer in sorted(_3d_layers.keys()):
                        hbox:
                            style_group "action_editor"
                            label "[layer]"
                            textbutton _("loop") action ToggleDict(_viewers.loops, layer+"_loop")
                            textbutton "{}".format(_3d_layers[layer]) action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.generate_layer_z_changed(layer), 0, default=_3d_layers[layer])
                            bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_layer_z, value=_3d_layers[layer], page=1, changed=_viewers.camera_viewer.generate_layer_z_changed(layer)) xalign 1.
            hbox:
                style_group "action_editor"
                xfill False
                xalign 1.
                if tab == "images":
                    if tag:
                        textbutton _("clipboard") action Function(_viewers.transform_viewer.put_show_clipboard, tag, layer)
                    # textbutton _("add") action Function(_viewers.transform_viewer.add_image, layer)
                    # textbutton _("remove") action [SensitiveIf(tag), Function(_viewers.transform_viewer.state_org[layer].pop, tag), Function(renpy.hide, tag, layer), Show("_action_editor", tab=tab, layer=layer)]
                    textbutton _("reset") action [_viewers.transform_viewer.reset, renpy.restart_interaction]
                elif tab == "2D Camera":
                    textbutton _("clipboard") action Function(_viewers.camera_viewer.put_clipboard, True)
                    textbutton _("reset") action [_viewers.camera_viewer.camera_reset, renpy.restart_interaction]
                elif tab == "3D Layers":
                    textbutton _("clipboard") action Function(_viewers.camera_viewer.put_clipboard, False)
                    textbutton _("reset") action [_viewers.camera_viewer.layer_reset, renpy.restart_interaction]
                elif tab == "3D Camera":
                    textbutton _("clipboard") action Function(_viewers.camera_viewer.put_clipboard, True)
                    textbutton _("reset") action [_viewers.camera_viewer.camera_reset, renpy.restart_interaction]

    if time:
        add _viewers.dragged at _delay_show(time + 1)
    else:
        add _viewers.dragged

init -1600:
    style action_editor_button size_group "action_editor"
    style action_editor_images_button size_group "action_editor_images"
    style action_editor_layers_button size_group "action_editor_layers"
    style action_editor_times_button size_group "action_editor_times"
    style action_editor_button_text xalign .5
    style action_editor_label xminimum 110
    style action_editor_vbox xfill True

screen _input_screen(message="type value", default=""):
    modal True
    zorder 100
    key "game_menu" action Return("")

    frame:
        style_group "input_screen"

        has vbox

        label message

        hbox:
            input default default

init -1600:
    style input_screen_frame xfill True ypos .1 xmargin .05 ymargin .05
    style input_screen_vbox xfill True spacing 30
    style input_screen_label xalign .5
    style input_screen_hbox  xalign .5

screen _warper_selecter():
    modal True
    zorder 100
    key "game_menu" action Return("")

    frame:
        style_group "warper_selecter"

        has vbox

        label _("Select a warper function")

        hbox:
            for warper in renpy.atl.warpers:
                textbutton warper action [SetField(_viewers, "warper", warper), Return()] hovered Show("_warper_graph", warper=warper) unhovered Hide("_warper")


screen _warper_graph(warper="linear", t=120, length=300):
    # add Solid("#000", xsize=3, ysize=1.236*length, xpos=100+length/2, ypos=length/2+100, rotate=45, anchor=(.5, .5)) 
    add Solid("#CCC", xsize=length, ysize=length, xpos=100, ypos=100 ) 
    add Solid("#000", xsize=length, ysize=3, xpos=100, ypos=length+100 ) 
    add Solid("#000", xsize=length, ysize=3, xpos=100, ypos=100 ) 
    add Solid("#000", xsize=3, ysize=length, xpos=100+length, ypos=100)
    add Solid("#000", xsize=3, ysize=length, xpos=100, ypos=100)
    for i in range(1, t):
        add Solid("#000", xsize=length/t, ysize=int(length*renpy.atl.warpers[warper](i/float(t))), xpos=100+i*length/t, ypos=length+100, yanchor=1.) 


init -1098 python:
    # overwrite keymap
    km = renpy.Keymap(
        rollback = renpy.rollback,
        screenshot = _screenshot,
        toggle_fullscreen = renpy.toggle_fullscreen,
        toggle_skip = _keymap_toggle_skipping,
        fast_skip = _fast_skip,
        game_menu = _invoke_game_menu,
        hide_windows = renpy.curried_call_in_new_context("_hide_windows"),
        launch_editor = _launch_editor,
        reload_game = _reload_game,
        developer = _developer,
        quit = renpy.quit_event,
        iconify = renpy.iconify,
        help = _help,
        choose_renderer = renpy.curried_call_in_new_context("_choose_renderer"),
        console = _console.enter,
        profile_once = _profile_once,
        self_voicing = Preference("self voicing", "toggle"),
        action_editor = _viewers.action_editor,
        )

    config.underlay = [ km ]

    del km


init 1100 python:
    config.locked = False
    config.keymap["action_editor"] = ['P']
    config.locked = True


init -1600 python in _viewers:

    ##########################################################################
    # TransformViewer
    class TransformViewer(object):
        def __init__(self):

            self.int_range = 1500
            self.float_range = 7.0
            # layer->tag->property->value
            self.state_org = {}
            self.state = {}
            # ((property, default)...), default is used when property can't be got.
            self.props = (
            ("xpos", 0.), 
            ("ypos", 0.), 
            ("xanchor", 0.), 
            ("yanchor", 0.), 
            ("xzoom", 1.), 
            ("yzoom", 1.), 
            ("zoom", 1.), 
            ("rotate", 0,),
            ("alpha", 1.), 
            ("additive", 0.), 
            )
            self.force_float = ["zoom", "xzoom", "yzoom", "alpha", "additive"]

        def init(self):
            if not renpy.config.developer:
                return
            sle = renpy.game.context().scene_lists
            # back up for reset()
            for layer in renpy.config.layers:
                self.state_org[layer] = {}
                self.state[layer] = {}
                for tag in sle.layers[layer]:
                    if not tag[0]:
                        break
                    d = sle.get_displayable_by_tag(layer, tag[0])
                    if isinstance(d, renpy.display.screen.ScreenDisplayable):
                        break
                    pos = renpy.get_placement(d)
                    state = getattr(d, "state", None)

                    self.state_org[layer][tag[0]] = {}
                    for p in ["xpos", "ypos", "xanchor", "yanchor"]:
                        self.state_org[layer][tag[0]][p] = getattr(pos, p, None)
                    for p, d in self.props:
                        if p not in self.state_org[layer][tag[0]]:
                            self.state_org[layer][tag[0]][p] = getattr(state, p, None)

        def reset(self):
            for layer in renpy.config.layers:
                for tag, props in self.state_org[layer].iteritems():
                    if tag and props:
                        kwargs = props.copy()
                        for p, d in self.props:
                            if kwargs[p] is None and p != "rotate":
                                kwargs[p] = d
                        renpy.show(tag, [renpy.store.Transform(**kwargs)], layer=layer)
                for tag in self.state[layer]:
                    renpy.hide(tag, layer=layer)
                self.state[layer] = {}
            renpy.restart_interaction()

        def set_anchor_point(self, layer, tag, prop, value):

            if (tag, layer) not in all_anchor_points:
                all_anchor_points[(tag, layer)] = {}
            anchor_points = all_anchor_points[(tag, layer)].get(prop, [])
            if anchor_points:
                for i, (t, c) in enumerate(anchor_points):
                    if time < t:
                        anchor_points.insert(i, (time, (value, time, warper)))
                        break
                    elif time == t:
                        anchor_points[i] = (time, (value, time, warper))
                        break
                else:
                    anchor_points.append((time, (value, time, warper)))
            else:
                if time == 0:
                    all_anchor_points[(tag, layer)][prop] = [(time, (value, time, warper))]
                else:
                    org = {k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}[tag][prop]
                    all_anchor_points[(tag, layer)][prop] = [(0, (org, 0, None)), (time, (value, time, warper))]
            sort_anchor_points()

        def play(self, play):
            for layer in renpy.config.layers:
                for tag in {k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}:
                    check_points = {}
                    for prop, d in self.props:
                        if (tag, layer) in all_anchor_points and prop in all_anchor_points[(tag, layer)]:
                            check_points[prop] =  [ c for t, c in all_anchor_points[(tag, layer)][prop] ]
                    loop = {prop+"_loop": loops[tag+"_"+layer+"_"+prop+"_loop"] for prop, d in self.props}
                    if play:
                        renpy.show(tag, [renpy.store.Transform(function=renpy.curry(self.transform)(check_points=check_points, loop=loop))], layer=layer)
                    else:
                        # check_points = { prop: ( (value, time, warper).. ) }
                        kwargs = {}
                        kwargs.subpixel = True
                        # kwargs.transform_anchor = True
                        st = renpy.store._viewers.time

                        for p, cs in check_points.items():
                            time = st
                            if loop[p+"_loop"] and cs[-1][1]:
                                time = time % cs[-1][1]

                            for i in xrange(1, len(cs)):
                                checkpoint = cs[i][1]
                                pre_checkpoint = cs[i-1][1]
                                if time < checkpoint:
                                    start = cs[i-1]
                                    goal = cs[i]
                                    if checkpoint != pre_checkpoint:
                                        g = renpy.atl.warpers[goal[2]]((time - pre_checkpoint) / float(checkpoint - pre_checkpoint))
                                    else:
                                        g = 1.
                                    for p2, d in self.props:
                                        if p2 == p:
                                            default = d
                                    if goal[0] is not None:
                                        if isinstance(goal[0], int) and p not in self.force_float:
                                            if start[0] is None:
                                                v = g*(goal[0]-default)+default
                                            else:
                                                v = g*(goal[0]-start[0])+start[0]
                                            v = int(v)
                                        else:
                                            if start[0] is None:
                                                v = g*(goal[0]-default)+default
                                            else:
                                                v = g*(goal[0]-start[0])+start[0]
                                        kwargs[p] = v
                                    break
                            else:
                                kwargs[p] = cs[-1][0]

                        renpy.show(tag, [renpy.store.Transform(**kwargs)], layer=layer)

        def transform(self, tran, st, at, check_points, loop, subpixel=True):
            # check_points = { prop: [ (value, time, warper).. ] }
            tran.subpixel = subpixel
            # tran.transform_anchor = True

            for p, cs in check_points.items():
                time = st
                if loop[p+"_loop"] and cs[-1][1]:
                    time = st % cs[-1][1]

                for i in xrange(1, len(cs)):
                    checkpoint = cs[i][1]
                    pre_checkpoint = cs[i-1][1]
                    if time < checkpoint:
                        start = cs[i-1]
                        goal = cs[i]
                        if checkpoint != pre_checkpoint:
                            g = renpy.atl.warpers[goal[2]]((time - pre_checkpoint) / float(checkpoint - pre_checkpoint))
                        else:
                            g = 1.
                        for p2, d in self.props:
                            if p2 == p:
                                default = d
                        if goal[0] is not None:
                            if isinstance(goal[0], int) and p not in self.force_float:
                                if start[0] is None:
                                    v = g*(goal[0]-default)+default
                                else:
                                    v = g*(goal[0]-start[0])+start[0]
                                v = int(v)
                            else:
                                if start[0] is None:
                                    v = g*(goal[0]-default)+default
                                else:
                                    v = g*(goal[0]-start[0])+start[0]
                            setattr(tran, p, v)
                        break
                else:
                    setattr(tran, p, cs[-1][0])
            return .005


        def generate_changed(self, layer, tag, prop):
            state={k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}[tag][prop]
            def changed(v):
                kwargs = {}
                for p, d in self.props:
                    kwargs[p] = self.get_property(layer, tag, p, False)
                    if p == prop:
                        default = d
                if prop not in self.force_float and ( (state is None and isinstance(default, int)) or isinstance(state, int) ):
                    kwargs[prop] = v - self.int_range
                else:
                    kwargs[prop] = round(v -self.float_range, 2)

                self.set_anchor_point(layer, tag, prop, kwargs[prop])
                renpy.show(tag, [renpy.store.Transform(**kwargs)], layer=layer)
                renpy.restart_interaction()
            return changed

        def get_property(self, layer, tag, prop, default=True):
            sle = renpy.game.context().scene_lists
            if tag in self.state[layer]:
                #TODO
                default = True
            if tag:
                d = sle.get_displayable_by_tag(layer, tag)
                pos = renpy.get_placement(d)
                state = getattr(pos, prop, None)
                if state is None:
                    state = getattr(getattr(d, "state", None), prop, None)
                if state is None and default:
                    for p, d in self.props:
                        if p == prop:
                            state = d
                return state
            return None

        def put_prop_clipboard(self, prop, value):
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, "%s %s" % (prop, value))
            except:
                renpy.notify(_("Can't open clipboard"))
            else:
                renpy.notify(__('Putted "%s %s" on clipboard') % (prop, value))

        def put_show_clipboard(self, tag, layer):
            string = """
    show %s onlayer %s""" % (tag, layer)
            for p, d in self.props:
                value = self.get_property(layer, tag, p)
                if value != d:
                    if string.find(":") < 0:
                        string += ":\n        "
                    string += "%s %s " % (p, value)
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, string)
            except:
                renpy.notify(_("Can't open clipboard"))
            else:
                renpy.notify(__('Putted "%s" on clipboard') % string)

        def edit_value(self, function, int=False, default=""):
            v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", default=default)
            if v:
                try:
                    if int:
                        v = renpy.python.py_eval(v) + self.int_range
                    else:
                        v = renpy.python.py_eval(v) + self.float_range
                    function(v)
                except:
                    renpy.notify(_("Please type value"))

        def add_image(self, layer):
            name = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", message=_("Type a image name"))
            if name:
                try:
                    tag = name.split()[0]
                    self.state[layer][tag] = {}
                    renpy.show(name, layer=layer)
                    for p, d in self.props:
                        self.state[layer][tag][p] = self.get_property(layer, tag, p)
                    renpy.show_screen("_action_editor", tab="images", layer=layer, tag=tag)
                except:
                    renpy.notify(_("Please type value"))
    transform_viewer = TransformViewer()

    ##########################################################################
    # CameraViewer
    class CameraViewer(object):

        def __init__(self):
            self.range_camera_pos   = 6000
            self.range_rotate       = 360
            self.range_layer_z   = 10000

        def init(self):
            if not renpy.config.developer:
                return
            self._camera_x = renpy.store._camera_x
            self._camera_y = renpy.store._camera_y
            self._camera_z = renpy.store._camera_z
            self._camera_rotate = renpy.store._camera_rotate
            self._3d_layers = renpy.store._3d_layers.copy()

        def camera_reset(self):
            renpy.store.camera_move(self._camera_x, self._camera_y, self._camera_z, self._camera_rotate)
            renpy.restart_interaction()

        def layer_reset(self):
            for layer in renpy.store._3d_layers:
                renpy.store.layer_move(layer, self._3d_layers[layer])
            renpy.restart_interaction()

        def x_changed(self, v):
            v=int(v)
            renpy.store.camera_move(v - self.range_camera_pos, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate)
            self.set_camera_anchor_point("_camera_x", v-self.range_camera_pos)
            renpy.restart_interaction()

        def y_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, v - self.range_camera_pos, renpy.store._camera_z, renpy.store._camera_rotate)
            self.set_camera_anchor_point("_camera_y", v-self.range_camera_pos)
            renpy.restart_interaction()

        def z_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, v - self.range_camera_pos, renpy.store._camera_rotate)
            self.set_camera_anchor_point("_camera_z", v-self.range_camera_pos)
            renpy.restart_interaction()

        def r_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, v - self.range_rotate)
            self.set_camera_anchor_point("_camera_rotate", v-self.range_camera_pos)
            renpy.restart_interaction()

        def generate_layer_z_changed(self, l):
            def layer_z_changed(v):
                renpy.store.layer_move(l, int(v))
                self.set_layer_anchor_point(l)
                renpy.restart_interaction()
            return layer_z_changed

        def put_clipboard(self, camera_tab):
            string = ""
            if camera_tab:
                string = """
    $camera_move(%s, %s, %s, %s, duration=0)""" % (renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate)
            else:
                for layer in renpy.store._3d_layers:
                    string += """
    $layer_move("%s", %s, duration=0)""" % (layer, renpy.store._3d_layers[layer])
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, string)
            except:
                renpy.notify(_("Can't open clipboard"))
            else:
                renpy.notify(__("Putted '%s' on clipboard") % string)

        def edit_value(self, function, range, default=""):
            v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", default=default)
            if v:
                try:
                    function(renpy.python.py_eval(v) + range)
                except:
                    renpy.notify(_("Please type value"))

        def set_camera_anchor_point(self, coordinate, value):
            anchor_points = all_anchor_points.get(coordinate, [])
            if anchor_points:
                for i, (t, c) in enumerate(anchor_points):
                    if time < t:
                        anchor_points.insert(i, (time, (value, time, warper)))
                        break
                    elif time == t:
                        anchor_points[i] = (time, (value, time, warper))
                        break
                else:
                    anchor_points.append((time, (value, time, warper)))
            else:
                if time == 0:
                    all_anchor_points[coordinate] = [(time, (value, time, warper))]
                else:
                    all_anchor_points[coordinate] = [(0, (getattr(self, coordinate), 0, None)), (time, (value, time, warper))]
            sort_anchor_points()

        def set_layer_anchor_point(self, layer):
            anchor_points = all_anchor_points.get("layer "+layer, [])
            if anchor_points:
                for i, (t, c) in enumerate(anchor_points):
                    if time < t:
                        anchor_points.insert(i, (time, (renpy.store._3d_layers[layer], time, warper)))
                        break
                    elif time == t:
                        anchor_points[i] = (time, (renpy.store._3d_layers[layer], time, warper))
                        break
                else:
                    anchor_points.append((time, (renpy.store._3d_layers[layer], time, warper)))
            else:
                if time == 0:
                    all_anchor_points["layer "+layer] = [(time, (renpy.store._3d_layers[layer], time, warper))]
                else:
                    all_anchor_points["layer "+layer] = [(0, (self._3d_layers[layer], 0, None)), (time, (renpy.store._3d_layers[layer], time, warper))]
            sort_anchor_points()

        def play(self, play):
            camera_check_points = {}
            for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
                if coordinate in all_anchor_points:
                    camera_check_points[coordinate[8:]] = [c for t, c in all_anchor_points[coordinate]]

            layer_check_points = {}
            loop = {}
            for layer in renpy.store._3d_layers:
                if "layer "+layer in all_anchor_points:
                    layer_check_points[layer]=[c for t, c in all_anchor_points["layer "+layer]]
                loop[layer+"_loop"] = loops[layer+"_loop"]
            for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
                loop[coordinate[8:]+"_loop"] = loops[coordinate+"_loop"]
            if camera_check_points or layer_check_points:
                renpy.store.all_moves(camera_check_points=camera_check_points, layer_check_points=layer_check_points, play=play, **loop)

    camera_viewer = CameraViewer()

    class Dragged(renpy.Displayable):

        def __init__(self, child, **properties):
            super(Dragged, self).__init__(**properties)
            # The child.
            self.child = renpy.displayable(child)
            self.cx = self.x = (0.5 + renpy.store._camera_x/(2.*camera_viewer.range_camera_pos))*renpy.config.screen_width
            self.cy = self.y = (0.5 + renpy.store._camera_y/(2.*camera_viewer.range_camera_pos))*renpy.config.screen_height
            self.dragging = False

        def render(self, width, height, st, at):

            # Create a render from the child.
            child_render = renpy.render(self.child, width, height, st, at)

            # Get the size of the child.
            self.width, self.height = child_render.get_size()

            # Create the render we will return.
            render = renpy.Render(renpy.config.screen_width, renpy.config.screen_height)

            # Blit (draw) the child's render to our render.
            render.blit(child_render, (self.x-self.width/2., self.y-self.height/2.))

            # Return the render.
            return render

        def event(self, ev, x, y, st):

            if renpy.map_event(ev, "mousedown_1"):
                if self.x-self.width/2. <= x and x <= self.x+self.width/2. and self.y-self.height/2. <= y and y <= self.y+self.height/2.:
                    self.dragging = True
            elif renpy.map_event(ev, "mouseup_1"):
                self.dragging = False

            # if x <= 0:
            #     x = 0
            # if renpy.config.screen_width <= x:
            #     x = renpy.config.screen_width
            # if y <= 0:
            #     y = 0
            # if renpy.config.screen_height <= y:
            #     y = renpy.config.screen_height

            if renpy.store._camera_x != int(self.cx) or renpy.store._camera_y != int(self.cy):
                self.x = (0.5 + renpy.store._camera_x/(2.*camera_viewer.range_camera_pos))*renpy.config.screen_width
                self.y = (0.5 + renpy.store._camera_y/(2.*camera_viewer.range_camera_pos))*renpy.config.screen_height
                renpy.redraw(self, 0)

            if self.dragging:
                if self.x != x or self.y != y:
                    self.cx = int(2*camera_viewer.range_camera_pos*( float(x)/renpy.config.screen_width - 0.5))
                    self.cy = int(2*camera_viewer.range_camera_pos*( float(y)/renpy.config.screen_height - 0.5))
                    if self.cx != renpy.store._camera_x:
                        camera_viewer.set_camera_anchor_point("_camera_x", self.cx)
                    if self.cy != renpy.store._camera_y:
                        camera_viewer.set_camera_anchor_point("_camera_y", self.cy)
                    renpy.store.camera_move(self.cx, self.cy, renpy.store._camera_z, renpy.store._camera_rotate)
                    self.x, self.y = x, y
                    renpy.restart_interaction()
                    renpy.redraw(self, 0)

            # Pass the event to our child.
            return self.child.event(ev, x, y, st)

        def per_interact(self):
            renpy.redraw(self, 0)

        def visit(self):
            return [ self.child ]
    dragged = Dragged("camera.png")

    ##########################################################################
    #{(tag, layer):[(time, check_point, warper)...]}
    from collections import defaultdict
    loops = defaultdict(lambda:False)
    all_anchor_points = {}
    time = 0
    sorted_anchor_points = []
    warper = "linear"

    def edit_time():
        global time
        v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", default=time)
        if v:
            try:
                v = renpy.python.py_eval(v)
                if v < 0:
                    return
                change_time(v)
            except:
                renpy.notify(_("Please type value"))

    def next_time():
        if not sorted_anchor_points:
            change_time(0)
            return
        else:
            for i, t in enumerate(sorted_anchor_points):
                if time < t:
                    change_time(sorted_anchor_points[i])
                    break
            else:
                change_time(sorted_anchor_points[0])

    def prev_time():
        if not sorted_anchor_points:
            change_time(0)
            return
        else:
            for i, t in enumerate(sorted_anchor_points):
                if time <= t:
                    change_time(sorted_anchor_points[i-1])
                    break
            else:
                change_time(sorted_anchor_points[-1])

    def select_time_warper():
        renpy.invoke_in_new_context(renpy.call_screen, "_warper_selecter")

    def clear_anchor_points():
        all_anchor_points.clear()
        sorted_anchor_points[:]=[]

    def remove_anchor_point(time):
        remove_list = []
        for k, v in all_anchor_points.items():
            if isinstance(k, tuple):
                for k2, v2 in v.items():
                    for t, c in v2:
                        if t == time:
                            if time != 0 or (time == 0 and len(v2) == 1):
                                remove_list.append((k, k2, (t, c)))
        for k, k2, c in remove_list:
            all_anchor_points[k][k2].remove(c)
            if not all_anchor_points[k][k2]:
                del all_anchor_points[k][k2]

        remove_list = []
        for k, v in all_anchor_points.items():
            if not isinstance(k, tuple):
                for t, c in v:
                    if t == time:
                        if time != 0 or (time == 0 and len(v) == 1):
                            remove_list.append((k, (t, c)))
        for k, c in remove_list:
            all_anchor_points[k].remove(c)
            if not all_anchor_points[k]:
                del all_anchor_points[k]
        sort_anchor_points()

    def sort_anchor_points():
        global sorted_anchor_points
        sorted_anchor_points[:] = []
        for anchor_points in all_anchor_points.values():
            if isinstance(anchor_points, dict):
                for prop in anchor_points.values():
                    for t, c in prop:
                        if t not in sorted_anchor_points:
                            sorted_anchor_points.append(t)
            else:
                for t, c in anchor_points:
                    if t not in sorted_anchor_points:
                        sorted_anchor_points.append(t)
        sorted_anchor_points.sort()

    def change_time(v):
        global time
        time = round(v, 2)
        transform_viewer.play(False)
        camera_viewer.play(False)
        renpy.restart_interaction()

    # def set_anchor_point():
    #     camera_viewer.set_camera_anchor_point()
    #     for layer in renpy.store._3d_layers:
    #         camera_viewer.set_layer_anchor_point(layer)
    #     for layer in transform_viewer.state_org:
    #         for tag in {k: v for dic in [transform_viewer.state_org[layer], transform_viewer.state[layer]] for k, v in dic.items()}:
    #             kwargs = {p:transform_viewer.get_property(layer, tag, p, False) for p, d in transform_viewer.props} 
    #             transform_viewer.set_anchor_point(layer, tag, kwargs)

    def rollback():
        renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z-100, renpy.store._camera_rotate)
        camera_viewer.set_camera_anchor_point("_camera_z", renpy.store._camera_z)
        renpy.restart_interaction()

    def rollforward():
        renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z+100, renpy.store._camera_rotate)
        camera_viewer.set_camera_anchor_point("_camera_z", renpy.store._camera_z)
        renpy.restart_interaction()

    def action_editor():
        global time
        if not renpy.config.developer:
            return
        transform_viewer.init()
        camera_viewer.init()
        loops.clear()
        renpy.invoke_in_new_context(renpy.call_screen, "_action_editor")
        clear_anchor_points()
        time = 0
        camera_viewer.layer_reset()
        camera_viewer.camera_reset()

    def put_clipboard():
        camera_check_points = {}
        for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
            if coordinate in all_anchor_points:
                camera_check_points[coordinate[8:]] = [c for t, c in all_anchor_points[coordinate]]
                if len(camera_check_points[coordinate[8:]]) == 1 and camera_check_points[coordinate[8:]][0][0] == getattr(renpy.store._viewers, coordinate):
                    del camera_check_points[coordinate[8:]]

        layer_check_points = {}
        loop = {}
        for layer in renpy.store._3d_layers:
            if "layer "+layer in all_anchor_points:
                layer_check_points[layer]=[c for t, c in all_anchor_points["layer "+layer]]
                if len(layer_check_points[layer]) == 1 and layer_check_points[layer][0][0] == camera_viewer._3d_layers[layer]:
                    del layer_check_points[layer]
                if loops[layer+"_loop"]:
                    loop[layer+"_loop"] = True
        for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
            if loops[coordinate+"_loop"]:
                loop[coordinate[8:]+"_loop"] = True
        string = ""

        if camera_check_points or layer_check_points:
            string += """
    $all_moves(camera_check_points={}, layer_check_points={}, subpixel=True, **{})""".format(camera_check_points, layer_check_points, loop)

        for k, v in all_anchor_points.items():
            if isinstance(k, tuple):
                tag, layer = k
                string += """
    show {} onlayer {}:
        subpixel True """.format(*k)
                # kwargs_org = {k2: v2 for dic in [transform_viewer.state_org[layer], transform_viewer.state[layer]] for k2, v2 in dic.items()}[tag]
                for p, d in transform_viewer.props:
                    if p in all_anchor_points[k]:
                        check_points = [c for t, c in all_anchor_points[k][p]]
                        # if kwargs_org[p] is None and p != "rotate":
                        #     kwargs_org[p] = d

                        string += """
        parallel:"""
                        # if check_points[0][0] != kwargs_org[p]:
                        string += """
            {} {}""".format(p, check_points[0][0])
                        for i, check_point in enumerate(check_points[1:]):
                            string += """
            {} {} {} {}""".format(check_point[2], check_points[i+1][1]-check_points[i][1], p, check_point[0])
                        if loops[tag+"_"+layer+"_"+p+"_loop"]:
                                string += """
            repeat"""

        if string:
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, string)
            except:
                renpy.notify(_("Can't open clipboard"))
            else:
                #syntax hilight error in vim
                renpy.notify("Putted\n{}\n\non clipboard".format(string).replace("{", "{{").replace("[", "[["))
        else:
            renpy.notify(_("Nothing to put"))

