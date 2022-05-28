#version 330 core
layout (location = 0) in vec2 aPos;

uniform mat4 projection;
uniform mat4 model;
uniform float depth;
uniform int flipX;
uniform int flipY;

out vec2 TexCoord;
out vec3 FragPos;

void main() {
    gl_Position = projection * model * vec4(aPos, 0.0, depth);
    TexCoord = aPos;
    TexCoord *= 1 - vec2(flipX, flipY) * 2;
}
