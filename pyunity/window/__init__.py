"""
pyunity.window
==============
A module used to load the window providers.

Windows
-------
The window is provided by one of three
providers: FreeGLUT, GLFW and Pygame.
When you first import PyUnity, it checks
to see if any of the three providers
work. The testing order is as above, so
Pygame is tested last.

To create your own provider, create a
class that has the following methods:

- `__init__`: initiate your window and
    check to see if it works.
- `start`: start the main loop in your
    window. The first parameter is
    ``update_func``, which is called
    when you want to do the OpenGL calls.

Check the source code of any of the window
providers for an example. If you have a
window provider, then please email it
to me at tankimarshal2@gmail.com.

"""

def LoadWindowProvider(win):
    if win == "glut":
        from .glutWindow import Window as glutWindow
        return glutWindow
    if win == "pygame":
        from .pygameWindow import Window as pygameWindow
        return pygameWindow
    if win == "glfw":
        from .glfwWindow import Window as glfwWindow
        return glfwWindow