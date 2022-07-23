#version 330 core
#define NR_LIGHTS 8
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoord;

uniform int numLights;
uniform mat4 projection;
uniform mat3 normModel;
uniform mat4 view;
uniform mat4 model;
uniform mat4 lightSpaceMatrices[NR_LIGHTS];

out vec2 TexCoord;
out vec3 normal;
out vec3 FragPos;
out vec4 FragPosLightSpaces[NR_LIGHTS];

void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
    normal = vec3(normModel * aNormal);
    FragPos = vec3(model * vec4(aPos, 1.0));

    for (int i = 0; i < numLights; i++) {
        FragPosLightSpaces[i] = lightSpaceMatrices[i] * vec4(FragPos, 1.0);
    }
}
