#version 330 core
out vec4 FragColor;
in vec2 TexCoord;
in vec3 normal;
in vec3 FragPos;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 objectColor;
uniform vec3 lightColor;
uniform sampler2D aTexture;
uniform int textured = 0;
uniform int lighting = 1;
uniform float lightDistance = 1f;

void main() {
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor;
    vec3 result;
    if (lighting == 0) {
        result = ambient * objectColor;
    } else {
        vec3 norm = normalize(normal);
        vec3 lightDir = normalize(lightPos - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * lightColor;

        float specularStrength = 0.5;
        vec3 viewDir = normalize(viewPos - FragPos);
        // vec3 reflectDir = reflect(-lightDir, norm);
        // float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 halfwayDir = normalize(lightDir + viewDir);
        float spec = pow(max(dot(norm, halfwayDir), 0.0), 16.0);
        vec3 specular = specularStrength * spec * lightColor;

        // float strength;
        // if (length(lightDir) < (lightDistance - 1f)) {
        //     strength = 1f;
        // } else {
        //     strength = 1f / pow((length(lightDir) - lightDistance + 1f), 2.1f);
        // }
        result = (ambient + diffuse + specular) * objectColor;
    }
    if (textured != 0) {
        FragColor = texture(aTexture, TexCoord) * vec4(result, 1.0);
    } else {
        FragColor = vec4(result, 1.0);
    }
}
