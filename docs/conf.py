project = "pyunity"
copyright = "2020, Ray Chen"
author = "Ray Chen"

master_doc = "index"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]

language = "en"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"

html_static_path = ["_static"]

todo_include_todos = True

autodoc_mock_imports = ["OpenGL", "glfw", "pygame"]