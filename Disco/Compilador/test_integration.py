#!/usr/bin/env python3
"""
Script de prueba para verificar la integración entre el lexer y el parser.
"""

from sintactic_analyzer import parse

# Código de prueba simple
test_code = """
struct Punto {
        int x;
        int y;
    }
    
    func int suma(int a, int b) {
        return a + b;
    }
    
    func void main() {
        int resultado = 0;
        float pi = 3.14159;
        bool activo = true;
        char letra = 'A';
        int arr[10];
        int mat[3][3];
    
        struct Punto p;
        p.x = 5;
        p.y = 10;
    
        // Estructura de selección
        if (resultado == 0) {
            resultado = suma(p.x, p.y);
        } else {
            resultado = 0;
        }
    
        // Estructura de iteración
        int i = 0;
        while (i < 10) {
            arr[i] = i * 2;
            i += 1;
        }
    
        for (int j = 0; j < 3; j += 1) {
            mat[j][0] = j;
        }
    
        // Manejo de pila
        push(resultado);
        int valor = pop();
    }
"""

print("Analizando código...")
print("=" * 60)
print(test_code)
print("=" * 60)

result = parse(test_code)

if result:
    print("\n✓ Análisis exitoso!")
    print("\nÁrbol sintáctico:")
    print(result)
else:
    print("\n✗ Error durante el análisis")
