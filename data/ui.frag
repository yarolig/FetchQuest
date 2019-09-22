#version 330

in vec3 v_color;
in vec2 v_tex;
uniform sampler2D sampler;
out vec3 f_color;

void main() {
    f_color = v_color + texture(sampler, v_tex).xyz;
}