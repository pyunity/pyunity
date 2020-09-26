import sys
import sdl2
import sdl2.ext
from sdl2 import video

class Window:
	def __init__(self, title, width, height, fpsTarget):
		self.title = title
		self.width = int(width)
		self.height = int(height)
		self.fpsTarget = fpsTarget
		self.fps = fpsTarget
		sdl2.ext.init()
		self.screen = self.createScreen()
		self.context = self.createSDLContext()
		self.initClearScreen()
		self._startTime = sdl2.timer.SDL_GetTicks()
		self._currTime = self._startTime
		self._fpsDisplayDelay = 100
		self._fpsDisplayCounter = 100
		self.update()
	
	def createScreen(self):
		screen = sdl2.SDL_CreateWindow(self.title,
		sdl2.SDL_WINDOWPOS_UNDEFINED,
		sdl2.SDL_WINDOWPOS_UNDEFINED, self.width, self.height,
		sdl2.SDL_WINDOW_OPENGL)
		return screen
	
	def initClearScreen(self):
		renderer = sdl2.SDL_CreateRenderer(self.screen, -1, 0)
		sdl2.SDL_SetRenderDrawColor(renderer, *(0, 0, 0, 255))
		sdl2.SDL_RenderClear(renderer)
		sdl2.SDL_RenderPresent(renderer)
	
	def createSDLContext(self):
		video.SDL_GL_SetAttribute(video.SDL_GL_MULTISAMPLEBUFFERS, 1);
		video.SDL_GL_SetAttribute(video.SDL_GL_MULTISAMPLESAMPLES, 8);
		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 1)
		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK, video.SDL_GL_CONTEXT_PROFILE_CORE)
		
		context = sdl2.SDL_GL_CreateContext(self.screen)
		return context
		
	def close(self):
		sdl2.ext.quit()
		sys.exit()
		
	def update(self):
		events = sdl2.ext.get_events()
		for event in events:
			if event.type == sdl2.SDL_QUIT:
				self.close()
		self.tick()
		
	def tick(self):
		prevTime = self._currTime
		self._currTime = sdl2.timer.SDL_GetTicks()
		diff = self._currTime - prevTime
		self.fps = min(self.fpsTarget, 1000/diff) if diff != 0 else self.fpsTarget
		sdl2.SDL_GL_SwapWindow(self.screen)
		sdl2.SDL_Delay(1000//self.fpsTarget)
		self._fpsDisplayCounter += diff
		if self._fpsDisplayCounter >= self._fpsDisplayDelay:
			sdl2.SDL_SetWindowTitle(self.screen, self.title + b": " + bytes(str(self.fps), "utf-8"))
			self._fpsDisplayCounter = 0
