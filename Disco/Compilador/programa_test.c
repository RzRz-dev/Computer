
struct Punto {
    int x;
    int y;
};

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
    }

    // Estructura de iteración
    int i = 0;
    while (i < 10) {
        arr[i] = i * 2;
        i += 1;
    }

}