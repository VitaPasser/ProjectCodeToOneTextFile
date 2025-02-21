import configparser
import json
import os.path

config = configparser.ConfigParser()
config.read('settings.ini')

txt_ext: list[str] = json.loads(config['PROJECT']['EXTENSIONS_FILES'])
exclude: list[str] = json.loads(config['PROJECT']['EXCLUDE'])

def get_content_from_files(path, here_path='./'):
    list_files_and_dirs = []
    for x in os.listdir(path):
        name, ext = os.path.splitext(x)
        if '.' == name[0] and name not in txt_ext:
            continue
        if ext == '' and x not in exclude:
            for [xx, here_path_] in get_content_from_files(f'{path}/{name}', f'{here_path}/{name}/'):
                yield [xx, here_path_]
        if ext[1:] in txt_ext and x not in exclude:
            yield [x, here_path]
            list_files_and_dirs.append(x)

    # return list_files_and_dirs
    # print(list_files_and_dirs)

# print(get_content_from_files(config['PROJECT']['PROJECT_PATH']))

with open(config['PROJECT']['OUTPUT_FILE_NAME'], 'wt') as output_file:
    for [filename, current_path] in get_content_from_files(config['PROJECT']['PROJECT_PATH']):
        path = f'{current_path}{filename}'.replace('//', '/')
        output_file.write(f'{path}\n') # Write file title with path
        with open(f'{config["PROJECT"]["PROJECT_PATH"]}/{path[1:]}', 'rt') as read_file:
            output_file.write(read_file.read()) # Write file content
            output_file.write('\n\n\n') # Write file content

