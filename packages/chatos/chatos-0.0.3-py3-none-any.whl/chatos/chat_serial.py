import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import serial
import serial.tools.list_ports

class ChatSerial:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Serial ")

        self.ser = None

        # Frame para los controles superiores
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(padx=10, pady=5)

        # Crear un Combobox para seleccionar el puerto serie
        self.puerto_combobox = ttk.Combobox(self.top_frame, state='readonly')
        self.puerto_combobox.pack(side=tk.LEFT, padx=5)

        # Botón para actualizar la lista de puertos
        self.actualizar_button = tk.Button(self.top_frame, text="Actualizar Puertos", command=self.actualizar_puertos)
        self.actualizar_button.pack(side=tk.LEFT, padx=5)

        # Botón para conectar al puerto seleccionado
        self.conectar_button = tk.Button(self.top_frame, text="Conectar", command=self.conectar_puerto)
        self.conectar_button.pack(side=tk.LEFT, padx=5)

        # Crear la caja de chat
        self.chat_log = scrolledtext.ScrolledText(root, height=15, width=50)
        self.chat_log.pack(padx=10, pady=10)

        # Crear la entrada de mensaje y botón de enviar
        self.enviar_entry = tk.Entry(root, width=40)
        self.enviar_entry.pack(padx=10, pady=5)
        self.enviar_entry.bind("<Return>", self.enviar_mensaje_event)  # Enviar con Enter

        self.enviar_button = tk.Button(root, text="Enviar", command=self.enviar_mensaje)
        self.enviar_button.pack(padx=10, pady=5)

        # Botón para borrar la consola
        self.borrar_button = tk.Button(root, text="Borrar Consola", command=self.borrar_consola)
        self.borrar_button.pack(padx=10, pady=5)

        # Detectar y mostrar los puertos disponibles al inicio
        self.actualizar_puertos()

        # Iniciar el hilo para leer mensajes
        self.leer_hilo = threading.Thread(target=self.leer_mensajes)
        self.leer_hilo.daemon = True
        self.leer_hilo.start()

        # Manejar el cierre de la ventana para cerrar el puerto serial si está abierto
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def enviar_mensaje(self):
        mensaje = self.enviar_entry.get()
        self.enviar_entry.delete(0, tk.END)
        self.chat_log.insert(tk.END, f"Yo: {mensaje}\r\n")
        if self.ser and self.ser.is_open:
            self.ser.write(mensaje.encode()+b'\n')

    def enviar_mensaje_event(self, event):
        self.enviar_mensaje()

    def leer_mensajes(self):
        while True:
            if self.ser and self.ser.is_open:
                try:
                    mensaje = self.ser.readline().decode().strip()
                    if mensaje:
                        self.chat_log.insert(tk.END, f"Otro: {mensaje}\n")
                        self.chat_log.see(tk.END)  # Desplazar automáticamente hacia abajo
                except Exception as e:
                    print("Error al leer mensaje:", e)

    def detectar_puertos(self):
        puertos = serial.tools.list_ports.comports()
        return [puerto.device for puerto in puertos]

    def actualizar_puertos(self):
        puertos = self.detectar_puertos()
        self.puerto_combobox['values'] = puertos
        if puertos:
            self.puerto_combobox.current(0)

    def conectar_puerto(self):
        puerto_seleccionado = self.puerto_combobox.get()
        try:
            self.ser = serial.Serial(puerto_seleccionado, 9600, timeout=0.1)
            self.chat_log.insert(tk.END, f"Conectado a {puerto_seleccionado}\n")
        except Exception as e:
            self.chat_log.insert(tk.END, f"Error al conectar: {e}\n")

    def borrar_consola(self):
        self.chat_log.delete(1.0, tk.END)

    def on_closing(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatSerial(root)
    root.mainloop()
