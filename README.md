# Chat P2P Basado en Consola

Un sistema de chat en tiempo real que utiliza una arquitectura Peer-to-Peer (P2P). En este modelo, cada usuario funciona tanto como cliente como servidor, lo que permite una comunicación directa y descentralizada entre los pares.

## Características

- **TCP** para comunicaciones seguras y confiables.
- **P2P** donde cada usuario actúa como cliente y servidor.
- **Descubrimiento de Pares** mediante la adición de nuevos contactos usando su dirección IP y puerto.
- **Conexión Bidireccional** para una comunicación privada.
- **Interfaz Basada en Consola** para una experiencia de usuario sencilla.
- **Formato** mensajes estructurados en formato JSON.
- **Almacenamiento y Gestión de Contactos** para mantener un registro de pares conectados.
- **Asincronía y Concurrency** utilizando operaciones asíncronas y múltiples hilos.
- **Etiquetas/Nombres de Usuario** para identificar usuarios en una red local.

## Uso

1. Al iniciar, se te pedirá que ingreses un nombre de usuario y un puerto.
2. Una vez ingresados, se mostrará el menú principal con las siguientes opciones:
    - Conectar con otro Peer
    - Enviar mensaje
    - Mostrar contactos
    - Ver mensajes
    - Salir

3. ¡Eso es todo! Puedes comenzar a conectarte con otros pares y chatear.
