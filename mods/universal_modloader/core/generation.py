import ast


class HookCodeGenerator:
    @staticmethod
    def create_hook_block(target_module, selector, at_type, available_vars):
        template = f"""
_uml_ctx = locals()
universal_modloader.core.runtime.trigger_hooks('{target_module}', '{selector}', '{at_type}', _uml_ctx)
"""
        for var_name in available_vars:
            if var_name == "__return__":
                continue
            template += (
                f"if '{var_name}' in _uml_ctx: {var_name} = _uml_ctx['{var_name}']\n"
            )

        return ast.parse(template).body

    @staticmethod
    def create_return_block(target_module, selector, original_return_node):
        ret_val_node = (
            original_return_node.value
            if original_return_node.value
            else ast.Constant(value=None)
        )

        template = f"""
_uml_ctx = locals()
_uml_ctx['__return__'] = None
universal_modloader.core.runtime.trigger_hooks('{target_module}', '{selector}', 'RETURN', _uml_ctx)
return _uml_ctx['__return__']
"""
        nodes = ast.parse(template).body
        nodes[1].value = ret_val_node
        return nodes
