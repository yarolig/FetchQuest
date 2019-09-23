#version 130

in vec3 in_vert;
uniform mat4 u_proj;
uniform mat4 u_view;

out vec2 v_tex;

void main() {
    vec4 view_pos = u_view * vec4(in_vert, 1.0) ;
    v_tex = in_vert.xy * 0.1;
    gl_Position = u_proj * view_pos;
}