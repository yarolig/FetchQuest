#version 330

in vec3 in_vert;
in vec3 in_color;
out vec3 v_color;

void main() {
    v_color = in_color;
    gl_Position = vec4(in_vert, 1.0);
}