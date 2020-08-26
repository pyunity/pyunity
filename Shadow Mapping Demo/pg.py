import pygame
pygame.init()
from shader import Shader
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
from PIL import Image

def loadAA7(dataUrl):
    """
    Loads the mesh data from a file with a .aa7 extension.
    This is my custom model format, which is just a simplified obj (no indexing).
    Lines are just 3 vertex coords, then 2 tex coords, then 3 normal coords.
    """
    vData = []
    tData = []
    nData = []
    inFile = open(dataUrl, "r")
    for line in inFile.readlines():
        lineList = line.strip().split("\t")
        vData.extend([float(v) for v in lineList[0:3]])
        tData.extend([float(v) for v in lineList[3:5]])
        nData.extend([float(v) for v in lineList[5:]])
    vertexData = np.array(vData, dtype=np.float32)
    texCoordData = np.array(tData, dtype=np.float32)
    normalData = np.array(nData, dtype=np.float32)
    return vertexData, texCoordData, normalData

def createMeshBuffers(vertices, texCoords, normals):
    """
    Creates vertex buffer objects for the vertices, texCoords, and normals.
    Binds the ids to the vertex data.
    """
    v, t, n = vertices, texCoords, normals
    vbo, tbo, nbo = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(v)*4, v, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, tbo)
    glBufferData(GL_ARRAY_BUFFER, len(t)*4, t, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, nbo)
    glBufferData(GL_ARRAY_BUFFER, len(n)*4, n, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo, tbo, nbo

if __name__ == "__main__":
    #First, we create the window and set some rendering parameters.
    width = 800
    height = 600
    window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Shadow Mapping Test")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_CULL_FACE)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glPointSize(5.0)
    shadowMapSize = 512
    
    rotation = 0
    lightPos = (60, 90, 50)
    lightDir = np.negative(lightPos)
    lightColor = (1.0, 1.0, 1.0)
    lightInnerAngle = 20
    lightOuterAngle = 30
    cameraPos = (0, 300, 400)
    
    v, t, n = loadAA7("blockworld.aa7")
    vbo, tbo, nbo = createMeshBuffers(v, t, n)
    shadowMapShader = Shader("shadowMap.vert", "shadowMap.frag")
    shadowMapShader.compile()
    displayShader = Shader("display.vert", "display.frag")
    displayShader.compile()
    
    rendertarget = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, rendertarget)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, shadowMapSize, shadowMapSize, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, rendertarget, 0)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        rotation += 1.0
        
        """
        Pass 1: Render to Texture
        This renders the scene offscreen from the light's POV to a framebuffer.
        The linearized depth is stored in our previously bound depth texture.
        """
        shadowMapShader.enable()
        glCullFace(GL_FRONT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 1, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        params = list(lightPos) + [0, 0, 0] + [0, 1, 0]
        gluLookAt(*params)
        #We do not do the rotation here as the scene is not rotating RELATIVE to the light
        lightProj = glGetFloatv(GL_PROJECTION_MATRIX).flatten()
        lightView = glGetFloatv(GL_MODELVIEW_MATRIX).flatten()
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        glViewport(0, 0, shadowMapSize, shadowMapSize)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, vbo); glVertexPointer(3, GL_FLOAT, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDrawArrays(GL_TRIANGLES, 0, len(v)//3)
        glDisableClientState(GL_VERTEX_ARRAY)
        shadowMapShader.disable()
        
        """
        Pass 2: Render the scene with shadows
        This pass renders the scene onscreen from the camera's POV.
        It passes shadow and light info to the shaders for the depth comparison and spotlight calculations respectively.
        """
        glCullFace(GL_BACK)
        bias = [0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.5, 0.5, 0.5, 1.0]
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(bias)
        glMultMatrixf(lightProj)
        glMultMatrixf(lightView)
        biasMVPMatrix = glGetFloatv(GL_MODELVIEW_MATRIX).flatten()
        glViewport(0, 0, width, height)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30, float(800)/600, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        params = list(cameraPos) + [0, 0, 0] + [0, 1, 0]
        gluLookAt(*params)
        glRotate(rotation, 0, 1, 0)
        cameraProj = glGetFloatv(GL_PROJECTION_MATRIX).flatten()
        cameraView = glGetFloatv(GL_MODELVIEW_MATRIX).flatten()
        displayShader.enable()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, rendertarget)
        displayShader.setUniform("u_modelTexture", "sampler2D", 0)
        displayShader.setUniform("u_shadowMap", "sampler2D", 1)
        displayShader.setUniform("u_biasMVPMatrix", "mat4", biasMVPMatrix)
        displayShader.setUniform("u_light.color", "vec3", lightColor)
        displayShader.setUniform("u_light.direction", "vec3", lightDir)
        displayShader.setUniform("u_light.position", "vec3", lightPos)
        displayShader.setUniform("u_light.innerAngle", "float", lightInnerAngle)
        displayShader.setUniform("u_light.outerAngle", "float", lightOuterAngle)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, vbo); glVertexPointer(3, GL_FLOAT, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, tbo); glTexCoordPointer(2, GL_FLOAT, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, nbo); glNormalPointer(GL_FLOAT, 0, None)
        glDrawArrays(GL_TRIANGLES, 0, len(v)//3)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        displayShader.disable()
        
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixf(cameraProj)
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(cameraView)
        glBegin(GL_POINTS)
        glColor3f(*lightColor)
        glVertex3f(*lightPos)
        glEnd()

        pygame.display.flip()
        clock.tick(60)