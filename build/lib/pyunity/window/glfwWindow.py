import glfw, time
from ..errors import *

from .. import config

class Window:
    def __init__(self, size, name):
        glfw.init()

        self.window = glfw.create_window(*size, name, None, None)
        if not self.window:
            glfw.terminate()
            raise PyUnityException("Cannot open GLFW window")
        
        glfw.make_context_current(self.window)
    
    def start(self, updateFunc):
        last = glfw.get_time()
        while not glfw.window_should_close(self.window):
            updateFunc()
            glfw.swap_buffers(self.window)
            glfw.poll_events()

            while (glfw.get_time() < last + 1 / config.fps):
                pass

            last += 1 / config.fps
        glfw.terminate()