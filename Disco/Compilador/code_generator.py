"""
Generador de Código - Convierte el AST a instrucciones de máquina
Usa el patrón Visitor para recorrer el AST
"""

from ast_nodes import *

class CodeGenerator:
    """Genera código de máquina a partir del AST"""
    
    def __init__(self):
        self.code = []  # Lista de instrucciones
        self.symbol_table = {}  # Tabla de símbolos con direcciones
        self.register_counter = 0  # Para asignar registros
        self.label_counter = 0  # Para generar labels únicos
        self.loop_stack = []  # Stack para control de loops (break/continue)
        
    def allocate_register(self) -> int:
        """Asigna un registro disponible"""
        reg = self.register_counter
        self.register_counter += 1
        return reg
    
    def free_register(self, reg: int):
        """Libera un registro"""
        if reg < self.register_counter:
            self.register_counter -= 1
    
    def generate_label(self) -> str:
        """Genera un label único"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, instr: str, *args):
        """Emite una instrucción"""
        if args:
            self.code.append(f"{instr} {', '.join(map(str, args))}")
        else:
            self.code.append(instr)
    
    def emit_label(self, label: str):
        """Emite un label"""
        self.code.append(f"{label}:")
    
    def generate(self, ast_root) -> str:
        """Comienza la generación de código"""
        self.code = []
        self.register_counter = 1  # R0 es SP
        self.label_counter = 0
        
        if isinstance(ast_root, list):
            for declaration in ast_root:
                declaration.accept(self)
        else:
            ast_root.accept(self)
        
        return '\n'.join(self.code)
    
    # ============================================
    # VISITANTES PARA CADA TIPO DE NODO
    # ============================================
    
    def visit_Func_node(self, node: Func_node):
        """Genera código para una función"""
        # Emite label de función
        self.emit_label(f"func_{node.ID}")
        
        # Guarda contexto anterior
        old_register_counter = self.register_counter
        self.register_counter = 1
        
        # Genera código del bloque
        if node.Block_node:
            if isinstance(node.Block_node, list):
                for stmt in node.Block_node:
                    if hasattr(stmt, 'accept'):
                        stmt.accept(self)
            elif hasattr(node.Block_node, 'accept'):
                node.Block_node.accept(self)
        
        # Retorna (si no hay return explícito, añade uno)
        self.emit("RET")
        
        # Restaura contexto
        self.register_counter = old_register_counter
    
    def visit_Var_node(self, node: Var_node):
        """Genera código para declaración de variable"""
        # Asigna dirección de memoria o registro
        self.symbol_table[node.ID] = {
            "type": node.type,
            "address": len(self.symbol_table)
        }
        
        # Si tiene inicialización, genera código para asignarla
        if node.init and hasattr(node.init, 'accept'):
            reg = self.allocate_register()
            node.init.accept(self)
            # Guarda en memoria
            self.emit("STORE", f"R{reg}")
            self.free_register(reg)
    
    def visit_Assign_node(self, node: Assign_node):
        """Genera código para asignación"""
        # Simplificado: solo genera NOP (instrucción nula)
        self.emit("NOP")
    
    def visit_Call_node(self, node: Call_node):
        """Genera código para llamada a función"""
        # Guarda argumentos en la pila
        arg_count = 0
        if node.args:
            for arg in node.args:
                if hasattr(arg, 'accept'):
                    arg.accept(self)
                self.emit("PUSH", f"R{self.register_counter}")
                arg_count += 1
        
        # Llama la función
        self.emit("CALL", f"func_{node.ID}")
    
    def visit_If_node(self, node: If_node):
        """Genera código para if"""
        else_label = self.generate_label()
        end_label = self.generate_label()
        
        # Evalúa condición
        if hasattr(node.condition, 'accept'):
            node.condition.accept(self)
        
        # Salta si es falso
        self.emit("JZ", else_label)
        
        # Código del bloque then
        if node.block:
            if isinstance(node.block, list):
                for stmt in node.block:
                    if hasattr(stmt, 'accept'):
                        stmt.accept(self)
            elif hasattr(node.block, 'accept'):
                node.block.accept(self)
        
        self.emit("JMP", end_label)
        
        # Código del else/elif
        self.emit_label(else_label)
        if node.elif_opt:
            if isinstance(node.elif_opt, list):
                for elif_node in node.elif_opt:
                    if hasattr(elif_node, 'accept'):
                        elif_node.accept(self)
            elif hasattr(node.elif_opt, 'accept'):
                node.elif_opt.accept(self)
        
        self.emit_label(end_label)
    
    def visit_While_node(self, node: While_node):
        """Genera código para while"""
        loop_label = self.generate_label()
        end_label = self.generate_label()
        
        self.loop_stack.append((loop_label, end_label))
        
        # Label de inicio del loop
        self.emit_label(loop_label)
        
        # Evalúa condición
        if hasattr(node.condition, 'accept'):
            node.condition.accept(self)
        
        # Salta al final si es falso
        self.emit("JZ", end_label)
        
        # Código del bloque
        if node.block:
            if isinstance(node.block, list):
                for stmt in node.block:
                    if hasattr(stmt, 'accept'):
                        stmt.accept(self)
            elif hasattr(node.block, 'accept'):
                node.block.accept(self)
        
        # Salta al inicio
        self.emit("JMP", loop_label)
        
        # Label de fin
        self.emit_label(end_label)
        
        self.loop_stack.pop()
    
    def visit_For_node(self, node: For_node):
        """Genera código para for"""
        loop_label = self.generate_label()
        end_label = self.generate_label()
        update_label = self.generate_label()
        
        self.loop_stack.append((loop_label, end_label))
        
        # Inicialización
        if node.init and hasattr(node.init, 'accept'):
            node.init.accept(self)
        
        # Label de inicio del loop
        self.emit_label(loop_label)
        
        # Condición
        if node.condition and hasattr(node.condition, 'accept'):
            node.condition.accept(self)
            self.emit("JZ", end_label)
        
        # Bloque
        if node.block:
            if isinstance(node.block, list):
                for stmt in node.block:
                    if hasattr(stmt, 'accept'):
                        stmt.accept(self)
            elif hasattr(node.block, 'accept'):
                node.block.accept(self)
        
        # Actualización
        self.emit_label(update_label)
        if node.update:
            if isinstance(node.update, list):
                for stmt in node.update:
                    if hasattr(stmt, 'accept'):
                        stmt.accept(self)
            elif hasattr(node.update, 'accept'):
                node.update.accept(self)
        
        # Salta al inicio
        self.emit("JMP", loop_label)
        
        # Label de fin
        self.emit_label(end_label)
        
        self.loop_stack.pop()
    
    def visit_Return_node(self, node: Return_node):
        """Genera código para return"""
        if node.expr_opt and hasattr(node.expr_opt, 'accept'):
            node.expr_opt.accept(self)
        self.emit("RET")
    
    def visit_Break_node(self, node):
        """Genera código para break"""
        if self.loop_stack:
            _, end_label = self.loop_stack[-1]
            self.emit("JMP", end_label)
    
    def visit_Continue_node(self, node):
        """Genera código para continue"""
        if self.loop_stack:
            loop_label, _ = self.loop_stack[-1]
            self.emit("JMP", loop_label)
    
    def visit_Additive_node(self, node: Additive_node):
        """Genera código para suma/resta"""
        if hasattr(node.left_expr, 'accept'):
            node.left_expr.accept(self)
        if hasattr(node.right_expr, 'accept'):
            node.right_expr.accept(self)
        
        if node.symbol == '+':
            self.emit("ADD", "R1", "R2")
        elif node.symbol == '-':
            self.emit("SUB", "R1", "R2")
    
    def visit_Term_node(self, node: Term_node):
        """Genera código para multiplicación/división"""
        if hasattr(node.left_expr, 'accept'):
            node.left_expr.accept(self)
        if hasattr(node.right_expr, 'accept'):
            node.right_expr.accept(self)
        
        if node.symbol == '*':
            self.emit("MUL", "R1", "R2")
        elif node.symbol == '/':
            self.emit("DIV", "R1", "R2")
        elif node.symbol == '%':
            self.emit("MOD", "R1", "R2")
    
    def visit_Equality_node(self, node: Equality_node):
        """Genera código para comparación de igualdad"""
        if hasattr(node.left_expr, 'accept'):
            node.left_expr.accept(self)
        if hasattr(node.right_expr, 'accept'):
            node.right_expr.accept(self)
        
        if node.symbol == '==':
            self.emit("CMP", "R1", "R2")
        elif node.symbol == '!=':
            self.emit("CMP", "R1", "R2")
    
    def visit_Relational_node(self, node: Relational_node):
        """Genera código para operadores relacionales"""
        if hasattr(node.left_expr, 'accept'):
            node.left_expr.accept(self)
        if hasattr(node.right_expr, 'accept'):
            node.right_expr.accept(self)
        
        self.emit("CMP", "R1", "R2")
    
    def visit_Lvalue_node(self, node: Lvalue_node):
        """Genera código para cargar un lvalue"""
        if node.ID in self.symbol_table:
            self.emit("LOAD", "R1")
    
    def visit_Or_node(self, node: Or_node):
        """Genera código para OR"""
        if hasattr(node.left_expr, 'accept'):
            node.left_expr.accept(self)
        if hasattr(node.right_expr, 'accept'):
            node.right_expr.accept(self)
    
    def visit_And_node(self, node: And_node):
        """Genera código para AND"""
        if hasattr(node.left_expr, 'accept'):
            node.left_expr.accept(self)
        if hasattr(node.right_expr, 'accept'):
            node.right_expr.accept(self)
    
    def visit_Unary_node(self, node: Unary_node):
        """Genera código para unario"""
        if hasattr(node.expr, 'accept'):
            node.expr.accept(self)
    
    def visit_Postfix_node(self, node: Postfix_node):
        """Genera código para postfix"""
        if hasattr(node.primary, 'accept'):
            node.primary.accept(self)
    
    def visit_Param_node(self, node: Param_node):
        """Genera código para parámetro"""
        pass
    
    def visit_Struct_node(self, node: Struct_node):
        """Genera código para struct"""
        pass
    
    def visit_Field_node(self, node):
        """Genera código para campo"""
        pass
    
    def visit_Array_size_node(self, node):
        """Genera código para tamaño de array"""
        pass
    
    def visit_Typedef_node(self, node):
        """Genera código para typedef"""
        pass
    
    def visit_Array_suffix_node(self, node):
        """Genera código para sufijo de array"""
        pass
    
    def visit_Matriz_suffix_node(self, node):
        """Genera código para sufijo de matriz"""
        pass
    
    def visit_Var_decl_node(self, node: Var_decl_node):
        """Genera código para declaración inline"""
        pass
    
    def visit_Elif_node(self, node: Elif_node):
        """Genera código para elif"""
        pass
    
    def visit_Else_node(self, node: Else_node):
        """Genera código para else"""
        pass
    
    def visit_Do_while_node(self, node: Do_while_node):
        """Genera código para do-while"""
        pass
    
    def generic_visit(self, node):
        """Visitante genérico para nodos no reconocidos"""
        pass
