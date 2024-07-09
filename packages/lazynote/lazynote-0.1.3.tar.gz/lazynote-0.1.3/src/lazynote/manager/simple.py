import inspect
import textwrap

from typing import Callable, Optional

import libcst as cst

from lazynote.manager.base import BaseManager,DocstringMode




class DocstringHandler:
    @staticmethod
    def handle_translate(old_docstring: Optional[str], node_code: str) -> str:
        # TODO
        return f"Translated: {old_docstring}" or None

    @staticmethod
    def handle_polish(old_docstring: Optional[str], node_code: str) -> str:
        # 实现润色逻辑
        # TODO
        return f"Polished: {old_docstring }" or None

    @staticmethod
    def handle_clear(old_docstring: Optional[str], node_code: str) -> str:
        return None

    @staticmethod
    def handle_fill(old_docstring: Optional[str], node_code: str) -> str:
        # 实现填入逻辑
        if old_docstring:
            return f"{old_docstring}"
        else:
            return None

    @staticmethod
    def get_handler(pattern: DocstringMode) -> Callable[[Optional[str], str], str]:
        try:
            # 自动映射模式到相应的处理函数
            handler_method_name = f"handle_{pattern.value}"
            return getattr(DocstringHandler, handler_method_name)
        except AttributeError:
            raise ValueError(f"No handler found for pattern: {pattern}")

class SimpleManager(BaseManager):
    """
        Initialize the SimpleManager.

        :param pattern: The docstring handling pattern. Should be one of:
                        - DocstringMode.TRANSLATE
                        - DocstringMode.POLISH
                        - DocstringMode.CLEAR
                        - DocstringMode.FILL
    """
    

    def gen_docstring(self, old_docstring: Optional[str], node_code: str) -> str:

        handler = DocstringHandler.get_handler(self.pattern)

        return handler(old_docstring, node_code)

