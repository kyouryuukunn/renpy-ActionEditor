 youtube sample
 <https://www.youtube.com/watch?v=XQDl9x9L-es>

 日本語マニュアルはドキュメント後半にあります。

 This script adds the ability to simulate a 3D camera within Ren'Py, along with an
 in-game Action Editor and Image Viewer GUI to assist in animating the camera.
 To install, copy all files in the camera directory to your game directory.

 Ren'Py <http://www.renpy.org/>

 Action Editor
================

 This allows you to adjusts coordinates of the simulated camera, 3D layers, and transform properties
 of images in real-time with a GUI. It can then generate a script based on these changes and
 place it on the clipboard for later pasting into Ren'Py scripts.

 When `config.developer` is True, pressing action_editor (by default,
 "shift+P") will open the Action editor.
 
 The Action Editor has the following features:
 
  * View and adjust the transform properties of images, camera coordinates, and 3D layer depth with bars
  * View and adjust the x and y coordinates of the camera with a mouse-positionable camera
  * Adjust the z coordinate of the camera with the mouse wheel.
  * Alternatively, each value can be adjusted with the keyboard without going back to the original script.
  * Add, delete, and edit keyframes on a timeline.
  * After setting up a scene with the desired look and animations, the Action Editor will generate a script and place it on your clipboard for pasting into your Ren'Py scripts. (v6.99 and later only)

 Image Viewer
================
 
 Press Shift+U to open Image Viewer and view all currently generated displayables.


 Camera
================

 With some limitations, Ren'Py can simulate 3D camera motion. This will
 let you achieve a parallax effect by placing sprites and assets on a 3D field.
 This script works by applying ATL transforms to all displayables on 3D layers in a manner that respects distance from a virtual camera.

 To start using the 3D camera, set additional layers to be registered
 as 3D layers. If no layers are registered as 3D layers, this script will 
 register the default `master` layer as a 3D layer.

 To get started, add the following to options.rpy to add `background`, `middle`, and `forward` as regular 2D layers:

         config.layers = ['master', 'background', 'middle', 'forward', 'transient', 'screens', 'overlay']

 Second, register any layers that you want to respect 3D motion as 3d layers by using
 :func:`register_3d_layer`. The z coordinates of these layers can be moved and can have their positions and transforms affected by the camera. If no layers are registered as 3D layers, the default `master` layer becomes the sole 3D layer:

         init python:
             register_3d_layer('background', 'middle', 'forward')

 This sample script should give an idea of how the system works:

          label start:
              # Resets the camera and layers positions
              $ camera_reset()
              # Instantly sets layer distances from the camera
              $ layer_move("background", 2000)
              $ layer_move("middle", 1500)
              $ layer_move("forward", 1000)
              scene bg onlayer background
              # WARNING: The 'scene' command will reset the depth of whatever layer the image
              # is displayed on. Make sure you reset the depth after you call the 'scene' command.
              $ layer_move("background", 2000)
              show A onlayer middle
              show B onlayer forward
              with dissolve
              "Moves the camera to (1800, 0, 0) in 1 second."
              $ camera_move(1800, 0, 0, 0, 1)
              "Moves the camera to (0, 0, 1600) in 5 seconds."
              $ camera_move(0, 0, 1600, 0, 5)
              "Moves the camera to (0, 0, 0) instantaneously."
              $ camera_move(0, 0, 0)
              "Rotates the camera 180 degrees in 1 second.""
              $ camera_move(0, 0, 0, 180, 1)
              'Rotates the camera -180 degrees in 1 second and subsequently moves the camera to (-1800, 0, 500) in 1.5 seconds'
              $ camera_moves( ( (0, 0, 0, 0, 1, 'linear'), (-1800, 0, 500, 0, 1.5, 'linear') ) )
              'Continually moves the camera between (-1800, 0, 500) and (0, 0, 0), taking 0.5 seconds for the first move and 1 second for the second until the action is interrupted.'
              $ camera_moves( ( (0, 0, 0, 0, .5, 'linear'), (-1800, 0, 500, 0, 1, 'linear') ), loop=True)

 There are some limitations to the 3D camera:

 * Only rotations perpindicular to the camera (Z rotations) can be performed due to the 3D camera relying
   on Ren'Py's existing transform system.

 * 3D camera motion applies its own transforms to 3D layers, so the `show layer` statement or
   :func:`renpy.show_layer_at` can't be used with registered 3D layers.

 * Layers still stack in the order they are registered, regardless of what their z coordinates are. In our above example, `background` will always be below the other layers because it was registered first, even if its z coordinate was at `0` and the `forward` layer's z coordinate was at `1000`.

 * `camera_move`, `camera_moves`, `layer_move`, `layer_moves`, and `all_moves` can't play
   simultaneously within the same interaction. If multiple camera actions are called in the same interaction,
   only the last one will play out and earlier actions will be done instantenously before the last action is played.

 * By default, the `scene` and `hide` statements use the `master` layer or a specified layer.
   If you use 3D layers preferentially, write code like below:


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

         Register layers as 3D layers. Only 3D layers will be affected by camera
         movement and 3D layer transforms. This should be called in an init
         block. If no layers are registered as 3D layers, the 'master' layer
         will become a 3D layer by default.

         `layers`
              This should be a string or a group of strings naming registered layers.
         """

    def camera_reset():
        """
         :doc: camera

         Resets the camera and 3D layers positions.
         """

    def camera_restore():
        """
         :doc: camera

         Safety method used internally to deal with unexpected camera behavior.

         """

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

    def all_moves(camera_check_points=None, layer_check_points=None, subpixel=True, play=True, x_loop=False, y_loop=False, z_loop=False, rotate_loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, camera_spline=False, **kwargs):
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


 このスクリプトはRen'Pyに擬似的な3Dカメラ機能及びとそれをGUI上で設定する演出エディター、さらに画像ビューワー、便利なワーパー関数を追加します。フォルダ内のファイルをgameフォルダにコピーしてください。


 演出エディター
================

 演出エディターでは変換プロパティーやカメラ、レイヤーの座標設定をGUI上で変更し、
 結果を確認できます。さらにそれらの値を時間軸に沿って変更可能なので、スクリプト
 を変更するたびに、リロードで結果を確認する従来の方法より遥かに短時間で動的演出
 を作成可能です。設定した値はクリップボードに送られ、スクリプトに貼り付けられま
 す。

 config.developer が True なら、Shift+Pで演出エディターが起動します。
 
 演出エディターでは以下の機能が利用可能です。:
 
 * 各画像の変換プロパティーやカメラ、レイヤー座標を直接入力またはバーの操作により変更
 * カメラアイコンのドラッグまたはマウスホイール、キーボード(hjkl,HJKL)によるカメラ移動
 * 動画編集ソフトの様にキーフレームを設定して時間軸にそった演出を作成
 * 作成した演出のコードをクリップボードに送る(v6.99以上, Windows限定)

 イメージビューワー
================
 定義された画像を画像タグ、属性から縛り込んで表示します。

 config.developer が True なら、Shift+Uで起動します。

 カメラ
================

 三次元を再現する関数群をRen'Py に追加します。これらは3Dレイヤーに登録された各レ
 イヤーにz座標を与え、カメラとの位置関係により拡大縮小移動させて三次元をシ
 ミュレートします。これにより奥行きの表現が簡単に可能になります。この機能を
 利用するには、先ず3Dレイヤーに登録するレイヤーを追加しなければなりません。3Dレ
 イヤーに何も登録されていない場合、デフォルトで"master"レイヤーのみが3Dレイ
 ヤーに登録されます。

 例

         options.rpy に以下のような設定を加え、'background', 'middle', 'forward' レイヤーを追加します。

                config.layers = [ 'master', 'background', 'middle', 'forward', 'transient', 'screens', 'overlay']

 次に register_3d_layer 関数で3Dレイヤーを登録します。これらのレイヤーはz座標を移動出来、カメラの影響を受けます。register_3d_layerが使用されないと、デフォルトで"master"レイヤーが登録されます。

        init python:
            register_3d_layer( 'background', 'middle', 'forward',)

 以上の設定で、ゲーム中でカメラ動かせるようになります。

        label start:
            # カメラ、レイヤー位置をリセット
            $ camera_reset()
            # 0秒でレイヤーz座標を変更します。
            $ layer_move("background", 2000)
            $ layer_move("middle", 1500)
            $ layer_move("forward", 1000)
            scene bg onlayer background
            # 注意: 'scene' ステートメントは画像が表示されるだけでなく、その画像が表示されるレイヤーの状態もリセットします。
            # 問題が発生する場合はsceneステートメント後にlayer_move関数でレイヤー位置を再設定してください。
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

 * カメラモーションは3Dレイヤーに対して変換を適用して再現しているため、3Dレイヤーに対して show layer ステートメントや renpy.show_layer_at 関数は使用出来ません。
 * レイヤーの重なり順はレイヤーのz座標を反映しません。
 * camera_move, camera_moves, layer_move, layer_moves, all_moves はそれぞれ排他的です。ひとつのインタラクション中に複数回呼び出されると、最後に呼び出されたもののみが正常に動作し、それ以外は瞬時に移動します。

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

	      カメラとレイヤーを初期位置に戻します。
             """

         def camera_restore():
             """
              :doc: camera

	      カメラとレイヤーを現在設定されている位置に戻します。
	      sceneステートメントや、show layerステートメントで画像位置が狂ったときの修正ようです。
              """

        def camera_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, **kwargs):
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
             `<layer name>_express`
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時
                   間軸の秒数を引数に呼び出され、数字を返します。この結果は指定
                   したレイヤーの座標に加えられます。
              """

        def camera_relative_move(x, y, z, rotate=0, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, **kwargs):
             """
              :doc: camera

              カメラの座標と角度を指定の時間かけて変更します。

              `x`
                   現在の座標に対して相対的なカメラのx座標の数字です。
              `y`
                   現在の座標に対して相対的なカメラのy座標の数字です。
              `z`
                   現在の座標に対して相対的なカメラのy座標の数字です。
              `rotate`
                   デフォルトは0で、現在の角度に対して相対的なカメラの傾きの数字です。
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
             `<layer name>_express`
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時
                   間軸の秒数を引数に呼び出され、数字を返します。この結果は指定
                   したレイヤーの座標に加えられます。
              """

        def camera_moves(check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None, spline=False, **kwargs):
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
             `<layer name>_express`
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時
                   間軸の秒数を引数に呼び出され、数字を返します。この結果は指定
                   したレイヤーの座標に加えられます。
             `spline`
                 カメラの座標に対してスプライン補間を有効にします。True ならワーパーは無視されます。これはデフォルトでFalseです。
              """

        def layer_move(layer, z, duration=0, warper='linear', subpixel=True, loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, layer_express=None):
             """
              :doc: camera

              3Dレイヤーのz座標を指定の時間かけて変更します。

              `layer`
                   移動するレイヤー名の文字列です。
              `z`
                   レイヤーのz座標の数字です。
              `duration`
                   デフォルトは0で、レイヤー移動にかかる時間の秒数です。
              `warper`
                   デフォルトは'linear'で, 時間補間に使用する関数名の文字列です。こ
                   れにはATLに登録された時間補間関数が指定出来ます。
              `subpixel`
                   デフォルトは Trueで、 True なら、1 pixel 以下の値を使用して画面
                  に描画します。
              `loop`
                   デフォルトは Falseで、True ならこのモーションが繰り替えされます。
             `layer_express`
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時
                   間軸の秒数を引数に呼び出され、数字を返します。この結果はレイ
                   ヤーの座標に加えられます。
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
             `<layer name>_express`
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時
                   間軸の秒数を引数に呼び出され、数字を返します。この結果は指定
                   したレイヤーの座標に加えられます。
             `spline`
                 レイヤーの座標に対してスプライン補間を有効にします。True ならワーパーは無視されます。これはデフォルトでFalseです。
              """

        def layer_moves(layer, check_points, loop=False, subpixel=True, x_express=None, y_express=None, z_express=None, rotate_express=None, layer_express=None, spline=False):
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
             `layer_express`
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時
                   間軸の秒数を引数に呼び出され、数字を返します。この結果はレイ
                   ヤーの座標に加えられます。
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
             `spline`
                 レイヤーの座標に対してスプライン補間を有効にします。True ならワーパーは無視されます。これはデフォルトでFalseです。
             """

        def all_moves(camera_check_points=None, layer_check_points=None, subpixel=True, play=True, x_loop=False, y_loop=False, z_loop=False, rotate_loop=False, x_express=None, y_express=None, z_express=None, rotate_express=None, camera_spline=False, **kwargs):
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
             `x_loop`
                   デフォルトは Falseで、True ならカメラのモーションが繰り替えされます。
             `y_loop`
                   デフォルトは Falseで、True ならカメラのモーションが繰り替えされます。
             `z_loop`
                   デフォルトは Falseで、True ならカメラのモーションが繰り替えされます。
             `rotate_loop`
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
             `<layer name>_express`
                   これは呼出可能なオブジェクトで、出現時間軸とアニメーション時
                   間軸の秒数を引数に呼び出され、数字を返します。この結果は指定
                   したレイヤーの座標に加えられます。
             `camera_spline`
                 カメラの座標に対してスプライン補間を有効にします。True ならワーパーは無視されます。これはデフォルトでFalseです。
             `spline`
                 レイヤーの座標に対してスプライン補間を有効にします。True ならワーパーは無視されます。これはデフォルトでFalseです。

              キーワード引数として <レイヤー名>_loop をとります。デフォルトは Falseで、True ならそのレイヤーのモーションが繰り替えされます。
             """
