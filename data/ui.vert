#version 130

in vec2 in_vert;
in vec2 in_tex;
in vec3 in_color;

uniform vec2 u_pos;
uniform vec2 u_size;

out vec3 v_color;
out vec2 v_tex;

void main() {
    v_color = in_color.xyy;
    v_tex = in_tex.xy;
    gl_Position = vec4(u_pos.xy+in_vert.xy*u_size.xy, 0.0, 1.0);
}