from pathlib import Path
import shutil
from send2trash import send2trash

PROJECTS_DIR = Path.home() / "AtlasProjects"

PROJECTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def resolve_path(path: str) -> Path:

    path = path.strip()

    shortcuts = {
        "desktop": Path.home() / "Desktop",
        "downloads": Path.home() / "Downloads",
        "documents": Path.home() / "Documents",
        "pictures": Path.home() / "Pictures",
        "home": Path.home(),
        "projects": PROJECTS_DIR
    }

    if path.lower() in shortcuts:
        return shortcuts[path.lower()]

    return Path(path).expanduser()


def build_target(path, name=""):

    base = resolve_path(path)

    if name:
        return base / name

    return base


# ==========================
# ACTIONS
# ==========================

def create_folder(path, name=""):

    target = build_target(path, name)

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    return f"Created folder: {target}"


def create_file(
    path,
    name="",
    content=""
):

    target = build_target(path, name)

    target.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    target.write_text(
        content,
        encoding="utf-8"
    )

    return f"Created file: {target}"


def delete(path, name=""):

    target = build_target(path, name)

    if not target.exists():
        return "File or folder not found"

    send2trash(str(target))

    return f"Moved to recycle bin: {target}"


def read_file(
    path,
    name=""
):

    target = build_target(path, name)

    if not target.exists():
        return "File not found"

    return target.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def write_file(
    path,
    name="",
    content="",
    append=False
):

    target = build_target(path, name)

    target.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    mode = "a" if append else "w"

    with open(
        target,
        mode,
        encoding="utf-8"
    ) as file:

        file.write(content)

    return f"Written to: {target}"


def rename(
    path,
    name="",
    new_name=""
):

    target = build_target(path, name)

    if not target.exists():
        return "File not found"

    new_path = target.parent / new_name

    target.rename(new_path)

    return f"Renamed to: {new_name}"


def move(source, destination):

    src = resolve_path(source)
    dst = resolve_path(destination)

    dst.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.move(
        str(src),
        str(dst)
    )

    return "Move successful"


def copy(source, destination):

    src = resolve_path(source)
    dst = resolve_path(destination)

    dst.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if src.is_file():

        shutil.copy2(
            src,
            dst
        )

    else:

        shutil.copytree(
            src,
            dst,
            dirs_exist_ok=True
        )

    return "Copy successful"


def list_files(
    path
):

    target = resolve_path(path)

    if not target.exists():
        return "Path not found"

    files = []

    for item in target.iterdir():

        if item.is_dir():

            files.append(
                f"📁 {item.name}"
            )

        else:

            files.append(
                f"📄 {item.name}"
            )

    return "\n".join(files)


def find_files(path, keyword):

    target = resolve_path(path)

    if not target.exists():
        return "Path not found"

    results = []

    for item in target.rglob("*"):

        if keyword.lower() in item.name.lower():

            results.append(
                str(item)
            )

    if not results:
        return "No files found"

    return "\n".join(
        results[:50]
    )

def file_info(
    path,
    name=""
):

    target = build_target(path, name)

    if not target.exists():
        return "Not found"

    stat = target.stat()

    return (
        f"Name: {target.name}\n"
        f"Type: {'Folder' if target.is_dir() else 'File'}\n"
        f"Size: {stat.st_size} bytes\n"
        f"Location: {target.parent}"
    )


# ==========================
# DISPATCHER
# ==========================

ACTIONS = {

    "create_file": create_file,
    "create_folder": create_folder,

    "delete": delete,

    "read": read_file,
    "write": write_file,

    "rename": rename,

    "move": move,
    "copy": copy,

    "list": list_files,

    "find": find_files,

    "info": file_info
}


def file_controller(parameters: dict):

    params = parameters.copy()

    action = params.pop(
        "action",
        ""
    ).lower()

    func = ACTIONS.get(action)

    if not func:

        return f"Unknown action: {action}"

    try:

        return func(**params)

    except Exception as e:

        return f"File Controller Error: {e}"