from typing import Optional

from lazynote.manager.base import BaseManager


class CustomManager(BaseManager):
    def gen_docstring(self, old_docstring: Optional[str], pattern: str, node_code: str) -> str:
        """
        自定义生成新的文档字符串的逻辑。

        :param old_docstring: 旧的文档字符串
        :param pattern: 模式字符串
        :param node_code: 节点代码
        :return: 新的文档字符串
        """
        if old_docstring:
            return f"{old_docstring}\n\n{pattern}"
        else:
            return f"{pattern}"
