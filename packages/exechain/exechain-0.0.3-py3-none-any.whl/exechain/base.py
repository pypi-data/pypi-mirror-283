"""
Copyright (c) 2024 Leonov Artur (depish.eskry@yandex.ru)

Permission is hereby granted to use, copy, modify, and distribute this code in any form, provided that the above copyright notice and this permission notice appear in all copies.

DISCLAIMER:
This source code is provided "as is", without any warranty of any kind, express or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the code is with you.



Copyright (c) 2024 Леонов Артур (depish.eskry@yandex.ru)

Разрешается использовать, копировать, изменять и распространять этот код в любом виде, при условии сохранения данного уведомления.

ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ:
Этот исходный код предоставляется "как есть" без каких-либо гарантий, явных или подразумеваемых, включая, но не ограничиваясь, подразумеваемыми гарантиями товарной пригодности и пригодности для конкретной цели. Вся ответственность за использование данного кода лежит на вас.
"""


import os
from pathlib import Path
import json
import shutil
import platform
import subprocess
import glob
import os

from exechain.internal import file1_newer_file2


def which(name):
    search_dirs = os.environ["PATH"].split(os.pathsep)
    
    for path in search_dirs:
        test = Path(path) / name
        if test.is_file() and os.access(test, os.X_OK):
            return test

    return None


def exit_with_message(message, code):
    print(message)
    exit(code)


def _get_path(path) -> Path:
    if isinstance(path, str):
        return Path(path)
    else:
        return path


_TARGET_POOL: dict = {}
_VARIBLE_POOL: dict = {}


def get_target_by_name(name: str ):
    return _TARGET_POOL[name]


def get_target_names() -> list[str]:
    return list(_TARGET_POOL.keys())


def exec_target(name: str):
    if name not in _TARGET_POOL:
        raise Exception(f"error target '{name}': not found")
    return _TARGET_POOL[name]._invoke(None)


def target_pool() -> dict:
    return _TARGET_POOL


class BaseTool:
    """Данный класс служит меткой для обозначения подклассов инструментов.
    
    Инструмент - это callable который выполняется при выполнении инструкций у класса Target и его подклассов.
    """
    def __init__(self) -> None:
        pass


class Target:
    """
    Target class выполняет цепочки действий в зависимости от состояния target. (Аналогично тому как работают цели в Makefile).
    
    Как и у make - у класса Target целью является файл или папка. И дальшее выполнение инструкций выполняется в зависимости от состояния этой цели.
    Если файл/папка не существует - данная цель будет выполнена.
    Если файл/папка существует - этап сборки этой цели будет пропущен.
    
    При создании экземпляра класса он автоматически добавляется в пулл целей.
    
    Attributes
    ----------
    target : Path
        Файл/папка или произвольное название - проверяемая цель для выполнения цепочки действий.
        Если файла не существует то это означает необходимость его создать для этой цели выполняются цепочки действий по порядку,
        сперва выполняется обработка dependecies затем recept.
        
    dependencies : list[&quot;callable&quot;]
        Список зависимостей которые будут выполнены перед рецептами (recept) для сборки данного target.
        Данные зависимости определяют что необходимо выполнить чтобы далее выполнить сборку данной цели (recept).
        
    recept : list[&quot;callable&quot;]
        Инструкции которые будут выполнены. Предполагается что выполнение данных инструкций удовлетворит требование target.
        
    target_name : str
        Имя цели в виде строки
        
    target_run_lock : bool
        Флаг указывающий что данная цель уже выполняется. Необходимо для предотвращения циклической зависимости
        
    vars : dict
        Список переменных которые будут использованы при выполнении цепочки действий. 
        Данные переменные могут использоваться для подстановки плейсхолдеров у строк.
    """
    def __init__(self, target: Path, dependencies: list["Target"] = [], recept: list["callable"] = []) -> None:
        """
        Args:
            target (Path): Путь к файлу или папке а так же цель для выполнения цепочки действий (сборки).
            dependencies (list[&quot;Target&quot;], optional): Список зависимостей которые будут выполнены перед рецептами (recept) для сборки данного target.. Defaults to [].
            recept (list[&quot;callable&quot;], optional): Список зависимостей которые будут выполнены после dependencies и предполагают содание требуемого объекта target.. Defaults to [].

        Raises:
            Exception: _description_
            Exception: _description_
        """
        self.target: Path = _get_path(target)
        self.recept: list["callable"] = recept
        self.dependencies: list["Target"]  = dependencies
        self.target_name = str(target)

        if not dependencies and not recept:
            raise Exception(f"error [target {str(self.target)}: nothing to do]")
        
        if self.target_name in _TARGET_POOL:
            raise Exception(f"error [target {str(self.target)}: already exists]")
        
        _TARGET_POOL[self.target_name] = self
        self.target_run_lock = False
        self.exec_cond_cache = None
                
        self.vars = {
            "target-name": self.target_name
        }


    def __str__(self) -> str:
        return f"target '{self.target_name}'"
    
    
    def _is_file(self) -> bool:
        return True
    
    
    def _invoke(self, parent, vars = {}):
        # TODO: Возможно стоит ставить флаг что цель была собрана и выполнена 
        
        if self.target_run_lock:
            print(f"❕ Предотвращение циклической зависимости {parent.target_name if parent else '_'} -> {self.target_name}")
            return

        self.target_run_lock = True
        # try:
        def _run_recept():
            print(f"🔹 target [{self.target_name}]")
            for cmd in self.recept:
                if not cmd(self.vars):
                    exit_with_message(f"Ошибка при выполнении: {str(cmd)}", -1)
        
        def _run_dependencies(dependency_list):
            for dependency in dependency_list:
                dependency._invoke(self, self.vars)
        
        need_exec, dep_list = self.need_exec_target()
        if need_exec:
            _run_dependencies(dep_list)
            _run_recept()
            
        # except Exception as e:
        #     exit_with_message(f"‼️ Ошибка при выполнении: {str(e)}",  -2)
        self.target_run_lock = False

    
    def need_exec_target(self, restore_cache: bool = False):
        if self.exec_cond_cache and not restore_cache:
            return self.exec_cond_cache
        
        # Если цель не существует то необходимо выполнить все для ее построения
        if not self.target.exists():
            return (True, self.dependencies)
        
        # TODO: Возможно стоит добавить кеш на результат (сохранять состояние возвращаемого значения)
        # Так как этот метод будет вызываться множество раз при большой глубине зависимостей.
        
        if self.target.exists():
            dependencies_to_run = []
            for dep in self.dependencies:
                if dep.need_exec_target():
                    dependencies_to_run.append(dep)
                elif dep._is_file():
                    if file1_newer_file2(dep.target_name, self.target_name):
                        dependencies_to_run.append(dep)
                        
            self.exec_cond_cache = (True, dependencies_to_run)
        else:
            self.exec_cond_cache = (False, [])
        
        return self.exec_cond_cache
    

class TargetRef:
    """Класс TargetRef управляет ссылками на целевые объекты, которые хранятся в глобальном пуле целей (_TARGET_POOL).
    
    Конструктор:
    -------------
    __init__(self, target) -> None
        Инициализирует экземпляр класса TargetRef. Преобразует целевую задачу в строку и сохраняет её.

        Параметры:
        target : любое значение, которое может быть преобразовано в строку;
            Имя или файл/папка.

    Методы:
    -------
    __call__(self, vars = None)
        Вызывает объект из глобального пула целей (_TARGET_POOL) по имени, если он существует.
        
        Параметры:
        vars : dict, optional
            Необязательный словарь переменных. 

        Возвращает:
        Объект из пула целей (_TARGET_POOL) по имени.

        Исключения:
        KeyError
            Если целевая задача не найдена в пуле целей (_TARGET_POOL), выбрасывается исключение с соответствующим сообщением.
    """
    def __init__(self, target) -> None:
        self.target = str(target)


    def _invoke(self, parent, vars = {}):
        """
        Вызывает объект из глобального пула целей (_TARGET_POOL) по имени, если он существует.
        
        Параметры:
        vars : dict, optional
            Необязательный словарь переменных.

        Возвращает:
        Объект из пула целей (_TARGET_POOL) по имени.

        Исключения:
        KeyError
            Если целевая задача не найдена в пуле целей (_TARGET_POOL), выбрасывается исключение с соответствующим сообщением.
        """
        if self.target not in _TARGET_POOL:
            raise KeyError(f"not found target {self.target} for TargetRef class")
        return _TARGET_POOL[self.target]._invoke(parent, vars)


class ConditionalTarget:
    def __init__(self, condition, if_true: callable = None, if_false: callable = None):
        self.if_true = if_true
        self.if_false = if_false
        self.condition = condition

    def _invoke(self, parent, vars = {}):
        res = None
        if isinstance(self.condition, callable):
            res = self.condition()
        else:
            res = self.condition
        
        if res:
            if self.if_true is not None:
                self.if_true()
        else:
            if self.if_false is not None:
                self.if_false()
        
        return True


class TargetShellContains(Target):
    def __init__(self, target: Path, check_command: str, dependencies: list = [], recept: list = []) -> None:
        super().__init__(target, dependencies, recept)
        self.check_command = check_command
    
    def need_exec_target(self) -> bool:
        result = subprocess.run(
            self.check_command, 
            shell=True, 
            check=True, 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        return self.target_name not in result.stdout


class TargetFileWithLine(Target):
    def __init__(self, target: Path, search_line: str, dependencies: list = [], recept: list = []) -> None:
        super().__init__(target, dependencies, recept)
        self.search_line = search_line
        
    def need_exec_target(self) -> bool:
        with open(self.target, 'r', encoding='utf-8') as file:
            for line in file:
                if self.search_line in line:
                    return True
        return False


class ForEachFileTarget:
    def __init__(self, 
                 target, 
                 dependency: list["callable"] =[], 
                 recept: list["callable"] = [],  
                 glob_pattern = "*",
                 target_suffix = None) -> None:
        
        self.target = _get_path(target)
        self.pattern = glob_pattern
        self.dependency = dependency
        self.recept = recept
        self.suffix = target_suffix

        self._invoke(None)
        
    
    def _invoke(self, parent, vars = {}):
        fpath = str(self.target / self.pattern)
        files = glob.glob(fpath)
        if not files:
            raise Exception(f"error target '{str(self.target)}' pattern '{fpath}' ({self.pattern}): not found files")

        if self.suffix:
            suffixed = []
            for file in files:
                suffixed.append(
                    Target(f"{file}{self.suffix}", dependencies=[
                        Target(file, dependencies=self.dependency, recept=self.recept)
                    ])
                )
                
            Target(self.target, dependencies=suffixed)
        else:
            Target(self.target, dependencies=[Target(file if not self.suffix else f"{file}{self.suffix}", dependencies=self.dependency, recept=self.recept) for file in files])
     

# def make_targets_for_files(directory, file_pattern = "*", dependencies=[], recept_appender: callable = None):
#     target = _get_path(directory)
#     files = glob.glob(str(target / file_pattern))
    
#     refs = []
#     for file in files:
#         Target(file, dependencies=dependencies, recept=recept_appender(file))
#         refs.append(TargetRef(file))
    
#     return refs



_IMPORT_STRINGS = """
from exechain.exechain import *

"""


def include(file) -> None:
    """Включат файл сборки в текущий файл

    Args:
        file (Path | str): Путь до файла *.exechain

    Raises:
        FileNotFoundError: Файл не найден
    """
    path = _get_path(file)
    
    if not path.exists():
        raise FileNotFoundError(f"error include file '{str(path)}': not found file")
    
    script = _IMPORT_STRINGS
    
    with open(path, "r") as f:
        script += f.read()

    exec(script)


def add_folder_to_path(folder):
    """Добавляет путь в переменную окружения PATH. 
    
    Если данный путь уже существует в переменной PATH он будет проигнорирован.

    Функция поддерживает несколько типов переменной folder. Особенности имеет лишь тип dict:
    При передачи типа dict ожидается что он будет содержать праметр с ключем 'target-name',
    в котором будет указан путь.
    
    Args:
        folder (Path | str | dict | list): Путь который необходимо добавить
    
    Raises:
        Exception: Если переданный тип не поддерживается
    """
    folders_list = []
    if isinstance(folder, str) or isinstance(folder, Path):
        folders_list = [str(folder)]
    elif isinstance(folder, dict):
        folders_list = [folder["target-name"]]
    elif isinstance(folder, list):
        folders_list = [str(f) for f in folder]
    else:
        raise Exception(f"Unsupported type on variable 'folder': {folder}")
    
    tmp_path = os.environ.get("PATH")
    for folder in folders_list:
        if folder in tmp_path:
            continue
        tmp_path = f"{folder}{os.pathsep}{tmp_path}"

    os.environ["PATH"] = tmp_path
