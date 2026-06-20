import shutil
from pathlib import Path


def file_manager(parameters: dict) -> str:
    """
    Actions:
        create_file
        create_folder
        delete_file
        delete_folder
        rename
        move
        copy
        list_files
    """

    action = parameters.get("action", "").lower()

    try:

        # CREATE FILE
        if action == "create_file":
            path = Path(parameters["path"]).expanduser()

            path.parent.mkdir(parents=True, exist_ok=True)

            content = parameters.get("content", "")

            path.write_text(content, encoding="utf-8")

            return f"Created file: {path}"

        # CREATE FOLDER
        elif action == "create_folder":
            path = Path(parameters["path"]).expanduser()

            path.mkdir(parents=True, exist_ok=True)

            return f"Created folder: {path}"

        # DELETE FILE
        elif action == "delete_file":
            path = Path(parameters["path"]).expanduser()

            if path.exists():
                path.unlink()

                return f"Deleted file: {path}"

            return "File not found"

        # DELETE FOLDER
        elif action == "delete_folder":
            path = Path(parameters["path"]).expanduser()

            if path.exists():
                shutil.rmtree(path)

                return f"Deleted folder: {path}"

            return "Folder not found"

        # RENAME
        elif action == "rename":
            old_path = Path(parameters["old_path"]).expanduser()
            new_path = Path(parameters["new_path"]).expanduser()

            old_path.rename(new_path)

            return f"Renamed to: {new_path}"

        # MOVE
        elif action == "move":
            source = Path(parameters["source"]).expanduser()
            destination = Path(parameters["destination"]).expanduser()

            shutil.move(str(source), str(destination))

            return f"Moved {source} → {destination}"

        # COPY
        elif action == "copy":
            source = Path(parameters["source"]).expanduser()
            destination = Path(parameters["destination"]).expanduser()

            if source.is_file():
                shutil.copy2(source, destination)
            else:
                shutil.copytree(source, destination)

            return f"Copied {source} → {destination}"

        # LIST FILES
        elif action == "list_files":
            path = Path(parameters["path"]).expanduser()

            if not path.exists():
                return "Path not found"

            items = [item.name for item in path.iterdir()]

            return "\n".join(items)

        return f"Unknown action: {action}"

    except Exception as e:
        return f"File Manager Error: {e}"