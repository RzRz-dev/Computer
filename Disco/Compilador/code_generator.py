from ast_nodes import *

class CodeGenerator:

    def visit_Struct_node(self, node):
        # No se genera código para definiciones de estructuras
        pass

    def generic_visit(self, node):
        raise Exception(f"No se implementó visit_{node.__class__.__name__} en CodeGenerator")

    def __init__(self):
        self.code = []
        self.data = []
        self.symbol_table = {}
        self.register_counter = 1  # R0 reservado (SP)
        self.label_counter = 0
        self.loop_stack = []

    # ========================
    # UTILIDADES
    # ========================

    def allocate_register(self):
        reg = self.register_counter
        self.register_counter += 1
        return reg

    def free_register(self):
        if self.register_counter > 1:
            self.register_counter -= 1

    def generate_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def emit(self, instr, *args):
        if args:
            self.code.append(f"{instr} {', '.join(map(str, args))}")
        else:
            self.code.append(instr)

    def emit_label(self, label):
        self.code.append(f"{label}:")

    def generate(self, ast_root):
        self.code = []
        self.symbol_table = {}
        self.register_counter = 1
        self.label_counter = 0

        if isinstance(ast_root, list):
            for node in ast_root:
                node.accept(self)
        else:
            ast_root.accept(self)

        return "\n".join(self.code)

    # ========================
    # VARIABLES
    # ========================

    def visit_Var_node(self, node):
        
        self.symbol_table[node.ID] = {
            "address": len(self.symbol_table)
        }

        if node.Var_suffix_node:
            if isinstance(node.Var_suffix_node, Array_suffix_node):
                self.symbol_table[node.ID]["size"] = node.Var_suffix_node.size
                self.emit_label(node.ID)
                self.emit(".SIZE", node.Var_suffix_node.size)
            elif isinstance(node.Var_suffix_node, Matriz_suffix_node):
                self.symbol_table[node.ID]["size"] = node.Var_suffix_node.size1 * node.Var_suffix_node.size2
                self.emit_label(node.ID)
                self.emit(".SIZE", node.Var_suffix_node.size1 * node.Var_suffix_node.size2)
        else:
            self.emit_label(node.ID)
            self.emit(".SIZE",1)
        if node.init:
            reg = node.init.accept(self)
            self.emit("STORE", f"R{reg}", node.ID)
            self.free_register()

    def visit_Lvalue_node(self, node):
        info = self.symbol_table[node.ID]

        # 🔹 Caso 1: parámetro ya cargado en registro
        if info.get("type") == "param" and "reg" in info:
            return info["reg"]

        # 🔹 Caso 2: variable normal en memoria
        reg = self.allocate_register()
        self.emit("LOAD", f"R{reg}", node.ID)
        return reg

    def visit_Assign_node(self, node):
        reg = node.expr_node.accept(self)
        
        self.emit("STORE", f"R{reg}", node.Lvalue_node.ID)
        self.free_register()

    # ========================
    # LITERALES
    # ========================

    def visit_Number_node(self, node):
        reg = self.allocate_register()
        self.emit("LOADV", f"R{reg}", node.value)
        return reg

    # ========================
    # EXPRESIONES
    # ========================

    def visit_Additive_node(self, node):
        r1 = node.left_expr.accept(self)
        r2 = node.right_expr.accept(self)

        if node.symbol == '+':
            self.emit("ADD", f"R{r1}", f"R{r2}")
        else:
            self.emit("SUB", f"R{r1}", f"R{r2}")

        self.free_register()
        return r1

    def visit_Term_node(self, node):
        r1 = node.left_expr.accept(self)
        r2 = node.right_expr.accept(self)

        if node.symbol == '*':
            self.emit("MUL", f"R{r1}", f"R{r2}")
        elif node.symbol == '/':
            self.emit("DIV", f"R{r1}", f"R{r2}")
        else:
            self.emit("MOD", f"R{r1}", f"R{r2}")

        self.free_register()
        return r1

    def visit_Relational_node(self, node):
        r1 = node.left_expr.accept(self)
        r2 = node.right_expr.accept(self)

        self.emit("CMP", f"R{r1}", f"R{r2}")
        self.free_register()
        return r1

    def visit_Equality_node(self, node):
        r1 = node.left_expr.accept(self)
        r2 = node.right_expr.accept(self)

        self.emit("CMP", f"R{r1}", f"R{r2}")
        self.free_register()
        return r1

    # ========================
    # CONTROL DE FLUJO
    # ========================

    def visit_If_node(self, node):
        else_label = self.generate_label()
        end_label = self.generate_label()

        cond_reg = node.condition.accept(self)
        self.emit("JZ", else_label)

        for stmt in node.block:
            stmt.accept(self)

        self.emit("JMP", end_label)

        self.emit_label(else_label)

        if node.elif_opt:
            node.elif_opt.accept(self)

        self.emit_label(end_label)

    def visit_While_node(self, node):
        start = self.generate_label()
        end = self.generate_label()

        self.loop_stack.append((start, end))

        self.emit_label(start)

        cond_reg = node.condition.accept(self)
        self.emit("JZ", end)

        for stmt in node.block:
            stmt.accept(self)

        self.emit("JMP", start)
        self.emit_label(end)

        self.loop_stack.pop()

    def visit_Break_node(self, node):
        _, end = self.loop_stack[-1]
        self.emit("JMP", end)

    def visit_Continue_node(self, node):
        start, _ = self.loop_stack[-1]
        self.emit("JMP", start)

    # ========================
    # FUNCIONES
    # ========================

    def visit_Func_node(self, node):
        self.emit_label(f"func_{node.ID}")

        # Registrar parámetros en la tabla de símbolos
        if node.params:
            for param in reversed(node.params):
                reg = self.allocate_register()
                self.emit("POP", f"R{reg}")
                self.symbol_table[param.ID] = {
                    "type": "param",
                    "reg": reg
                }

        for stmt in node.Block_node:
            stmt.accept(self)


    def visit_Call_node(self, node):
        for arg in node.args:
            reg = arg.accept(self)
            self.emit("PUSH", f"R{reg}")
            self.free_register()

        self.emit("CALL", f"func_{node.ID}")

        reg = self.allocate_register()
        return reg

    def visit_Return_node(self, node):
        if node.expr_opt:
            reg = node.expr_opt.accept(self)
        self.emit("RET")