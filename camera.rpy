#
# 3D Camera motion
# ================
#
# With some limitations, Ren'Py can simulate 3D camera motion. This will easily
# let you achieve a parallax effect by placing sprites and assets on a 3D field.
# Ren'Py applies transforms to each layers which are registered as 3D layer by
# positions of a camera and 3D layers on a 3D field to simulate 3D camera motion.
#
# If you use this feature, in the first, set additional layers to be
# registered as 3D layer.
#
# For example, Write a code like below in options.rpy and add 'background', 'middle', 'forward'  layers.::
#
#         config.layers = ['master', 'background', 'middle', 'forward', 'transient', 'screens', 'overlay']
#
# Second, register layers which participate to a 3D motion as 3d layers by :func:`register_3d_layer`::
#
#         init python:
#             register_3d_layer('background', 'middle', 'forward')
#
# Then, a camera and layers can move. ::
#
#          label start:
#              # reset a camera and layers positions
#              $ camera_reset()
#              scene bg onlayer background
#              show A onlayer middle
#              show B onlayer forward
#              # It takes 0 second to move layers
#              $ layer_move("background", 2000)
#              $ layer_move("middle", 1500)
#              $ layer_move("forward", 1000)
#              with dissolve
#              'It takes 1 second to move a camera to (1800, 0, 0)'
#              $ camera_move(1800, 0, 0, 0, 1)
#              'It takes 5 seconds to move a camera to (0, 0, 1600)'
#              $ camera_move(0, 0, 1600, 0, 5)
#              'A camera moves to (0, 0, 0) at the moment'
#              $ camera_move(0, 0, 0)
#              'It takes 1 second to rotate a camera to 180 degrees'
#              $ camera_move(0, 0, 0, 180, 1)
#              'It takes 1 second to rotate a camera to -180 degrees and 0.5 second to move a camera to (-1800, 0, 500)'
#              $ camera_moves( ( (0, 0, 0, 0, 1), (-1800, 0, 500, 0, 1.5) ) )
#              'a camera shuttles between (-1800, 0, 500) and (0, 0, 0)'
#              $ camera_moves( ( (0, 0, 0, 0, .5), (-1800, 0, 500, 0, 1) ), loop=True)
#
# When :var:`config.developer` is True, pressing position_viewer (by default,
# "shift+P"), will open Position Viewer. This allow you to adjustment a camera
# ,3D layers and images positions by bars and manual inputs and see the result at
# the moment.
#
# Notice that 3D camera motion has some limits.:
#
# * 3D camera motion applies transforms to 3D layers, so the show layer statement or
#   :func:`renpy.show_layer_at` to 3D layers can't be usable.
#
# * z coordinates of 3D layers don't affect the stacking order of 3d layers.
#
# * A camera and a layer can't move at the same time.
#
# * By default, the scene, hide statements use master or the given layer
#   only. If you use 3D layers preferentially, set Ren'py like below.::
#
#         init -1 python hide:
#             def hide(name, layer='master'):
#                 for l in _3d_layers:
#                     if renpy.showing(name, l):
#                         renpy.hide(name, l)
#                         break
#                 else:
#                     renpy.hide(name, layer)
#
#             config.hide = hide
#
#             def scene(layer='master'):
#
#                 renpy.scene(layer)
#                 for l in _3d_layers:
#                     renpy.scene(l)
#
#             config.scene = scene
#
# Camera Functions
# ----------------
#
#    def register_3d_layer(*layers):
#        """
#         :doc: camera
#
#         Register layers as 3D layers. 3D layers is applied transforms to by
#         positions of a camera and 3D layers. You can use this in game again
#         and again.
#
#         `layers`
#              This should be the string or strings of a layer name.
#         """
#
#    def camera_reset():
#        """
#         :doc: camera
#
#         Reset a camera and 3D layers positions.
#         """
#
#    def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False):
#        """
#         :doc: camera
#
#         Move the coordinate and rotate of a camera and apply transforms to all 3D layers.
#
#         `x`
#              the x coordinate of a camera
#         `y`
#              the y coordinate of a camera
#         `z`
#              the z coordinate of a camera
#         `rotate`
#              Defaul 0, the rotate of a camera
#         `duration`
#              Default 0, this is the second times taken to move a camera.
#         `warper`
#              Default 'linear', this should be string and the name of a warper
#              registered with ATL.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#         `loop`
#              Default False, if True, this motion repeats.
#         """
#
#    def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False):
#        """
#         :doc: camera
#
#         Move the z coordinate of a layer and apply transform to the layer.
#
#         `layer`
#              the string of a layer name to be moved
#         `z`
#              the z coordinate of a layer
#         `duration`
#              Default 0, this is the second times taken to move a camera.
#         `warper`
#              Default 'linear', this should be the string of the name of a
#              warper registered with ATL.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#         `loop`
#              Default False, if True, this motion repeats.
#         """
#
#    def camera_moves(check_points, warper='linear', loop=False, subpixel=True):
#        """
#         :doc: camera
#
#         Move a camera through check points and apply transforms to all 3D
#         layers.
#
#         `check_points`
#              tuples of x, y, z, rotate, duration
#         `loop`
#              Default False, if True, this sequence of motions repeats.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#         """
#
#    def layer_moves(layer, check_points, warper='linear', loop=False, subpixel=True):
#        """
#         :doc: camera
#
#         Move a layer through check points and apply transform to the layer.
#
#         `layer`
#              the string of a layer name to be moved
#         `check_points`
#              tuples of z, duration
#         `loop`
#              Default False, if True, this sequence of motions repeats.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#         """

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

         Register layers as 3D layers. 3D layers is applied transforms to by
         positions of a camera and 3D layers. You can use this in game again
         and again.

         `layers`
              This should be the string or strings of a layer name.
         """
        global _3d_layers
        af_3d_layers = {}
        for layer in layers:
            af_3d_layers[layer] = _layer_z
        _3d_layers = af_3d_layers

    def camera_reset():
        """
         :doc: camera

         Reset a camera and 3D layers positions.
         """
        camera_move(0, 0, 0, 0)
        for layer in _3d_layers:
            layer_move(layer, _layer_z)

    def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False):
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
         """

        camera_moves(((x, y, z, rotate, duration), ), warper=warper, subpixel=subpixel, loop=loop)

    def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False):
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
         """

        layer_moves(layer, ((z, duration), ), warper=warper, subpixel=subpixel, loop=loop)

    def camera_moves(check_points, warper='linear', loop=False, subpixel=True):
        """
         :doc: camera

         Move a camera through check points and apply transforms to all 3D
         layers.

         `check_points`
              tuples of x, y, z, rotate, duration
         `loop`
              Default False, if True, this sequence of motions repeats.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         """
        global _camera_x, _camera_y, _camera_z, _camera_rotate

        af_3d_layers = {}
        for layer in _3d_layers:
            start_xanchor = _focal_length*_camera_x/(config.screen_width *_layer_z) + .5
            start_yanchor = _focal_length*_camera_y/(config.screen_height*_layer_z) + .5

            check_points2 = [(_camera_z, _camera_rotate, start_xanchor, start_yanchor, _3d_layers[layer], 0), ]
            for c in check_points:
                xanchor = _focal_length*c[0]/(config.screen_width *_layer_z) + .5
                yanchor = _focal_length*c[1]/(config.screen_height*_layer_z) + .5
                duration = float(c[4])
                check_points2.append((c[2], c[3], xanchor, yanchor, _3d_layers[layer], duration))

            renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(function=renpy.curry(_camera_trans)(check_points=check_points2, warper=warper, loop=loop, subpixel=subpixel, layer=layer))])

        _camera_x = check_points[-1][0]
        _camera_y = check_points[-1][1]
        _camera_z = check_points[-1][2]
        _camera_rotate = check_points[-1][3]

    def layer_moves(layer, check_points, warper='linear', loop=False, subpixel=True):
        """
         :doc: camera

         Move a layer through check points and apply transform to the layer.

         `layer`
              the string of a layer name to be moved
         `check_points`
              tuples of z, duration
         `loop`
              Default False, if True, this sequence of motions repeats.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         """
        global _3d_layers, _camera_x, _camera_y, _camera_z, _camera_rotate

        start_xanchor = _focal_length*_camera_x/(config.screen_width *_layer_z) + .5
        start_yanchor = _focal_length*_camera_y/(config.screen_height*_layer_z) + .5

        check_points2 = [(_camera_z, _camera_rotate, start_xanchor, start_yanchor, _3d_layers[layer], 0), ]
        af_3d_layers = _3d_layers.copy()
        for c in check_points:
            check_points2.append((_camera_z, _camera_rotate, start_xanchor, start_yanchor, c[0], float(c[1])))

        renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(function=renpy.curry(_camera_trans)(check_points=check_points2, warper=warper, loop=loop, subpixel=subpixel, layer=layer))])

        af_3d_layers[layer] = check_points[-1][0]
        _3d_layers = af_3d_layers

    def _camera_trans(tran, st, at, check_points, warper, loop, subpixel, layer):
        # check_points = (z, r, xanchor, yanchor, layer_z, duration)
        duration = check_points[-1][5]
        tran.xpos    = .5 
        tran.ypos    = .5
        tran.subpixel = subpixel
        tran.transform_anchor = True
        if duration > 0:
            g = renpy.atl.warpers[warper](st/duration) 
            if loop:
                g = g % 1

            for i in xrange(1, len(check_points)):
                checkpoint_g = check_points[i][5]/duration
                pre_checkpoint_g = check_points[i-1][5]/duration
                if g <= checkpoint_g:
                    start = check_points[i-1]
                    goal = check_points[i]
                    ch_g = (g - pre_checkpoint_g) / (checkpoint_g - pre_checkpoint_g)

                    z = ch_g*(goal[0]-start[0])+start[0]
                    layer_z = ch_g*(goal[4]-start[4])+start[4]
                    distance = float(layer_z - z)
                    if distance == 0:
                        distance = .1

                    tran.xanchor = ch_g*(goal[2]-start[2]) + start[2]
                    tran.yanchor = ch_g*(goal[3]-start[3]) + start[3]
                    tran.rotate  = ch_g*(goal[1]  -  start[1]) + start[1]

                    if distance >= 0:
                        tran.alpha = 1
                        tran.zoom = _layer_z / distance
                    else:
                        tran.alpha = 0
                    return .005
        distance = float(check_points[-1][4] - check_points[-1][0])
        if distance == 0:
            distance = .1
        tran.xanchor = check_points[-1][2]
        tran.yanchor = check_points[-1][3]
        tran.zoom = _layer_z / distance
        tran.rotate = check_points[-1][1]
        if distance >= 0:
            tran.alpha = 1
        else:
            tran.alpha = 0
        return None



init -1600 python:

    ##########################################################################
    # TransformViewer
    class TransformViewer(object):
        def __init__(self):

            self.int_range = 1500
            self.float_range = 7.0
            # layer->tag->property->value
            self.state_org = {}
            # {property:(default, float)}, default is used when property can't be got.
            self.props_default = {
            "xpos":(0., False),
            "ypos":(0., False),
            "xanchor":(0., False),
            "yanchor":(0., False),
            "xzoom":(1., True),
            "yzoom":(1., True),
            "zoom":(1., True),
            "rotate":(0, False),
            "alpha":(1., True),
            "additive":(0., True),
            }

        def init(self):
            if not config.developer:
                return
            sle = renpy.game.context().scene_lists
            # back up for reset()
            for layer in config.layers:
                self.state_org[layer] = {}
                for tag in sle.layers[layer]:
                    d = sle.get_displayable_by_tag(layer, tag[0])
                    if isinstance(d, renpy.display.screen.ScreenDisplayable):
                        break
                    pos = renpy.get_placement(d)
                    state = getattr(d, "state", None)

                    self.state_org[layer][tag[0]] = {}
                    for p in ["xpos", "ypos", "xanchor", "yanchor"]:
                        self.state_org[layer][tag[0]][p] = getattr(pos, p, None)
                    for p in self.props_default:
                        if not self.state_org[layer][tag[0]].has_key(p):
                            self.state_org[layer][tag[0]][p] = getattr(state, p, None)

        def reset(self):
            for layer in config.layers:
                for tag, props in self.state_org[layer].iteritems():
                    if tag and props:
                        kwargs = props.copy()
                        for p in self.props_default:
                            if kwargs[p] is None and p != "rotate":
                                kwargs[p] = self.props_default[p][0]
                        renpy.show(tag, [Transform(**kwargs)], layer=layer)
            renpy.restart_interaction()

        def generate_changed(self, layer, tag, prop, int=False):
            def changed(v):
                kwargs = {}
                for p in self.props_default:
                    kwargs[p] = self.get_state(layer, tag, p, False)

                if int and not self.props_default[prop][1]:
                    kwargs[prop] = v - self.int_range
                else:
                    kwargs[prop] = v -self.float_range
                renpy.show(tag, [Transform(**kwargs)], layer=layer)
                renpy.restart_interaction()
            return changed

        def get_state(self, layer, tag, prop, default=True):
            sle = renpy.game.context().scene_lists

            if tag:
                d = sle.get_displayable_by_tag(layer, tag)
                pos = renpy.get_placement(d)
                state = getattr(pos, prop, None)
                if state is None:
                    state = getattr(getattr(d, "state", None), prop, None)
                # set default
                if state is None and default:
                    state = self.props_default[prop][0]
                if state and self.props_default[prop][1]:
                    state = float(state)
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
            string = "show %s onlayer %s" % (tag, layer)
            for k, v in self.props_default.iteritems():
                value = self.get_state(layer, tag, k)
                if value != v[0]:
                    if string.find(":") < 0:
                        string += ":\n    "
                    string += "%s %s " % (k, value)
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, string)
            except:
                renpy.notify(_("Can't open clipboard"))
            else:
                renpy.notify(__('Putted "%s" on clipboard') % string)

        def edit_value(self, function, int=False):
            v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen")
            if v:
                try:
                    if int:
                        v = renpy.python.py_eval(v) + self.int_range
                    else:
                        v = renpy.python.py_eval(v) + self.float_range
                    function(v)
                except:
                    renpy.notify(_("Please type value"))
    _transform_viewer = TransformViewer()

    ##########################################################################
    # CameraViewer
    class CameraViewer(object):

        def __init__(self):
            self.range_camera_pos   = 6000
            self.range_rotate       = 360
            self.range_layer_z   = 10000

        def init(self):
            if not config.developer:
                return
            self._camera_x = _camera_x
            self._camera_y = _camera_y
            self._camera_z = _camera_z
            self._camera_rotate = _camera_rotate
            self._3d_layers = _3d_layers.copy()

        def camera_reset(self):
            camera_move(self._camera_x, self._camera_y, self._camera_z, self._camera_rotate)
            renpy.restart_interaction()

        def layer_reset(self):
            global _3d_layers
            for layer in _3d_layers:
                layer_move(layer, self._3d_layers[layer])
            renpy.restart_interaction()

        def x_changed(self, v):
            camera_move(v - self.range_camera_pos, _camera_y, _camera_z, _camera_rotate)
            renpy.restart_interaction()

        def y_changed(self, v):
            camera_move(_camera_x, v - self.range_camera_pos, _camera_z, _camera_rotate)
            renpy.restart_interaction()

        def z_changed(self, v):
            camera_move(_camera_x, _camera_y, v - self.range_camera_pos, _camera_rotate)
            renpy.restart_interaction()

        def r_changed(self, v):
            camera_move(_camera_x, _camera_y, _camera_z, v - self.range_rotate)
            renpy.restart_interaction()

        def generate_layer_z_changed(self, l):
            def layer_z_changed(v):
                layer_move(l, v)
                renpy.restart_interaction()
            return layer_z_changed

        def put_clipboard(self, camera_tab, layer=""):
            string = '$camera_move(%s, %s, %s, %s, duration=0)' % (_camera_x, _camera_y, _camera_z, _camera_rotate)
            if not camera_tab:
                string = '$layer_move("%s", %s, duration=0)' % (layer, _3d_layers[layer])
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, string)
            except:
                renpy.notify(_("Can't open clipboard"))
            else:
                renpy.notify(__("Putted '%s' on clipboard") % string)

        def edit_value(self, function, range):
            v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen")
            if v:
                try:
                    function(renpy.python.py_eval(v) + range)
                except:
                    renpy.notify(_("Please type value"))
    _camera_viewer = CameraViewer()

    def _position_viewer():
        if not config.developer:
            return
        _transform_viewer.init()
        _camera_viewer.init()
        renpy.invoke_in_new_context(renpy.call_screen, "_position_viewer")
        _camera_viewer.layer_reset()
        _camera_viewer.camera_reset()

screen _rot(): #show rule of thirds
    for i in range(1, 3):
        add Solid("#F00", xsize=config.screen_width, ysize=1, ypos=config.screen_height*i/3) 
        add Solid("#F00", xsize=1, ysize=config.screen_height, xpos=config.screen_width*i/3) 

screen _position_viewer(tab="images", layer="master", tag=""):
    key "game_menu" action Return()
    zorder 10

    frame:
        xfill True
        style_group "position_viewer"
        has vbox

        hbox:
            xfill False
            textbutton _("Images") action [SelectedIf(tab == "images"), Show("_position_viewer", tab="images")]
            textbutton _("3D Layers") action [SelectedIf(tab == "3D"), Show("_position_viewer", tab="3D")]
            textbutton _("Camera") action [SelectedIf(tab == "camera"), Show("_position_viewer", tab="camera")]
            textbutton _("Rule of thirds") action [SelectedIf(renpy.get_screen("_rot")), If(renpy.get_screen("_rot"), true=Hide("_rot"), false=Show("_rot"))]
        null height 10
        if tab == "images":
            hbox:
                xfill False
                label _("layers")
                for l in config.layers:
                    if l not in ["screens", "transient", "overlay"]:
                        textbutton "[l]" action [SelectedIf(l == layer), Show("_position_viewer", tab=tab, layer=l)]
            hbox:
                xfill False
                label _("images")
                for t in _transform_viewer.state_org[layer]:
                    textbutton "[t]" action [SelectedIf(t == tag), Show("_position_viewer", tab=tab, layer=layer, tag=t)]

            if tag:
                textbutton _("clip board") action Function(_transform_viewer.put_show_clipboard, tag, layer)
                for p in sorted(_transform_viewer.props_default.keys()):
                    $state = _transform_viewer.get_state(layer, tag, p)
                    if isinstance(state, int):
                        hbox:
                            $ f = _transform_viewer.generate_changed(layer, tag, p, True)
                            textbutton "[p]" action Function(_transform_viewer.put_prop_clipboard, p, state)
                            textbutton "[state]" action Function(_transform_viewer.edit_value, f, int)
                            bar adjustment ui.adjustment(range=_transform_viewer.int_range*2, value=state+_transform_viewer.int_range, page=1, changed=f) xalign 1.
                    elif isinstance(state, float):
                        hbox:
                            $ f = _transform_viewer.generate_changed(layer, tag, p)
                            textbutton "[p]" action Function(_transform_viewer.put_prop_clipboard, p, state)
                            textbutton "[state:>.4]" action Function(_transform_viewer.edit_value, f)
                            bar adjustment ui.adjustment(range=_transform_viewer.float_range*2, value=state+_transform_viewer.float_range, page=.05, changed=f) xalign 1.
        elif tab == "camera":
            textbutton _("clip board") action Function(_camera_viewer.put_clipboard, True)
            hbox:
                label "x"
                textbutton "[_camera_x]" action Function(_camera_viewer.edit_value, _camera_viewer.x_changed, _camera_viewer.range_camera_pos)
                bar adjustment ui.adjustment(range=_camera_viewer.range_camera_pos*2, value=_camera_x+_camera_viewer.range_camera_pos, page=1, changed=_camera_viewer.x_changed) xalign 1.
            hbox:
                label "y"
                textbutton "[_camera_y]" action Function(_camera_viewer.edit_value, _camera_viewer.y_changed, _camera_viewer.range_camera_pos)
                bar adjustment ui.adjustment(range=_camera_viewer.range_camera_pos*2, value=_camera_y+_camera_viewer.range_camera_pos, page=1, changed=_camera_viewer.y_changed) xalign 1.
            hbox:
                label "z"
                textbutton "[_camera_z]" action Function(_camera_viewer.edit_value, _camera_viewer.z_changed, _camera_viewer.range_camera_pos)
                bar adjustment ui.adjustment(range=_camera_viewer.range_camera_pos*2, value=_camera_z+_camera_viewer.range_camera_pos, page=1, changed=_camera_viewer.z_changed) xalign 1.
            hbox:
                label "rotate"
                textbutton "[_camera_rotate]" action Function(_camera_viewer.edit_value, _camera_viewer.r_changed, _camera_viewer.range_rotate)
                bar adjustment ui.adjustment(range=_camera_viewer.range_rotate*2, value=_camera_rotate+_camera_viewer.range_rotate, page=1, changed=_camera_viewer.r_changed) xalign 1.
        elif tab == "3D":
            for layer in sorted(_3d_layers.keys()):
                hbox:
                    textbutton "[layer]" action Function(_camera_viewer.put_clipboard, False, layer)
                    textbutton "{}".format(int(_3d_layers[layer])) action Function(_camera_viewer.edit_value, _camera_viewer.generate_layer_z_changed(layer), 0)
                    bar adjustment ui.adjustment(range=_camera_viewer.range_layer_z, value=_3d_layers[layer], page=1, changed=_camera_viewer.generate_layer_z_changed(layer)) xalign 1.
        hbox:
            xfill False
            xalign 1.
            if tab == "images":
                textbutton _("reset") action [_transform_viewer.reset, renpy.restart_interaction]
            elif tab == "camera":
                textbutton _("reset") action [_camera_viewer.camera_reset, renpy.restart_interaction]
            elif tab == "3D":
                textbutton _("reset") action [_camera_viewer.layer_reset, renpy.restart_interaction]
            textbutton _("close") action Return()

init -1600:
    style position_viewer_frame background "#0006"
    style position_viewer_button size_group "transform_viewer"
    style position_viewer_button_text xalign .5
    style position_viewer_label xminimum 100
    style position_viewer_vbox xfill True

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
        position_viewer = _position_viewer,
        )

    config.underlay = [ km ]

    del km


init 1100 python:
    config.locked = False
    config.keymap["position_viewer"] = ['P']
    config.locked = True
