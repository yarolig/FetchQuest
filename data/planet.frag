#version 130

in vec2 v_tex;
uniform sampler2D sampler;
out vec3 f_color;

void main() {
    f_color = texture(sampler, v_tex).xyz;
}