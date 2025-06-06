import configparser
import json
from pathlib import Path

config = configparser.ConfigParser()
config.read("settings.ini")

txt_ext = json.loads(config["PROJECT"]["EXTENSIONS_FILES"])
exclude = json.loads(config["PROJECT"]["EXCLUDE"])


def get_content_from_files(current_dir: Path, base_dir: Path):
    for item in current_dir.iterdir():
        if item.name in exclude:
            continue

        if item.is_dir():
            yield from get_content_from_files(item, base_dir)
        elif item.is_file():
            if item.name.startswith(".") and item.suffix[1:] not in txt_ext:
                continue

            if item.suffix[1:] in txt_ext:
                relative_path = item.relative_to(base_dir)
                yield item, relative_path


project_root_path = Path(config["PROJECT"]["PROJECT_PATH"])

if not project_root_path.exists():
    print(
        f"Error: Project path '{project_root_path}' does not exist. Please check your settings.ini file."
    )
else:
    output_file_name = Path(config["PROJECT"]["OUTPUT_FILE_NAME"])

    try:
        with open(output_file_name, "wt", encoding="utf-8") as output_file:
            for full_path, relative_path in get_content_from_files(
                project_root_path, project_root_path
            ):
                file_content = ""
                try:
                    with open(full_path, "rt", encoding="utf-8") as read_file:
                        file_content = read_file.read()
                except UnicodeDecodeError:
                    output_file.write(
                        f"// WARNING: Could not decode content for {relative_path} (not UTF-8 compatible?)\n"
                    )
                    continue
                except Exception as e:
                    output_file.write(
                        f"// ERROR: Could not read file {relative_path}: {e}\n"
                    )
                    continue

                if file_content.strip():
                    output_file.write(f"{relative_path}\n")
                    output_file.write(file_content)
                    output_file.write("\n\n\n")
                else:
                    print(f"Ignoring empty file: {relative_path}")

        print(f"Content successfully written to '{output_file_name}'")
    except Exception as e:
        print(f"Error writing to output file '{output_file_name}': {e}")
