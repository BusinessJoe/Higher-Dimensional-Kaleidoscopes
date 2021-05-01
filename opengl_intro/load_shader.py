from OpenGL.GL import *
from OpenGL.GL import shaders


class Shader:
    def __init__(self, vertex_file_path, fragment_file_path):
        self.vertex_source = None
        self.fragment_source = None
        self.program = None
        self._load_shaders(vertex_file_path, fragment_file_path)

    def use(self):
        return self._compile_shaders()

    def _load_shaders(self, vertex_file_path, fragment_file_path):
        with open(vertex_file_path) as f:
            self.vertex_source = f.read()

        with open(fragment_file_path) as f:
            self.fragment_source = f.read()

    def _compile_shaders(self):
        # Compile vertex shader
        vertex_shader = shaders.compileShader(self.vertex_source, GL_VERTEX_SHADER)

        # Check vertex shader

        # Compile fragment shader
        fragment_shader = shaders.compileShader(self.fragment_source, GL_FRAGMENT_SHADER)

        # Check fragment shader

        # Link the program
        program = shaders.compileProgram(vertex_shader, fragment_shader)

        glDetachShader(program, vertex_shader)
        glDetachShader(program, fragment_shader)

        # glDeleteShader(vertex_shader)
        # glDeleteShader(fragment_shader)

        self.program = program
        return program
