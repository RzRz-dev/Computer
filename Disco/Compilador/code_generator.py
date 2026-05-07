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

    def generate(self, ast_root, symbol_table):
        self.code = []
        self.symbol_table = symbol_table
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

        info = self.symbol_table[node.ID]

        if node.Var_suffix_node:
            if isinstance(node.Var_suffix_node, Array_suffix_node):
                self.emit_label(node.ID)
                self.emit(".SIZE", self.symbol_table[node.ID].get("array_size"))
            elif isinstance(node.Var_suffix_node, Matriz_suffix_node):
                self.emit_label(node.ID)
                self.emit(".SIZE", self.symbol_table[node.ID].get("array_size"))
        elif (info["type"] not in ("int", "struct", "float", "void", "string", "char", "bool", "func")):
            

            for field in self.symbol_table[info["type"]]["field_list"]:
                self.emit_label(f"{node.ID}_{field}")
                self.emit(".SIZE", self.symbol_table[field]["array_size"] if self.symbol_table[field].get("array_size") else 1)
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
        if info.get("param") == True and "reg" in info:
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
        end_label = self.generate_label()
        next_label = self.generate_label()  # Para elif o else

        cond = node.condition
        salto_emitido = False
        # Soporte para condiciones relacionales y de igualdad
        if isinstance(cond, Relational_node):
            r1 = cond.left_expr.accept(self)
            r2 = cond.right_expr.accept(self)
            self.emit("CMP", f"R{r1}", f"R{r2}")
            self.free_register()
            if cond.symbol == '<':
                self.emit("JZ", next_label)
                self.emit("JP", next_label)
                salto_emitido = True
            elif cond.symbol == '>':
                self.emit("JZ", next_label)
                self.emit("JN", next_label)
                salto_emitido = True
            elif cond.symbol == '<=':
                self.emit("JP", next_label)
                salto_emitido = True
            elif cond.symbol == '>=':
                self.emit("JN", next_label)
                salto_emitido = True
        elif isinstance(cond, Equality_node):
            r1 = cond.left_expr.accept(self)
            r2 = cond.right_expr.accept(self)
            self.emit("CMP", f"R{r1}", f"R{r2}")
            self.free_register()
            if cond.symbol == '==':
                self.emit("JNZ", next_label)
                salto_emitido = True
            elif cond.symbol == '!=':
                self.emit("JZ", next_label)
                salto_emitido = True
        if not salto_emitido:
            cond_reg = cond.accept(self)
            self.emit("JZ", next_label)

        for stmt in node.block:
            stmt.accept(self)

        self.emit("JMP", end_label)
        self.emit_label(next_label)

        if isinstance(node.elif_opt, Elif_node):
            node.elif_opt.end_label = end_label  # Pasar etiqueta de fin
            node.elif_opt.accept(self)
        elif isinstance(node.elif_opt, Else_node):
            node.elif_opt.end_label = end_label
            node.elif_opt.accept(self)

        self.emit_label(end_label)

    def visit_Elif_node(self, node):
        # end_label es pasado desde el if o elif anterior y guardado en el nodo
        next_label = self.generate_label()
        cond = node.condition
        salto_emitido = False
        if isinstance(cond, Relational_node):
            r1 = cond.left_expr.accept(self)
            r2 = cond.right_expr.accept(self)
            self.emit("CMP", f"R{r1}", f"R{r2}")
            self.free_register()
            if cond.symbol == '<':
                self.emit("JZ", next_label)
                self.emit("JP", next_label)
                salto_emitido = True
            elif cond.symbol == '>':
                self.emit("JZ", next_label)
                self.emit("JN", next_label)
                salto_emitido = True
            elif cond.symbol == '<=':
                self.emit("JP", next_label)
                salto_emitido = True
            elif cond.symbol == '>=':
                self.emit("JN", next_label)
                salto_emitido = True
        elif isinstance(cond, Equality_node):
            r1 = cond.left_expr.accept(self)
            r2 = cond.right_expr.accept(self)
            self.emit("CMP", f"R{r1}", f"R{r2}")
            self.free_register()
            if cond.symbol == '==':
                self.emit("JNZ", next_label)
                salto_emitido = True
            elif cond.symbol == '!=':
                self.emit("JZ", next_label)
                salto_emitido = True
        if not salto_emitido:
            cond_reg = cond.accept(self)
            self.emit("JZ", next_label)

        for stmt in node.block:
            stmt.accept(self)

        self.emit("JMP", node.end_label)
        self.emit_label(next_label)

        if isinstance(node.elif_opt, Elif_node):
            node.elif_opt.end_label = node.end_label  # Pasar etiqueta de fin
            node.elif_opt.accept(self)
        elif isinstance(node.elif_opt, Else_node):
            node.elif_opt.end_label = node.end_label
            node.elif_opt.accept(self)


    def visit_Else_node(self, node):
        # end_label es pasado desde el if o elif anterior y guardado en el nodo
        for stmt in node.block:
            stmt.accept(self)
        self.emit("JMP", node.end_label)
    
    def visit_While_node(self, node):
        start = self.generate_label()
        end = self.generate_label()

        self.loop_stack.append((start, end))

        self.emit_label(start)

        # Soporte para condiciones relacionales
        cond = node.condition
        salto_emitido = False
        if isinstance(cond, Relational_node):
            r1 = cond.left_expr.accept(self)
            r2 = cond.right_expr.accept(self)
            self.emit("CMP", f"R{r1}", f"R{r2}")
            self.free_register()
            # Saltos según el símbolo
            if cond.symbol == '<':
                self.emit("JZ", end)  
                self.emit("JP", end)  
                salto_emitido = True
            elif cond.symbol == '>':
                self.emit("JZ", end)    
                self.emit("JN", end)   
                salto_emitido = True
            elif cond.symbol == '<=':
                self.emit("JP", end)    
                salto_emitido = True
            elif cond.symbol == '>=':
                self.emit("JN", end)  
                salto_emitido = True
        elif isinstance(cond, Equality_node):
            r1 = cond.left_expr.accept(self)
            r2 = cond.right_expr.accept(self)
            self.emit("CMP", f"R{r1}", f"R{r2}")
            self.free_register()
            if cond.symbol == '==':
                self.emit("JNZ", end)   
                salto_emitido = True
            elif cond.symbol == '!=':
                self.emit("JZ", end)    
                salto_emitido = True
        if not salto_emitido:
            # Condición booleana normal
            cond_reg = cond.accept(self)
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
                self.symbol_table[param.ID]["param"] = True
                self.symbol_table[param.ID]["reg"] = reg


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