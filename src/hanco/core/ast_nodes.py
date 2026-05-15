class Program:
    def __init__(self, statements): self.statements = statements

class Function:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Call:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Return:
    def __init__(self, value): self.value = value

class Binary:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Literal:
    def __init__(self, value): self.value = value

class Var:
    def __init__(self, name): self.name = name

class Index:
    def __init__(self, target, index):
        self.target = target
        self.index = index

class MethodCall:
    def __init__(self, target, method, args):
        self.target = target
        self.method = method
        self.args = args

class If:
    def __init__(self, branches, else_branch):
        self.branches = branches
        self.else_branch = else_branch

class ListDecl:
    def __init__(self, name, items):
        self.name = name
        self.items = items

class VarDecl:
    def __init__(self, type_name, name, value):
        self.type_name = type_name
        self.name = name
        self.value = value

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IndexAssign:
    def __init__(self, target, index, value):
        self.target = target
        self.index = index
        self.value = value

class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForLoop:
    def __init__(self, var_name, start, end, body):
        self.var_name = var_name
        self.start = start
        self.end = end
        self.body = body

class Break:
    pass

class Continue:
    pass

class Use:
    def __init__(self, names):
        self.names = names
