#version 130

in vec2 v_tex;
in vec3 v_pos;
uniform sampler2D sampler;
out vec3 f_color;

void main() {
    f_color = texture(sampler, v_tex, -1.0).xyz * vec3(1.0, 1.0, 1.0 - v_pos.z * 0.003);
}