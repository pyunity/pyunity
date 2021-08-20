#version 330 core
in vec2 TexCoord;
in vec3 FragPos;

out vec4 color;

uniform sampler2D image;

void main() {
    color = texture(image, TexCoord);
}