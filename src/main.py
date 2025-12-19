import sys
from .webpage_server import generate_pages_recursively, cp_static_to_public

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    cp_static_to_public("static", "docs")
    generate_pages_recursively(basepath, "content", "content/template.html", "docs")

if __name__ == "__main__":
    main()