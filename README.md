 youtube sample
 <https://www.youtube.com/watch?v=XQDl9x9L-es>

 日本語マニュアルはドキュメント後半にあります。

 This script adds Ren'Py GUI Action editor and 3D camera functions. Please
 copy camera.rpy and camera.png to your game directory.

 Ren'Py <http://www.renpy.org/>

 Action editor
================

 This allows you to adjusts coordinates of the camera or 3D layers or values
 of transform properties of images by GUI. This generates a script based on
 the result of the adjustment and puts it on clipboard.

 When :var:`config.developer` is True, pressing action_editor (by default,
 "shift+P"), will open Action editor.
 
 Action editor has below features.:
 
  * Each transform property of images, coordinates of the camera or layers can be changed by bars.
  * The x, y coordinates of the camera can be changed by dragging the camera icon.
  * The z coordinate of the camera can be changed by mouse wheel.
  * Each value can be inputted by keyboard.
  * keyframes can be added to the time bar.
  * Each transform property of images, coordinates of the camera and layers or actions can be putted on clipboard.(v6.99 or later, only winows?)


 Camera
================

 With some limitations, Ren'Py can simulate 3D camera motion. This will easily
 let you achieve a parallax effect by placing sprites and assets on a 3D field.
 This script applies transforms to each layers which are registered as 3D layer by
 positions of a camera and 3D layers on a 3D field to simulate 3D camera motion.

 If you use this feature, in the first, set additional layers to be registered
 as 3D layer. If anything isn't registered as 3D layers, this script register
 "master" layer as 3D layers.

 For example, Write a code like below in options.rpy and add 'background', 'middle', 'forward'  layers.::

         config.layers = ['master', 'background', 'middle', 'forward', 'transient', 'screens', 'overlay']

 Second, register layers which participate to a 3D motion as 3d layers by
 :func:`register_3d_layer`. The z coordinates of these layers can be moved and
 applied transforms to by positions of the camera and 3D layers. If anything
 isn't registered as 3D layers, this script registers 'master' layer as 3D
 layer.::

         init python:
             register_3d_layer('background', 'middle', 'forward')

 Then, a camera and layers can move. ::

          label start:
              # reset the camera and layers positions and allow layers position to be saved.
              $ camera_reset()
              # It takes 0 second to move layers
              $ layer_move("background", 2000)
              $ layer_move("middle", 1500)
              $ layer_move("forward", 1000)
              scene bg onlayer background
              show A onlayer middle
              show B onlayer forward
              with dissolve
              'It takes 1 second to move a camera to (1800, 0, 0)'
              $ camera_move(1800, 0, 0, 0, 1)
              'It takes 5 seconds to move a camera to (0, 0, 1600)'
              $ camera_move(0, 0, 1600, 0, 5)
              'A camera moves to (0, 0, 0) at the moment'
              $ camera_move(0, 0, 0)
              'It takes 1 second to rotate a camera to 180 degrees'
              $ camera_move(0, 0, 0, 180, 1)
              'It takes 1 second to rotate a camera to -180 degrees and 0.5 second to move a camera to (-1800, 0, 500)'
              $ camera_moves( ( (0, 0, 0, 0, 1, 'linear'), (-1800, 0, 500, 0, 1.5, 'linear') ) )
              'a camera shuttles between (-1800, 0, 500) and (0, 0, 0)'
              $ camera_moves( ( (0, 0, 0, 0, .5, 'linear'), (-1800, 0, 500, 0, 1, 'linear') ), loop=True)

 Notice that 3D camera motion has some limits.:

 * 3D camera motion applies transforms to 3D layers, so the show layer statement or
   :func:`renpy.show_layer_at` to 3D layers can't be usable.

 * z coordinates of 3D layers don't affect the stacking order of 3d layers.

 * camera_move, camera_moves, layer_move, layer_moves, all_moves can't play
   within the same interaction. The last one only follows a instruction and
   others works momentarily if they are called from within the same
   interaction.

 * By default, the scene, hide statements use master or the given layer
   only. If you use 3D layers preferentially, write code like below.::


	init -1 python hide:
	    def hide(name, layer='master'):
		for l in _3d_layers:
		    if renpy.showing(name, l):
		renpy.hide(name, l)
		break
		else:
		    renpy.hide(name, layer)

	    config.hide = hide

	    def scene(layer='master'):

		renpy.scene(layer)
		for l in _3d_layers:
		    renpy.scene(l)

	    config.scene = scene

 Camera Functions
 ----------------

        def register_3d_layer(*layers):
            """
             :doc: camera

             Register layers as 3D layers. 3D layers are applied transforms to by
             positions of a camera and 3D layers. This should be called in init
             block. If anything isn't registered as 3D layers, this script
             register "master" layer as 3D layers

             `layers`
                  This should be the string or strings of a layer name.
             """

        def camera_reset():
            """
             :doc: camera

             Reset a camera and 3D layers positions. Please call this at least once
             when the game has started. If this doesn't called, The position of 3D
             layers don't be saved.
             """

        def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None):
            """
             :doc: camera

             Move the coordinate and rotate the camera.

             `x`
                  The x coordinate of the camera
             `y`
                  The y coordinate of the camera
             `z`
                  The z coordinate of the camera
             `rotate`
                  Defaul 0, the angle of the camera
             `duration`
                  Default 0, this is the second times taken to move the camera.
             `loop`
                  Default False, if True, this motion repeats.
             `warper`
                  Default 'linear', this should be the string of the name of a
                  warper registered with ATL.
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

        def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None):
            """
             :doc: camera

             Move the z coordinate of a layer.

             `layer`
                  The string of a layer name to be moved
             `z`
                  The z coordinate of a layer
             `duration`
                  Default 0, this is the second times taken to move a layer.
             `loop`
                  Default False, if True, this motion repeats.
             `warper`
                  Default 'linear', this should be the string of the name of a
                  warper registered with ATL.
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

        def camera_moves(check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None):
            """
             :doc: camera

             Move a camera through check points.

             `check_points`
                  A list of tuples of x, y, z, rotate, duration, warper.
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

        def layer_moves(layer, check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None):
            """
             :doc: camera

             Move the z coordinate of a layer through check points.

             `layer`
                  the string of a layer name to be moved
             `check_points`
                  A list of tuples of z, duration, warper
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

        def all_moves(camera_check_points=None, layer_check_points=None, subpixel=True, play=True, x_loop=False, y_loop=False, z_loop=False, rotate_loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, **kwargs):
            """
             :doc: camera

             Move the camera and layers through check points.

             `camera_check_points`
                  This is the map from the string of a camera parameter name to list of
                  tuples of value, duration, warper.
                  {
                      'x':[(x, duration, warper)...],
                      'y':[(y, duration, warper)...],
                      'z':[(z, duration, warper)...],
                      'rotate':[(rotate, duration, warper)...],
                  }
             `layer_check_points`
                  This is the map from the string of a layer name to list of
                  tuples of z, duration, warper.
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

              If keyword arguments 'layer name'_loop is given, the layer motion is repeats.
             """





 このスクリプトはRen'PyにGUIの演出エディターとカメラ機能を追加します。camera.rpyとcamera.pngをgameフォルダにコピーしてください。

 演出エディター
================

 GUIを利用して画像の変換プロパティーやカメラ、レイヤーの座標調整、時間軸にそった演出作成を可能にします。設定した値からスクリプトを自動生成し、クリップボードに送ります。

 config.developer が True なら、Shift+Pで演出エディターが起動します。
 
 演出エディターでは以下の機能が利用可能です。:
 
 * 各画像の変換プロパティーやカメラ、レイヤーの座標をバーから変更出来ます。
 * カメラアイコンのドラッグでカメラを移動出来ます。
 * マウスのホイールからカメラのz座標を変更出来ます。
 * 各パラメーターをキーボードから入力出来ます。
 * アンカーポイントを設定して時間軸にそった演出が作れます。
 * 画像の変換プロパティーやカメラ、レイヤーの座標、時間軸にそった演出をそれぞれクリップボードに送れます。(v6.99以上, Windows限定? Macで動作するかは判りま
   せん。)

 カメラ
================

 三次元を再現する関数をRen'Py に追加します。これらは3Dレイヤーに登録された各レイヤーにz座標を与え、カメラとの位置関係により拡大縮小移動させて三次元をシミュレートします。これにより奥行きの表現が簡単に可能になるでしょう。この機能を利用するには、先ず3Dレイヤーに登録するレイヤーを追加しなければなりません。3Dレイヤーに何も登録されていない場合、"master"レイヤーのみを3Dレイヤーに登録します。

 例

         options.rpy に以下のような設定を加え、'background', 'middle', 'forward' レイヤーを追加します。

                config.layers = [ 'master', 'background', 'middle', 'forward', 'transient', 'screens', 'overlay']

 次に register_3d_layer 関数で3Dレイヤーを登録します。これらのレイヤーはz座標を移動出来、カメラの影響を受けます。register_3d_layerが使用されないと、デフォルトで"master"レイヤーが登録されます。

        init python:
            register_3d_layer( 'background', 'middle', 'forward',)

 以上の設定で、ゲーム中でカメラ動かせるようになります。

        label start:
            # カメラ、レイヤー位置をリセットし、レイヤー位置がセーブされるようにします。
            $ camera_reset()
            # 0秒でレイヤーz座標を変更します。
            $ layer_move("background", 2000)
            $ layer_move("middle", 1500)
            $ layer_move("forward", 1000)
            scene bg onlayer background
            show A onlayer middle
            show B onlayer forward
            with dissolve
            '1秒でカメラを(0, 130, 0)まで移動させます。'
            $ camera_move(0, 130, 0, 0, 1)
            '5秒でカメラを(-70, 130, 1000)まで移動させます。'
            $ camera_move(-70, 130, 1000, 0, 5)
            '0秒かけてカメラを(0, 0, 0)まで移動させます。'
            $ camera_move(0, 0, 0)
            '1秒かけてカメラを時計回りに180度回転します。'
            $ camera_move(0, 0, 0, 180, 1)
            '1秒かけてカメラを反時計回りに180度回転させ、4秒かけてカメラを(100, 100, 100)まで移動させます。'
            $ camera_moves( ( (0, 0, 0, 0, 1, 'linear'), (100, 100, 100, 0, 5, 'linear') ) )
            'カメラが(100, 100, 100)から(0, 0, 0)までを繰り返し往復します'
            $ camera_moves( ( (0, 0, 0, 0, 1, 'linear'), (100, 100, 100, 0, 2, 'linear') ), loop=True)

 カメラ機能にはいくつかの制限があることに注意してください。

 * カメラモーションは3Dレイヤーに対して変換を適用して再現しているため、3レイヤーに対して show layer ステートメントや renpy.show_layer_at 関数は使用出来ません。
 * レイヤーの重なり順はレイヤーのz座標を反映しません。
 * camera_move, camera_moves, layer_move, layer_moves, all_moves はそれぞれ排他的です。ひとつのインタラクション中に複数回呼び出されると、最後に呼び出されたもののみが正常に動作し、それ以外は瞬間移動になります。

 デフォルトではRen'Pyの scene, show, hide ステートメントは master レイヤー又は指定されたレイヤーにのみ作用します。3Dレイヤーに対して優先的に作用させたい場合は以下のようにしてRen'Pyの設定を変更してください。

        init -1 python hide:

            def hide(name, layer='master'):
                for l in _3d_layers:
                    if renpy.showing(name, l):
                        renpy.hide(name, l)
                else:
                    renpy.hide(name, layer)

            config.hide = hide

            def scene(layer='master'):

                renpy.scene(layer)
                for l in _3d_layers:
                    renpy.scene(l)

            config.scene = scene

 カメラ関数
 ----------------

         def register_3d_layer(*layers):
             """
              :doc: camera

              レイヤーを3Dレイヤーとして登録します。3Dレイヤーに登録されたレイヤー
              には、そのz座標とカメラの位置に基づいた変換が適用されます。initブ
              ロックで一度だけ呼び出してください。3Dレイヤーになにも登録されていな
              い場合、"master"レイヤーを3Dレイヤーに登録します。

              `layers`
                   3Dレイヤーに登録する、一つ以上のレイヤー名の文字列です。
              """

         def camera_reset():
             """
              :doc: camera

              カメラとレイヤーを初期位置に戻します。ゲーム開始後に少くとも一度は呼
              び出してください。呼び出されない場合、3Dレイヤーの座標が保存されませ
              ん。
              """

        def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None):
             """
              :doc: camera

              カメラの座標と角度を指定の時間かけて変更します。

              `x`
                   カメラのx座標の数字です。
              `y`
                   カメラのy座標の数字です。
              `z`
                   カメラのy座標の数字です。
              `rotate`
                   デフォルトは0で、カメラの傾きの数字です。
              `duration`
                   デフォルトは0で、カメラ移動にかかる時間の秒数です。
              `loop`
                   デフォルトは Falseで、True ならこのモーションが繰り替えされます。
              `warper`
                   デフォルトは'linear'で, 時間補間に使用する関数名の文字列です。こ
                   れにはATLに登録された時間補間関数が指定出来ます。
              `subpixel`
                   デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
                   に描画します。
             'x_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   x座標に加えられます。
             'y_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   y座標に加えられます。
             'z_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   z座標に加えられます。
             'rotate_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   rotate座標に加えられます。
              """

        def camera_moves(check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None):
             """
              :doc: camera

              1つ以上のチェックポイントを通ってカメラを動かします。

              `check_points`
                   カメラのx,y,z座標、傾き、カメラの移動開始からその位置に到達
                   するまでの秒数、その間の時間補間関数名の文字列からなるタプル
                   のリストです。カメラはここで指定された各タプルを順番に移動す
                   るので、タプルは時系列に沿って並べてください。
              `loop`
                   デフォルトは Falseで、True ならこのモーションが繰り替えされます。
              `subpixel`
                   デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
                   に描画します。
             'x_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   x座標に加えられます。
             'y_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   y座標に加えられます。
             'z_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   z座標に加えられます。
             'rotate_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   rotate座標に加えられます。
              """

        def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None):
             """
              :doc: camera

              レイヤーのz座標を指定の時間かけて変更します。

              `layer`
                   移動するレイヤー名の文字列です。
              `z`
                   レイヤーの移動先z座標の数字です。
              `duration`
                   デフォルトは0で、レイヤー移動にかかる時間の秒数です。
              `loop`
                   デフォルトは Falseで、True ならこのモーションが繰り替えされます。
              `warper`
                   デフォルトは'linear'で, 時間補間に使用する関数名の文字列です。こ
                   れにはATLに登録された時間補間関数が指定出来ます。
              `subpixel`
                   デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
                   に描画します。
             'x_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   x座標に加えられます。
             'y_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   y座標に加えられます。
             'z_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   z座標に加えられます。
             'rotate_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   rotate座標に加えられます。
             """

        def layer_moves(layer, check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None):
             """
              :doc: camera

              1つ以上のチェックポイントを通って3Dレイヤーを動かします。

              `layer`
                   移動するレイヤー名の文字列です。
              `check_points`
                   レイヤーのz座標の数字、レイヤーの移動開始からその位置に到達するまでの
                   秒数の数字、その間の時間補間関数の文字列からなるタプルのlistです。
                   レイヤーはここで指定された各タプルを順番に移動するので、タプル
                   は時系列に沿って並べてください。
              `loop`
                   デフォルトは Falseで、True ならこのモーションが繰り替えされます。
              `subpixel`
                   デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
                   に描画します。
             'x_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   x座標に加えられます。
             'y_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   y座標に加えられます。
             'z_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   z座標に加えられます。
             'rotate_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   rotate座標に加えられます。
             """

        def all_moves(camera_check_points=None, layer_check_points=None, subpixel=True, x_loop=False, y_loop=False, z_loop=False, rotate_loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, **kwargs):
            """
             :doc: camera

              1つ以上のチェックポイントを通ってカメラと3Dレイヤーを同時に動かします。

             `camera_check_points`
                   カメラの各パラメーター名の文字列をキーとし、その値、その値に
                   なるまでの秒数、その間の時間補間関数名の文字列からなるタプル
                   のリストを値に持つ辞書です。カメラはここで指定された各タプル
                   を順番に移動するので、タプルは時系列に沿って並べてください。
                  {
                      'x':[(x, duration, warper)...],
                      'y':[(y, duration, warper)...],
                      'z':[(z, duration, warper)...],
                      'rotate':[(rotate, duration, warper)...],
                  }
             `layer_check_points`
                   移動するレイヤー名の文字列をキーとし、レイヤーのz座標の数字、レ
                   イヤーの移動開始からその位置に到達するまでの秒数の数字、その間
                   の時間補間関数の文字列からなるタプルのリストを値に持つ辞書で
                   す。レイヤーはここで指定された各タプルを順番に移動するので、タ
                   プルは時系列に沿って並べてください。
              `loop_x`
                   デフォルトは Falseで、True ならカメラのモーションが繰り替えされます。
              `loop_y`
                   デフォルトは Falseで、True ならカメラのモーションが繰り替えされます。
              `loop_z`
                   デフォルトは Falseで、True ならカメラのモーションが繰り替えされます。
              `loop_rotate`
                   デフォルトは Falseで、True ならカメラのモーションが繰り替えされます。
              `subpixel`
                   デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
                   に描画します。
             'x_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   x座標に加えられます。
             'y_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   y座標に加えられます。
             'z_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   z座標に加えられます。
             'rotate_express'
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時間
                   軸の秒数を引数に呼び出され、数字を返します。この結果はカメラの
                   rotate座標に加えられます。

              キーワード引数として <レイヤー名>_loop をとります。デフォルトは Falseで、True ならそのレイヤーのモーションが繰り替えされます。
             """
