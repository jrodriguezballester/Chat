# Práctica 4.1 - Sockets

<https://github.com/jrodriguezballester/Chat.git>
![logo Python](/Imagenes/Python.png)


## Ejercicio 1 - Sockets

Vamos a crear un chatroom con una interfaz visual que nos proporciona el módulo tkinter de Python. Para ello crearemos un servidor multihilo a través de los cuales mantendrá las conexiones de cada uno de los clientes y será capaz de registrar cada uno de los eventos que le llegan y distribuirlos a los clientes.

Como no queremos arriesgar a que haya pérdidas de datos, crearemos tanto la parte de servidor como la de cliente sobre sockets TCP.

Dos ejemplos a partir de los cuales podéis desarrollar la práctica.

<https://www.geeksforgeeks.org/simple-chat-room-using-python/>
<https://www.geeksforgeeks.org/gui-chat-application-using-tkinter-in-python/>

## Resolución

### Servidor

Se crea un servidor con la direccion IP local para conectar varios ordenadores dentro de la misma red.
La consola del servidor informa de la Ip a la que tienen que conectarse los clientes, la Ip del cliente y el hilo.
El servidor guarda los nombres de los clientes, sus direcciones y los vincula con el hilo que crea para cada conexión.
Cuando un cliente empieza y finaliza la conexión es notificado al resto de clientes

![Consola Servidor ](/Imagenes/servidor1.png)

### Cliente

Se crea el una interface cliente con la libreria tkinter.

En una primera pantalla se pide que se identifique el cliente, y crea un hilo esperando recibir mensajes del servidor.

![Primera pantalla Cliente ](/Imagenes/clientelogin.png)

En la pantalla principal, se muestran la fecha, hora y autor de los mensajes, en la parte inferior se envian los mensajes. los mensajes propios se muestran en verde en el lado derecho

![Pantalla Principal ](/Imagenes/cliente4.png)
![Pantalla Principal ](/Imagenes/cliente3.png)
