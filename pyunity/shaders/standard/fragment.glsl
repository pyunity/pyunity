#version 330 core
#define NR_LIGHTS 8
layout (location = 0) out vec4 FragColor;

in vec2 TexCoord;
in vec3 normal;
in vec3 FragPos;
in vec4 FragPosLightSpaces[NR_LIGHTS];

struct Light {
    vec3 pos;
    float strength;
    vec3 color;
    vec3 dir;
    int type;
};

uniform int light_num;
uniform Light lights[NR_LIGHTS];
uniform vec3 viewPos;
uniform vec3 objectColor;
uniform sampler2D aTexture;
uniform sampler2DShadow shadowMaps[NR_LIGHTS];
uniform int textured = 0;
uniform int useShadowMap = 1;

float getDiffuse(Light light, vec3 norm) {
    if (light.type == 0) {
        light.dir = normalize(FragPos - light.pos);
    }
    float diffuse = max(-dot(norm, light.dir), 0.0);
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

float getShadow(int num, sampler2DShadow tex) {
    // perform perspective divide
    vec3 projCoords = FragPosLightSpaces[num].xyz / FragPosLightSpaces[num].w;
    // transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;

    if (projCoords.z > 1.0) {
        return 0.0;
    }

    // get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    // check whether current frag pos is in shadow
    float bias = max(0.05 * (1.0 - dot(normal, lights[num].dir)), 0.005);

    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(tex, 0);
    const int halfkernelWidth = 2;
    for (int x = -halfkernelWidth; x <= halfkernelWidth; ++x) {
        for (int y = -halfkernelWidth; y <= halfkernelWidth; ++y) {
            vec2 posXY = projCoords.xy + vec2(x, y) * texelSize;
            // Query depth as z coord
            vec3 pos = vec3(posXY, currentDepth - bias);
            shadow += 1.0 - texture(tex, pos);
        }
    }
    shadow /= ((halfkernelWidth*2+1)*(halfkernelWidth*2+1));

    return shadow;
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
        float shadow = (useShadowMap == 1) ? getShadow(i, shadowMaps[i]) : 0.0;
        // if (shadow == 0.0) discard;
        total += (1.0 - shadow) * strength * lights[i].color;
    }

    total += ambient;
    vec3 result = total * objectColor;
    if (textured != 0) {
        FragColor = texture(aTexture, TexCoord) * vec4(result, 1.0);
    } else {
        FragColor = vec4(result, 1.0);
    }
}
