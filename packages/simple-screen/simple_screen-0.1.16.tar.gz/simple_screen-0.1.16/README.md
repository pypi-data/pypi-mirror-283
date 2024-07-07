# Simple Screen

Provee una serie de funciones basadas en curses, para permitir usar print e input de forma posicionada y jugar con colores.

La idea es poder crear programas que vayan enfrentando a situaciones algo mas reales que con print e input, pero sin necesitar librerias que metan ruido a la hora de enseñar. Es un paso previo.

## Funciones que aporta

Aquí tienes un listado de las funciones públicas del archivo proporcionado junto con una breve explicación de cada una:

1. **pause(ms: int)**
   - Pausa la ejecución del programa durante una cantidad de milisegundos especificada.

2. **init()**
   - Inicializa la pantalla de curses y configura los parámetros básicos como dimensiones, colores y pares de colores.

3. **finish()**
   - Finaliza el uso de curses y restaura la configuración del terminal a su estado original.

4. **cls(refresh: bool = True)**
   - Limpia la pantalla y opcionalmente refresca la pantalla para mostrar los cambios inmediatamente.

5. **locate(x: int, y: int, cad: str = None)**
   - Mueve el cursor a la posición (x, y) especificada en la pantalla.
   - Si x o y está fuera de los límites de la terminal se produce una excepcion OverflowError.
   - Si se informa cad, lo imprime en la posición indicada, sin salto de línea.

6. **Print(cadena: object = "", refresh: bool = True)**
   - Imprime una cadena en la pantalla en la posición actual del cursor y opcionalmente refresca la pantalla para mostrar los cambios inmediatamente.
   - Situa el cursor en la línea siguiente (salto de línea siempre)

7. **Input(mensaje: str = "") -> str**
   - Muestra un mensaje en la pantalla y espera la entrada del usuario. Devuelve la cadena de entrada del usuario.

8. **inkey(timeout: int = 100) -> str**
   - Espera el tiempo indicado en timeout en milisegundos para la pulsacion de una tecla. Si no se pulsa nada devuelve "" en otro caso devuelve su caracter o el nombre de la tecla si es especial.

   - En el caso de BACKSPACE puede devolver cualquiera de los valores `chr(8) o chr(127)` por tanto si quieres preguntar directamente por BACKSPACE debes preguntar
   ```
   if simple_screen.inkey() in simple_screen.BACKSPACE:
   ```
   en lugar de 
   ```
   if simple_screen.inkey() == simple_screen.BACKSPACE
   ```
   que no se cumplirá nunca.

9. **pair(_pen: Color, _paper: Color, refresh: bool = True)**
   - Configura el par de colores activo con los colores de primer plano (_pen) y fondo (_paper) especificados, y opcionalmente refresca la pantalla para mostrar los cambios inmediatamente.

10. **pen(color: Color, refresh: bool = True)**
   - Cambia el color del "bolígrafo" (texto) al color de primer plano especificado y opcionalmente refresca la pantalla para mostrar los cambios inmediatamente.

11. **paper(color: Color, refresh: bool = True)**
    - Cambia el color del "papel" (fondo) al color de fondo especificado y opcionalmente refresca la pantalla para mostrar los cambios inmediatamente.

12. **center(cad: str) -> int**
    - Devuelve la columna en que debe imprimirse la cadena cad para estar centrada en la 
    ventana actual.

13. **center_print(cad: str, fila: int = 0)**
    - Imprime la cadena cad centrada en la fila que se indique, o en cero.

14. **app(func: Callable[..., None]) -> Callable[..., None]**
    - Decorador que asegura que la función proporcionada se ejecute en un contexto de curses y llama a `_end()` al finalizar la ejecución.

15. **Simple_ScreenContextManager**
    - Clase manejadora de contexto para asegurar que `finish()` se llame al salir del bloque `with`.

16. **Atributos** Se pueden activar y desactivar los siguientes atributos del texto. Por ejemplo, para activar la negrita usar **A_BOLD.on()** y para volver a desactivar **A_BOLD.off()**.
     - **A_NORMAL**: Atributo estándar sin formato especial aplicado.
     - **A_STANDOUT**: Atributo que hace que el texto se destaque, usualmente mediante la inversión de colores o un cambio de color de fondo.
     - **A_UNDERLINE**: Atributo que subraya el texto.
     - **A_REVERSE**: Atributo que invierte los colores del texto y del fondo.
     - **A_BLINK**: Atributo que hace que el texto parpadee.
     - **A_DIM**: Atributo que reduce el brillo del texto.
     - **A_BOLD**: Atributo que hace que el texto sea negrita o más brillante.
     - **A_INVIS**: Atributo que hace que el texto sea invisible.


### Explicación detallada de las funciones internas:

1. **_init_curses()**
   - Inicializa la pantalla de curses, configura el modo cbreak y empieza el modo de color. Devuelve la pantalla inicializada.

2. **_end(scr)**
   - Restaura la configuración del terminal y finaliza el uso de curses.

3. **_create_color(ix: int, color: Color)**
   - Crea un color en curses utilizando el índice y el valor de color especificados.

4. **_retrievePos()**
   - Actualiza la posición del cursor global `POS` obteniendo la posición actual del cursor en la pantalla.

Estas funciones y clases proporcionan una interfaz para manejar de manera más sencilla la biblioteca curses en Python, permitiendo inicializar y finalizar correctamente el entorno curses, manipular colores, limpiar la pantalla, mover el cursor, y manejar entradas y salidas de texto en la consola.