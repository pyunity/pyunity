#version 330 core
in vec3 TexCoord;

out vec4 color;

uniform sampler2D image;

void main() {
    color = texture(image, TexCoord.xy);
    if (color.a < 0.1) {
        discard;
    }
    gl_FragDepth = TexCoord.z;
}
