import ast

from .ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.expr_stop_stack = []
        self.var_types = {"숫자", "실수", "문자열", "참거짓", "목록", "자유"}
        self.type_aliases = {"문자": "문자열", "-": "자유"}

    def cur(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek(self, offset=1):
        index = self.pos + offset
        return self.tokens[index] if index < len(self.tokens) else None

    def skip_newlines(self):
        while self.cur() and self.cur().type == "NEWLINE":
            self.pos += 1

    def eat(self, v=None):
        tok = self.cur()
        if not tok:
            raise Exception("예상치 못한 EOF")

        if v == ">" and tok.value == ">>":
            tok.value = ">"
            return tok

        if v and tok.value != v:
            raise Exception(f"[{tok.line}번 줄] '{v}' 필요 (현재: {tok.value})")

        self.pos += 1
        return tok

    def push_expr_stops(self, *values):
        self.expr_stop_stack.append(set(values))

    def pop_expr_stops(self):
        self.expr_stop_stack.pop()

    def is_expr_stop(self, value):
        return any(value in stops for stops in self.expr_stop_stack)

    def parse(self):
        s = []
        self.skip_newlines()
        while self.cur():
            s.append(self.stmt())
            self.skip_newlines()
        return Program(s)

    def stmt(self):
        self.skip_newlines()
        tok = self.cur()

        if tok.value == "함수": return self.func()
        if tok.value == "반환": return self.ret()
        if tok.value == "조건": return self.if_stmt()
        if tok.value == "반복": return self.loop_stmt()
        if tok.value == "멈춤": return self.break_stmt()
        if tok.value == "건너뛰기": return self.continue_stmt()
        if tok.value == "사용": return self.use_stmt()
        if tok.value == "변수": return self.var_decl()
        if tok.value == "출력": return self.print_stmt()

        if self.is_assignment_stmt():
            return self.assign_stmt()

        return self.expr()

    def use_stmt(self):
        line = self.cur().line
        self.eat("사용")
        self.eat("<")

        names = []
        while True:
            names.append(self.eat().value)
            if self.cur().value != ",":
                break
            self.eat(",")

        self.eat(">")
        return Use(names, line)

    def print_stmt(self):
        line = self.cur().line
        self.eat("출력")
        self.eat("<")

        args = []
        self.push_expr_stops(">", ">>", ",")
        try:
            if self.cur().value not in {">", ">>"}:
                while True:
                    args.append(self.expr())
                    if self.cur().value != ",":
                        break
                    self.eat(",")
        finally:
            self.pop_expr_stops()
        self.eat(">")

        return Call("출력", args, line)

    def parse_call_args(self):
        self.eat("<")
        args = []
        self.push_expr_stops(">", ">>", ",")
        try:
            if self.cur().value not in {">", ">>"}:
                while True:
                    args.append(self.expr())
                    if self.cur().value != ",":
                        break
                    self.eat(",")
        finally:
            self.pop_expr_stops()
        self.eat(">")
        return args

    def parse_method_args(self, method):
        self.eat("<")

        if method == "자르기":
            self.push_expr_stops("~")
            try:
                start = self.expr()
            finally:
                self.pop_expr_stops()
            self.eat("~")
            self.push_expr_stops(">", ">>")
            try:
                end = self.expr()
            finally:
                self.pop_expr_stops()
            self.eat(">")
            return [start, end]

        args = []
        self.push_expr_stops(">", ">>", ",")
        try:
            if self.cur().value not in {">", ">>"}:
                while True:
                    args.append(self.expr())
                    if self.cur().value != ",":
                        break
                    self.eat(",")
        finally:
            self.pop_expr_stops()
        self.eat(">")
        return args

    def parse_block(self):
        if self.cur() and self.cur().value == "<":
            self.eat("<")

        body = []
        self.skip_newlines()
        while self.cur() and self.cur().value != ">" and self.cur().value != "아니면":
            body.append(self.stmt())
            self.skip_newlines()
        self.eat(">")
        return body

    def parse_if_block(self):
        self.eat("<")
        body = []
        self.skip_newlines()
        while self.cur() and self.cur().value != ">" and self.cur().value != "아니면":
            body.append(self.stmt())
            self.skip_newlines()
        if self.cur() and self.cur().value == ">":
            self.eat(">")
        return body

    def loop_stmt(self):
        line = self.cur().line
        self.eat("반복")

        if self.cur().value == "[":
            self.eat("[")
            condition = self.expr()
            self.eat("]")
            return WhileLoop(condition, self.parse_block(), line)

        var_name = self.eat().value
        self.eat("[")
        start = self.expr()
        self.eat("~")
        end = self.expr()
        self.eat("]")
        body = self.parse_block()
        return ForLoop(var_name, start, end, body, line)

    def var_decl(self):
        line = self.cur().line
        self.eat("변수")

        type_tok = self.cur()
        if not type_tok:
            raise Exception("예상치 못한 EOF")

        raw_type_name = self.type_aliases.get(type_tok.value, type_tok.value)
        if raw_type_name not in self.var_types:
            raise Exception(f"[{type_tok.line}번 줄] 알 수 없는 자료형")

        self.eat()
        type_name = raw_type_name
        name = self.eat().value
        self.eat("=")

        if type_name == "목록" and self.cur().value == "(":
            self.eat("(")
            items = []
            if self.cur().value != ")":
                while True:
                    items.append(self.expr())
                    if self.cur().value != ",":
                        break
                    self.eat(",")
            self.eat(")")
            return ListDecl(name, items, line)

        value = self.expr()
        return VarDecl(type_name, name, value, line)

    def is_assignment_stmt(self):
        tok = self.cur()
        if not tok or tok.type != "IDENT":
            return False

        i = self.pos + 1
        while i < len(self.tokens) and self.tokens[i].value == "[":
            depth = 1
            i += 1
            while i < len(self.tokens) and depth > 0:
                if self.tokens[i].value == "[":
                    depth += 1
                elif self.tokens[i].value == "]":
                    depth -= 1
                i += 1
            if depth > 0:
                return False

        return i < len(self.tokens) and self.tokens[i].value == "="

    def assign_stmt(self):
        line = self.cur().line
        target = Var(self.eat().value, line)

        while self.cur() and self.cur().value == "[":
            index_line = self.cur().line
            self.eat("[")
            index = self.expr()
            self.eat("]")
            target = Index(target, index, index_line)

        self.eat("=")
        value = self.expr()

        if isinstance(target, Var):
            return Assign(target.name, value, line)
        if isinstance(target, Index):
            return IndexAssign(target.target, target.index, value, line)

        raise Exception(f"[{self.cur().line}번 줄] 대입 대상 오류")

    def func(self):
        line = self.cur().line
        self.eat("함수")
        name = self.eat().value
        self.eat("인수")

        params = []
        while self.cur().value != "<":
            if self.cur().value != ",":
                params.append(self.eat().value)
            else:
                self.eat(",")

        body = self.parse_block()
        return Function(name, params, body, line)

    def if_stmt(self):
        line = self.cur().line
        branches = []
        else_branch = []

        self.eat("조건")
        self.eat("[")
        cond = self.expr()
        self.eat("]")

        body = self.parse_if_block()
        branches.append((cond, body))
        self.skip_newlines()

        while self.cur() and self.cur().value == "아니면":
            self.eat("아니면")

            if self.cur().value == "[":
                self.eat("[")
                cond = self.expr()
                self.eat("]")
                body = self.parse_if_block()
                branches.append((cond, body))
                self.skip_newlines()
            else:
                else_branch = self.parse_if_block()
                break

        return If(branches, else_branch, line)

    def ret(self):
        line = self.cur().line
        self.eat("반환")
        self.push_expr_stops(">")
        try:
            value = self.expr()
        finally:
            self.pop_expr_stops()
        return Return(value, line)

    def break_stmt(self):
        line = self.cur().line
        self.eat("멈춤")
        return Break(line)

    def continue_stmt(self):
        line = self.cur().line
        self.eat("건너뛰기")
        return Continue(line)

    def expr(self):
        return self.logic()

    def logic(self):
        left = self.equality()
        while (
            self.cur()
            and not self.is_expr_stop(self.cur().value)
            and self.cur().value in ["그리고", "또는"]
        ):
            op_tok = self.eat()
            right = self.equality()
            left = Binary(left, op_tok.value, right, op_tok.line)
        return left

    def equality(self):
        left = self.comparison()
        while (
            self.cur()
            and not self.is_expr_stop(self.cur().value)
            and self.cur().value in ["==", "!="]
        ):
            op_tok = self.eat()
            right = self.comparison()
            left = Binary(left, op_tok.value, right, op_tok.line)
        return left

    def comparison(self):
        left = self.additive()
        while (
            self.cur()
            and not self.is_expr_stop(self.cur().value)
            and self.cur().value in ["<<", ">>", "<<=", ">>="]
        ):
            op_tok = self.eat()
            right = self.additive()
            left = Binary(left, op_tok.value, right, op_tok.line)
        return left

    def additive(self):
        left = self.multiplicative()
        while (
            self.cur()
            and not self.is_expr_stop(self.cur().value)
            and self.cur().value in ["+", "-"]
        ):
            op_tok = self.eat()
            right = self.multiplicative()
            left = Binary(left, op_tok.value, right, op_tok.line)
        return left

    def multiplicative(self):
        left = self.term()
        while (
            self.cur()
            and not self.is_expr_stop(self.cur().value)
            and self.cur().value in ["*", "/", "%"]
        ):
            op_tok = self.eat()
            right = self.term()
            left = Binary(left, op_tok.value, right, op_tok.line)
        return left

    def term(self):
        tok = self.cur()
        expr = None

        if tok.type == "FLOAT":
            self.eat()
            expr = Literal(float(tok.value), tok.line)

        elif tok.type == "NUMBER":
            self.eat()
            expr = Literal(int(tok.value), tok.line)

        elif tok.type == "STRING":
            self.eat()
            expr = Literal(ast.literal_eval(tok.value), tok.line)

        elif tok.type == "BOOL":
            self.eat()
            expr = Literal(tok.value == "참", tok.line)

        elif tok.type == "IDENT":
            name = self.eat().value
            expr = Var(name, tok.line)

        else:
            raise Exception(f"[{tok.line}번 줄] 식 오류")

        while self.cur() and self.cur().value in ["<", "[", ":"]:
            if self.cur().value == "<":
                if not isinstance(expr, Var):
                    break
                call_start = self.pos
                try:
                    expr = Call(expr.name, self.parse_call_args(), tok.line)
                except Exception:
                    self.pos = call_start
                    break
                continue

            if self.cur().value == "[":
                index_line = self.cur().line
                self.eat("[")
                index = self.expr()
                self.eat("]")
                expr = Index(expr, index, index_line)
                continue

            self.eat(":")
            method_tok = self.cur()
            method = self.eat().value
            expr = MethodCall(expr, method, self.parse_method_args(method), method_tok.line)

        return expr
