# **Create Module Command**
This command helps you create an Ellar project module, like a small app within a project.
It depends on the existence of an Ellar project.

```shell
ellar create-module my_project_module directory
```
for example:
```shell
ellar create-module my_project_module apps/
```
will create a folder as follows:
```angular2html
john_doe/
├─ apps/
│  ├─ my_project_module/
│  │  ├─ tests/
│  │  │  ├─ __init__.py
│  │  ├─ controllers.py
│  │  ├─ module.py
│  │  ├─ routers.py
│  │  ├─ services.py
│  │  ├─ __init__.py
│  ├─ __init__.py
├─ core/
├─ domain/
├─ tests/
│  ├─ __init__.py
├─ __init__.py/
├─ config.py
├─ root_module.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         dsssss                                                                                                                                                                                                                                                        cxccccccxxcxxnew_file
├─ server.py

```

## **New Command CLI Arguments**
- `module-name` Set the resulting module name.
- `directory` Path to dump the scaffolded files. `.` can be used to select current directory.
