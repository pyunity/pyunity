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

uniform int numLights;
uniform Light lights[NR_LIGHTS];
uniform vec3 viewPos;
uniform vec3 objectColor;
uniform sampler2D aTexture;
uniform sampler2DShadow shadowMaps[NR_LIGHTS];
uniform int textured = 0;
uniform int useShadowMap = 1;

float when_eq(float x, float y) {
    return 1.0 - abs(sign(x - y));
}

float when_neq(float x, float y) {
    return abs(sign(x - y));
}

float when_eq_val(float x, float y, float a, float b) {
    return when_eq(x, y) * a + when_neq(x, y) * b;
}

vec4 when_eq_val(float x, float y, vec4 a, vec4 b) {
    return when_eq(x, y) * a + when_neq(x, y) * b;
}

float when_gt(float x, float y) {
    return max(sign(x - y), 0.0);
}

float when_le(float x, float y) {
    return 1.0 - when_gt(x, y);
}

float getDiffuse(Light light, vec3 norm) {
    light.dir = when_neq(light.type, 0) * light.dir;
    light.dir += when_eq(light.type, 0) * normalize(FragPos - light.pos);
    float diffuse = max(-dot(norm, light.dir), 0.0);
    return diffuse;
}

float getSpecular(Light light, vec3 norm) {
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 halfwayDir = normalize(normalize(light.dir) + viewDir);
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

    return shadow * when_le(projCoords.z, 1.0);
}

void main() {
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * vec3(1.0, 1.0, 1.0);
    vec3 norm = normalize(normal);

    float shadows[NR_LIGHTS];

    #if __VERSION__ > 400
    for (int i = 0; i < NR_LIGHTS; i++) {
        shadows[i] = (useShadowMap == 1) ? getShadow(i, shadowMaps[i]) : 0.0;
    }
    #else
    shadows[0] = (useShadowMap == 1) ? getShadow(0, shadowMaps[0]) : 0.0;
    shadows[1] = (useShadowMap == 1) ? getShadow(1, shadowMaps[1]) : 0.0;
    shadows[2] = (useShadowMap == 1) ? getShadow(2, shadowMaps[2]) : 0.0;
    shadows[3] = (useShadowMap == 1) ? getShadow(3, shadowMaps[3]) : 0.0;
    shadows[4] = (useShadowMap == 1) ? getShadow(4, shadowMaps[4]) : 0.0;
    shadows[5] = (useShadowMap == 1) ? getShadow(5, shadowMaps[5]) : 0.0;
    shadows[6] = (useShadowMap == 1) ? getShadow(6, shadowMaps[6]) : 0.0;
    shadows[7] = (useShadowMap == 1) ? getShadow(7, shadowMaps[7]) : 0.0;
    #endif

    vec3 total = vec3(0);
    for (int i = 0; i < NR_LIGHTS; i++) {
        if (i == numLights) {
            break;
        }
        float strength = getDiffuse(lights[i], norm);
        strength += when_eq(lights[i].type, 0) * getSpecular(lights[i], norm);
        strength *= when_eq_val(lights[i].type, 0, getAttenuation(lights[i]), 1.0);
        float shadow = shadows[i];
        // if (shadow == 0.0) discard;
        total += (1.0 - shadow) * strength * lights[i].color;
    }

    total += ambient;
    vec3 result = total * objectColor;

    FragColor = vec4(result, 1.0);
    FragColor *= when_eq_val(textured, 1, texture(aTexture, TexCoord), vec4(1, 1, 1, 1));
}
