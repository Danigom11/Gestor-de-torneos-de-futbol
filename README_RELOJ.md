# Enunciado Tarea 4 tema 6: Reloj digital con PySide6

## Título: Creación de un componente visual reutilizable - Reloj digital

### Descripción

Usando la herramienta de diseño de interfaces gráficas Qt Designer, el lenguaje Python y la biblioteca PySide6, crear un componente visual reutilizable que represente un reloj digital y que pueda insertarse en cualquier interfaz gráfica. El reloj deberá poder integrarse en cualquier interfaz gráfica sin depender de elementos externos, gestionando internamente todas sus funcionalidades (hora, temporizador, cronómetro y alarmas) y exponiendo una serie de propiedades configurables y eventos propios. El componente deberá poder funcionar tanto como reloj digital (mostrando la hora actual) como temporizador o cronómetro, permitiendo su uso en distintos contextos.

Por último, se deberá integrar el reloj digital en la aplicación de gestión de torneos de fútbol. En este caso, el reloj servirá para cronometrar los partidos y deberá ser visible en la interfaz durante el desarrollo de un partido. El reloj debe poder configurarse desde la aplicación, y la señal de alarma o aviso del reloj deberá reflejarse en algún componente de la interfaz, mostrando un mensaje cuando se cumpla el tiempo del partido.

### Notas

- Cualquier validación del componente se podrá realizar directamente mediante su integración en la aplicación.
- La configuración del componente desde la aplicación de gestión de torneos deberá realizarse exclusivamente a través de sus propiedades y métodos públicos, sin acceder directamente a variables internas ni a la lógica de funcionamiento del reloj.

---

## Requisitos de la práctica

### 1. Funcionalidades básicas que implementar

- Una propiedad **mode** que determine su modo de funcionamiento.
- Esta propiedad será de tipo enumerado (Enum) y podrá tomar, al menos, los siguientes valores:
  - **clock**: el componente funcionará como reloj digital, mostrando la hora actual y permitiendo el uso de alarmas.
  - **timer**: el componente funcionará como temporizador o cronómetro.

### 2. Funcionalidades de reloj

- Una propiedad booleana para indicar si el formato es de 12 o 24 horas.
- Una propiedad booleana para indicar si queremos activar una alarma.
- El funcionamiento de la alarma consistirá en que se podrá configurar el componente para que, a una determinada hora, se muestre un mensaje.
- Dos propiedades de tipo entero para determinar la hora y el minuto para los cuales queremos programar la alarma.
- Una propiedad de tipo texto (String) para configurar el mensaje de texto que se mostrará cuando se produzca el salto de la alarma.
- Función de alarma: si se programa a una hora determinada, deberá generar un evento o señal cuando se llegue a dicha hora.

### 3. Funcionalidades de temporizador/cronómetro

- El componente deberá poder funcionar en modo temporizador, permitiendo medir el tiempo de forma progresiva o regresiva.
- Gestionar internamente el paso del tiempo mediante un QTimer.
- Permitir iniciar, pausar y reiniciar el conteo del tiempo.
- Disponer de propiedades configurables como:
  - Modo de funcionamiento (reloj / temporizador).
  - Duración del temporizador.
  - Formato de visualización del tiempo.
- El componente deberá emitir una señal o evento cuando se alcance el tiempo configurado en el temporizador.

### 4. Internacionalización (traducciones)

- El componente y la aplicación deberán estar preparados para mostrar textos en distintos idiomas.
- Se deberá investigar el sistema de traducciones de Qt, utilizando las herramientas y clases proporcionadas por PySide6.
- Como mínimo, la aplicación deberá poder mostrarse en dos idiomas distintos.
- El cambio de idioma deberá reflejarse en los textos visibles del componente y de la interfaz (Investigar QTranslator).

---

## Entregables

1. La entrega se realizará en un único fichero comprimido (zip) con el proyecto según modelo MVC.
2. El proyecto (gestión torneo + componente) y el componente reutilizable deberán entregarse por separado en formato ejecutable (.exe) funcional por doble clic.
3. Se deberá incluir un archivo README con consideraciones o instrucciones.

---

## Criterios de evaluación
| Criterio | Puntuación |
| :--- | :--- |
| Creación del componente: clase autónoma con reloj, cronómetro y alarma. | 15% |
| Propiedades y métodos de acceso: getters y setters (modo, formato, alarma). | 10% |
| Eventos y señales: crear alarmTriggered y timerFinished. | 10% |
| Actualización del tiempo: código para refresco cada segundo. | 10% |
| Gestión de alarma: lógica interna sin detener el cronómetro. | 20% |
| Prueba del widget: funcionamiento autónomo como widget independiente. | 10% |
| Reacción a eventos: capturar señal desde la app padre. | 10% |
| Integración y traducciones: integración en app de torneos y uso de QTranslator. | 10% |
---

## Sugerencias para los alumnos

- Definir las propiedades de los componentes como públicas para que aparezcan en el panel de propiedades del componente.
- Definir una interfaz para la definición de los métodos que necesites implementar cuando el componente sea utilizado.
- Se adjunta código de ejemplo para la creación y uso de un nuevo componente.