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

from exechain.base import BaseTool
from exechain.exechain_system import exchain_replace_variables

import os


class Shell(BaseTool):
    def __init__(self, command) -> None:
        super().__init__()
        self.command = command

    def __call__(self, vars = None):
        command = exchain_replace_variables(self.command, vars) if vars else self.command
        return os.system(command) == 0

    def __str__(self):
        return f"Shell({self.command})"


class Print(BaseTool):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg

    def __call__(self, vars = None):
        tmp = exchain_replace_variables(self.msg, vars) if vars else self.msg
        
        print(f"print [{tmp}]")
        print(tmp)
        return True
