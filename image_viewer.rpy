#Shift+U: Open Image Viewer
#2016 1/22 v6.99
init -2000 python:
    def _open_image_viewer():
        if not renpy.config.developer:
            return
        default = ()
        while True:
            name = renpy.invoke_in_new_context(renpy.call_screen, "_image_selecter", default=default)
            if isinstance(name, tuple): #press button
                default = tuple(set(name))
            elif name: #from input text
                default = tuple(name.split())
            else:
                renpy.notify(_("Please type image name"))
                return
