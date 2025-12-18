from src.webpage_server import cp_static_to_public, generate_page, generate_pages_recursively
def main():
    cp_static_to_public("static", "public")
    generate_pages_recursively("content", "content/template.html", "public")

if __name__ == "__main__":
    main()