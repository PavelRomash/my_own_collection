# Yandex Cloud ELK Collection

Коллекция Ansible для работы с Yandex Cloud и ELK stack.

## Установка

```bash
ansible-galaxy collection install my_own_namespace.yandex_cloud_elk-1.0.0.tar.gz
Модули
my_own_module
Создает текстовый файл на удаленном хосте.

Параметры:

path (обязательный) - путь для создания файла

content (обязательный) - содержимое файла

force (опциональный, default: false) - принудительная перезапись

Пример:

yaml
- name: Create file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/example.txt
    content: "Hello World"
    force: true
Роль file_creator
Переменные:

file_path - путь к файлу (default: "/tmp/default_file.txt")

file_content - содержимое файла (default: "Default content from role")

force_overwrite - принудительная перезапись (default: false)

display_result - показывать результат (default: true)

Пример использования:

yaml
- hosts: localhost
  roles:
    - role: file_creator
      file_path: "/tmp/test.txt"
      file_content: "Test content"
