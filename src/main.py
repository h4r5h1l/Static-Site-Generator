import os
import shutil
def main():
    def cp_static_to_public(static_path, public_path):
        for dir_file in os.listdir(public_path):
            path = os.path.join(public_path, dir_file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                print(f"Error removing {path}: {e}")
        for dir_file in os.listdir(static_path):
            src_path = os.path.join(static_path, dir_file)
            dest_path = os.path.join(public_path, dir_file)
            try:
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied {src_path} to {dest_path}")
                elif os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path)
                    print(f"Copied directory {src_path} to {dest_path}")
            except Exception as e:
                print(f"Error copying {src_path} to {dest_path}: {e}")
        
    cp_static_to_public("static", "public")

if __name__ == "__main__":
    main()