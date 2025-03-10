import os

project_dir = "ollamatrans_gui"
main_file = os.path.join(project_dir, "main.py")
epub_parser_file = os.path.join(project_dir, "files_parser.py")
translator_file = os.path.join(project_dir, "ollama_translator.py")

if not os.path.exists(project_dir):
    os.makedirs(project_dir)

with open(main_file, "w") as f:
    pass

with open(epub_parser_file, "w") as f:
    pass

with open(translator_file, "w") as f:
    pass