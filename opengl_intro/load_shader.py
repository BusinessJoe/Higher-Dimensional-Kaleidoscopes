from OpenGL.GL import *
from OpenGL.GL import shaders


class Shader:
    def __init__(self, vertex_file_path, fragment_file_path):
        self.shader = None

        self._load_shaders(vertex_file_path, fragment_file_path)

    def use(self):
        glUseProgram(self.shader)

    def _load_shaders(self, vertex_file_path, fragment_file_path):
        with open(vertex_file_path) as f:
            vertex_source = f.read()
        with open(fragment_file_path) as f:
            fragment_source = f.read()

        self._compile_shaders(vertex_source, fragment_source)

    def _compile_shaders(self, vertex_source, fragment_source):
        # Compile vertex shader
        vertex_shader = shaders.compileShader(vertex_source, GL_VERTEX_SHADER)

        # Check vertex shader

        # Compile fragment shader
        fragment_shader = shaders.compileShader(fragment_source, GL_FRAGMENT_SHADER)

        # Check fragment shader

        # Link the program
        program = shaders.compileProgram(vertex_shader, fragment_shader)

        # glDetachShader(program, vertex_shader)
        # glDetachShader(program, fragment_shader)
        # glDeleteShader(vertex_shader)
        # glDeleteShader(fragment_shader)

        self.shader = program

    def set_vec3(self, name, x, y, z):
        glUniform3f(glGetUniformLocation(self.shader, name), x, y, z)

    def set_vec3v(self, name, v):
        glUniform3fv(glGetUniformLocation(self.shader, name), 1, v)

    def set_mat4(self, name, m):
        glUniformMatrix4fv(glGetUniformLocation(self.shader, name), 1, GL_FALSE, m)