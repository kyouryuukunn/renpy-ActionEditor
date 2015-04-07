# 日本語マニュアルは224行目からです。
#
# This script adds Ren'Py GUI Action editor and 3D camera functions. Please
# copy camera.rpy and camera.png to your game directory.
#####################################################################################################
# Action editor
#
# This allows you to adjusts coordinates of the camera or 3D layers or values
# of transform properties of images by GUI. This generates a script based on
# the result of the adjustment and puts it on clipboard.
#
# When :var:`config.developer` is True, pressing action_editor (by default,
# "shift+P"), will open Action editor.
# 
# Action editor has below features.:
# 
#  * Each transform property of images, coordinates of the camera or layers can be changed by bars.
#  * The x, y coordinates of the camera can be changed by dragging the camera icon.
#  * The z coordinate of the camera can be changed by mouse wheel.
#  * Each value can be inputted by keyboard.
#  * Anchor points can be added to the time bar.
#  * Each transform property of images, coordinates of the camera and layers or actions can be putted on clipboard.(v6.99 or later, only winows?)
#
#####################################################################################################
# Camera
# ================
#
# With some limitations, Ren'Py can simulate 3D camera motion. This will easily
# let you achieve a parallax effect by placing sprites and assets on a 3D field.
# This script applies transforms to each layers which are registered as 3D layer by
# positions of a camera and 3D layers on a 3D field to simulate 3D camera motion.
#
# If you use this feature, in the first, set additional layers to be registered
# as 3D layer. If anything isn't registered as 3D layers, this script register
# "master" layer as 3D layers.
#
# For example, Write a code like below in options.rpy and add 'background', 'middle', 'forward'  layers.::
#
#         config.layers = ['master', 'background', 'middle', 'forward', 'transient', 'screens', 'overlay']
#
# Second, register layers which participate to a 3D motion as 3d layers by
# :func:`register_3d_layer`. Z coordinates of these layers can be moved and
# applied transforms to by positions of the camera and 3D layers. If anything
# isn't registered as 3D layers, this script registers 'master' layer as 3D
# layer.::
#
#         init python:
#             register_3d_layer('background', 'middle', 'forward')
#
# Then, a camera and layers can move. ::
#
#          label start:
#              # reset the camera and layers positions and allow layers position to be saved.
#              $ camera_reset()
#              # It takes 0 second to move layers
#              $ layer_move("background", 2000)
#              $ layer_move("middle", 1500)
#              $ layer_move("forward", 1000)
#              scene bg onlayer background
#              show A onlayer middle
#              show B onlayer forward
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
#              $ camera_moves( ( (0, 0, 0, 0, 1, 'linear'), (-1800, 0, 500, 0, 1.5, 'linear') ) )
#              'a camera shuttles between (-1800, 0, 500) and (0, 0, 0)'
#              $ camera_moves( ( (0, 0, 0, 0, .5, 'linear'), (-1800, 0, 500, 0, 1, 'linear') ), loop=True)
#
# Notice that 3D camera motion has some limits.:
#
# * 3D camera motion applies transforms to 3D layers, so the show layer statement or
#   :func:`renpy.show_layer_at` to 3D layers can't be usable.
#
# * z coordinates of 3D layers don't affect the stacking order of 3d layers.
#
# * By default, the scene, hide statements use master or the given layer
#   only. If you use 3D layers preferentially, write code like below.::
# * camera_move, camera_moves, layer_move, layer_moves, all_moves はそれぞれ排
#   他的です。ひとつのインタラクション中に複数回呼び出されると、最後に呼び出され
#   たもののみが正常に動作し、それ以外は瞬間移動になります。
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
#         Register layers as 3D layers. 3D layers are applied transforms to by
#         positions of a camera and 3D layers. This should be called in init
#         block. If anything isn't registered as 3D layers, this script
#         register "master" layer as 3D layers
#
#         `layers`
#              This should be the string or strings of a layer name.
#         """
#
#    def camera_reset():
#        """
#         :doc: camera
#
#         Reset a camera and 3D layers positions. Please call this at least once
#         when the game has started. If this doesn't called, The position of 3D
#         layers don't be saved.
#         """
#
#    def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False):
#        """
#         :doc: camera
#
#         Move the coordinate and rotate the camera.
#
#         `x`
#              The x coordinate of the camera
#         `y`
#              The y coordinate of the camera
#         `z`
#              The z coordinate of the camera
#         `rotate`
#              Defaul 0, the angle of the camera
#         `duration`
#              Default 0, this is the second times taken to move the camera.
#         `loop`
#              Default False, if True, this motion repeats.
#         `warper`
#              Default 'linear', this should be the string of the name of a
#              warper registered with ATL.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#         """
#
#    def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False):
#        """
#         :doc: camera
#
#         Move the z coordinate of a layer.
#
#         `layer`
#              The string of a layer name to be moved
#         `z`
#              The z coordinate of a layer
#         `duration`
#              Default 0, this is the second times taken to move a layer.
#         `loop`
#              Default False, if True, this motion repeats.
#         `warper`
#              Default 'linear', this should be the string of the name of a
#              warper registered with ATL.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#         """
#
#    def camera_moves(check_points, loop=False, subpixel=True):
#        """
#         :doc: camera
#
#         Move a camera through check points.
#
#         `check_points`
#              A tuple of tuples of x, y, z, rotate, duration, warper.
#         `loop`
#              Default False, if True, this sequence of motions repeats.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#         """
#
#    def layer_moves(layer, check_points, loop=False, subpixel=True):
#        """
#         :doc: camera
#
#         Move the z coordinate of a layer through check points.
#
#         `layer`
#              the string of a layer name to be moved
#         `check_points`
#              A tuple of tuples of z, duration, warper
#         `loop`
#              Default False, if True, this sequence of motions repeats.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#         """
#
#    def all_moves(camera_check_points=None, layer_check_points={}, loop=False, subpixel=True, **kwargs):
#        """
#         :doc: camera
#
#         Move the camera and layers through check points.
#
#         `camera_check_points`
#              A tuple of tuples of x, y, z, rotate, duration, warper.
#         `layer_check_points`
#              This is the map. Its key is the string of a layer name to be moved, value is A tuple of tuples of z, duration, warper
#         `loop`
#              Default False, if True, this sequence of motions repeats.
#         `subpixel`
#              Default True, if True, causes things to be drawn on the screen
#              using subpixel positioning
#
#          If keyword arguments 'layer name'_loop is given, the layer motion is repeats.
#         """
# """
#####################################################################################################
# このスクリプトはRen'PyにGUIの演出エディターとカメラ機能を追加します。
# camera.rpyとcamera.pngをgameフォルダにコピーしてください。
#####################################################################################################
# 演出エディター
#
# GUIを利用して画像の変換プロパティーやカメラ、レイヤーの座標調整、時間軸にそっ
# た演出作成を可能にします。設定した値からスクリプトを自動生成し、クリップボー
# ドに送ります。
#
# config.developer が True なら、Shift+Pで演出エディターが起動します。
# 
# 演出エディターでは以下の機能が利用可能です。:
# 
# * 各画像の変換プロパティーやカメラ、レイヤーの座標をバーから変更出来ます。
# * カメラアイコンのドラッグでカメラを移動出来ます。
# * マウスのホイールからカメラのz座標を変更出来ます。
# * 各パラメーターをキーボードから入力出来ます。
# * アンカーポイントを設定して時間軸にそった演出が作れます。
# * 画像の変換プロパティーやカメラ、レイヤーの座標、時間軸にそった演出をそれぞ
#   れクリップボードに送れます。(v6.99以上, Windows限定? Macで動作するかは判りま
#   せん。)
#####################################################################################################
# カメラ
#
# 三次元を再現する関数をRen'Py に追加します。これらは3Dレイヤーに登録された
# 各レイヤーにz座標を与え、カメラとの位置関係により拡大縮小移動させて三次元をシ
# ミュレートします。これにより奥行きの表現が簡単に可能になるでしょう。この機能
# を利用するには、先ず3Dレイヤーに登録するレイヤーを追加しなければなりません。
# 3Dレイヤーに何も登録されていない場合、"master"レイヤーのみを3Dレイヤーに登録
# します。
#
# 例
#
# options.rpy に以下のような設定を加え、'background', 'middle', 'forward' レイヤーを追加します。
#
#        config.layers = [ 'master', 'background', 'middle', 'forward', 'transient', 'screens', 'overlay']
#
# 次に register_3d_layer 関数で3Dレイヤーを登録します。これらのレイヤーはz座標
# を移動出来、カメラの影響を受けます。register_3d_layerが使用されないと、デフォ
# ルトで"master"レイヤーが登録されます。
#
#    init python:
#        register_3d_layer( 'background', 'middle', 'forward',)
#
# 以上の設定で、ゲーム中でカメラ動かせるようになります。
#
#    label start:
#        # カメラ、レイヤー位置をリセットし、レイヤー位置がセーブされるようにします。
#        $ camera_reset()
#        # 0秒でレイヤーz座標を変更します。
#        $ layer_move("background", 2000)
#        $ layer_move("middle", 1500)
#        $ layer_move("forward", 1000)
#        scene bg onlayer background
#        show A onlayer middle
#        show B onlayer forward
#        with dissolve
#        '1秒でカメラを(0, 130, 0)まで移動させます。'
#        $ camera_move(0, 130, 0, 0, 1)
#        '5秒でカメラを(-70, 130, 1000)まで移動させます。'
#        $ camera_move(-70, 130, 1000, 0, 5)
#        '0秒かけてカメラを(0, 0, 0)まで移動させます。'
#        $ camera_move(0, 0, 0)
#        '1秒かけてカメラを時計回りに180度回転します。'
#        $ camera_move(0, 0, 0, 180, 1)
#        '1秒かけてカメラを反時計回りに180度回転させ、4秒かけてカメラを(100, 100, 100)まで移動させます。'
#        $ camera_moves( ( (0, 0, 0, 0, 1, 'linear'), (100, 100, 100, 0, 5, 'linear') ) )
#        'カメラが(100, 100, 100)から(0, 0, 0)までを繰り返し往復します'
#        $ camera_moves( ( (0, 0, 0, 0, 1, 'linear'), (100, 100, 100, 0, 2, 'linear') ), loop=True)
#
# カメラ機能にはいくつかの制限があることに注意してください。
#
# * カメラモーションは3Dレイヤーに対して変換を適用して再現しているため、3レイ
#   ヤーに対して show layer ステートメントや renpy.show_layer_at 関数は使用出来ま
#   せん。
# * レイヤーの重なり順はレイヤーのz座標を反映しません。
# * camera_move, camera_moves, layer_move, layer_moves, all_moves はそれぞれ排
#   他的です。ひとつのインタラクション中に複数回呼び出されると、最後に呼び出され
#   たもののみが正常に動作し、それ以外は瞬間移動になります。
#
# デフォルトではRen'Pyの scene, show, hide ステートメントは master レイヤー又は
# 指定されたレイヤーにのみ作用します。3Dレイヤーに対して優先的に作用させたい場
# 合は以下のようにしてRen'Pyの設定を変更してください。
#        init -1 python hide:
#
#            def hide(name, layer='master'):
#                for l in _3d_layers:
#                    if renpy.showing(name, l):
#                        renpy.hide(name, l)
#                else:
#                    renpy.hide(name, layer)
#
#            config.hide = hide
#
#            def scene(layer='master'):
#
#                renpy.scene(layer)
#                for l in _3d_layers:
#                    renpy.scene(l)
#
#            config.scene = scene
# """
#
#     def register_3d_layer(*layers):
#         """
#          :doc: camera
#
#          レイヤーを3Dレイヤーとして登録します。3Dレイヤーに登録されたレイヤー
#          には、そのz座標とカメラの位置に基づいた変換が適用されます。initブ
#          ロックで一度だけ呼び出してください。3Dレイヤーになにも登録されていな
#          い場合、"master"レイヤーを3Dレイヤーに登録します。
#
#          `layers`
#               3Dレイヤーに登録する、一つ以上のレイヤー名の文字列です。
#          """
#
#     def camera_reset():
#         """
#          :doc: camera
#
#          カメラとレイヤーを初期位置に戻します。ゲーム開始後に少くとも一度は呼
#          び出してください。呼び出されない場合、3Dレイヤーの座標が保存されませ
#          ん。
#          """
#
#     def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False):
#         """
#          :doc: camera
#
#          カメラの座標と角度を指定の時間かけて変更します。
#
#          `x`
#               カメラのx座標の数字です。
#          `y`
#               カメラのy座標の数字です。
#          `z`
#               カメラのy座標の数字です。
#          `rotate`
#               デフォルトは0で、カメラの傾きの数字です。
#          `duration`
#               デフォルトは0で、カメラ移動にかかる時間の秒数です。
#          `loop`
#               デフォルトは Falseで、True ならこのモーションが繰り替えされます。
#          `warper`
#               デフォルトは'linear'で, 時間補間に使用する関数名の文字列です。こ
#               れにはATLに登録された時間補間関数が指定出来ます。
#          `subpixel`
#               デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
#               に描画します。
#          """
#
#     def camera_moves(check_points, loop=False, subpixel=True):
#         """
#          :doc: camera
#
#          1つ以上のチェックポイントを通ってカメラを動かします。
#
#          `check_points`
#               カメラのx,y,z座標、傾き、カメラの移動開始からその位置に到達する
#               までの秒数、その間の時間補間関数名の文字列からなるタプルのタプ
#               ルです。カメラはここで指定された各タプルを順番に移動するので、
#               タプルは時系列に沿って並べてください。
#          `loop`
#               デフォルトは Falseで、True ならこのモーションが繰り替えされます。
#          `subpixel`
#               デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
#               に描画します。
#          """
#
#     def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False):
#         """
#          :doc: camera
#
#          レイヤーのz座標を指定の時間かけて変更します。
#
#          `layer`
#               移動するレイヤー名の文字列です。
#          `z`
#               レイヤーの移動先z座標の数字です。
#          `duration`
#               デフォルトは0で、レイヤー移動にかかる時間の秒数です。
#          `loop`
#               デフォルトは Falseで、True ならこのモーションが繰り替えされます。
#          `warper`
#               デフォルトは'linear'で, 時間補間に使用する関数名の文字列です。こ
#               れにはATLに登録された時間補間関数が指定出来ます。
#          `subpixel`
#               デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
#               に描画します。
#
#     def layer_moves(layer, check_points, loop=False, subpixel=True):
#         """
#          :doc: camera
#
#          1つ以上のチェックポイントを通って3Dレイヤーを動かします。
#
#          `layer`
#               移動するレイヤー名の文字列です。
#          `check_points`
#               レイヤーのz座標の数字、レイヤーの移動開始からその位置に到達するまでの
#               秒数の数字、その間の時間補間関数の文字列からなるタプルのタプルです。
#               レイヤーはここで指定された各タプルを順番に移動するので、タプル
#               は時系列に沿って並べてください。
#          `loop`
#               デフォルトは Falseで、True ならこのモーションが繰り替えされます。
#          `subpixel`
#               デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
#               に描画します。
#
#    def all_moves(camera_check_points=None, layer_check_points={}, loop=False, subpixel=True, **kwargs):
#        """
#         :doc: camera
#
#          1つ以上のチェックポイントを通ってカメラと3Dレイヤーを同時に動かします。
#
#         `camera_check_points`
#               カメラのx,y,z座標、傾き、カメラの移動開始からその位置に到達する
#               までの秒数、その間の時間補間関数名の文字列からなるタプルのタプ
#               ルです。カメラはここで指定された各タプルを順番に移動するので、
#               タプルは時系列に沿って並べてください。
#         `layer_check_points`
#               移動するレイヤー名の文字列をキーとし、レイヤーのz座標の数字、レ
#               イヤーの移動開始からその位置に到達するまでの秒数の数字、その間
#               の時間補間関数の文字列からなるタプルのタプルを値に持つ辞書で
#               す。レイヤーはここで指定された各タプルを順番に移動するので、タ
#               プルは時系列に沿って並べてください。
#          `loop`
#               デフォルトは Falseで、True ならカメラのモーションが繰り替えされます。
#          `subpixel`
#               デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
#               に描画します。
#
#          キーワード引数として <レイヤー名>_loop をとります。デフォルトは Falseで、True ならそのレイヤーのモーションが繰り替えされます。
#         """

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
        layer_check_points = {layer:((_layer_z, 0, None), ) for layer in _3d_layers}
        all_moves(camera_check_points=((0, 0, 0, 0, 0, None), ), layer_check_points=layer_check_points)

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

        camera_moves(((x, y, z, rotate, duration, warper), ), subpixel=subpixel, loop=loop)

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

        layer_moves(layer, ((z, duration, warper), ), subpixel=subpixel, **{layer+"_loop":loop})

    def camera_moves(check_points, loop=False, subpixel=True):
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
         """
        all_moves(camera_check_points=check_points, loop=loop, subpixel=subpixel)

    def layer_moves(layer, check_points, loop=False, subpixel=True, **kwargs):
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
         """
        all_moves(layer_check_points={layer:check_points}, subpixel=subpixel, **{layer+"_loop":loop})

    def all_moves(camera_check_points=None, layer_check_points=None, loop=False, subpixel=True, play=True, **kwargs):
        """
         :doc: camera

         Move a layer and camera through check points and apply transform to the layer.

         `camera_check_points`
              A tuple of (x, y, z, rotate, duration, warper)
         `layer_check_points`
              {layer:((z, duration, warper)...), ...}
         `loop`
              Default False, if True, this sequence of motions repeats.
         `subpixel`
              Default True, if True, causes things to be drawn on the screen
              using subpixel positioning
         """
        global _camera_x, _camera_y, _camera_z, _camera_rotate, _3d_layers
        if camera_check_points is None:
            camera_check_points = ((_camera_x, _camera_y, _camera_z, _camera_rotate, 0, None), )

        if layer_check_points is None:
            layer_check_points = {}
        for layer in _3d_layers:
            if layer not in layer_check_points:
                layer_check_points[layer] = ((_3d_layers[layer], 0, None), )

            start_xanchor = _focal_length*_camera_x/(renpy.config.screen_width *_layer_z) + .5
            start_yanchor = _focal_length*_camera_y/(renpy.config.screen_height*_layer_z) + .5

            camera_check_points2 = [(_camera_z, _camera_rotate, start_xanchor, start_yanchor, 0, None), ]
            for c in camera_check_points:
                xanchor = _focal_length*c[0]/(renpy.config.screen_width *_layer_z) + .5
                yanchor = _focal_length*c[1]/(renpy.config.screen_height*_layer_z) + .5
                duration = float(c[4])
                camera_check_points2.append((c[2], c[3], xanchor, yanchor, duration, c[5]))

            layer_check_points2 = [(_3d_layers[layer], 0, None), ]
            for c in layer_check_points[layer]:
                layer_check_points2.append((c[0], float(c[1]), c[2]))
            
            layer_loop = kwargs.get(layer+"_loop", False)

            if play:
                renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(function=renpy.curry(_camera_trans)(camera_check_points=camera_check_points2, layer_check_points=layer_check_points2, loop=loop, subpixel=subpixel, layer=layer, layer_loop=layer_loop))])
                layer_z = layer_check_points2[-1][0]
            else:
                st = _viewers.time
                if loop:
                    st %= camera_check_points2[-1][4]
                # This is used when the time bar is changed by Action Editor
                for i in xrange(1, len(camera_check_points2)):
                    checkpoint = camera_check_points2[i][4]
                    pre_checkpoint = camera_check_points2[i-1][4]
                    if st <= checkpoint:
                        start = camera_check_points2[i-1]
                        goal = camera_check_points2[i]
                        if checkpoint != pre_checkpoint:
                            g = renpy.atl.warpers[goal[5]]((st - pre_checkpoint) / float(checkpoint - pre_checkpoint))
                        else:
                            g = 1.

                        z = g*(goal[0]-start[0])+start[0]
                        layer_z = get_layer_z(layer_check_points2, st, layer_loop)
                        distance = float(layer_z - z)
                        if distance == 0:
                            distance = .1

                        xanchor = g*(goal[2]-start[2]) + start[2]
                        yanchor = g*(goal[3]-start[3]) + start[3]
                        rotate = g*(goal[1]  -  start[1]) + start[1]

                        if distance >= 0:
                            alpha = 1
                            zoom = _layer_z / distance
                            renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(xpos=.5, ypos=.5, alpha=alpha, transform_anchor=True, xanchor=xanchor, yanchor=yanchor, zoom=zoom, rotate=rotate)])
                        else:
                            alpha = 0
                            renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(xpos=.5, ypos=.5, alpha=alpha, transform_anchor=True, xanchor=xanchor, yanchor=yanchor, rotate=rotate)])
                        break
                else:
                    goal = camera_check_points2[-1]
                    z = goal[0]
                    layer_z = get_layer_z(layer_check_points2, st, layer_loop)
                    distance = float(layer_z - z)
                    if distance == 0:
                        distance = .1
                    xanchor = goal[2]
                    yanchor = goal[3]
                    zoom = _layer_z / distance
                    rotate = goal[1]
                    if distance >= 0:
                        alpha = 1
                    else:
                        alpha = 0
                    renpy.game.context().scene_lists.set_layer_at_list(layer, [Transform(xpos=.5, ypos=.5, alpha=alpha, transform_anchor=True, xanchor=xanchor, yanchor=yanchor, zoom=zoom, rotate=rotate)])

            _3d_layers[layer] = int(layer_z)
        if play:
            _camera_x = camera_check_points[-1][0]
            _camera_y = camera_check_points[-1][1]
            _camera_z = camera_check_points[-1][2]
            _camera_rotate = camera_check_points[-1][3]
            _3d_layers = _3d_layers
        else:
            _camera_x         = int(((xanchor-.5)*renpy.config.screen_width*_layer_z)/_focal_length)
            _camera_y         = int(((yanchor-.5)*renpy.config.screen_height*_layer_z)/_focal_length)
            _camera_z         = int(z)
            _camera_rotate    = int(rotate)
            _3d_layers = _3d_layers



    def _camera_trans(tran, st, at, camera_check_points, layer_check_points, loop, layer_loop, subpixel, layer):
        # camera_check_points = (z, r, xanchor, yanchor, duration, warper)
        # layer_check_points = (layer_z, duration, warper)
        tran.xpos    = .5 
        tran.ypos    = .5
        tran.subpixel = subpixel
        tran.transform_anchor = True
        camera_st = st
        if loop and camera_check_points[-1][4]:
            camera_st %= camera_check_points[-1][4]

        for i in xrange(1, len(camera_check_points)):
            checkpoint = camera_check_points[i][4]
            pre_checkpoint = camera_check_points[i-1][4]
            if camera_st <= checkpoint:
                start = camera_check_points[i-1]
                goal = camera_check_points[i]
                if checkpoint != pre_checkpoint:
                    g = renpy.atl.warpers[goal[5]]((camera_st - pre_checkpoint) / float(checkpoint - pre_checkpoint))
                else:
                    g = 1.

                z = g*(goal[0]-start[0])+start[0]
                layer_z = get_layer_z(layer_check_points, st, layer_loop)
                distance = float(layer_z - z)
                if distance == 0:
                    distance = .1

                tran.xanchor = g*(goal[2]-start[2]) + start[2]
                tran.yanchor = g*(goal[3]-start[3]) + start[3]
                tran.rotate  = g*(goal[1]  -  start[1]) + start[1]

                if distance >= 0:
                    tran.alpha = 1
                    tran.zoom = _layer_z / distance
                else:
                    tran.alpha = 0

                # get_camera_coordinate(tran, z, layer, layer_z)
                break
        else:
            goal = camera_check_points[-1]
            layer_z = get_layer_z(layer_check_points, st, layer_loop)
            distance = float(layer_z - goal[0])
            if distance == 0:
                distance = .1
            tran.xanchor = goal[2]
            tran.yanchor = goal[3]
            tran.zoom = _layer_z / distance
            tran.rotate = goal[1]
            if distance >= 0:
                tran.alpha = 1
            else:
                tran.alpha = 0
            # get_camera_coordinate(tran, goal[0], layer, layer_z)
        return .005

    def get_layer_z(check_points, time, loop):
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
        if time:
            at _delay_show(time + 1)
        style_group "action_editor"
        xfill True
        vbox:

            hbox:
                xfill False
                textbutton _("Images") action [SelectedIf(tab == "images"), Show("_action_editor", tab="images")]
                textbutton _("2D Camera") action [SensitiveIf(_3d_layers.keys() == ["master"]), SelectedIf(tab == "2D Camera"), Show("_action_editor", tab="2D Camera")]
                textbutton _("3D Layers") action [SelectedIf(tab == "3D Layers"), Show("_action_editor", tab="3D Layers")]
                textbutton _("3D Camera") action [SelectedIf(tab == "3D Camera"), Show("_action_editor", tab="3D Camera")]
                textbutton _("ROT") action [SelectedIf(renpy.get_screen("_rot")), If(renpy.get_screen("_rot"), true=Hide("_rot"), false=Show("_rot"))]
            null height 10
            if tab == "images":
                hbox:
                    xfill False
                    style_group "action_editor_layers"
                    label _("layers")
                    for l in config.layers:
                        if l not in ["screens", "transient", "overlay"]:
                            textbutton "[l]" action [SelectedIf(l == layer), Show("_action_editor", tab=tab, layer=l)]
                hbox:
                    xfill False
                    style_group "action_editor_images"
                    label _("images")
                    for t in state:
                        textbutton "[t]" action [SelectedIf(t == tag), Show("_action_editor", tab=tab, layer=layer, tag=t)]

                if tag in state:
                    for p, d in _viewers.transform_viewer.props:
                        $prop = _viewers.transform_viewer.get_property(layer, tag, p)
                        $ f = _viewers.transform_viewer.generate_changed(layer, tag, p)
                        if p not in _viewers.transform_viewer.force_float and ((state[tag][p] is None and isinstance(d, int)) or isinstance(state[tag][p], int)):
                            hbox:
                                textbutton "[p]" action Function(_viewers.transform_viewer.put_prop_clipboard, p, prop)
                                textbutton "[prop]" action Function(_viewers.transform_viewer.edit_value, f, True, default=prop)
                                bar adjustment ui.adjustment(range=_viewers.transform_viewer.int_range*2, value=prop+_viewers.transform_viewer.int_range, page=1, changed=f) xalign 1.
                        else:
                            hbox:
                                textbutton "[p]" action Function(_viewers.transform_viewer.put_prop_clipboard, p, prop)
                                textbutton "[prop]" action Function(_viewers.transform_viewer.edit_value, f, False, default=prop)
                                bar adjustment ui.adjustment(range=_viewers.transform_viewer.float_range*2, value=prop+_viewers.transform_viewer.float_range, page=.05, changed=f) xalign 1.
            elif tab == "3D Camera" or tab == "2D Camera":
                if _3d_layers.keys() == ["master"] and tab == "3D Camera":
                    label _("Please regist 3D layers")
                else:
                    hbox:
                        label "x"
                        textbutton "[_camera_x: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.x_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_x)
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_x+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.x_changed) xalign 1.
                    hbox:
                        label "y"
                        textbutton "[_camera_y: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.y_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_y)
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_y+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.y_changed) xalign 1.
                    hbox:
                        label "z"
                        textbutton "[_camera_z: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.z_changed, _viewers.camera_viewer.range_camera_pos, default=_camera_z)
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_camera_pos*2, value=_camera_z+_viewers.camera_viewer.range_camera_pos, page=1, changed=_viewers.camera_viewer.z_changed) xalign 1.
                    hbox:
                        label "rotate"
                        textbutton "[_camera_rotate: >5]" action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.r_changed, _viewers.camera_viewer.range_rotate, default=_camera_rotate)
                        bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_rotate*2, value=_camera_rotate+_viewers.camera_viewer.range_rotate, page=1, changed=_viewers.camera_viewer.r_changed) xalign 1.
            elif tab == "3D Layers":
                if _3d_layers.keys() == ["master"]:
                    label _("Please regist 3D layers")
                else:
                    for layer in sorted(_3d_layers.keys()):
                        hbox:
                            label "[layer]"
                            textbutton "{}".format(_3d_layers[layer]) action Function(_viewers.camera_viewer.edit_value, _viewers.camera_viewer.generate_layer_z_changed(layer), 0, default=_3d_layers[layer])
                            textbutton _("loop") action ToggleDict(_viewers.loops, layer+"_loop")
                            bar adjustment ui.adjustment(range=_viewers.camera_viewer.range_layer_z, value=_3d_layers[layer], page=1, changed=_viewers.camera_viewer.generate_layer_z_changed(layer)) xalign 1.
            hbox:
                xfill False
                xalign 1.
                if tab == "images":
                    if tag:
                        textbutton _("loop") action ToggleDict(_viewers.loops, layer+"_"+tag+"_loop")
                        textbutton _("clipboard") action Function(_viewers.transform_viewer.put_show_clipboard, tag, layer)
                    # textbutton _("add") action Function(_viewers.transform_viewer.add_image, layer)
                    # textbutton _("remove") action [SensitiveIf(tag), Function(_viewers.transform_viewer.state_org[layer].pop, tag), Function(renpy.hide, tag, layer), Show("_action_editor", tab=tab, layer=layer)]
                    textbutton _("reset") action [_viewers.transform_viewer.reset, renpy.restart_interaction]
                elif tab == "2D Camera":
                    textbutton _("loop") action ToggleDict(_viewers.loops, "camera_loop")
                    textbutton _("clipboard") action Function(_viewers.camera_viewer.put_clipboard, True)
                    textbutton _("reset") action [_viewers.camera_viewer.camera_reset, renpy.restart_interaction]
                elif tab == "3D Layers":
                    textbutton _("clipboard") action Function(_viewers.camera_viewer.put_clipboard, False)
                    textbutton _("reset") action [_viewers.camera_viewer.layer_reset, renpy.restart_interaction]
                elif tab == "3D Camera":
                    textbutton _("loop") action ToggleDict(_viewers.loops, "camera_loop")
                    textbutton _("clipboard") action Function(_viewers.camera_viewer.put_clipboard, True)
                    textbutton _("reset") action [_viewers.camera_viewer.camera_reset, renpy.restart_interaction]

    frame:
        if time:
            at _delay_show(time + 1)
        xfill True
        yalign 1.0
        vbox:

            hbox:
                textbutton _("time: [_viewers.time:>.2f] s") action Function(_viewers.edit_time)
                textbutton _("warper") action _viewers.select_time_warper
                textbutton _("<") action Function(_viewers.prev_time)
                textbutton _(">") action Function(_viewers.next_time)
                bar adjustment ui.adjustment(range=7.0, value=_viewers.time, changed=_viewers.change_time) xalign 1.
            hbox:
                xfill True
                hbox:
                    textbutton _("clear anchor") action [Function(_viewers.clear_anchor_points), renpy.restart_interaction]
                    if _viewers.sorted_anchor_points:
                        # if _viewers.time in _viewers.sorted_anchor_points:
                        #     textbutton _("remove anchor") action [Function(_viewers.remove_anchor_point, _viewers.time), renpy.restart_interaction]
                        # else:
                        #     textbutton _("add    anchor") action [_viewers.set_anchor_point, renpy.restart_interaction]
                        textbutton _("remove anchor") action [SensitiveIf(_viewers.time in _viewers.sorted_anchor_points), Function(_viewers.remove_anchor_point, _viewers.time), renpy.restart_interaction]
                        textbutton _("play") action [SensitiveIf(_viewers.sorted_anchor_points), Function(_viewers.camera_viewer.play, play=True), Function(_viewers.transform_viewer.play, play=True), Hide("_action_editor"), Show("_action_editor", tab=tab, layer=layer, tag=tag, time=_viewers.sorted_anchor_points[-1]), renpy.restart_interaction]
                    else:
                        # textbutton _("add    anchor") action [_viewers.set_anchor_point, renpy.restart_interaction]
                        textbutton _("remove anchor") action [SensitiveIf(_viewers.time in _viewers.sorted_anchor_points), Function(_viewers.remove_anchor_point, _viewers.time), renpy.restart_interaction]
                        textbutton _("play") action [SensitiveIf(_viewers.sorted_anchor_points), Function(_viewers.camera_viewer.play, play=True), Function(_viewers.transform_viewer.play, play=True), Hide("_action_editor"), Show("_action_editor", tab=tab, layer=layer, tag=tag), renpy.restart_interaction]
                    textbutton _("clipboard") action Function(_viewers.put_clipboard)
                hbox:
                    xalign 1.
                    textbutton _("close") action Return()

    if time:
        add _viewers.dragged at _delay_show(time + 1)
    else:
        add _viewers.dragged

init -1600:
    style action_editor_frame background "#0006"
    style action_editor_button size_group "action_editor"
    style action_editor_images_button size_group "action_editor_images"
    style action_editor_layers_button size_group "action_editor_layers"
    style action_editor_times_button size_group "action_editor_times"
    style action_editor_times_frame background "#0006"
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
        yalign .98
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

        def set_anchor_point(self, layer, tag, kwargs):

            anchor_points = all_anchor_points.get((tag, layer), [])
            if anchor_points:
                for i, (t, c, w) in enumerate(anchor_points):
                    if time < t:
                        anchor_points.insert(i, (time, kwargs, warper))
                        break
                    elif time == t:
                        anchor_points[i] = (time, kwargs, warper)
                        break
                else:
                    anchor_points.append((time, kwargs, warper))
            else:
                if time == 0:
                    all_anchor_points[(tag, layer)] = [(time, kwargs, warper)]
                else:
                    kwargs_org = {k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}[tag]
                    all_anchor_points[(tag, layer)] = [(0, kwargs_org, warper), (time, kwargs, warper)]
            sort_anchor_points()

        def play(self, play):
            for layer in renpy.config.layers:
                for tag in {k: v for dic in [self.state_org[layer], self.state[layer]] for k, v in dic.items()}:
                    if (tag, layer) in all_anchor_points:
                        check_points=all_anchor_points[(tag, layer)]
                        if play:
                            renpy.show(tag, [renpy.store.Transform(function=renpy.curry(self.transform)(check_points=check_points, loop=loops[layer+"_"+tag+"_loop"]))], layer=layer)
                        else:
                            kwargs = {}
                            # check_points = [(time, kwargs, warper)..]
                            kwargs.subpixel = True
                            st = time
                            if loops[layer+"_"+tag+"_loop"]:
                                st %= check_points[-1][0]

                            if st < check_points[-1][0]:
                                for i in xrange(1, len(check_points)):
                                    checkpoint = check_points[i][0]
                                    pre_checkpoint = check_points[i-1][0]
                                    if st <= checkpoint:
                                        start = check_points[i-1][1]
                                        goal = check_points[i][1]
                                        if checkpoint != pre_checkpoint:
                                            g = renpy.atl.warpers[check_points[i][2]]((st - pre_checkpoint) / float(checkpoint - pre_checkpoint))
                                        else:
                                            g = 1.
                                        for p, d in self.props:
                                            if goal[p] is not None:
                                                if isinstance(goal[p], int) and p not in self.force_float:
                                                    if start[p] is None:
                                                        v = g*(goal[p]-d)+d
                                                    else:
                                                        v = g*(goal[p]-start[p])+start[p]
                                                    v = int(v)
                                                else:
                                                    if start[p] is None:
                                                        v = g*(goal[p]-d)+d
                                                    else:
                                                        v = g*(goal[p]-start[p])+start[p]
                                                    v = round(v, 2)
                                                kwargs[p] = v
                                        renpy.show(tag, [renpy.store.Transform(**kwargs)], layer=layer)
                                        break
                            else:

                                for k, v in check_points[-1][1].iteritems():
                                    if isinstance(v, float):
                                        v = round(v, 2)
                                    kwargs[k] = v
                                renpy.show(tag, [renpy.store.Transform(**kwargs)], layer=layer)

        def transform(self, tran, st, at, check_points, subpixel=True, loop=False):
            # check_points = [(time, kwargs, warper)..]
            tran.subpixel = subpixel
            if loop:
                st %= check_points[-1][0]

            if st < check_points[-1][0]:
                for i in xrange(1, len(check_points)):
                    checkpoint = check_points[i][0]
                    pre_checkpoint = check_points[i-1][0]
                    if st <= checkpoint:
                        start = check_points[i-1][1]
                        goal = check_points[i][1]
                        if checkpoint != pre_checkpoint:
                            g = renpy.atl.warpers[check_points[i][2]]((st - pre_checkpoint) / float(checkpoint - pre_checkpoint))
                        else:
                            g = 1.
                        for p, d in self.props:
                            if goal[p] is not None:
                                if isinstance(goal[p], int) and p not in self.force_float:
                                    if start[p] is None:
                                        v = g*(goal[p]-d)+d
                                    else:
                                        v = g*(goal[p]-start[p])+start[p]
                                    v = int(v)
                                else:
                                    if start[p] is None:
                                        v = g*(goal[p]-d)+d
                                    else:
                                        v = g*(goal[p]-start[p])+start[p]
                                setattr(tran, p, v)

                        return .005
            for k, v in check_points[-1][1].iteritems():
                setattr(tran, k, v)
            return None

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

                self.set_anchor_point(layer, tag, kwargs)
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
            self.set_camera_anchor_point()
            renpy.restart_interaction()

        def y_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, v - self.range_camera_pos, renpy.store._camera_z, renpy.store._camera_rotate)
            self.set_camera_anchor_point()
            renpy.restart_interaction()

        def z_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, v - self.range_camera_pos, renpy.store._camera_rotate)
            self.set_camera_anchor_point()
            renpy.restart_interaction()

        def r_changed(self, v):
            v=int(v)
            renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, v - self.range_rotate)
            self.set_camera_anchor_point()
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

        def set_camera_anchor_point(self):
            anchor_points = all_anchor_points.get("camera", [])
            if anchor_points:
                for i, (t, c, w) in enumerate(anchor_points):
                    if time < t:
                        anchor_points.insert(i, (time, (renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate, time, warper), warper))
                        break
                    elif time == t:
                        anchor_points[i] = (time, (renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate, time, warper), warper)
                        break
                else:
                    anchor_points.append((time, (renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate, time, warper), warper))
            else:
                if time == 0:
                    all_anchor_points["camera"] = [(time, (renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate, time, warper), warper)]
                else:
                    all_anchor_points["camera"] = [(0, (self._camera_x, self._camera_y, self._camera_z, self._camera_rotate, 0, None), None), (time, (renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z, renpy.store._camera_rotate, time, warper), warper)]
            sort_anchor_points()

        def set_layer_anchor_point(self, layer):
            anchor_points = all_anchor_points.get("layer "+layer, [])
            if anchor_points:
                for i, (t, c, w) in enumerate(anchor_points):
                    if time < t:
                        anchor_points.insert(i, (time, (renpy.store._3d_layers[layer], time, warper), warper))
                        break
                    elif time == t:
                        anchor_points[i] = (time, (renpy.store._3d_layers[layer], time, warper), warper)
                        break
                else:
                    anchor_points.append((time, (renpy.store._3d_layers[layer], time, warper), warper))
            else:
                if time == 0:
                    all_anchor_points["layer "+layer] = [(time, (renpy.store._3d_layers[layer], time, warper), warper)]
                else:
                    all_anchor_points["layer "+layer] = [(0, (self._3d_layers[layer], 0, None), None), (time, (renpy.store._3d_layers[layer], time, warper), warper)]
            sort_anchor_points()

        def play(self, play):
            if "camera" in all_anchor_points:
                camera_check_points = [c for t, c, w in all_anchor_points["camera"]]
            else:
                camera_check_points = None

            layer_check_points = {}
            layer_loop = {}
            for layer in renpy.store._3d_layers:
                if "layer "+layer in all_anchor_points:
                    layer_check_points[layer]=[c for t, c, w in all_anchor_points["layer "+layer]]
                layer_loop[layer+"_loop"] = loops[layer+"_loop"]
            layer_loop["loop"] = loops["camera_loop"]
            if camera_check_points or layer_check_points:
                renpy.store.all_moves(camera_check_points=camera_check_points, layer_check_points=layer_check_points, play=play, **layer_loop)

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
                    renpy.store.camera_move(self.cx, self.cy, renpy.store._camera_z, renpy.store._camera_rotate)
                    self.x, self.y = x, y
                    renpy.restart_interaction()
                    renpy.redraw(self, 0)
                    camera_viewer.set_camera_anchor_point()

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
                time = v
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
        if time == 0 and len(sorted_anchor_points) > 1:
            return

        remove_list=[(k, (t, c, w)) for k, v in all_anchor_points.items() for t, c, w in v if t == time]
        for k, a in remove_list:
            if len(all_anchor_points[k]) == 1:
                del all_anchor_points[k]
            else:
                all_anchor_points[k].remove(a)
        sort_anchor_points()

    def sort_anchor_points():
        global sorted_anchor_points
        sorted_anchor_points[:] = []
        for anchor_points in all_anchor_points.values():
            for t, c, w in anchor_points:
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
        camera_viewer.set_camera_anchor_point()
        renpy.restart_interaction()

    def rollforward():
        renpy.store.camera_move(renpy.store._camera_x, renpy.store._camera_y, renpy.store._camera_z+100, renpy.store._camera_rotate)
        camera_viewer.set_camera_anchor_point()
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
        if "camera" in all_anchor_points:
            camera_check_points = [c for t, c, w in all_anchor_points["camera"]]
            if len(camera_check_points) == 1 and camera_check_points[0][0:5] == (camera_viewer._camera_x, camera_viewer._camera_y, camera_viewer._camera_z, camera_viewer._camera_rotate, 0,):
                camera_check_points=None
        else:
            camera_check_points = None

        layer_check_points = {}
        layer_loop = {}
        for layer in renpy.store._3d_layers:
            if "layer "+layer in all_anchor_points:
                layer_check_points[layer]=[c for t, c, w in all_anchor_points["layer "+layer]]
                if len(layer_check_points[layer]) == 1 and layer_check_points[layer][0][0] == camera_viewer._3d_layers[layer]:
                    del layer_check_points[layer]
                layer_loop[layer+"_loop"] = loops[layer+"_loop"]
        string = ""

        if camera_check_points or layer_check_points:
            string += """
    $all_moves(camera_check_points={}, layer_check_points={}, loop={}, subpixel=True, **{})""".format(camera_check_points, layer_check_points, loops["camera_loop"], layer_loop)
        for k, v in all_anchor_points.items():
            if isinstance(k, tuple):
                string += """
    show {} onlayer {}:
        subpixel True transform_anchor True """.format(*k)
                kwargs_org = {k2: v2 for dic in [transform_viewer.state_org[k[1]], transform_viewer.state[k[1]]] for k2, v2 in dic.items()}[k[0]]
                for p, d in transform_viewer.props:
                    if kwargs_org[p] is None and p != "rotate":
                        kwargs_org[p] = d

                for prop, value in v[0][1].items():
                    if value != kwargs_org[prop]:
                        string += "{} {} ".format(prop, value)
                for i, t in enumerate(v[1:]):
                    string += """
        {} {} """.format(t[2], t[0]-v[i][0])
                    for prop, value in t[1].items():
                    # for i, (prop, value) in enumerate(t[1].items()):
                    #     for t2, k2, w2, in v[:i]:
                    #         if value = [prop]:
                        string += "{} {} ".format(prop, value)
                if string[-46:] == (":\n        subpixel True transform_anchor True "):
                    string = string[:-46]
                elif loops[k[1]+"_"+k[0]+"_loop"]:
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

