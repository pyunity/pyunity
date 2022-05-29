#version 330 core
layout (location = 0) in vec2 aPos;

uniform mat4 projection;
uniform mat4 model;
uniform float depth = 0.0;
uniform int flipX;
uniform int flipY;

out vec3 TexCoord;

void main() {
    gl_Position = projection * model * vec4(aPos, 0.0, 0.5);
    vec2 coords = aPos * (1 - vec2(flipX, flipY) * 2);
    TexCoord = vec3(coords, 0.5 - depth / 2.0);
}
