#version 330 core
out vec4 FragColor;
in vec2 TexCoord;
in vec3 normal;
in vec3 FragPos;

struct Light {
    vec3 pos;
    float strength;
    vec3 color;
    vec3 dir;
    int type;
};

#define NR_LIGHTS 8
uniform int light_num;
uniform Light lights[NR_LIGHTS];
uniform vec3 viewPos;
uniform vec3 objectColor;
uniform sampler2D aTexture;
uniform int textured = 0;

float getDiffuse(Light light, vec3 norm) {
    if (light.type == 0) {
        light.dir = normalize(light.pos - FragPos);
    }
    float diffuse = max(dot(norm, light.dir), 0.0);
    return diffuse;
}

float getSpecular(Light light, vec3 norm) {
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 halfwayDir = normalize(light.dir + viewDir);
    float spec = pow(max(dot(norm, halfwayDir), 0.0), 16.0);
    float specular = specularStrength * spec;
    return specular;
}

float getAttenuation(Light light) {
    float linear = 5 / light.strength;
    float quad = 70 / (light.strength * light.strength);
    float distance = length(light.pos - FragPos);
    float attenuation = 1.0 / (1.0 + distance * (linear + quad * distance));
    return attenuation;
}

void main() {
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * vec3(1.0, 1.0, 1.0);
    vec3 norm = normalize(normal);

    vec3 total;
    for (int i = 0; i < light_num; i++) {
        float strength = getDiffuse(lights[i], norm);
        if (lights[i].type == 0) {
            strength += getSpecular(lights[i], norm);
            strength *= getAttenuation(lights[i]);
        }
        total += strength * lights[i].color;
    }

    total += ambient;
    vec3 result = total * objectColor;
    if (textured != 0) {
        FragColor = texture(aTexture, TexCoord) * vec4(result, 1.0);
    } else {
        FragColor = vec4(result, 1.0);
    }
}
