from OpenGL.GL import *
from OpenGL.GL import shaders


def load_shaders(vertex_file_path, fragment_file_path):
    with open(vertex_file_path) as f:
        vertex_source = f.read()

    with open(fragment_file_path) as f:
        fragment_source = f.read()

    # Compile vertex shader
    vertex_shader = shaders.compileShader(vertex_source, GL_VERTEX_SHADER)

    # Check vertex shader

    # Compile fragment shader
    fragment_shader = shaders.compileShader(fragment_source, GL_FRAGMENT_SHADER)

    # Check fragment shader

    # Link the program
    program = shaders.compileProgram(vertex_shader, fragment_shader)

    glDetachShader(program, vertex_shader)
    glDetachShader(program, fragment_shader)

    # glDeleteShader(vertex_shader)
    # glDeleteShader(fragment_shader)

    return program
