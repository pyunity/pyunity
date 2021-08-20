#version 330 core
layout (location = 0) in vec2 aPos;

uniform mat4 projection;
uniform mat4 position;

out vec2 TexCoord;
out vec3 FragPos;

void main() {
    gl_Position = projection * position * vec4(aPos, 0.0, 1.0);
    TexCoord = aPos;
}
