import inspect
from typing import Callable, Optional

import libcst as cst
import libcst.matchers as m


class BaseEditor(cst.CSTTransformer):
    '''
    A tool for code text Transformer new code text
    '''

    def __init__(self, gen_docstring: Callable, pattern: str, module):
        self.gen_docstring = gen_docstring
        self.pattern = pattern
        self.module = module
        self.module_dict = self.create_module_dict(module)
        self.current_class = None

    def create_module_dict(self, module):
        module_dict = {}
        seen_objects = set()
        for name, obj in inspect.getmembers(module):
            module_dict[name] = obj
            if inspect.isclass(obj):
                self.add_class_members_to_dict(
                    module_dict, obj, name, seen_objects)
        return module_dict

    def add_class_members_to_dict(self, module_dict, cls, parent_name, seen_objects):
        if cls in seen_objects:
            return
        seen_objects.add(cls)
        for name, obj in inspect.getmembers(cls):
            full_name = f"{parent_name}.{name}"
            module_dict[full_name] = obj
            if inspect.isclass(obj):
                self.add_class_members_to_dict(
                    module_dict, obj, full_name, seen_objects)

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        full_name = f"{self.current_class}.{original_node.name.value}" if self.current_class else original_node.name.value
        obj = self._get_obj_by_name(full_name)
        docstring = obj.__doc__ if obj else None
        return self._update_node_with_new_docstring(original_node, updated_node, docstring)

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        self.current_class = node.name.value

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        self.current_class = None
        obj = self._get_obj_by_name(original_node.name.value)
        docstring = obj.__doc__ if obj else None
        return self._update_node_with_new_docstring(original_node, updated_node, docstring)

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        return self._update_node_with_new_docstring(original_node, updated_node, self.module.__doc__)

    def _get_obj_by_name(self, name: str):
        return self.module_dict.get(name, None)

    def _update_node_with_new_docstring(self, original_node: cst.CSTNode, updated_node: cst.CSTNode, docstring: Optional[str]) -> cst.CSTNode:

        node_code = cst.Module([]).code_for_node(original_node)

        old_docstring = docstring
        new_body = []

        if isinstance(updated_node.body, tuple):
            body = updated_node.body
        else:
            body = getattr(updated_node.body, 'body', [])

        # Extract existing docstring if present and build new body without it
        for stmt in body:
            if m.matches(stmt, m.SimpleStatementLine(body=[m.Expr(m.SimpleString())])):
                old_docstring = cst.ensure_type(
                    stmt.body[0].value, cst.SimpleString).value.strip('\"\'')
            else:
                new_body.append(stmt)

        new_docstring = self.gen_docstring(
            old_docstring, node_code)

        # Create a new docstring node if new_docstring is provided
        new_docstring_node = (
            cst.SimpleStatementLine([cst.Expr(cst.SimpleString(
                f'"""{new_docstring}"""'))]) if new_docstring else None
        )

        # Handle single-line functions or methods
        if len(new_body) == 1 and isinstance(new_body[0], cst.SimpleStatementLine):
            # Convert single-line function to multi-line if necessary
            single_line_stmt = new_body[0]
            if new_docstring_node:
                new_body = [new_docstring_node, single_line_stmt]
            else:
                new_body = [single_line_stmt]
        else:
            # Insert the new docstring at the beginning of the body if it exists
            if new_docstring_node:
                new_body.insert(0, new_docstring_node)

        # Update the body with the new list of statements
        try:
            if isinstance(updated_node.body, tuple):
                updated_body = tuple(new_body)
            else:
                updated_body = updated_node.body.with_changes(body=new_body)
        except Exception as e:
            print(f"Error updating body with new statements: {new_body}")
            print(f"Error message: {e}")
            raise

        return updated_node.with_changes(body=updated_body)
