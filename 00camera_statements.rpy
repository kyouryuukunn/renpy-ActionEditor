#camera用の追加ステートメント集
#  dollyout 移動量 (時間) (warper)
#  dollyin
#  slideleft
#  slideright
#  craneup
#  cranedown
#  
#  craneup 100 5 linear #5秒かけてカメラを100上げる

python early hide:
    def parse_camera_statements(lex):
        #移動量、時間、ワーパーを返す
        amount = eval(lex.simple_expression())
        if not lex.eol():
            second = eval(lex.simple_expression())
        else:
            second = 0
        if not lex.eol():
            warper = lex.simple_expression()
        else:
            warper = "power_in_time_warp_real"
        return amount, second, warper
##################################################################################################
    def execute_dollyout(o):
        amount, second, warper = o
        camera_move(_camera_x, _camera_y, _camera_z-amount, _camera_rotate, second, warper=warper)

    renpy.register_statement("dollyout", parse=parse_camera_statements, execute=execute_dollyout)
##################################################################################################
    def execute_dollyin(o):
        amount, second, warper = o
        camera_move(_camera_x, _camera_y, _camera_z+amount, _camera_rotate, second, warper=warper)

    renpy.register_statement("dollyin", parse=parse_camera_statements, execute=execute_dollyin)
##################################################################################################
    def execute_slideleft(o):
        amount, second, warper = o
        camera_move(_camera_x-amount, _camera_y, _camera_z, _camera_rotate, second, warper=warper)

    renpy.register_statement("slideleft", parse=parse_camera_statements, execute=execute_slideleft)
##################################################################################################
    def execute_slideright(o):
        amount, second, warper = o
        camera_move(_camera_x+amount, _camera_y, _camera_z, _camera_rotate, second, warper=warper)

    renpy.register_statement("slideright", parse=parse_camera_statements, execute=execute_slideright)
##################################################################################################
    def execute_craneup(o):
        amount, second, warper = o
        camera_move(_camera_x, _camera_y-amount, _camera_z, _camera_rotate, second, warper=warper)

    renpy.register_statement("craneup", parse=parse_camera_statements, execute=execute_craneup)
##################################################################################################
    def execute_cranedown(o):
        amount, second, warper = o
        camera_move(_camera_x, _camera_y+amount, _camera_z, _camera_rotate, second, warper=warper)

    renpy.register_statement("cranedown", parse=parse_camera_statements, execute=execute_cranedown)
