# Python Modules

# 3rd Party Modules
from livereload import Server, shell

# Project Modules


if __name__ == '__main__':
    server = Server()
    server.watch('../README.md.rst', shell('make html'), delay=1)
    server.watch('source/*.rst', shell('make html'), delay=1)
    server.watch('source/*.md', shell('make html'), delay=1)
    server.watch('source/*.py', shell('make html'), delay=1)
    server.watch('source/_static/*', shell('make html'), delay=1)
    server.watch('source/_templates/*', shell('make html'), delay=1)
    server.serve(root='build/html')
