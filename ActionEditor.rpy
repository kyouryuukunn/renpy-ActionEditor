screen _action_editor(tab="images", layer="master", name="", time=0):
    key "game_menu" action Return()
    key "rollback"    action _viewers.rollback
    key "rollforward" action _viewers.rollforward
    if _viewers.sorted_keyframes:
        key "K_SPACE" action [SensitiveIf(_viewers.sorted_keyframes), Function(_viewers.camera_viewer.play, play=True), Function(_viewers.transform_viewer.play, play=True), Hide("_action_editor"), Show("_action_editor", tab=tab, layer=layer, name=name, time=_viewers.sorted_keyframes[-1]), renpy.restart_interaction]
    else:
        key "K_SPACE" action [SensitiveIf(_viewers.sorted_keyframes), Function(_viewers.camera_viewer.play, play=True), Function(_viewers.transform_viewer.play, play=True), Hide("_action_editor"), Show("_action_editor", tab=tab, layer=layer, name=name), renpy.restart_interaction]
    if _viewers.fps_keymap:
        key "s" action Function(_viewers.camera_viewer.y_changed, _camera_y+100+_viewers.camera_viewer.range_camera_pos)
        key "w" action Function(_viewers.camera_viewer.y_changed, _camera_y-100+_viewers.camera_viewer.range_camera_pos)
        key "a" action Function(_viewers.camera_viewer.x_changed, _camera_x-100+_viewers.camera_viewer.range_camera_pos)
        key "d" action Function(_viewers.camera_viewer.x_changed, _camera_x+100+_viewers.camera_viewer.range_camera_pos)
        key "S" action Function(_viewers.camera_viewer.y_changed, _camera_y+1000+_viewers.camera_viewer.range_camera_pos)
        key "W" action Function(_viewers.camera_viewer.y_changed, _camera_y-1000+_viewers.camera_viewer.range_camera_pos)
        key "A" action Function(_viewers.camera_viewer.x_changed, _camera_x-1000+_viewers.camera_viewer.range_camera_pos)
        key "D" action Function(_viewers.camera_viewer.x_changed, _camera_x+1000+_viewers.camera_viewer.range_camera_pos)
    else:
        key "j" action Function(_viewers.camera_viewer.y_changed, _camera_y+100+_viewers.camera_viewer.range_camera_pos)
        key "k" action Function(_viewers.camera_viewer.y_changed, _camera_y-100+_viewers.camera_viewer.range_camera_pos)
        key "h" action Function(_viewers.camera_viewer.x_changed, _camera_x-100+_viewers.camera_viewer.range_camera_pos)
        key "l" action Function(_viewers.camera_viewer.x_changed, _camera_x+100+_viewers.camera_viewer.range_camera_pos)
        key "J" action Function(_viewers.camera_viewer.y_changed, _camera_y+1000+_viewers.camera_viewer.range_camera_pos)
        key "K" action Function(_viewers.camera_viewer.y_changed, _camera_y-1000+_viewers.camera_viewer.range_camera_pos)
        key "H" action Function(_viewers.camera_viewer.x_changed, _camera_x-1000+_viewers.camera_viewer.range_camera_pos)
        key "L" action Function(_viewers.camera_viewer.x_changed, _camera_x+1000+_viewers.camera_viewer.range_camera_pos)

    if time:
        timer time+1 action Function(_viewers.change_time, _viewers.time)
    $state={k: v for dic in [_viewers.transform_viewer.state_org[layer], _viewers.transform_viewer.state[layer]] for k, v in dic.items()}

    if _viewers.default_rot and store._first_load:
        $store._first_load = False
        on "show" action Show("_rot")

    frame:
        background "#0006"
        if time:
            at _delay_show(time + 1)
        vbox:

            hbox:
                style_group "action_editor_a"
                textbutton _("time: [_viewers.time:>.2f] s") action Function(_viewers.edit_time)
                textbutton _("<") action Function(_viewers.prev_time)
                textbutton _(">") action Function(_viewers.next_time)
                bar adjustment ui.adjustment(range=7.0, value=_viewers.time, changed=_viewers.change_time) xalign 1. yalign .5
            hbox:
                style_group "action_editor_a"
                hbox:
                    textbutton _("default warper") action _viewers.select_default_warper
                    textbutton _("rot") action [SelectedIf(renpy.get_screen("_rot")), If(renpy.get_screen("_rot"), true=Hide("_rot"), false=Show("_rot"))]
                    textbutton _("hide") action HideInterface()
                    # textbutton _("window") action _viewers.AddWindow() #renpy.config.empty_window
                    if _viewers.sorted_keyframes:
                        textbutton _("play") action [SensitiveIf(_viewers.sorted_keyframes), Function(_viewers.camera_viewer.play, play=True), Function(_viewers.transform_viewer.play, play=True), Hide("_action_editor"), Show("_action_editor", tab=tab, layer=layer, name=name, time=_viewers.sorted_keyframes[-1]), renpy.restart_interaction]
                    else:
                        textbutton _("play") action [SensitiveIf(_viewers.sorted_keyframes), Function(_viewers.camera_viewer.play, play=True), Function(_viewers.transform_viewer.play, play=True), Hide("_action_editor"), Show("_action_editor", tab=tab, layer=layer, name=name), renpy.restart_interaction]
                    textbutton _("clipboard") action Function(_viewers.put_clipboard)
                hbox:
                    xalign 1.
                    textbutton _("close") action Return()
            hbox:
                style_group "action_editor_a"
                textbutton _("clear keyframes") action [SensitiveIf(_viewers.sorted_keyframes), Function(_viewers.clear_keyframes), renpy.restart_interaction]
                textbutton _("remove keyframes") action [SensitiveIf(_viewers.time in _viewers.sorted_keyframes), Function(_viewers.remove_keyframes, _viewers.time), renpy.restart_interaction]
                textbutton _("move keyframes") action [SensitiveIf(_viewers.time in _viewers.sorted_keyframes), SetField(_viewers, "moved_time", _viewers.time), Show("_move_keyframes")]
                textbutton _("last moves") action [SensitiveIf(_last_camera_arguments), Function(_viewers.last_moves), renpy.restart_interaction]
            null height 10
            hbox:
                style_group "action_editor_a"
                xfill False
                textbutton _("Images") action [SelectedIf(tab == "images"), Show("_action_editor", tab="images")]
                textbutton _("2D Camera") action [SensitiveIf(list(_3d_layers.keys()) == ["master"]), SelectedIf(tab == "2D Camera"), Show("_action_editor", tab="2D Camera")]
                textbutton _("3D Layers") action [SelectedIf(tab == "3D Layers"), Show("_action_editor", tab="3D Layers")]
                textbutton _("3D Camera") action [SelectedIf(tab == "3D Camera"), Show("_action_editor", tab="3D Camera")]
            if tab == "images":
                hbox:
                    style_group "action_editor_a"
                    for l in config.layers:
                        if l not in ["screens", "transient", "overlay"]:
                            textbutton "[l]" action [SelectedIf(l == layer), Show("_action_editor", tab=tab, layer=l)]
                hbox:
                    style_group "action_editor_a"
                    textbutton _("+") action Function(_viewers.transform_viewer.add_image, layer)
                    for n in state:
                        textbutton "{}".format(n.split()[0]) action [SelectedIf(n == name), Show("_action_editor", tab=tab, layer=layer, name=n)]

                if name in state:
                    for p, d in _viewers.transform_viewer.props:
                        $prop = _viewers.transform_viewer.get_property(layer, name.split()[0], p)
                        $ f = _viewers.transform_viewer.generate_changed(layer, name, p)
                        if p not in _viewers.transform_viewer.force_float and ((state[name][p] is None and isinstance(d, int)) or isinstance(state[name][p], int)):
                            hbox:
                                style_group "action_editor"
                                textbutton "[p]" action [SensitiveIf((name, layer, p) in _viewers.all_keyframes), SelectedIf(_viewers.keyframes_exist((name, layer, p))), Show("_edit_keyframe", k=(name, layer, p), int=True)]
                                textbutton "[prop]" action Function(_viewers.transform_viewer.edit_value, f, True, default=prop) alternate Function(_viewers.transform_viewer.reset, name, layer, p)
                                bar adjustment ui.adjustment(range=_viewers.transform_viewer.int_range*2, value=prop+_viewers.transform_viewer.int_range, page=1, changed=f) xalign 1. yalign .5
                        else:
                            hbox:
                                style_group "action_editor"
                                textbutton "[p]" action [SensitiveIf((name, layer, p) in _viewers.all_keyframes), SelectedIf(_viewers.keyframes_exist((name, layer, p))), Show("_edit_keyframe", k=(name, layer, p))]
                                textbutton "[prop:>.2f]" action Function(_viewers.transform_viewer.edit_value, f, False, default=prop) alternate Function(_viewers.transform_viewer.reset, name, layer, p)
                                bar adjustment ui.adjustment(range=_viewers.transform_viewer.float_range*2, value=prop+_viewers.transform_viewer.float_range, page=.05, changed=f) xalign 1. yalign .5
            elif tab == "3D Camera" or tab == "2D Camera":
                if list(_3d_layers.keys()) == ["master"] and tab == "3D Camera":
                    label _("Please register 3D layers")
                else:
                    hbox:
                        style_group "action_editor"
                        textbutton "x" action [SensitiveIf("_camera_x" in _viewers.all_keyframes), SelectedIf(_viewers.keyframes_exist("_camera_x")), Show("_edit_keyframe", k="_camera_x")]
                        textbutton "[_camera_x: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.x_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_x) alternate [Function(camera_move, _viewers.camera_viewer._camera_x, _camera_y, _camera_z, _camera_rotate), renpy.restart_interaction]
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_x+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.x_changed) xalign 1. yalign .5
                    hbox:
                        style_group "action_editor"
                        textbutton "y" action [SensitiveIf("_camera_y" in _viewers.all_keyframes), SelectedIf(_viewers.keyframes_exist("_camera_y")), Show("_edit_keyframe", k="_camera_y")]
                        textbutton "[_camera_y: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.y_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_y) alternate [Function(camera_move, _camera_x, _viewers.camera_viewer._camera_y, _camera_z, _camera_rotate), renpy.restart_interaction]
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_y+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.y_changed) xalign 1. yalign .5
                    hbox:
                        style_group "action_editor"
                        textbutton "z" action [SensitiveIf("_camera_z" in _viewers.all_keyframes), SelectedIf(_viewers.keyframes_exist("_camera_z")), Show("_edit_keyframe", k="_camera_z")]
                        textbutton "[_camera_z: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.z_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_z) alternate [Function(camera_move, _camera_x, _camera_y, _viewers.camera_viewer._camera_z, _camera_rotate), renpy.restart_interaction]
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_z+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.z_changed) xalign 1. yalign .5
                    hbox:
                        style_group "action_editor"
                        textbutton "rotate" action [SensitiveIf("_camera_rotate" in _viewers.all_keyframes), SelectedIf(_viewers.keyframes_exist("_camera_rotate")), Show("_edit_keyframe", k="_camera_rotate")]
                        textbutton "[_camera_rotate: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.r_changed, _viewers.camera_viewer.range_rotate, default=_camera_rotate) alternate [Function(camera_move, _camera_x, _camera_y, _camera_z, _viewers.camera_viewer._camera_rotate), renpy.restart_interaction]
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_rotate*2, value=_camera_rotate+_viewers.camera_viewer.range_rotate, page=1, changed=_viewers.camera_viewer.r_changed) xalign 1. yalign .5
                    if tab == "3D Camera":
                        hbox:
                            style_group "action_editor"
                            textbutton "focus"
                            textbutton "[_camera_focus: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.focus_changed, 0, default=_camera_focus) alternate [Function(focus_set, _viewers.camera_viewer._camera_focus), renpy.restart_interaction]
                            bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_focus, value=_camera_focus, page=1, changed=_viewers.camera_viewer.focus_changed) xalign 1. yalign .5
                        hbox:
                            style_group "action_editor"
                            textbutton "dof"
                            textbutton "[_camera_dof: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.dof_changed, 0, default=_camera_dof) alternate [Function(dof_set, _viewers.camera_viewer._camera_dof), renpy.restart_interaction]
                            bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_dof, value=_camera_dof, page=1, changed=_viewers.camera_viewer.dof_changed) xalign 1. yalign .5
            elif tab == "3D Layers":
                if list(_3d_layers.keys()) == ["master"]:
                    label _("Please register 3D layers")
                else:
                    for layer in sorted(_3d_layers.keys()):
                        hbox:
                            style_group "action_editor"
                            textbutton "[layer]" action [SensitiveIf(layer in _viewers.all_keyframes), SelectedIf(_viewers.keyframes_exist(layer)), SetField(_viewers, "moved_time", _viewers.time), Show("_edit_keyframe", k=layer)]
                            textbutton "{}".format(_3d_layers[layer]) action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.generate_layer_z_changed(layer), 0, default=_3d_layers[layer]) alternate [Function(layer_move, layer, _viewers.camera_viewer._3d_layers[layer]), renpy.restart_interaction]
                            bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_layer_z, value=_3d_layers[layer], page=1, changed=_viewers.camera_viewer.generate_layer_z_changed(layer)) xalign 1. yalign .5
            hbox:
                style_group "action_editor"
                xfill False
                xalign 1.
                if tab == "images":
                    if name:
                        textbutton _("remove") action [SensitiveIf(name in _viewers.transform_viewer.state[layer]), Show("_action_editor", tab=tab, layer=layer), Function(renpy.hide, name, layer), Function(_viewers.transform_viewer.state[layer].pop, name, layer), Function(_viewers.transform_viewer.remove_keyframes, name=name, layer=layer), _viewers.sort_keyframes]
                        textbutton _("clipboard") action Function(_viewers.transform_viewer.put_show_clipboard, name, layer)
                    textbutton _("reset") action [_viewers.transform_viewer.image_reset, renpy.restart_interaction]
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

init -1598:
    style action_editor_button:
        size_group "action_editor"
        outlines [ (absolute(1), "#000", absolute(0), absolute(0)) ]
        idle_background None
        insensitive_background None
    style action_editor_button_text:
        color "#aaa"
        selected_color "#fff"
        insensitive_color "#777"
        outlines [ (absolute(1), "#000", absolute(0), absolute(0)) ]
    style action_editor_a_button:
        take action_editor_button
        size_group None
    style action_editor_a_button_text take action_editor_button_text

    style action_editor_label:
        xminimum 110
    style action_editor_vbox xfill True

screen _input_screen(message="type value", default=""):
    modal True
    key "game_menu" action Return("")

    frame:
        background "#0006"
        style_group "input_screen"

        has vbox

        label message

        hbox:
            input default default

init -1598:
    style input_screen_frame xfill True ypos .1 xmargin .05 ymargin .05
    style input_screen_vbox xfill True spacing 30
    style input_screen_label xalign .5
    style input_screen_hbox  xalign .5

transform _delay_show(time):
    alpha 0
    pause time
    alpha 1

screen _rot(): #show rule of thirds
    for i in range(1, 3):
        add Solid("#F00", xsize=config.screen_width, ysize=1, ypos=config.screen_height*i//3)
        add Solid("#F00", xsize=1, ysize=config.screen_height, xpos=config.screen_width*i//3)

screen _warper_selecter(current_warper=""):
    modal True
    key "game_menu" action Return("")

    frame:
        background "#0006"
        style_group "warper_selecter"

        has vbox

        label _("Select a warper function")
        viewport:
            mousewheel True
            edgescroll (100, 100)
            xsize config.screen_width-500
            ysize config.screen_height-200
            scrollbars "vertical"
            vbox:
                for warper in sorted(renpy.atl.warpers.keys()):
                    textbutton warper action [SelectedIf((_viewers.warper == warper and not current_warper) or warper == current_warper), Return(warper)] hovered Show("_warper_graph", warper=warper) unhovered Hide("_warper")
        hbox:
            textbutton _("add") action OpenURL("http://renpy.org/wiki/renpy/doc/cookbook/Additional_basic_move_profiles")
            textbutton _("close") action Return("")

screen _warper_graph(warper):
    $ t=120
    $ length=300
    $ xpos=config.screen_width-400
    $ ypos=100
    # add Solid("#000", xsize=3, ysize=1.236*length, xpos=xpos+length/2, ypos=length/2+xpos, rotate=45, anchor=(.5, .5)) 
    add Solid("#CCC", xsize=length, ysize=length, xpos=xpos, ypos=ypos ) 
    add Solid("#000", xsize=length, ysize=3, xpos=xpos, ypos=length+ypos ) 
    add Solid("#000", xsize=length, ysize=3, xpos=xpos, ypos=ypos ) 
    add Solid("#000", xsize=3, ysize=length, xpos=xpos+length, ypos=ypos)
    add Solid("#000", xsize=3, ysize=length, xpos=xpos, ypos=ypos)
    for i in range(1, t):
        $ysize=int(length*renpy.atl.warpers[warper](i/float(t)))
        if ysize >= 0:
            add Solid("#000", xsize=length//t, ysize=ysize, xpos=xpos+i*length//t, ypos=length+ypos, yanchor=1.) 
        else:
            add Solid("#000", xsize=length//t, ysize=-ysize, xpos=xpos+i*length//t, ypos=length+ypos-ysize, yanchor=1.) 

screen _move_keyframes:
    modal True
    key "game_menu" action Hide("_move_keyframes")
    frame:
        background "#0006"
        has vbox
        textbutton _("time: [_viewers.moved_time:>.2f] s") action Function(_viewers.edit_move_all_keyframes)
        bar adjustment ui.adjustment(range=7.0, value=_viewers.moved_time, changed=renpy.curry(_viewers.move_keyframes)(old=_viewers.moved_time)) xalign 1. yalign .5
        textbutton _("close") action Hide("_move_keyframes") xalign .98

# _edit_keyframe((name, layer), "xpos")
# _edit_keyframe(_camera_x)
screen _edit_keyframe(k, int=False):
    $check_points = _viewers.all_keyframes[k]
    modal True
    key "game_menu" action Hide("_edit_keyframe")
    frame:
        background "#0009"
        xfill True
        has vbox
        label _("KeyFrames") xalign .5
        for v, t, w in check_points:
            if t != 0:
                hbox:
                    textbutton _("x") action [Function(_viewers.remove_keyframe, remove_time=t, k=k), renpy.restart_interaction] background None
                    textbutton _("{}".format(v)) action Function(_viewers.edit_the_value, check_points=check_points, old=t, value_org=v, int=int)
                    textbutton _("{}".format(w)) action Function(_viewers.edit_the_warper, check_points=check_points, old=t, value_org=w)
                    textbutton _("[t:>.2f] s") action Function(_viewers.edit_move_keyframes, check_points=check_points, old=t)
                    bar adjustment ui.adjustment(range=7.0, value=t, changed=renpy.curry(_viewers.move_keyframe)(old=t, check_points=check_points)) xalign 1. yalign .5
        hbox:
            textbutton _("loop") action ToggleDict(_viewers.loops, k)
            if k[:8] == "_camera_":
                textbutton _("expression") action Function(_viewers.edit_expression, k)
                textbutton _("spline") action ToggleDict(_viewers.splines, "camera")
            elif not isinstance(k, tuple):
                textbutton _("expression") action Function(_viewers.edit_expression, k)
                textbutton _("spline") action ToggleDict(_viewers.splines, k)
            textbutton _("close") action Hide("_edit_keyframe") xalign .98

init -1098 python:
    # Added keymap
    config.underlay.append(renpy.Keymap(
        # self_voicing = Preference("self voicing", "toggle"), #TODO ???
        action_editor = _viewers.action_editor,
        image_viewer = _open_image_viewer,
        ))

init -1598 python in _viewers:
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
            # ("xoffset", 0.), 
            # ("yoffset", 0.), 
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


                    string = ""
                    for e in tag.name:
                        string += str(e) + " "
                    name = string[:-1]
                    self.state_org[layer][name] = {}
                    for p in ["xpos", "ypos", "xanchor", "yanchor"]:
                        self.state_org[layer][name][p] = getattr(pos, p, None)
                    for p, d in self.props:
                        if p not in self.state_org[layer][name]:
                            self.state_org[layer][name][p] = getattr(state, p, None)

        def reset(self, name, layer, prop):
            state={k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}[name][prop]
            kwargs = {}
            for p, d in self.props:
                value = self.get_property(layer, name.split()[0], p, False)
                if value is not None:
                    kwargs[p] = value
                elif p != "rotate":
                    kwargs[p] = d
            kwargs[prop] = state
            renpy.show(name, [renpy.store.Transform(**kwargs)], layer=layer)
            renpy.restart_interaction()

        def image_reset(self):
            for layer in renpy.config.layers:
                for name, props in {k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}.iteritems():
                    for prop in props:
                        self.reset(name, layer, prop)

        def set_keyframe(self, layer, name, prop, value):

            keyframes = all_keyframes.get((name, layer, prop), [])
            if keyframes:
                for i, (v, t, w) in enumerate(keyframes):
                    if time < t:
                        keyframes.insert(i, (value, time, warper))
                        break
                    elif time == t:
                        keyframes[i] = ( value, time, warper)
                        break
                else:
                    keyframes.append((value, time, warper))
            else:
                if time == 0:
                    all_keyframes[(name, layer, prop)] = [(value, time, warper)]
                else:
                    org = {k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}[name][prop]
                    all_keyframes[(name, layer, prop)] = [(org, 0, None), (value, time, warper)]
            sort_keyframes()

        def play(self, play):
            for layer in renpy.config.layers:
                for name in {k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}:
                    check_points = {}
                    for prop, d in self.props:
                        if (name, layer, prop) in all_keyframes:
                            check_points[prop] = all_keyframes[(name, layer, prop)]
                    if not check_points: # ビューワー上でのアニメーション(フラッシュ等)の誤動作を抑制
                        continue
                    loop = {prop+"_loop": loops[(name, layer, prop)] for prop, d in self.props}
                    if play:
                        renpy.show(name, [renpy.store.Transform(function=renpy.curry(self.transform)(check_points=check_points, loop=loop))], layer=layer)
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

                        renpy.show(name, [renpy.store.Transform(**kwargs)], layer=layer)

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


        def generate_changed(self, layer, name, prop):
            state={k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}[name][prop]
            def changed(v):
                kwargs = {}
                for p, d in self.props:
                    value = self.get_property(layer, name.split()[0], p, False)
                    if value is not None:
                        kwargs[p] = value
                    elif p != "rotate":
                        kwargs[p] = d
                    if p == prop:
                        default = d
                if prop not in self.force_float and ( (state is None and isinstance(default, int)) or isinstance(state, int) ):
                    kwargs[prop] = v - self.int_range
                else:
                    kwargs[prop] = round(v -self.float_range, 2)

                self.set_keyframe(layer, name, prop, kwargs[prop])
                renpy.show(name, [renpy.store.Transform(**kwargs)], layer=layer)
                renpy.restart_interaction()
            return changed

        def get_property(self, layer, tag, prop, default=True):
            sle = renpy.game.context().scene_lists
            # if tag in self.state[layer]:
            #     #TODO
            #     default = True
            if tag:
                d = sle.get_displayable_by_tag(layer, tag)
                pos = renpy.get_placement(d)
                state = getattr(pos, prop, None)
                if state is None:
                    state = getattr(getattr(d, "state", None), prop, None)
                if state is None and default:
                    for p, value in self.props:
                        if p == prop:
                            state = value
                return state
            return None

        def put_show_clipboard(self, name, layer):
            string = """
    show %s onlayer %s""" % (name, layer)
            for p, d in self.props:
                value = self.get_property(layer, name.split()[0], p)
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
                renpy.notify(__('Placed \n"%s"\n on clipboard') % string)

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
            default = ()
            while True:
                name = renpy.invoke_in_new_context(renpy.call_screen, "_image_selecter", default=default)
                if isinstance(name, tuple): #press button
                    for n in renpy.display.image.images:
                        if set(n) == set(name):
                            string=""
                            for e in n:
                                string += e + " "
                            self.state[layer][string] = {}
                            renpy.show(string, layer=layer)
                            for p, d in self.props:
                                self.state[layer][string][p] = self.get_property(layer, string.split()[0], p, False)
                            all_keyframes[(string, layer, "xpos")] = [(self.state[layer][string]["xpos"], 0, None)]
                            remove_list = [n_org for n_org in self.state_org[layer] if n_org.split()[0] == n[0]]
                            for n_org in remove_list:
                                del self.state_org[layer][n_org]
                                for k in [k for k in all_keyframes if isinstance(k, tuple) and k[0] == n_org and k[1] == layer]:
                                    del all_keyframes[k]
                            sort_keyframes()
                            renpy.show_screen("_action_editor", tab="images", layer=layer, name=string)
                            return
                    else:
                        default = name
                elif name: #from input text
                    # for n in renpy.display.image.images: #テキスト入力からはいきなり表示しないようにする。
                    #     if set(n) == set(name.split()):
                    #         self.state[layer][name] = {}
                    #         renpy.show(name, layer=layer)
                    #         for p, d in self.props:
                    #             self.state[layer][name][p] = self.get_property(layer, name.split()[0], p, False)
                    #         all_keyframes[(name, layer, "xpos")] = [(self.state[layer][name]["xpos"], 0, None)]
                    #         remove_list = [n_org for n_org in self.state_org[layer] if n_org.split()[0] == n[0]]
                    #         for n_org in remove_list:
                    #             del self.state_org[layer][n_org]
                    #             transform_viewer.remove_keyframes(n_org, layer)
                    #         sort_keyframes()
                    #         renpy.show_screen("_action_editor", tab="images", layer=layer, name=name)
                    #         return
                    default = tuple(name.split())
                else:
                    renpy.notify(_("Please type image name"))
                    return

        def remove_keyframes(self, name, layer):
            for k in [k for k in all_keyframes if isinstance(k, tuple) and k[0] == name and k[1] == layer]:
                del all_keyframes[k]
    transform_viewer = TransformViewer()

    ##########################################################################
    # CameraViewer
    class CameraViewer(object):

        def __init__(self):
            self.range_camera_pos   = 6000
            self.range_rotate       = 360
            self.range_layer_z   = 10000
            self.range_focus       = 10000
            self.range_dof       = 2000

        def init(self):
            if not renpy.config.developer:
                return
            self._camera_x = renpy.store._camera_x
            self._camera_y = renpy.store._camera_y
            self._camera_z = renpy.store._camera_z
            self._camera_rotate = renpy.store._camera_rotate
            self._camera_focus = renpy.store._camera_focus
            self._camera_dof = renpy.store._camera_dof
            self._3d_layers = renpy.store._3d_layers.copy()

        def camera_reset(self):
            renpy.store.camera_move(self._camera_x, self._camera_y, self._camera_z, self._camera_rotate)
            renpy.store.focus_set(self._camera_focus)
            renpy.store.dof_set(self._camera_dof)
            renpy.restart_interaction()

        def layer_reset(self):
            for layer in renpy.store._3d_layers:
                renpy.store.layer_move(layer, self._3d_layers[layer])
            renpy.restart_interaction()

        def x_changed(self, v):
            v=int(v)
            renpy.store.camera_move(v - self.range_camera_pos, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate)
            self.set_camera_keyframe("_camera_x", v-self.range_camera_pos)
            renpy.restart_interaction()

        def y_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, v - self.range_camera_pos, renpy.store._camera_z, renpy.store._camera_rotate)
            self.set_camera_keyframe("_camera_y", v-self.range_camera_pos)
            renpy.restart_interaction()

        def z_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, v - self.range_camera_pos, renpy.store._camera_rotate)
            self.set_camera_keyframe("_camera_z", v-self.range_camera_pos)
            renpy.restart_interaction()

        def r_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, v - self.range_rotate)
            self.set_camera_keyframe("_camera_rotate", v-self.range_rotate)
            renpy.restart_interaction()

        def focus_changed(self, v):
            v=int(v)
            renpy.store.focus_set(v)
            self.set_camera_keyframe("_camera_focus", v)
            renpy.restart_interaction()

        def dof_changed(self, v):
            v=int(v)
            renpy.store.dof_set(v)
            self.set_camera_keyframe("_camera_dof", v)
            renpy.restart_interaction()

        def generate_layer_z_changed(self, l):
            def layer_z_changed(v):
                renpy.store.layer_move(l, int(v))
                self.set_layer_keyframe(l)
                renpy.restart_interaction()
            return layer_z_changed

        def put_clipboard(self, camera_tab):
            string = ""
            if camera_tab:
                string = """
    $camera_move(%s, %s, %s, %s, duration=0)""" % (renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate)
                string += """
    $focus_set(%s, duration=0)""" % (renpy.store._camera_focus)
                string += """
    $dof_set(%s, duration=0)""" % (renpy.store._camera_dof)
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
                renpy.notify(__("Placed \n'%s'\n on clipboard") % string)

        def edit_value(self, function, range, default=""):
            v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", default=default)
            if v:
                try:
                    function(renpy.python.py_eval(v) + range)
                except:
                    renpy.notify(_("Please type value"))

        def set_camera_keyframe(self, coordinate, value):
            keyframes = all_keyframes.get(coordinate, [])
            if keyframes:
                for i, (v, t, w) in enumerate(keyframes):
                    if time < t:
                        keyframes.insert(i, (value, time, warper))
                        break
                    elif time == t:
                        keyframes[i] = (value, time, warper)
                        break
                else:
                    keyframes.append((value, time, warper))
            else:
                if time == 0:
                    all_keyframes[coordinate] = [(value, time, warper)]
                else:
                    all_keyframes[coordinate] = [(getattr(self, coordinate), 0, None), (value, time, warper)]
            sort_keyframes()

        def set_layer_keyframe(self, layer):
            keyframes = all_keyframes.get(layer, [])
            if keyframes:
                for i, (v, t, w)  in enumerate(keyframes):
                    if time < t:
                        keyframes.insert(i, (renpy.store._3d_layers[layer], time, warper))
                        break
                    elif time == t:
                        keyframes[i] = (renpy.store._3d_layers[layer], time, warper)
                        break
                else:
                    keyframes.append((renpy.store._3d_layers[layer], time, warper))
            else:
                if time == 0:
                    all_keyframes[layer] = [(renpy.store._3d_layers[layer], time, warper)]
                else:
                    all_keyframes[layer] = [(self._3d_layers[layer], 0, None), (renpy.store._3d_layers[layer], time, warper)]
            sort_keyframes()

        def play(self, play):
            camera_check_points = {}
            for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
                if coordinate in all_keyframes:
                    camera_check_points[coordinate[8:]] = all_keyframes[coordinate]

            layer_check_points = {}
            kwargs = {}
            for layer in renpy.store._3d_layers:
                if layer in all_keyframes:
                    layer_check_points[layer] = all_keyframes[layer]
                kwargs[layer+"_loop"] = loops[layer]
                kwargs[layer+"_spline"] = splines[layer]

            focus_check_points = {}
            for i in ["_camera_focus", "_camera_dof"]:
                if i in all_keyframes:
                    focus_check_points[i[8:]] = all_keyframes[i]

            for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
                kwargs[coordinate[8:]+"_loop"] = loops[coordinate]
            for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
                if expressions[coordinate]:
                    kwargs[coordinate[8:]+"_express"] = renpy.python.py_eval(expressions[coordinate])
            if camera_check_points or layer_check_points or focus_check_points:
                renpy.store.all_moves(camera_check_points=camera_check_points, layer_check_points=layer_check_points, focus_check_points=focus_check_points, play=play, camera_spline=splines["camera"], **kwargs)

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
                        camera_viewer.set_camera_keyframe("_camera_x", self.cx)
                    if self.cy != renpy.store._camera_y:
                        camera_viewer.set_camera_keyframe("_camera_y", self.cy)
                    renpy.store.camera_move(self.cx, self.cy, renpy.store._camera_z, renpy.store._camera_rotate)
                    self.x, self.y = x, y
                    renpy.restart_interaction()
                    renpy.redraw(self, 0)

            # Pass the event to our child.
            # return self.child.event(ev, x, y, st)

        def per_interact(self):
            renpy.redraw(self, 0)

        def visit(self):
            return [ self.child ]
    dragged = Dragged("camera.png")

    ##########################################################################
    from collections import defaultdict
    loops = defaultdict(lambda:False)
    expressions = defaultdict(lambda:None)
    splines = defaultdict(lambda:False)
    all_keyframes = {}
    time = 0
    moved_time = 0
    sorted_keyframes = []
    warper = default_warper

    def edit_expression(k):
        value = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", default=expressions[k])
        try:
            result = renpy.python.py_eval(value)(0, 0)
            if isinstance(result, float) or isinstance(result, int):
                expressions[k] = value
            else:
                raise
        except:
            renpy.notify(_("This isn't a valid expression"))
        renpy.restart_interaction()

    def edit_the_value(check_points, old, value_org, int=False):
        value = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", default=value_org)
        try:
            value = renpy.python.py_eval(value)
            if int:
                value = int(value)
            else:
                value = float(value)
            for i, (v, t, w) in enumerate(check_points):
                if t == old:
                    check_points[i] = (value, t, w)
                    break
        except:
            renpy.notify(_("Please type value"))
        renpy.restart_interaction()

    def edit_the_warper(check_points, old, value_org):
        warper = renpy.invoke_in_new_context(renpy.call_screen, "_warper_selecter", current_warper=value_org)
        if warper:
            for i, (v, t, w) in enumerate(check_points):
                if t == old:
                    check_points[i] = (v, t, warper)
                    break
        renpy.restart_interaction()

    def edit_move_keyframes(check_points, old):
        v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", default=old)
        if v:
            try:
                v = renpy.python.py_eval(v)
                if v < 0:
                    return
                move_keyframe(v, old, check_points)
            except:
                renpy.notify(_("Please type value"))

    def edit_move_all_keyframes():
        v = renpy.invoke_in_new_context(renpy.call_screen, "_input_screen", default=moved_time)
        if v:
            try:
                v = renpy.python.py_eval(v)
                if v < 0:
                    return
                move_keyframes(v, moved_time)
            except:
                renpy.notify(_("Please type value"))

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
        if not sorted_keyframes:
            change_time(0)
            return
        else:
            for i, t in enumerate(sorted_keyframes):
                if time < t:
                    change_time(sorted_keyframes[i])
                    return
            change_time(sorted_keyframes[0])

    def prev_time():
        if not sorted_keyframes:
            change_time(0)
            return
        else:
            for i, t in enumerate(sorted_keyframes):
                if time <= t:
                    change_time(sorted_keyframes[i-1])
                    break
            else:
                change_time(sorted_keyframes[-1])

    def select_default_warper():
        global warper
        v = renpy.invoke_in_new_context(renpy.call_screen, "_warper_selecter")
        if v:
            warper = v

    # @renpy.pure
    # class AddWindow(renpy.store.Action, renpy.store.DictEquality):
    #     def __init__(self):
    #         pass
    #     def __call__(self):
    #         if renpy.shown_window():
    #             renpy.scene("window")
    #         else:
    #             renpy.add_layer("window", below="screens")
    #             renpy.config.empty_window()
    #         renpy.restart_interaction()
    #     def get_selected(self):
    #         if renpy.shown_window():
    #             return True
    #         return False

    def clear_keyframes():
        all_keyframes.clear()
        sorted_keyframes[:]=[]

    def remove_keyframe(remove_time, k):
        remove_list = []
        for (v, t, w) in all_keyframes[k]:
            if t == remove_time:
                if remove_time != 0 or (remove_time == 0 and len(all_keyframes[k]) == 1):
                    remove_list.append((v, t, w))
        for c in remove_list:
            all_keyframes[k].remove(c)
            if not all_keyframes[k]:
                del all_keyframes[k]
        sort_keyframes()
        change_time(time)

    def remove_keyframes(time):
        keylist = [k for k in all_keyframes]
        for k in keylist:
            remove_keyframe(time, k)

    def sort_keyframes():
        global sorted_keyframes
        sorted_keyframes[:] = []
        for keyframes in all_keyframes.values():
            for (v, t, w) in keyframes:
                if t not in sorted_keyframes:
                    sorted_keyframes.append(t)
        sorted_keyframes.sort()

    def move_keyframes(new, old):
        global moved_time
        moved_time = round(new, 2)
        for k, v in all_keyframes.items():
            move_keyframe(new, old, v)
        renpy.restart_interaction()

    def move_keyframe(new, old, check_points):
        new = round(new, 2)
        for i, c in enumerate(check_points):
            if c[1] == old:
                (value, time, warper) = check_points.pop(i)
                for n, (v, t, w) in enumerate(check_points):
                    if new < t:
                        check_points.insert(n, (value, new, warper))
                        break
                    elif new == t:
                        # check_points[n] = (new, (value, new, w))
                        check_points.insert(n, (value, new, warper))
                        break
                else:
                    check_points.append((value, new, warper))
                if old == 0 and new != 0:
                    check_points.insert(0, (value, 0, None))
        sort_keyframes()
        renpy.restart_interaction()

    def keyframes_exist(k):
        if k not in all_keyframes:
            return False
        check_points = all_keyframes[k]
        for c in check_points:
            if c[1] == time:
                return True
        return False

    def change_time(v):
        global time
        time = round(v, 2)
        transform_viewer.play(False)
        camera_viewer.play(False)
        renpy.restart_interaction()

    def rollback():
        renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z-100, renpy.store._camera_rotate)
        camera_viewer.set_camera_keyframe("_camera_z", renpy.store._camera_z)
        renpy.restart_interaction()

    def rollforward():
        renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z+100, renpy.store._camera_rotate)
        camera_viewer.set_camera_keyframe("_camera_z", renpy.store._camera_z)
        renpy.restart_interaction()

    def action_editor():
        global time
        if not renpy.config.developer:
            return
        transform_viewer.init()
        camera_viewer.init()
        loops.clear()
        expressions.clear()
        renpy.store._first_load = True
        renpy.invoke_in_new_context(renpy.call_screen, "_action_editor")
        clear_keyframes()
        time = 0
        camera_viewer.layer_reset()
        camera_viewer.camera_reset()

    def last_moves():
        all_keyframes["_camera_x"] = renpy.store._last_camera_arguments[0]["x"]
        all_keyframes["_camera_y"] = renpy.store._last_camera_arguments[0]["y"]
        all_keyframes["_camera_z"] = renpy.store._last_camera_arguments[0]["z"]
        all_keyframes["_camera_rotate"] = renpy.store._last_camera_arguments[0]["rotate"]
        all_keyframes["_camera_z"] = renpy.store._last_camera_arguments[0]["z"]
        for k in renpy.store._last_camera_arguments[1]:
            all_keyframes[k] = renpy.store._last_camera_arguments[1][k]
        all_keyframes["_camera_focus"] = renpy.store._last_camera_arguments[2]["focus"]
        all_keyframes["_camera_dof"] = renpy.store._last_camera_arguments[2]["dof"]
        loops["_camera_x"] = renpy.store._last_camera_arguments[3]
        loops["_camera_y"] = renpy.store._last_camera_arguments[4]
        loops["_camera_z"] = renpy.store._last_camera_arguments[5]
        loops["_camera_rotate"] = renpy.store._last_camera_arguments[6]
        expressions["_camera_x"] = renpy.store._last_camera_arguments[7]
        expressions["_camera_y"] = renpy.store._last_camera_arguments[8]
        expressions["_camera_z"] = renpy.store._last_camera_arguments[9]
        expressions["_camera_rotate"] = renpy.store._last_camera_arguments[10]
        for k in renpy.store._last_camera_arguments[11]:
            if k.find("loop"):
                loops[k[:-5]] = renpy.store._last_camera_arguments[11][k]
            elif k.find("express"):
                expressions[k[:-8]] = renpy.store._last_camera_arguments[11][k]
        splines["camera"] = renpy.store._last_camera_arguments[17]
        all_keyframes["_camera_x"].insert(0, (renpy.store._last_camera_arguments[12], 0, None))
        all_keyframes["_camera_y"].insert(0, (renpy.store._last_camera_arguments[13], 0, None))
        all_keyframes["_camera_z"].insert(0, (renpy.store._last_camera_arguments[14], 0, None))
        all_keyframes["_camera_rotate"].insert(0, (renpy.store._last_camera_arguments[15], 0, None))
        for k in renpy.store._last_camera_arguments[1]:
            all_keyframes[k].insert(0, (renpy.store._last_camera_arguments[16][k], 0, None))
        all_keyframes["_camera_focus"].insert(0, (renpy.store._last_camera_arguments[17], 0, None))
        all_keyframes["_camera_dof"].insert(0, (renpy.store._last_camera_arguments[18], 0, None))
        sort_keyframes()
        change_time(0)

    def put_clipboard():
        camera_check_points = {}
        for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
            if coordinate in all_keyframes:
                camera_check_points[coordinate[8:]] = all_keyframes[coordinate]
                if len(camera_check_points[coordinate[8:]]) == 1 and camera_check_points[coordinate[8:]][0][0] == getattr(renpy.store._viewers.camera_viewer, coordinate):
                    del camera_check_points[coordinate[8:]]

        layer_check_points = {}
        loop = ""
        spline = ""
        expression = ""
        argments = ""
        for layer in renpy.store._3d_layers:
            if layer in all_keyframes:
                layer_check_points[layer] = all_keyframes[layer]
                if len(layer_check_points[layer]) == 1 and layer_check_points[layer][0][0] == camera_viewer._3d_layers[layer]:
                    del layer_check_points[layer]
                if loops[layer]:
                    loop += layer+"_loop=True, "
                if splines[layer]:
                    spline += layer+"_spline=True, "

        focus_check_points = {}
        for i in ["_camera_focus", "_camera_dof"]:
            if i in all_keyframes:
                focus_check_points[i[8:]] = all_keyframes[i]
                if len(focus_check_points[i[8:]]) == 1 and focus_check_points[i[8:]][0][0] == getattr(renpy.store._viewers.camera_viewer, i):
                    del focus_check_points[i[8:]]

        for coordinate in ["_camera_x", "_camera_y", "_camera_z", "_camera_rotate"]:
            if loops[coordinate]:
                loop += coordinate[8:]+"_loop=True, "
            if expressions[coordinate]:
                expression += coordinate[8:]+"_express="+expressions[coordinate]+", "
        if splines["camera"]:
            spline += "camera_spline=True, "
        string = ""

        if camera_check_points:
            argments += "camera_check_points={}, ".format(camera_check_points)
        if layer_check_points:
            argments += "layer_check_points={}, ".format(layer_check_points)
        if focus_check_points:
            argments += "focus_check_points={}, ".format(focus_check_points)
        if expression:
            argments += expression
        if loop:
            argments += loop
        if spline:
            argments += spline

        if argments:
            string += """
    $all_moves({})""".format(argments[:-2])

        for layer in transform_viewer.state_org:
            for name, kwargs_org in {k: v for dic in [transform_viewer.state_org[layer], transform_viewer.state[layer]] for k, v in dic.items()}.items():
                kwargs = {k[2]:v for k, v in all_keyframes.items() if isinstance(k, tuple) and k[0] == name and k[1] == layer}
                if kwargs:
                    string += """
    show {} onlayer {}:
        subpixel True """.format(name, layer)
                    for p, d in transform_viewer.props:
                        if p in kwargs and len(kwargs[p]) == 1:
                            string += "{} {} ".format(p, kwargs[p][0][0])
                        elif d != {k2: v2 for dic in [transform_viewer.state_org[layer], transform_viewer.state[layer]] for k2, v2 in dic.items()}[name][p]:
                            string += "{} {} ".format(p, {k2: v2 for dic in [transform_viewer.state_org[layer], transform_viewer.state[layer]] for k2, v2 in dic.items()}[name][p])
                    for p, check_points in kwargs.items():
                        if len(check_points) > 1:
                            string += """
        parallel:"""
                            string += """
            {} {}""".format(p, check_points[0][0])
                            for i, check_point in enumerate(check_points[1:]):
                                string += """
            {} {} {} {}""".format(check_point[2], check_points[i+1][1]-check_points[i][1], p, check_point[0])
                            if loops[(name,layer,p)]:
                                string += """
            repeat"""

        if string:
            string = string.replace("u'", "'", 999)
            try:
                from pygame import scrap, locals
                scrap.put(locals.SCRAP_TEXT, string)
            except:
                renpy.notify(_("Can't open clipboard"))
            else:
                #syntax hilight error in vim
                renpy.notify("Placed\n{}\n\non clipboard".format(string).replace("{", "{{").replace("[", "[["))
        else:
            renpy.notify(_("Nothing to put"))
