from OpenGL.GL import *
import numpy as np

class Shader:
    def __init__(self, vsUrl, fsUrl):
        self.vsUrl = vsUrl
        self.fsUrl = fsUrl
        self.vsStr, self.fsStr = self.getShaderStrings()
        self.vs = None
        self.fs = None
        self.program = None
        
    def getShaderStrings(self):
        vs = "\n".join(open(self.vsUrl).readlines())
        fs = "\n".join(open(self.fsUrl).readlines())
        return vs, fs
    
    def compile(self):
        self.vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vs, self.vsStr)
        glCompileShader(self.vs)
        check = glGetShaderiv(self.vs, GL_COMPILE_STATUS)
        if not(check):
            raise RuntimeError(glGetShaderInfoLog(self.vs))

        self.fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fs, self.fsStr)
        glCompileShader(self.fs)
        check = glGetShaderiv(self.fs, GL_COMPILE_STATUS)
        if not(check):
            raise RuntimeError(glGetShaderInfoLog(self.fs))

        self.program = glCreateProgram()
        glAttachShader(self.program, self.vs)
        glAttachShader(self.program, self.fs)
        glLinkProgram(self.program)
        check = glGetProgramiv(self.program, GL_LINK_STATUS)
        if not(check):
            raise RuntimeError(glGetProgramInfoLog(self.program))
    
    def enable(self):
        glUseProgram(self.program)
    
    def disable(self):
        glUseProgram(0)

    def getAttribLocation(self, aName):
        return glGetAttribLocation(self.program, aName)
        
    def getUniformLocation(self, uName):
        return glGetUniformLocation(self.program, uName)
    
    def setUniform(self, uName, uType, data):
        loc = self.getUniformLocation(uName)
        if uType == "sampler2D" or uType == "sampler2DShadow":
            glUniform1i(loc, data)
        elif uType == "mat4":
            glUniformMatrix4fv(loc, 1, False, data)
        elif uType == "vec3":
            glUniform3f(loc, *data)
        elif uType == "float":
            data = float(data)
            glUniform1f(loc, data)
        elif uType == "int":
            data = int(data)
            glUniform1i(loc, data)	
            
    def setAttribute(self, aName, aType, buff):
        loc = self.getAttribLocation(aName)
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, buff)
        if aType == "vec2":
            glVertexAttribPointer(loc, 2, GL_FLOAT, False, 0, None)
        elif aType == "vec3":
            glVertexAttribPointer(loc, 3, GL_FLOAT, False, 0, None)
        elif aType == "vec4":
            glVertexAttribPointer(loc, 4, GL_FLOAT, False, 0, None)
