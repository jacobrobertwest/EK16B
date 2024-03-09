import sys
from array import array

import pygame
import moderngl

pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

screen = pygame.display.set_mode((500, 500), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((500, 500))

ctx = moderngl.create_context()

clock = pygame.time.Clock()

img = pygame.image.load('img3.jpg')

quad_buffer = ctx.buffer(data=array('f', [
    # position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,   # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    // Calculate the rotation angle based on time
    float angle = time * 0.02; // Adjust the coefficient to control the rotation speed

    // Calculate the center of the texture
    vec2 center = vec2(0.5, 0.5);

    // Translate the texture coordinates so that the center of the texture becomes the origin
    vec2 translatedUVs = uvs - center;

    // Calculate the rotation matrix
    mat2 rotationMatrix = mat2(cos(angle), sin(angle), -sin(angle), cos(angle));

    // Apply the rotation
    vec2 sample_pos = rotationMatrix * translatedUVs;

    // Translate the rotated coordinates back
    sample_pos += center;

    // Sample the texture at the rotated coordinates
    vec4 tex_color = texture(tex, sample_pos);

    // Output the final color
    float greenshift = cos(time * 0.003);
    float blueshift = sin(time * 0.006);
    float redshift = cos(time * 0.010);
    f_color = vec4(texture(tex, sample_pos).r * redshift, texture(tex, sample_pos).g * greenshift, texture(tex, sample_pos).b * blueshift, 1.0);
}
'''

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

t = 0

while True:
    display.fill((0, 0, 0))
    display.blit(img, (0,0))
    
    t += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    frame_tex = surf_to_texture(display)
    frame_tex.use(0)
    program['tex'] = 0
    program['time'] = t
    render_object.render(mode=moderngl.TRIANGLE_STRIP)
    
    pygame.display.flip()
    
    frame_tex.release()
    
    clock.tick(60)
    