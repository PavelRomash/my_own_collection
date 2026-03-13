#!/usr/bin/python

# Copyright: (c) 2024, Your Name <your.email@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Модуль для создания текстового файла на удаленном хосте

version_added: "1.0.0"

description: Этот модуль создает текстовый файл по указанному пути с заданным содержимым на удаленном хосте.

options:
    path:
        description: Путь для создания файла на удаленном хосте
        required: true
        type: str
    content:
        description: Содержимое, которое будет записано в файл
        required: true
        type: str
    force:
        description: Принудительная перезапись файла, если он уже существует
        required: false
        type: bool
        default: false

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Создать файл с содержимым
- name: Create a file with content
  my_own_module:
    path: /tmp/myfile.txt
    content: "Hello, World!"

# Создать файл с принудительной перезаписью
- name: Create a file with force overwrite
  my_own_module:
    path: /tmp/myfile.txt
    content: "New content"
    force: true
'''

RETURN = r'''
path:
    description: Путь к созданному/измененному файлу
    type: str
    returned: always
    sample: '/tmp/myfile.txt'
content:
    description: Содержимое, которое было записано
    type: str
    returned: always
    sample: 'Hello, World!'
size:
    description: Размер файла в байтах
    type: int
    returned: when file exists
    sample: 13
'''

import os
from ansible.module_utils.basic import AnsibleModule

def write_file(module, path, content):
    """
    Функция для записи содержимого в файл
    """
    try:
        # Создаем директорию, если её нет
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, mode=0o755)
        
        # Записываем содержимое в файл
        with open(path, 'w') as f:
            f.write(content)
        
        # Устанавливаем права на файл
        os.chmod(path, 0o644)
        
        return True, None
    except Exception as e:
        return False, str(e)

def file_exists_and_different(path, content):
    """
    Проверяет, существует ли файл и отличается ли его содержимое
    """
    if not os.path.exists(path):
        return False, True  # Файл не существует, нужно создавать
    
    try:
        with open(path, 'r') as f:
            existing_content = f.read()
        return True, existing_content != content
    except:
        return True, True  # Если не можем прочитать, считаем что отличается

def run_module():
    # Определяем аргументы модуля
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        force=dict(type='bool', required=False, default=False)
    )

    # Инициализируем результат
    result = dict(
        changed=False,
        path='',
        content='',
        size=0
    )

    # Создаем объект модуля
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Получаем параметры
    path = module.params['path']
    content = module.params['content']
    force = module.params['force']

    # Проверяем состояние файла
    exists, different = file_exists_and_different(path, content)

    # Определяем, нужно ли что-то делать
    if not exists:
        # Файл не существует - нужно создавать
        result['changed'] = True
    elif different:
        # Файл существует, но содержимое отличается
        result['changed'] = True
    else:
        # Файл существует и содержимое совпадает
        result['changed'] = False

    # Если это check mode, просто возвращаем результат
    if module.check_mode:
        module.exit_json(**result)

    # Если изменений не требуется, выходим
    if not result['changed']:
        # Получаем размер файла для информации
        try:
            result['size'] = os.path.getsize(path)
        except:
            pass
        module.exit_json(**result)

    # Если файл существует, но force=false, и содержимое отличается - ошибка
    if exists and different and not force:
        module.fail_json(
            msg=f"Файл {path} уже существует и его содержимое отличается. "
                f"Используйте force=true для перезаписи.",
            **result
        )

    # Записываем файл
    success, error_msg = write_file(module, path, content)
    
    if not success:
        module.fail_json(msg=f"Не удалось создать файл: {error_msg}", **result)

    # Получаем информацию о созданном файле
    try:
        result['size'] = os.path.getsize(path)
    except:
        pass

    result['path'] = path
    result['content'] = content

    # Успешное завершение
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()