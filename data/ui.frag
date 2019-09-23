#version 130

in vec3 v_color;
in vec2 v_tex;
uniform sampler2D sampler;
out vec3 f_color;

void main() {
    if (texture(sampler, v_tex).z > 0.1) {
        f_color = v_color + texture(sampler, v_tex).xyz;
    } else {
        discard;
    }
}