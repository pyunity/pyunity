#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

// out vec4 gl_Position;
out vec2 TexCoord;
out vec3 normal;
out vec3 FragPos;

void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
    normal = vec3(transpose(inverse(mat3(model))) * aNormal);
    FragPos = vec3(model * vec4(aPos, 1.0));
}