import ast


class ScopeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.vars = set()

    def visit_arg(self, node):
        self.vars.add(node.arg)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.vars.add(node.id)

    def collect(self, node):
        self.vars.clear()
        if hasattr(node, "args"):
            for arg in node.args.args:
                self.visit_arg(arg)
        self.generic_visit(node)
        return self.vars
