import pygame
import random
import math
import json
import os
import time

pygame.init()

# ============================================================
# CONFIGURACIÓN
# ============================================================

ANCHO = 1000
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Mascota Virtual")

reloj = pygame.time.Clock()

FUENTE = pygame.font.SysFont("arial", 22)
FUENTE_GRANDE = pygame.font.SysFont("arial", 42, bold=True)
FUENTE_CHICA = pygame.font.SysFont("arial", 16)

ARCHIVO_GUARDADO = "mascota_data.json"


# ============================================================
# COLORES
# ============================================================

BLANCO = (255, 255, 255)
NEGRO = (30, 30, 30)

MARRON = (157, 95, 48)
MARRON_OSCURO = (104, 57, 25)
MARRON_CLARO = (191, 124, 68)

VERDE = (70, 190, 90)
VERDE_OSCURO = (45, 140, 65)

ROJO = (220, 70, 70)
AMARILLO = (245, 200, 60)

AZUL = (80, 160, 230)
AZUL_OSCURO = (50, 110, 190)

GRIS = (220, 220, 220)
GRIS_OSCURO = (120, 120, 120)

ROSA = (255, 160, 190)
CELESTE = (150, 220, 255)

FONDO = (245, 235, 220)


# ============================================================
# GUARDAR Y CARGAR DATOS
# ============================================================

def cargar_datos():
    datos_iniciales = {
        "hambre": 80,
        "energia": 80,
        "felicidad": 80,
        "limpieza": 80,
        "salud": 100,
        "monedas": 50
    }

    if os.path.exists(ARCHIVO_GUARDADO):
        try:
            with open(ARCHIVO_GUARDADO, "r") as archivo:
                datos = json.load(archivo)

            for clave in datos_iniciales:
                if clave not in datos:
                    datos[clave] = datos_iniciales[clave]

            return datos

        except:
            return datos_iniciales

    return datos_iniciales


def guardar_datos(datos):
    try:
        with open(ARCHIVO_GUARDADO, "w") as archivo:
            json.dump(datos, archivo)
    except:
        pass


datos = cargar_datos()


# ============================================================
# FUNCIONES GENERALES
# ============================================================

def limitar(valor):
    return max(0, min(100, valor))


def texto(superficie, contenido, fuente, color, x, y, centrado=True):

    render = fuente.render(contenido, True, color)

    rect = render.get_rect()

    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    superficie.blit(render, rect)


def boton(rect, contenido, color, hover_color=None):

    mouse = pygame.mouse.get_pos()

    color_actual = color

    if rect.collidepoint(mouse) and hover_color:
        color_actual = hover_color

    pygame.draw.rect(pantalla, color_actual, rect, border_radius=15)
    pygame.draw.rect(pantalla, NEGRO, rect, 3, border_radius=15)

    texto(
        pantalla,
        contenido,
        FUENTE,
        NEGRO,
        rect.centerx,
        rect.centery
    )


def barra(nombre, valor, y, color):

    x = 20
    ancho = 180
    alto = 24

    texto(
        pantalla,
        nombre,
        FUENTE_CHICA,
        NEGRO,
        x,
        y - 20,
        centrado=False
    )

    pygame.draw.rect(
        pantalla,
        GRIS,
        (x, y, ancho, alto),
        border_radius=10
    )

    ancho_valor = int(ancho * valor / 100)

    pygame.draw.rect(
        pantalla,
        color,
        (x, y, ancho_valor, alto),
        border_radius=10
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (x, y, ancho, alto),
        2,
        border_radius=10
    )

    texto(
        pantalla,
        str(int(valor)),
        FUENTE_CHICA,
        NEGRO,
        x + ancho + 10,
        y + 3,
        centrado=False
    )


# ============================================================
# MASCOTA
# ============================================================

class Mascota:

    def __init__(self):

        self.x = ANCHO // 2
        self.y = 390

        self.base_y = self.y

        self.ojos_cerrados = False

        self.boca_abierta = False

        self.tiempo = 0

        self.mensaje = ""
        self.tiempo_mensaje = 0


    def actualizar(self):

        self.tiempo += 0.05

        if not self.ojos_cerrados:

            self.y = self.base_y + math.sin(self.tiempo) * 5

        if self.tiempo_mensaje > 0:
            self.tiempo_mensaje -= 1

        else:
            self.mensaje = ""


    def hablar(self, mensaje):

        self.mensaje = mensaje
        self.tiempo_mensaje = 120


    def dibujar(self):

        # Sombra
        pygame.draw.ellipse(
            pantalla,
            (180, 160, 140),
            (
                self.x - 110,
                self.y + 120,
                220,
                35
            )
        )

        # Cuerpo principal
        puntos = [
            (self.x, self.y - 170),
            (self.x - 100, self.y - 50),
            (self.x - 120, self.y + 70),
            (self.x - 70, self.y + 130),
            (self.x + 70, self.y + 130),
            (self.x + 120, self.y + 70),
            (self.x + 100, self.y - 50)
        ]

        pygame.draw.polygon(
            pantalla,
            MARRON,
            puntos
        )

        pygame.draw.polygon(
            pantalla,
            MARRON_OSCURO,
            puntos,
            5
        )

        # Mejillas
        pygame.draw.circle(
            pantalla,
            MARRON_CLARO,
            (self.x - 65, self.y + 45),
            18
        )

        pygame.draw.circle(
            pantalla,
            MARRON_CLARO,
            (self.x + 65, self.y + 45),
            18
        )

        # Ojos
        if self.ojos_cerrados:

            pygame.draw.arc(
                pantalla,
                NEGRO,
                (
                    self.x - 70,
                    self.y - 60,
                    45,
                    30
                ),
                math.pi,
                2 * math.pi,
                3
            )

            pygame.draw.arc(
                pantalla,
                NEGRO,
                (
                    self.x + 25,
                    self.y - 60,
                    45,
                    30
                ),
                math.pi,
                2 * math.pi,
                3
            )

        else:

            pygame.draw.ellipse(
                pantalla,
                BLANCO,
                (
                    self.x - 75,
                    self.y - 70,
                    50,
                    70
                )
            )

            pygame.draw.ellipse(
                pantalla,
                BLANCO,
                (
                    self.x + 25,
                    self.y - 70,
                    50,
                    70
                )
            )

            pygame.draw.ellipse(
                pantalla,
                NEGRO,
                (
                    self.x - 60,
                    self.y - 45,
                    22,
                    38
                )
            )

            pygame.draw.ellipse(
                pantalla,
                NEGRO,
                (
                    self.x + 40,
                    self.y - 45,
                    22,
                    38
                )
            )

        # Boca
        if self.boca_abierta:

            pygame.draw.ellipse(
                pantalla,
                NEGRO,
                (
                    self.x - 35,
                    self.y + 50,
                    70,
                    45
                )
            )

        else:

            pygame.draw.arc(
                pantalla,
                NEGRO,
                (
                    self.x - 40,
                    self.y + 25,
                    80,
                    65
                ),
                0,
                math.pi,
                4
            )

        # Mensaje
        if self.mensaje != "":

            pygame.draw.rect(
                pantalla,
                BLANCO,
                (
                    self.x - 150,
                    self.y - 250,
                    300,
                    60
                ),
                border_radius=15
            )

            pygame.draw.rect(
                pantalla,
                NEGRO,
                (
                    self.x - 150,
                    self.y - 250,
                    300,
                    60
                ),
                3,
                border_radius=15
            )

            texto(
                pantalla,
                self.mensaje,
                FUENTE,
                NEGRO,
                self.x,
                self.y - 220
            )


mascota = Mascota()


# ============================================================
# COMIDA
# ============================================================

comidas = {
    "🍎": {
        "nombre": "Manzana",
        "hambre": 12,
        "felicidad": 4,
        "precio": 3
    },

    "🍕": {
        "nombre": "Pizza",
        "hambre": 25,
        "felicidad": 10,
        "precio": 8
    },

    "🍔": {
        "nombre": "Hamburguesa",
        "hambre": 35,
        "felicidad": 15,
        "precio": 12
    }
}


# ============================================================
# VARIABLES DEL JUEGO
# ============================================================

habitacion = "casa"

jugando_minijuego = False

pelota_x = 500
pelota_y = 500

pelota_dx = 5
pelota_dy = -5

barra_x = 430

puntos_juego = 0

ultimo_guardado = time.time()

ultimo_deterioro = time.time()


# ============================================================
# DIBUJAR CASA
# ============================================================

def dibujar_casa():

    pantalla.fill(FONDO)

    # Piso
    pygame.draw.rect(
        pantalla,
        (220, 190, 160),
        (0, 540, ANCHO, 160)
    )

    # Cuadro decorativo
    pygame.draw.rect(
        pantalla,
        CELESTE,
        (700, 120, 180, 120)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (700, 120, 180, 120),
        5
    )

    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (790, 175),
        35
    )

    # Título
    texto(
        pantalla,
        "Mi Mascota Virtual",
        FUENTE_GRANDE,
        MARRON_OSCURO,
        ANCHO // 2,
        50
    )

    mascota.dibujar()


# ============================================================
# COCINA
# ============================================================

def dibujar_cocina():

    pantalla.fill((255, 240, 220))

    texto(
        pantalla,
        "🍽️ Cocina",
        FUENTE_GRANDE,
        NEGRO,
        ANCHO // 2,
        50
    )

    # Mesa
    pygame.draw.rect(
        pantalla,
        MARRON_CLARO,
        (300, 480, 400, 80),
        border_radius=10
    )

    mascota.dibujar()

    texto(
        pantalla,
        "Elegí algo para comer",
        FUENTE,
        NEGRO,
        ANCHO // 2,
        570
    )


# ============================================================
# DORMITORIO
# ============================================================

def dibujar_dormitorio():

    pantalla.fill((45, 60, 110))

    texto(
        pantalla,
        "😴 Dormitorio",
        FUENTE_GRANDE,
        BLANCO,
        ANCHO // 2,
        50
    )

    # Luna
    pygame.draw.circle(
        pantalla,
        BLANCO,
        (850, 100),
        40
    )

    # Cama
    pygame.draw.rect(
        pantalla,
        (180, 120, 170),
        (280, 450, 440, 120),
        border_radius=20
    )

    pygame.draw.rect(
        pantalla,
        BLANCO,
        (300, 420, 160, 70),
        border_radius=15
    )

    mascota.dibujar()


# ============================================================
# BAÑO
# ============================================================

def dibujar_bano():

    pantalla.fill((190, 235, 250))

    texto(
        pantalla,
        "🛁 Baño",
        FUENTE_GRANDE,
        NEGRO,
        ANCHO // 2,
        50
    )

    # Bañera
    pygame.draw.rect(
        pantalla,
        BLANCO,
        (300, 430, 400, 130),
        border_radius=40
    )

    pygame.draw.rect(
        pantalla,
        AZUL,
        (320, 450, 360, 70),
        border_radius=30
    )

    mascota.dibujar()


# ============================================================
# MINIJUEGO
# ============================================================

def dibujar_minijuego():

    global pelota_x
    global pelota_y
    global pelota_dx
    global pelota_dy
    global barra_x
    global puntos_juego

    pantalla.fill((25, 30, 50))

    texto(
        pantalla,
        "🎮 Mini Juego",
        FUENTE_GRANDE,
        BLANCO,
        ANCHO // 2,
        50
    )

    texto(
        pantalla,
        "Mové la barra con las flechas",
        FUENTE,
        BLANCO,
        ANCHO // 2,
        90
    )

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        barra_x -= 8

    if teclas[pygame.K_RIGHT]:
        barra_x += 8

    barra_x = max(0, min(ANCHO - 160, barra_x))

    pelota_x += pelota_dx
    pelota_y += pelota_dy

    if pelota_x < 15 or pelota_x > ANCHO - 15:
        pelota_dx *= -1

    if pelota_y < 120:
        pelota_dy *= -1

    # Barra
    barra = pygame.Rect(
        barra_x,
        620,
        160,
        20
    )

    pygame.draw.rect(
        pantalla,
        VERDE,
        barra,
        border_radius=10
    )

    # Pelota
    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (int(pelota_x), int(pelota_y)),
        15
    )

    # Colisión
    if (
        pelota_y + 15 >= 620
        and pelota_y + 15 <= 650
        and barra_x <= pelota_x <= barra_x + 160
        and pelota_dy > 0
    ):

        pelota_dy *= -1

        puntos_juego += 1

    # Perdió
    if pelota_y > ALTO + 30:

        puntos_juego = 0

        pelota_x = ANCHO // 2
        pelota_y = 300

        pelota_dx = random.choice([-5, 5])
        pelota_dy = -5

        mascota.hablar("¡Casi!")

    texto(
        pantalla,
        f"Puntos: {puntos_juego}",
        FUENTE,
        BLANCO,
        100,
        50
    )

    texto(
        pantalla,
        "ESC para volver",
        FUENTE_CHICA,
        BLANCO,
        ANCHO - 100,
        680
    )


# ============================================================
# BARRA SUPERIOR
# ============================================================

def dibujar_estadisticas():

    barra(
        "Hambre",
        datos["hambre"],
        30,
        ROJO
    )

    barra(
        "Energía",
        datos["energia"],
        90,
        AZUL
    )

    barra(
        "Felicidad",
        datos["felicidad"],
        150,
        AMARILLO
    )

    barra(
        "Limpieza",
        datos["limpieza"],
        210,
        CELESTE
    )

    barra(
        "Salud",
        datos["salud"],
        270,
        VERDE
    )

    texto(
        pantalla,
        f"🪙 {datos['monedas']}",
        FUENTE,
        AMARILLO,
        110,
        330
    )


# ============================================================
# MENÚ INFERIOR
# ============================================================

def dibujar_menu():

    botones = {}

    nombres = [
        ("🏠", "casa"),
        ("🍽️", "cocina"),
        ("😴", "dormitorio"),
        ("🛁", "bano"),
        ("🎮", "juego")
    ]

    x = 250

    for emoji, nombre in nombres:

        rect = pygame.Rect(
            x,
            620,
            100,
            60
        )

        boton(
            rect,
            emoji,
            GRIS,
            BLANCO
        )

        botones[nombre] = rect

        x += 110

    return botones


# ============================================================
# INTERACCIÓN
# ============================================================

def alimentar(tipo):

    comida = comidas[tipo]

    if datos["monedas"] < comida["precio"]:

        mascota.hablar("¡No tengo monedas!")
        return

    datos["monedas"] -= comida["precio"]

    datos["hambre"] = limitar(
        datos["hambre"] + comida["hambre"]
    )

    datos["felicidad"] = limitar(
        datos["felicidad"] + comida["felicidad"]
    )

    mascota.boca_abierta = True

    mascota.hablar(
        f"¡Qué rico! {comida['nombre']} 😋"
    )


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

ejecutando = True

while ejecutando:

    reloj.tick(60)

    mascota.actualizar()

    # --------------------------------------------------------
    # DETERIORO CON EL TIEMPO
    # --------------------------------------------------------

    if time.time() - ultimo_deterioro > 8:

        datos["hambre"] = limitar(
            datos["hambre"] - 1
        )

        datos["energia"] = limitar(
            datos["energia"] - 1
        )

        datos["felicidad"] = limitar(
            datos["felicidad"] - 0.5
        )

        datos["limpieza"] = limitar(
            datos["limpieza"] - 0.5
        )

        if (
            datos["hambre"] < 20
            or datos["limpieza"] < 20
        ):

            datos["salud"] = limitar(
                datos["salud"] - 1
            )

        ultimo_deterioro = time.time()


    # --------------------------------------------------------
    # EVENTOS
    # --------------------------------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            guardar_datos(datos)

            ejecutando = False


        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                if habitacion == "juego":

                    habitacion = "casa"

                    mascota.hablar(
                        "¡Buen juego!"
                    )


        if evento.type == pygame.MOUSEBUTTONDOWN:

            mouse = pygame.mouse.get_pos()

            # ------------------------------------------------
            # COCINA
            # ------------------------------------------------

            if habitacion == "cocina":

                comida_rects = {
                    "🍎": pygame.Rect(300, 580, 100, 60),
                    "🍕": pygame.Rect(450, 580, 100, 60),
                    "🍔": pygame.Rect(600, 580, 100, 60)
                }

                for tipo, rect in comida_rects.items():

                    if rect.collidepoint(mouse):

                        alimentar(tipo)


            # ------------------------------------------------
            # DORMITORIO
            # ------------------------------------------------

            if habitacion == "dormitorio":

                dormir_rect = pygame.Rect(
                    760,
                    580,
                    200,
                    60
                )

                if dormir_rect.collidepoint(mouse):

                    mascota.ojos_cerrados = True

                    datos["energia"] = limitar(
                        datos["energia"] + 30
                    )

                    mascota.hablar("Zzz... 😴")


            # ------------------------------------------------
            # BAÑO
            # ------------------------------------------------

            if habitacion == "bano":

                bano_rect = pygame.Rect(
                    760,
                    580,
                    200,
                    60
                )

                if bano_rect.collidepoint(mouse):

                    datos["limpieza"] = limitar(
                        datos["limpieza"] + 30
                    )

                    datos["felicidad"] = limitar(
                        datos["felicidad"] + 5
                    )

                    mascota.hablar("¡Qué limpio! ✨")


    # --------------------------------------------------------
