import tkinter as tk
from tkinter import messagebox, colorchooser
import math
import os
import random
from pathlib import Path
import pygame
from PIL import Image, ImageDraw, ImageFont, ImageTk

# ── FORZAR RUTA ABSOLUTA ──────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_FONDO_ROSCO   = os.path.join(BASE_DIR, "fondo_rosco.png")
PATH_FONDO_CONTROL = os.path.join(BASE_DIR, "fondo_control.png")
# ──────────────────────────────────────────────────────────────────────────

# ── LAYOUT DE PANTALLAS ───────────────────────────────────────────────────
# Pantalla secundaria (roscos):  1600x900, a la IZQUIERDA  → x=0
# Pantalla principal (controles): 1280x720, a la DERECHA   → x=1600
SECONDARY_X = 0
SECONDARY_Y = 0
SECONDARY_W = 1600
SECONDARY_H = 900
PRIMARY_X   = 1600   # la secundaria ocupa 0..1599, la principal empieza en 1600
PRIMARY_Y   = 0
PRIMARY_W   = 1280
PRIMARY_H   = 720
CTRL_W      = PRIMARY_W // 2   # 640  — mitad exacta, lado a lado
CTRL_H      = PRIMARY_H        # 720
# ──────────────────────────────────────────────────────────────────────────

COLOR_FONDO_ALT    = "#0a0f24"
COLOR_ACIERTO      = "#1f9c54"
COLOR_ERROR        = "#ff3333"
COLOR_PASAPALABRA  = "#f1c40f"
COLOR_ACTUAL       = "#3498db"
COLOR_RESPUESTA    = "#5dade2"

FUENTE_LETRAS    = ("Segoe UI", 24, "bold")
FUENTE_RELOJ     = ("Consolas", 40, "bold")
FUENTE_PISTA     = ("Helvetica", 14, "bold")
FUENTE_TITULO    = ("Segoe UI", 18, "bold")
FUENTE_RESPUESTA = ("Segoe UI", 12, "italic")

BIBLIOTECA_ROSCOS = {
     "Rosco Real 1 ✓": [
  {"letra": "A", "pista": "Con la A: Dirigir a alguien una arenga.", "respuesta": "ARENGAR"},
  {"letra": "B", "pista": "Con la B: Dicho de una planta, nacer o salir de la tierra.", "respuesta": "BROTAR"},
  {"letra": "C", "pista": "Con la C: En el interior de los edificios, techo de superficie plana y lisa.", "respuesta": "CIELORRASO"},
  {"letra": "D", "pista": "Con la D: Pliegue que como remate se hace a la ropa en los bordes para coserla.", "respuesta": "DOBLADILLO"},
  {"letra": "E", "pista": "Con la E: Dicho de una embarcación, asentarse en arena, piedras o rocas y quedar inmovilizada en ellas.", "respuesta": "ENCALLAR - ENCALLAD"},
  {"letra": "F", "pista": "Con la F: Cada una de las divisiones académicas de una universidad en la que se agrupan los estudios de una carrera determinada.", "respuesta": "FACULTAD"},
  {"letra": "G", "pista": "Con la G: Hacer garabatos con la pluma, el lápiz, etc.", "respuesta": "GARABATEAR"},
  {"letra": "H", "pista": "Contiene la H: Zanja defensiva que permite disparar a cubierto del enemigo.", "respuesta": "TRINCHERA"},
  {"letra": "I", "pista": "Con la I: Encuentro de dos líneas, dos superficies o dos sólidos que se cortan entre sí.", "respuesta": "INTERSECCIÓN"},
  {"letra": "J", "pista": "Con la J: Tirar de algo o de alguien.", "respuesta": "JALAR"},
  {"letra": "L", "pista": "Con la L: Que padece lepra.", "respuesta": "LEPROSO"},
  {"letra": "M", "pista": "Con la M: Banda mexicana de pop rock formada en 1986 e intérprete de canciones como Mariposa Traicionera.", "respuesta": "MANÁ"},
  {"letra": "N", "pista": "Con la N: Que se puede negar.", "respuesta": "NEGABLE"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Apretado, ajustado.", "respuesta": "CEÑIDO"},
  {"letra": "O", "pista": "Con la O: Blanco para ejercitarse en el tiro.", "respuesta": "OBJETIVO"},
  {"letra": "P", "pista": "Con la P: Último signo del zodíaco de agua que representa a las personas nacidas entre el 19 de febrero y el 20 de marzo.", "respuesta": "PISCIS"},
  {"letra": "Q", "pista": "Con la Q: Por contraposición a físico, concerniente a la composición de los cuerpos.", "respuesta": "QUÍMICA"},
  {"letra": "R", "pista": "Con la R: Pérdida grande de los bienes de fortuna.", "respuesta": "RUINA"},
  {"letra": "S", "pista": "Con la S: Apellido de Claudia, modelo alemana que formó el trío de las supermodelos más famosas de los años 90.", "respuesta": "SCHIFFER"},
  {"letra": "T", "pista": "Con la T: Tronco del cuerpo humano.", "respuesta": "TORSO"},
  {"letra": "U", "pista": "Contiene la U: Apellido de Sigmund, médico neurólogo austríaco considerado el padre del psicoanálisis.", "respuesta": "FREUD"},
  {"letra": "V", "pista": "Con la V: Que practica el veganismo.", "respuesta": "VEGANO"},
  {"letra": "X", "pista": "Contiene la X: Situar algo en un determinado contexto.", "respuesta": "CONTEXTUALIZAR"},
  {"letra": "Y", "pista": "Contiene la Y: Diminutivo de rayo.", "respuesta": "RAYITO"},
  {"letra": "Z", "pista": "Contiene la Z: Pizza de origen napolitano rellena y doblada en forma de media luna.", "respuesta": "CALZONE"}
],
    "Rosco Real 2 ✓": [
  {"letra": "A", "pista": "Con la A: Hacer ampollas en la piel.", "respuesta": "AMPOLLAR"},
  {"letra": "B", "pista": "Con la B: Armas arrojadizas propias de los indígenas de Australia que lanzadas pueden volver al punto de partida.", "respuesta": "BOOMERANG"},
  {"letra": "C", "pista": "Con la C: Territorio dominado y administrado por una potencia extranjera.", "respuesta": "COLONIA"},
  {"letra": "D", "pista": "Con la D: Sustancia que se utiliza como medicamento.", "respuesta": "DROGA"},
  {"letra": "E", "pista": "Con la E: Aquello que constituye la naturaleza de las cosas, lo permanente e invariable en ellas.", "respuesta": "ESENCIA"},
  {"letra": "F", "pista": "Con la F: Animal salvaje o agresivo.", "respuesta": "FIERA - FELINA"},
  {"letra": "G", "pista": "Con la G: Sigla con la que se identifica el gas natural comprimido utilizado en vehículos.", "respuesta": "GNC"},
  {"letra": "H", "pista": "Con la H: Persona que por testamento o por ley sucede en una herencia.", "respuesta": "HEREDERO"},
  {"letra": "I", "pista": "Con la I: Que no se mueve.", "respuesta": "INMÓVIL"},
  {"letra": "J", "pista": "Con la J: Dicho de un deportista de categoría de edad inmediatamente inferior a las del senior.", "respuesta": "JUNIOR - JUVENIL"},
  {"letra": "L", "pista": "Con la L: Nombre de pila de la abogada argentina reconocida como la fan número uno de Susana Jiménez.", "respuesta": "LORNA"},
  {"letra": "M", "pista": "Con la M: Movimiento periódico de ascenso y descenso de las aguas del mar producido por la atracción del sol y la luna.", "respuesta": "MAREA"},
  {"letra": "N", "pista": "Con la N: Claro, evidente.", "respuesta": "NOTORIO - NÍTIDO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Aguardiente de graduación alcohólica muy elevada obtenido por la distilación de vinos y añejado en roble.", "respuesta": "COÑAC"},
  {"letra": "O", "pista": "Con la O: Decir o exponer qué cantidad se está dispuesto a pagar por algo.", "respuesta": "OFERTAR"},
  {"letra": "P", "pista": "Con la P: Ingrediente comestible que se extrae del tronco de ciertas especies de palmeras de las regiones tropicales.", "respuesta": "PALMITO"},
  {"letra": "Q", "pista": "Contiene la Q: Antónimo de tranquilo.", "respuesta": "INTRANQUILO"},
  {"letra": "R", "pista": "Con la R: En las monedas y medallas, cara opuesta al anverso.", "respuesta": "REVERSO"},
  {"letra": "S", "pista": "Con la S: Nombre del filósofo clásico griego a quien se le atribuye la frase 'Solo sé que no sé nada'.", "respuesta": "SÓCRATES"},
  {"letra": "T", "pista": "Con la T: Persona apasionada por el automovilismo.", "respuesta": "TUERCA"},
  {"letra": "U", "pista": "Contiene la U: Dicho de un mecanismo o proceso parcialmente automático.", "respuesta": "SEMIAUTOMÁTICO"},
  {"letra": "V", "pista": "Con la V: Taller donde se labra y se corta el vidrio.", "respuesta": "VIDRIERÍA"},
  {"letra": "X", "pista": "Contiene la X: Doctrina que funda el conocimiento sobre la experiencia inmediata de la existencia propia.", "respuesta": "EXISTENCIALISMO"},
  {"letra": "Y", "pista": "Con la Y: Caimán del litoral argentino.", "respuesta": "YACARÉ"},
  {"letra": "Z", "pista": "Contiene la Z: Apellido de Marta, cantante española intérprete de temas como Desesperada.", "respuesta": "SÁNCHEZ"}
],
    "Rosco Real 3 ✓": [
  {"letra": "A", "pista": "Con la A: Persona que se dedica a la astrología.", "respuesta": "ASTRÓLOGO"},
  {"letra": "B", "pista": "Con la B: Nombre de la famosa playa de Mar del Plata ubicada frente al centro urbano donde se encuentran los lobos marinos.", "respuesta": "BRISTOL"},
  {"letra": "C", "pista": "Con la C: Taller o tienda donde trabaja el carpintero.", "respuesta": "CARPINTERÍA"},
  {"letra": "D", "pista": "Con la D: Decir el nombre de cada una de las letras que constituyen una palabra.", "respuesta": "DELETREAR"},
  {"letra": "E", "pista": "Con la E: Poner en casillas.", "respuesta": "ENCASILLAR"},
  {"letra": "F", "pista": "Con la F: Hueso que forma la parte anterior y superior del cráneo y que en la primera edad se compone de dos mitades.", "respuesta": "FRONTAL"},
  {"letra": "G", "pista": "Con la G: Dicho de una persona nacida bajo el signo zodiacal de Géminis.", "respuesta": "GEMINIANO"},
  {"letra": "H", "pista": "Con la H: Persona alojada en un establecimiento de hostelería.", "respuesta": "HUÉSPED"},
  {"letra": "I", "pista": "Con la I: Necesario, obligatorio.", "respuesta": "INDISPENSABLE"},
  {"letra": "J", "pista": "Contiene la J: Animal que simboliza el signo zodiacal Cáncer.", "respuesta": "CANGREJO"},
  {"letra": "L", "pista": "Con la L: Ágil, veloz, pronto.", "respuesta": "LIGERO"},
  {"letra": "M", "pista": "Con la M: Movimiento que consiste en un giro lateral del cuerpo con las manos en el suelo y las piernas extendidas.", "respuesta": "MEDIALUNA"},
  {"letra": "N", "pista": "Con la N: País centroamericano cuya capital y ciudad más poblada es Managua.", "respuesta": "NICARAGUA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Limpiar el cristal o cualquier otra cosa lustrosa que estaba empañada.", "respuesta": "DESEMPAÑAR"},
  {"letra": "O", "pista": "Con la O: Que tiene ocho sílabas, aplicado a un verso.", "respuesta": "OCTOSÍLABO"},
  {"letra": "P", "pista": "Con la P: Utensilio para fumar consistente en un tubo con boquilla y una cazoleta.", "respuesta": "PIPA - PIPETA"},
  {"letra": "Q", "pista": "Contiene la Q: Conjunto de piezas duras y resistentes que da consistencia al cuerpo de los animales.", "respuesta": "ESQUELETO"},
  {"letra": "R", "pista": "Con la R: Complejo hotelero.", "respuesta": "RESORT"},
  {"letra": "S", "pista": "Con la S: Botes que dan las piedras lanzadas sobre la superficie del agua.", "respuesta": "SAPITO"},
  {"letra": "T", "pista": "Con la T: Apodo del gato que persigue incansablemente al ratón Jerry.", "respuesta": "TOM"},
  {"letra": "U", "pista": "Contiene la U: Diminutivo de nuca.", "respuesta": "NUQUITA"},
  {"letra": "V", "pista": "Con la V: Abertura en un muro o pared donde se coloca un elemento y da luz y ventilación.", "respuesta": "VENTANA"},
  {"letra": "X", "pista": "Contiene la X: Hacer operaciones destinadas a descubrir, comprobar o demostrar determinados fenómenos científicos.", "respuesta": "EXPERIMENTAR - EXPERIMENTO"},
  {"letra": "Y", "pista": "Contiene la Y: Cantar payadas.", "respuesta": "PAYAR"},
  {"letra": "Z", "pista": "Contiene la Z: Administrar el sacramento del bautismo a alguien.", "respuesta": "BAUTIZAR"}
],
    "Rosco Real 4 ✓": [
  {"letra": "A", "pista": "Con la A: Medicamento o sustancia que sirve para combatir la gripe.", "respuesta": "ANTIGRIPAL"},
  {"letra": "B", "pista": "Con la B: Que borra.", "respuesta": "BORRADOR"},
  {"letra": "C", "pista": "Con la C: Persona propuesta para un cargo, premio o distinción, aunque no lo solicite.", "respuesta": "CANDIDATO"},
  {"letra": "D", "pista": "Con la D: Número natural que sigue al 17.", "respuesta": "DIECIOCHO"},
  {"letra": "E", "pista": "Con la E: Poner espacio entre las cosas.", "respuesta": "ESPACIAR"},
  {"letra": "F", "pista": "Con la F: Nube de humo que anuncia el resultado de la votación en la elección del Papa.", "respuesta": "FUMATA"},
  {"letra": "G", "pista": "Con la G: Sabor que tienen las cosas.", "respuesta": "GUSTO"},
  {"letra": "H", "pista": "Contiene la H: Derecha política de ideología extremista.", "respuesta": "ULTRADERECHA"},
  {"letra": "I", "pista": "Con la I: Dotado de inteligencia.", "respuesta": "INTELIGENTE"},
  {"letra": "J", "pista": "Contiene la J: Juego de naipes donde gana quien hace 21 puntos o se queda más cerca.", "respuesta": "BLACKJACK"},
  {"letra": "L", "pista": "Con la L: Que profesa la doctrina de Martín Lutero.", "respuesta": "LUTERANO"},
  {"letra": "M", "pista": "Con la M: Cacahuete.", "respuesta": "MANÍ"},
  {"letra": "N", "pista": "Con la N: Tener necesidad de alguien o de algo.", "respuesta": "NECESITAR"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Armonía y buena correspondencia entre compañeros.", "respuesta": "COMPAÑERISMO"},
  {"letra": "O", "pista": "Con la O: Vibrante tono de verde con tonos amarillos que refiere al color de una aceituna inmadura.", "respuesta": "OLIVA"},
  {"letra": "P", "pista": "Con la P: Barrio de Buenos Aires donde se encuentran el Jardín Japonés y Plaza Italia.", "respuesta": "PALERMO"},
  {"letra": "Q", "pista": "Contiene la Q: Golpe fuerte dado con una raqueta.", "respuesta": "RAQUETAZO"},
  {"letra": "R", "pista": "Con la R: Nueva edición de un libro o publicación.", "respuesta": "REEDICIÓN"},
  {"letra": "S", "pista": "Con la S: Apellido de la cantante estadounidense de nombre Britney.", "respuesta": "SPEARS"},
  {"letra": "T", "pista": "Con la T: Mensaje telegráfico.", "respuesta": "TELEGRAMA"},
  {"letra": "U", "pista": "Contiene la U: País africano con tres capitales que fue sede del mundial 2010.", "respuesta": "SUDÁFRICA"},
  {"letra": "V", "pista": "Con la V: Dicho de un cargo o empleo que está sin proveer.", "respuesta": "VACANTE"},
  {"letra": "X", "pista": "Contiene la X: Que tiene extensión.", "respuesta": "EXTENSO - EXTENSIBLE"},
  {"letra": "Y", "pista": "Contiene la Y: Apellido de Luciano, cantante argentino intérprete de 'Porque aún te amo'.", "respuesta": "PEREYRA"},
  {"letra": "Z", "pista": "Contiene la Z: Nombre del personaje de cómic apodado el rey de los monos.", "respuesta": "TARZÁN"}
],
    "Rosco Real 5 ✓": [
  {"letra": "A", "pista": "Con la A: Personaje que se opone al protagonista en el conflicto esencial de una obra de ficción.", "respuesta": "ANTAGONISTA"},
  {"letra": "B", "pista": "Con la B: Apellido de la actriz, conductora y vedette argentina, madre de Federico Bal.", "respuesta": "BARBIERI"},
  {"letra": "C", "pista": "Con la C: Dicho de una persona nacida bajo el signo zodiacal de Capricornio.", "respuesta": "CAPRICORNIANO"},
  {"letra": "D", "pista": "Con la D: Una cantidad excesiva.", "respuesta": "DEMASIADO"},
  {"letra": "E", "pista": "Con la E: Desalojar a los habitantes de un lugar para evitarles algún daño.", "respuesta": "EVACUAR"},
  {"letra": "F", "pista": "Con la F: Juego entre dos equipos de once jugadores cuyo objetivo es entrar en la portería un balón que no puede ser tocado con las manos.", "respuesta": "FÚTBOL"},
  {"letra": "G", "pista": "Con la G: Personaje de la Tierra Media en el universo del Señor de los Anillos que repetía la frase 'mi precioso'.", "respuesta": "GOLLUM"},
  {"letra": "H", "pista": "Con la H: Medida de superficie equivalente a 100 áreas.", "respuesta": "HECTÁREAS"},
  {"letra": "I", "pista": "Con la I: Que no es coherente.", "respuesta": "INCOHERENTE"},
  {"letra": "J", "pista": "Con la J: Tienda donde se venden juguetes.", "respuesta": "JUGUETERÍA"},
  {"letra": "L", "pista": "Con la L: Texto en que se expone el contenido de una película, programa de radio o televisión para su realización.", "respuesta": "LIBRETO"},
  {"letra": "M", "pista": "Con la M: Ciudad costera argentina, cabecera del partido General Alvarado, cercana a Mar del Plata.", "respuesta": "MIRAMAR"},
  {"letra": "N", "pista": "Con la N: Regularizar o poner en orden lo que no estaba.", "respuesta": "NORMALIZAR"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Hacer creer a alguien que algo falso es verdadero.", "respuesta": "ENGAÑAR"},
  {"letra": "O", "pista": "Con la O: Natural de Omán, país de Asia.", "respuesta": "OMANÍ"},
  {"letra": "P", "pista": "Con la P: Utensilio usado para pintar compuesto de un mango y un manojo de pelos o fibras en el extremo.", "respuesta": "PINCEL"},
  {"letra": "Q", "pista": "Contiene la Q: Falta de tranquilidad.", "respuesta": "INTRANQUILIDAD"},
  {"letra": "R", "pista": "Con la R: Vapor que con la frialdad de la noche se condensa en la atmósfera en forma de pequeñas gotas.", "respuesta": "ROCÍO"},
  {"letra": "S", "pista": "Con la S: Utensilio para poner las servilletas de papel.", "respuesta": "SERVILLETERO"},
  {"letra": "T", "pista": "Con la T: Nombre del actor protagonista de películas como Forrest Gump, Náufrago y Rescatando al soldado Ryan.", "respuesta": "TOM - TOM_HANKS"},
  {"letra": "U", "pista": "Contiene la U: Apodo del cantante y productor musical venezolano, intérprete de 'Dueño de nada'.", "respuesta": "PUMA"},
  {"letra": "V", "pista": "Con la V: Disciplina que se ocupa de prevenir y curar las enfermedades de los animales.", "respuesta": "VETERINARIA"},
  {"letra": "X", "pista": "Contiene la X: Droga sintética que produce efectos alucinógenos y afrodisíacos.", "respuesta": "ÉXTASIS"},
  {"letra": "Y", "pista": "Contiene la Y: Apodo de la modelo y actriz de ascendencia griega que integra el panel de 'Cortá por Lozano'.", "respuesta": "VICKY"},
  {"letra": "Z", "pista": "Contiene la Z: Trago de tequila.", "respuesta": "TEQUILAZO"}
],
    "Rosco Real 6 ✓": [
  {"letra": "A", "pista": "Con la A: Aire que se expulsa al respirar.", "respuesta": "ALIENTO"},
  {"letra": "B", "pista": "Con la B: Utensilio para quitar lo escrito con tiza, tinta o lápiz.", "respuesta": "BORRAR - BORRADOR"},
  {"letra": "C", "pista": "Con la C: Estilo de natación que consiste en batir las piernas y mover alternativamente los brazos hacia adelante.", "respuesta": "CROL"},
  {"letra": "D", "pista": "Con la D: Número natural que sigue al 11.", "respuesta": "DOCE"},
  {"letra": "E", "pista": "Con la E: Sistema de signos utilizado para escribir.", "respuesta": "ESCRITURA"},
  {"letra": "F", "pista": "Con la F: Serie animada que cuenta las aventuras de un repartidor de pizza que despierta mil años después.", "respuesta": "FUTURAMA"},
  {"letra": "G", "pista": "Con la G: Apellido del músico y cantante argentino conocido por el tema 'Solo le pido a Dios'.", "respuesta": "GIECO"},
  {"letra": "H", "pista": "Contiene la H: Utensilio con un soporte y un gancho que sirve para colgar trajes u otras prendas.", "respuesta": "PERCHA"},
  {"letra": "I", "pista": "Con la I: Hacer subir algo tirando de la cuerda de que está colgado.", "respuesta": "IZAR"},
  {"letra": "J", "pista": "Con la J: Nombre del famoso perro de raza Yorkshire que acompañó a Susana Jiménez durante 17 años.", "respuesta": "JASMINE"},
  {"letra": "L", "pista": "Con la L: Persona o entidad que va a la cabeza entre los de su clase, especialmente en una competición.", "respuesta": "LÍDER"},
  {"letra": "M", "pista": "Con la M: Persona que trabaja en las minas.", "respuesta": "MINERO"},
  {"letra": "N", "pista": "Con la N: Apodo por el que era conocido el humorista rosarino Alberto Olmedo.", "respuesta": "NEGRO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Elemento que sirve para pescar y lleva en el extremo una cuerda con un anzuelo.", "respuesta": "CAÑA"},
  {"letra": "O", "pista": "Con la O: Cada una de las cosas a las que se puede optar.", "respuesta": "OPCIÓN"},
  {"letra": "P", "pista": "Con la P: Recipiente que se utiliza para colocar el pan en la mesa.", "respuesta": "PANERA"},
  {"letra": "Q", "pista": "Con la Q: Producto natural o preparado que sirve para quitar manchas.", "respuesta": "QUITAMANCHAS"},
  {"letra": "R", "pista": "Con la R: Hacer más fría una habitación u otra cosa por medios artificiales.", "respuesta": "REFRIGERAR"},
  {"letra": "S", "pista": "Con la S: Ciudad de España, capital de Andalucía, donde se encuentra el club en el que jugó Maradona.", "respuesta": "SEVILLA"},
  {"letra": "T", "pista": "Con la T: Juego entre dos personas o parejas que se lanzan con raquetas una pelota sobre una red.", "respuesta": "TENIS"},
  {"letra": "U", "pista": "Contiene la U: Cama pequeña para niños con bordes altos o barandillas.", "respuesta": "CUNA"},
  {"letra": "V", "pista": "Con la V: Agudeza o perspicacia de ingenio.", "respuesta": "VIVEZA"},
  {"letra": "X", "pista": "Contiene la X: Dicho de una persona especializada o con grandes conocimientos en una materia.", "respuesta": "EXPERTO"},
  {"letra": "Y", "pista": "Contiene la Y: Nombre del actor y cineasta estadounidense protagonista de películas como Rocky y Rambo.", "respuesta": "SYLVESTER"},
  {"letra": "Z", "pista": "Contiene la Z: Condimento o conjunto de ingredientes que se usan para sazonar las comidas.", "respuesta": "SAZONADOR - ADEREZO"}
],
    "Rosco Real 7 ✓": [
  {"letra": "A", "pista": "Con la A: Prueba que se hace un cantante o un músico, etc. para valorar sus cualidades.", "respuesta": "AUDICIÓN"},
  {"letra": "B", "pista": "Con la B: Cavidad en la cual están colocadas la lengua y los dientes.", "respuesta": "BOCA"},
  {"letra": "C", "pista": "Con la C: Apellido del director de cine argentino cuya película El secreto de sus ojos fue ganadora del Oscar al mejor film de habla no inglesa en 2010.", "respuesta": "CAMPANELLA"},
  {"letra": "D", "pista": "Con la D: Periodo de 10 años referido a las decenas del siglo.", "respuesta": "DÉCADA"},
  {"letra": "E", "pista": "Con la E: Residencia del embajador.", "respuesta": "EMBAJADA"},
  {"letra": "F", "pista": "Con la F: Partidario del fascismo.", "respuesta": "FASCISTA"},
  {"letra": "G", "pista": "Con la G: Voz muy esforzada y levantada.", "respuesta": "GRITO"},
  {"letra": "H", "pista": "Contiene la H: Ocupación transitoria por lo común en tareas menores.", "respuesta": "CHANGA"},
  {"letra": "I", "pista": "Con la I: Dicho especialmente del comportamiento propio de un niño.", "respuesta": "INFANTIL"},
  {"letra": "J", "pista": "Contiene la J: Conjunto de platos, fuentes, vasos, tazas, etcétera que se destina al servicio de la mesa.", "respuesta": "VAJILLA"},
  {"letra": "L", "pista": "Con la L: Nombre de la capital y ciudad más poblada de la República del Perú.", "respuesta": "LIMA"},
  {"letra": "M", "pista": "Con la M: Mesa o tablero que hay en las tiendas para presentar los géneros.", "respuesta": "MOSTRADOR"},
  {"letra": "N", "pista": "Con la N: Obra literaria narrativa de cierta extensión.", "respuesta": "NOVELA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Dicho de una persona que tiene entre 30 y 39 años.", "respuesta": "TREINTAÑERO"},
  {"letra": "O", "pista": "Con la O: Gigante que, según las mitologías y consejas de los pueblos del norte de Europa, se alimentaba de carne humana.", "respuesta": "OGRO"},
  {"letra": "P", "pista": "Con la P: Alimento, especialmente fruto o dulce, servido como final de una comida.", "respuesta": "POSTRE"},
  {"letra": "Q", "pista": "Contiene la Q: Arte de montar y manejar bien el caballo.", "respuesta": "EQUITACIÓN - EQUITAR"},
  {"letra": "R", "pista": "Con la R: Nombre de musical de rock de 1996 con libreto, música y letras de Jonathan Larson, basado en la ópera La Boheme de Giacomo Puccini.", "respuesta": "RENT"},
  {"letra": "S", "pista": "Con la S: Apodo con el que es conocido Saul Hudson, guitarrista líder del grupo de hard rock californiano Guns N' Roses.", "respuesta": "SLASH"},
  {"letra": "T", "pista": "Con la T: Periodo de tres meses.", "respuesta": "TRIMESTRE"},
  {"letra": "U", "pista": "Contiene la U: Nombre del legendario rey dueño de la espada de Excalibur que se reunía en la corte de Camelot con los caballeros de la mesa redonda.", "respuesta": "ARTURO"},
  {"letra": "V", "pista": "Con la V: Apellido del autor de libros como 20.000 leguas de viaje submarino.", "respuesta": "VERNE"},
  {"letra": "X", "pista": "Contiene la X: Instrumento usado para estrujar la materia cuyo zumo se requiere extraer.", "respuesta": "EXPRIMIDOR"},
  {"letra": "Y", "pista": "Contiene la Y: Palabrería que tiene el propósito de impresionar o convencer.", "respuesta": "CHAMUYO"},
  {"letra": "Z", "pista": "Contiene la Z: Límite visual de la superficie terrestre donde parece juntarse el cielo y la tierra.", "respuesta": "HORIZONTE"}
],
    "Rosco Real 8 ✓": [
  {"letra": "A", "pista": "Con la A: Día en que se cumplen años de algún suceso.", "respuesta": "ANIVERSARIO"},
  {"letra": "B", "pista": "Con la B: Dicho de un color castaño claro.", "respuesta": "BEIGE"},
  {"letra": "C", "pista": "Con la C: Cascada o salto grande de agua.", "respuesta": "CATARATA"},
  {"letra": "D", "pista": "Con la D: Plática entre dos o más personas que alternativamente manifiestan sus ideas o afectos.", "respuesta": "DIÁLOGO"},
  {"letra": "E", "pista": "Con la E: Hortaliza o conjunto de hortalizas mezcladas, cortadas en trozos y aderezadas con sal, aceite y vinagre y otros ingredientes.", "respuesta": "ENSALADA"},
  {"letra": "F", "pista": "Con la F: Pereza, desgana.", "respuesta": "FIACA - FLOJERA"},
  {"letra": "G", "pista": "Con la G: Embarcación pequeña de recreo sin palos ni cubierta por lo común con una carroza del centro que se usa principalmente en Venecia.", "respuesta": "GÓNDOLA"},
  {"letra": "H", "pista": "Contiene la H: Ciudad ucraniana en donde se produjo el mayor desastre nuclear de la historia el 26 de abril de 1986.", "respuesta": "CHERNOBYL"},
  {"letra": "I", "pista": "Con la I: Natural de Irlanda. País de Europa.", "respuesta": "IRLANDÉS"},
  {"letra": "J", "pista": "Con la J: Apellido de la actriz estadounidense protagonista de films como Maléfica, Lara Croft y El señor y la señora Smith.", "respuesta": "JOLIE"},
  {"letra": "L", "pista": "Con la L: Que tiene mucha longitud.", "respuesta": "LARGO"},
  {"letra": "M", "pista": "Con la M: Banda de pop argentina formada en 2002 que interpretó canciones como A veces y Tiene que cambiar.", "respuesta": "MAMBRÚ"},
  {"letra": "N", "pista": "Con la N: Pieza de caucho con cámara de aire y sin ella que se monta sobre la llanta de una rueda.", "respuesta": "NEUMÁTICO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Conducto formado de caños por donde se distribuyen las aguas o el gas.", "respuesta": "CAÑERÍA"},
  {"letra": "O", "pista": "Con la O: Inflamación del oído.", "respuesta": "OTITIS"},
  {"letra": "P", "pista": "Con la P: Videojuegos japonés de 1980 en el que un círculo amarillo recorre laberintos devorando pastillas, frutas y fantasmas a su paso.", "respuesta": "PACMAN"},
  {"letra": "Q", "pista": "Con la Q: Capitalista u organizador de quinielas.", "respuesta": "QUINIELERO"},
  {"letra": "R", "pista": "Con la R: Internet.", "respuesta": "RED"},
  {"letra": "S", "pista": "Con la S: Manecilla que señala los segundos en el reloj.", "respuesta": "SEGUNDERO"},
  {"letra": "T", "pista": "Con la T: Lienzo grande que se pone en el escenario de un teatro de modo que pueda bajarse y subirse.", "respuesta": "TELÓN"},
  {"letra": "U", "pista": "Contiene la U: Voz triste y prolongada del lobo, el perro y otros animales.", "respuesta": "AULLIDO"},
  {"letra": "V", "pista": "Con la V: Persona que no ha tenido relaciones sexuales / Traslado que se hace de una parte a otra por aire, mar o tierra.", "respuesta": "VIRGEN"},
  {"letra": "X", "pista": "Con la X: Apodo de Meneghel, cantante, presentadora de TV y modelo brasileña conocida como la reina de los bajitos.", "respuesta": "XUXA"},
  {"letra": "Y", "pista": "Contiene la Y: Natural del Paraguay, país de América.", "respuesta": "PARAGUAYO"},
  {"letra": "Z", "pista": "Contiene la Z: Que impide que algo se deslice o patine.", "respuesta": "ANTIDESLIZANTE"}
],
    "Rosco Real 9 ✓": [
  {"letra": "A", "pista": "Con la A: Persona que tiene a su cargo el manejo del ascensor.", "respuesta": "ASCENSORISTA"},
  {"letra": "B", "pista": "Con la B: Sitio en donde se arroja y amontona la basura.", "respuesta": "BASURAL"},
  {"letra": "C", "pista": "Con la C: Cálculo u operación aritmética.", "respuesta": "CUENTA"},
  {"letra": "D", "pista": "Con la D: Apellido del pintor español exponente del surrealismo del siglo XX, autor de La Persistencia de la Memoria.", "respuesta": "DALÍ"},
  {"letra": "E", "pista": "Con la E: Sapo.", "respuesta": "ESCUERZO"},
  {"letra": "F", "pista": "Con la F: Membrana que sujeta la lengua por la línea media de la parte inferior y que cuando se desarrolla demasiado impide mamar o hablar con soltura.", "respuesta": "FRENILLO"},
  {"letra": "G", "pista": "Con la G: Apodo del novelista colombiano Gabriel García Márquez.", "respuesta": "GABO"},
  {"letra": "H", "pista": "Contiene la H: Salsa cremosa.", "respuesta": "BECHAMEL"},
  {"letra": "I", "pista": "Con la I: Vestimenta de una persona para adorno o abrigo de su cuerpo.", "respuesta": "INDUMENTARIA"},
  {"letra": "J", "pista": "Contiene la J: Parte superior del edificio cubierta comúnmente de portejas.", "respuesta": "TEJADO"},
  {"letra": "L", "pista": "Con la L: Costado o parte del cuerpo de la persona o del animal comprendida entre el hombro y la cadera.", "respuesta": "LOMO"},
  {"letra": "M", "pista": "Con la M: Nombre del profeta árabe nacido en la ciudad de la Meca que fue el fundador del islam en el siglo VII de nuestra era.", "respuesta": "MAHOMA"},
  {"letra": "N", "pista": "Con la N: Conjunto o cuerpo de los nobles de un estado o de una región.", "respuesta": "NOBLEZA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: En un automóvil dispositivo para desempañar los cristales.", "respuesta": "DESEMPAÑADOR"},
  {"letra": "O", "pista": "Con la O: Que exhala olor.", "respuesta": "OLOROSO"},
  {"letra": "P", "pista": "Con la P: Caballo de poca alzada.", "respuesta": "POTRILLO - PONY - PETIZO"},
  {"letra": "Q", "pista": "Contiene la Q: Reconocimiento médico general.", "respuesta": "CHEQUEO"},
  {"letra": "R", "pista": "Con la R: Nombre del personaje del cómic Compañero inseparable del paladín de Ciudad Gótica Batman.", "respuesta": "ROBIN"},
  {"letra": "S", "pista": "Con la S: En todo o cualquier tiempo.", "respuesta": "SIEMPRE"},
  {"letra": "T", "pista": "Con la T: Alimento preparado con huevo batido, cuajado con aceite en la sartén y de forma redonda o alargada al que a veces se añaden otros ingredientes.", "respuesta": "TORTILLA"},
  {"letra": "U", "pista": "Contiene la U: Abertura situada en el centro del iris por la que entra la luz en el ojo.", "respuesta": "PUPILA"},
  {"letra": "V", "pista": "Con la V: Volcán ubicado en el sur de Italia que al erupcionar en el año 79 de nuestra era sepultó las antiguas ciudades de Pompeya y Herculano.", "respuesta": "VESUBIO"},
  {"letra": "X", "pista": "Contiene la X: Natural de México, país de América.", "respuesta": "MEXICANO"},
  {"letra": "Y", "pista": "Contiene la Y: Dispositivo mecánico utilizado para inyectar fluidos.", "respuesta": "INYECTOR - INYECCIÓN"},
  {"letra": "Z", "pista": "Contiene la Z: Gameto masculino destinado a la fecundación del óvulo.", "respuesta": "ESPERMATOZOIDE"}
],
    "Rosco Real 10 ✓": [
  {"letra": "A", "pista": "Con la A: Vehículo provisto de una bomba.", "respuesta": "AUTOBOMBA"},
  {"letra": "B", "pista": "Con la B: Apellido del actor estadounidense famoso por su papel de Rick Blaine en el film de 1942, Casablanca.", "respuesta": "BOGART"},
  {"letra": "C", "pista": "Con la C: Conjunto de escamillas blancuzcas que se forman en el cuero cabelludo.", "respuesta": "CASPA"},
  {"letra": "D", "pista": "Con la D: Piedra preciosa constituida por carbono cristalizado en el sistema cúbico que se utiliza en joyería por su brillo y transparencia.", "respuesta": "DIAMANTE"},
  {"letra": "E", "pista": "Con la E: Autor de obras escritas o impresas.", "respuesta": "ESCRITOR"},
  {"letra": "F", "pista": "Con la F: Cuchillo grande, recto y puntiagudo.", "respuesta": "FACÓN"},
  {"letra": "G", "pista": "Con la G: Gran isla de América del Norte ubicada entre el Océano Atlántico y el Glacial Ártico que pertenece al Reino de Dinamarca.", "respuesta": "GROENLANDIA"},
  {"letra": "H", "pista": "Con la H: Pirata informático.", "respuesta": "HACKER"},
  {"letra": "I", "pista": "Con la I: Estampa, grabado o dibujo que adorna o documenta un libro.", "respuesta": "IMAGEN - ILUSTRACIÓN"},
  {"letra": "J", "pista": "Con la J: Vaso por lo general de porcelana artísticamente labrado para adornar consolas, chimeneas, etc.", "respuesta": "JARRÓN"},
  {"letra": "L", "pista": "Con la L: Palabra o frase que se repite innecesariamente en una conversación.", "respuesta": "LATIGUILLO"},
  {"letra": "M", "pista": "Con la M: Apellido artístico del pianista y compositor argentino de tango. Autor de canciones como Taquito Militar y El Firulete.", "respuesta": "MORES"},
  {"letra": "N", "pista": "Con la N: Prominencia que forma el cartílago tiroides en la parte anterior del cuello del varón adulto.", "respuesta": "NUEZ"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Dicho de una persona que tiene entre 20 y 29 años.", "respuesta": "VEINTEAÑERO"},
  {"letra": "O", "pista": "Con la O: Tubería provista de bombas y otros aparatos para conducir el petróleo a larga distancia.", "respuesta": "OLEODUCTO"},
  {"letra": "P", "pista": "Con la P: Pieza de paso largo y estrecha en el interior de un edificio.", "respuesta": "PASILLO"},
  {"letra": "Q", "pista": "Contiene la Q: Dispositivo que pone en marcha el motor de una máquina, especialmente de un vehículo automóvil.", "respuesta": "ARRANQUE"},
  {"letra": "R", "pista": "Con la R: Apellido del actor estadounidense que formó un recordado dúo junto a P. Newman en El Golpe y Batch Cassidy and the Sundance Kid.", "respuesta": "REDFORD"},
  {"letra": "S", "pista": "Con la S: Correo basura.", "respuesta": "SPAM"},
  {"letra": "T", "pista": "Con la T: En tiempo anterior a lo oportuno, convenido, acostumbrado para alguien, algún fin o muy pronto.", "respuesta": "TEMPRANO"},
  {"letra": "U", "pista": "Contiene la U: Arrojar saliva por la boca.", "respuesta": "ESCUPIR"},
  {"letra": "V", "pista": "Con la V: Que se hace o estipula solo de palabra y no por escrito.", "respuesta": "VERBAL"},
  {"letra": "X", "pista": "Contiene la X: Especialista en sexología.", "respuesta": "SEXÓLOGO"},
  {"letra": "Y", "pista": "Contiene la Y: Apellido del pintor español del periodo rococó. Clásico autor de la Maja desnuda y Saturno devorando a su hijo.", "respuesta": "GOYA"},
  {"letra": "Z", "pista": "Contiene la Z: Hierba mala.", "respuesta": "MALEZA"}
],
    "Rosco Real 11 ✓": [
  {"letra": "A", "pista": "Con la A: Continente muy frío, mayormente despoblado, ubicado en el polo sur del planeta.", "respuesta": "ANTÁRTIDA"},
  {"letra": "B", "pista": "Con la B: Tazón sin asa, cuenco.", "respuesta": "BOWL"},
  {"letra": "C", "pista": "Con la C: Que tiene la cabeza inclinada hacia abajo por abatimiento, tristeza o preocupaciones graves.", "respuesta": "CABIZBAJO"},
  {"letra": "D", "pista": "Con la D: Eliminar el vello de alguien o de una parte de su cuerpo agarrándolo mediante sustancias apropiadas u otros procedimientos técnicos.", "respuesta": "DEPILAR"},
  {"letra": "E", "pista": "Con la E: No acertar algo.", "respuesta": "ERRAR"},
  {"letra": "F", "pista": "Con la F: Estampa de pequeño tamaño usada principalmente por niños para jugar, intercambiar o coleccionar un álbum.", "respuesta": "FIGURITAS"},
  {"letra": "G", "pista": "Con la G: Que tiene goma o se parece a ella.", "respuesta": "GOMOSO"},
  {"letra": "H", "pista": "Contiene la H: Prenda de abrigo cuadrado, rectangular de lana, de oveja, alpaca, vicuña u otro tejido que tiene en el centro una abertura para pasar la cabeza.", "respuesta": "PONCHO"},
  {"letra": "I", "pista": "Con la I: Que no se puede postergar.", "respuesta": "IMPOSTERGABLE"},
  {"letra": "J", "pista": "Con la J: Nombre artístico del actor cómico protagonista de las películas Mentiroso Mentiroso, Ace Ventura y Todopoderoso.", "respuesta": "JIM"},
  {"letra": "L", "pista": "Con la L: Extremidad del ojo próxima a la nariz.", "respuesta": "LAGRIMAL"},
  {"letra": "M", "pista": "Con la M: Echar maldiciones contra alguien o algo.", "respuesta": "MALDECIR"},
  {"letra": "N", "pista": "Con la N: Aparato electrodoméstico, cámara o mueble que produce frío para conservar alimentos u otras sustancias.", "respuesta": "NEVERA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: banda que se pone alrededor del antebrazo para sujetarla o protegerla como adorno", "respuesta": "muñequera"},
  {"letra": "O", "pista": "Con la O: Estorbar el paso, cerrar un conducto o camino.", "respuesta": "OBSTRUIR"},
  {"letra": "P", "pista": "Con la P: Pastel cubierto generalmente de dulce de membrillo o de leche y decorado con tiritas entrecruzadas de la misma masa que la base.", "respuesta": "PASTAFROLA"},
  {"letra": "Q", "pista": "Contiene la Q: Natural de Pakistán, país de Asia.", "respuesta": "PAQUISTANÍ"},
  {"letra": "R", "pista": "Con la R: Espacio de tiempo en que ejerce su función un rey o una reina.", "respuesta": "REINADO"},
  {"letra": "S", "pista": "Con la S: Personaje de ficción de la franquicia Marvel que recibió poderes sobrehumanos tras ser mordido por una araña radioactiva.", "respuesta": "SPIDER_MAN"},
  {"letra": "T", "pista": "Con la T: Borrar lo escrito haciendo unos trazos encima.", "respuesta": "TACHAR"},
  {"letra": "U", "pista": "Contiene la U: Chapa triangular u ovalada de carey, marfil o material plástico que se emplea para tocar ciertos instrumentos musicales de cuerda como la guitarra.", "respuesta": "PÚA"},
  {"letra": "V", "pista": "Con la V: Unión o atadura de una persona con otra.", "respuesta": "VÍNCULO"},
  {"letra": "X", "pista": "Contiene la X: Punto donde se realiza el enlace entre aparatos o sistemas.", "respuesta": "CONEXIÓN"},
  {"letra": "Y", "pista": "Contiene la Y: En la antigua Roma, persona que pertenecía a la plebe.", "respuesta": "PLEBEYO"},
  {"letra": "Z", "pista": "Con la Z: Nombre de la modelo y actriz argentina, ex conductora de Morfi, hermana de Wanda.", "respuesta": "ZAIRA"}
],
    "Rosco Real 12 ✓": [
  {"letra": "A", "pista": "Con la A: Manchado como la piel del tigre.", "respuesta": "ATIGRADO"},
  {"letra": "B", "pista": "Con la B: Porción de comida que cabe de una vez en la boca.", "respuesta": "BOCADO"},
  {"letra": "C", "pista": "Con la C: Elaboración de origen anglosajón formado por una capa de fruta fresca cubierta por una mezcla de harina, manteca y azúcar cuya terminación produce efecto de migas.", "respuesta": "CRUMBLE"},
  {"letra": "D", "pista": "Con la D: Flaco, de pocas carnes.", "respuesta": "DELGADO"},
  {"letra": "E", "pista": "Contiene la E: Vendedor de leña.", "respuesta": "LEÑADOR"},
  {"letra": "F", "pista": "Con la F: Que finge lo que no es o no siente.", "respuesta": "FARSANTE - FALSO"},
  {"letra": "G", "pista": "Con la G: En pastelería y repostería, recubrir con una capa de almíbar o de azúcar glas.", "respuesta": "GLASEAR"},
  {"letra": "H", "pista": "Contiene la H: Guardar dinero como previsión para necesidades futuras.", "respuesta": "AHORRAR"},
  {"letra": "I", "pista": "Con la I: Persona que suele hablar o proceder sin reflexión y cautela, dejándose llevar por la impresión del momento.", "respuesta": "IMPULSIVO"},
  {"letra": "J", "pista": "Contiene la J: Dar a alguien o algo un aspecto más joven.", "respuesta": "REJUVENECER"},
  {"letra": "L", "pista": "Con la L: Primer periodo de la vida de los mamíferos en el cual se alimentan solo de leche.", "respuesta": "LACTANCIA"},
  {"letra": "M", "pista": "Con la M: Horario establecido por una discoteca para el público adolescente.", "respuesta": "MATINÉ"},
  {"letra": "N", "pista": "Con la N: Natural de la ciudad de Nápoles, en Italia.", "respuesta": "NAPOLITANO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Enredo de los hilos o del cabello.", "respuesta": "MARAÑA"},
  {"letra": "O", "pista": "Con la O: Parte de la medicina que trata de las enfermedades del oído, nariz y laringe.", "respuesta": "OTORRINOLARINGÓLOGO"},
  {"letra": "P", "pista": "Con la P: Utensilio portátil para resguardarse de la lluvia compuesto de un eje y un varillaje cubierto de tela que puede extenderse y plegarse.", "respuesta": "PARAGUAS"},
  {"letra": "Q", "pista": "Contiene la Q: Colocar etiquetas, especialmente a un producto destinado a la venta.", "respuesta": "ETIQUETAR"},
  {"letra": "R", "pista": "Con la R: Nombre del periodista de espectáculos nacido en Uruguay de apellido Lussich.", "respuesta": "RODRIGO"},
  {"letra": "S", "pista": "Con la S: Pequeña imagen o animación que se utiliza en redes sociales, especialmente en WhatsApp.", "respuesta": "STICKER"},
  {"letra": "T", "pista": "Con la T: Baños de aguas minerales calientes.", "respuesta": "TERMAS"},
  {"letra": "U", "pista": "Contiene la U: Cirugía del sistema nervioso.", "respuesta": "NEUROCIRUGÍA"},
  {"letra": "V", "pista": "Con la V: Nombre artístico del actor norteamericano protagonista de la franquicia Rápido y Furioso, famoso por su calva.", "respuesta": "VIN - VIN_DIESEL"},
  {"letra": "X", "pista": "Contiene la X: Distrito del estado de Nueva York, cuna del rap y del hip hop con una importante población afroamericana.", "respuesta": "BRONX"},
  {"letra": "Y", "pista": "Contiene la Y: Endurecer con yeso los apósitos y vendajes destinados a sostener huesos rotos.", "respuesta": "ENYESAR"},
  {"letra": "Z", "pista": "Contiene la Z: Comprobar y certificar la autenticidad de un documento o de una firma.", "respuesta": "LEGALIZAR"}
],
    "Rosco Real 13 ✓": [
  {"letra": "A", "pista": "Con la A: Dueño de una o varias acciones en una compañía comercial, industrial o de otra índole.", "respuesta": "ACCIONISTA"},
  {"letra": "B", "pista": "Con la B: Autor de una biografía.", "respuesta": "BIÓGRAFO"},
  {"letra": "C", "pista": "Con la C: Someter alimentos a muy baja temperatura para que se conserven en buenas condiciones hasta su ulterior consumo.", "respuesta": "CONGELAR"},
  {"letra": "D", "pista": "Con la D: Apellido del escritor francés, figura representativa del romanticismo del siglo XIX, autor de Los Tres Mosqueteros y El Conde de Montecristo.", "respuesta": "DUMAS"},
  {"letra": "E", "pista": "Con la E: Pavimento formado artificialmente de piedras.", "respuesta": "EMPEDRADO"},
  {"letra": "F", "pista": "Con la F: Lodo glutinoso que se forma generalmente con los sedimentos térreos en los sitios donde hay agua detenida.", "respuesta": "FANGO"},
  {"letra": "G", "pista": "Con la G: Oprimir el gatillo de un arma de fuego para dispararla.", "respuesta": "GATILLAR"},
  {"letra": "H", "pista": "Contiene la H: Que tiene coherencia.", "respuesta": "COHERENTE"},
  {"letra": "I", "pista": "Con la I: Que se produce o se coloca en el interior de una vena.", "respuesta": "INTRAVENOSO"},
  {"letra": "J", "pista": "Contiene la J: Conjunto de hojas de los árboles y otras plantas.", "respuesta": "FOLLAJE"},
  {"letra": "L", "pista": "Con la L: Que profesa la doctrina de Martín Lutero, reformador protestante alemán del siglo XVI.", "respuesta": "LUTERANO"},
  {"letra": "M", "pista": "Con la M: Contrapuesto a lo antiguo, a lo clásico y establecido.", "respuesta": "MODERNO"},
  {"letra": "N", "pista": "Con la N: Apellido del matemático e inventor escocés reconocido por ser el primero en definir los logaritmos y por el uso de la coma decimal en aritmética.", "respuesta": "NAPIER"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Natural de Belice, país de América.", "respuesta": "BELICEÑO"},
  {"letra": "O", "pista": "Con la O: Perteneciente o relativo a la ontología.", "respuesta": "ONTOLÓGICO"},
  {"letra": "P", "pista": "Con la P: Que se produce tras un trauma o como consecuencia directa de él.", "respuesta": "POSTRAUMÁTICO"},
  {"letra": "Q", "pista": "Contiene la Q: Cada una de ciertas divinidades de la mitología escandinava que en los combates designaban los héroes que habían de morir y en el cielo les servían.", "respuesta": "VALQUIRIA"},
  {"letra": "R", "pista": "Con la R: Cosmético usado para colorear los labios que se presenta generalmente en forma de barra guardada en un estuche.", "respuesta": "ROUGE"},
  {"letra": "S", "pista": "Con la S: Imagen que se activa de manera automática en una computadora encendida u otro dispositivo electrónico cuando no está siendo utilizado.", "respuesta": "SALVAPANTALLAS"},
  {"letra": "T", "pista": "Con la T: Rebanada de pan empapada en leche o vino, rebozada con huevo, frita y endulzada.", "respuesta": "TORRIJA"},
  {"letra": "U", "pista": "Contiene la U: Grabación sonora del texto de un libro.", "respuesta": "AUDIOLIBRO"},
  {"letra": "V", "pista": "Con la V: Nombre de la capital del principado de Liechtenstein.", "respuesta": "VADUZ"},
  {"letra": "X", "pista": "Contiene la X: Acción y efecto de expatriar o expatriarse.", "respuesta": "EXPATRIACIÓN"},
  {"letra": "Y", "pista": "Contiene la Y: Calidad, especie y clase.", "respuesta": "LAYA"},
  {"letra": "Z", "pista": "Contiene la Z: Cubierta dura, de distinta naturaleza según los casos, que protege el cuerpo de ciertos animales como protozoos, crustáceos y quelonios.", "respuesta": "CAPARAZÓN"}
],
    "Rosco Real 14 ✓": [
  {"letra": "A", "pista": "Con la A: Alimento que ha sido procesado con humaredas para mejorar su gusto.", "respuesta": "AHUMADO"},
  {"letra": "B", "pista": "Con la B: Vello que crece en la zona cutánea situada bajo la nariz.", "respuesta": "BIGOTE"},
  {"letra": "C", "pista": "Con la C: Denominación coloquial del periodo de instrucción militar en Argentina.", "respuesta": "COLIMBA"},
  {"letra": "D", "pista": "Con la D: Prenda de tela que se ajusta a la cintura para no ensuciar la vestimenta.", "respuesta": "DELANTAL"},
  {"letra": "E", "pista": "Con la E: Persona que demuestra buenos modales y cortesía.", "respuesta": "EDUCADO"},
  {"letra": "F", "pista": "Con la F: Apellido de la cantante estadounidense de soul fallecida en 2018.", "respuesta": "FRANKLIN"},
  {"letra": "G", "pista": "Con la G: Banda o tira de material elástico.", "respuesta": "GOMITA"},
  {"letra": "H", "pista": "Con la H: Criatura fantástica femenina con alas y capacidades sobrenaturales.", "respuesta": "HADA"},
  {"letra": "I", "pista": "Con la I: Nación de Asia ubicada en el Levante mediterráneo con sede en Jerusalén.", "respuesta": "ISRAEL"},
  {"letra": "J", "pista": "Con la J: Tiempo que dura la labor de un trabajador durante un día.", "respuesta": "JORNADA"},
  {"letra": "L", "pista": "Con la L: Obra cinematográfica cuya extensión temporal supera los sesenta minutos.", "respuesta": "LARGOMETRAJE"},
  {"letra": "M", "pista": "Con la M: Nombre popular de la cancha del club de fútbol River Plate.", "respuesta": "MONUMENTAL"},
  {"letra": "N", "pista": "Con la N: Cuerpo de agua que posee profundidad suficiente para el paso de naves.", "respuesta": "NAVEGABLE"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Importe monetario que se paga como adelanto para asegurar una compra.", "respuesta": "SEÑA"},
  {"letra": "O", "pista": "Con la O: Que posee un contorno similar al de una elipse o un huevo.", "respuesta": "OVAL"},
  {"letra": "P", "pista": "Con la P: Variedad láctea curada y dura originaria de la región de Parma.", "respuesta": "PARMESANO"},
  {"letra": "Q", "pista": "Con la Q: Que se encuentra en la posición número cinco de una lista ordenada.", "respuesta": "QUINTO"},
  {"letra": "R", "pista": "Con la R: Dispositivo de fuego portátil con un cilindro para proyectiles.", "respuesta": "REVOLVER"},
  {"letra": "S", "pista": "Con la S: Identidad del perro de raza beagle que acompaña a Charlie Brown.", "respuesta": "SNOOPY"},
  {"letra": "T", "pista": "Con la T: Estado de las condiciones atmosféricas en un momento dado.", "respuesta": "TIEMPO"},
  {"letra": "U", "pista": "Con la U: Empleado de un club encargado de gestionar los bártulos de los atletas.", "respuesta": "UTILERO"},
  {"letra": "V", "pista": "Con la V: Instrumento que marca los kilómetros por hora a los que se desplaza un coche.", "respuesta": "VELOCÍMETRO"},
  {"letra": "X", "pista": "Contiene la X: Sistema estelar masivo compuesto por astros, gas y polvo.", "respuesta": "GALAXIA"},
  {"letra": "Y", "pista": "Contiene la Y: Relato de tradición popular sobre hechos maravillosos o históricos.", "respuesta": "LEYENDA"},
  {"letra": "Z", "pista": "Con la Z: Apellido de la recordada actriz uruguaya de la película Esperando la carroza.", "respuesta": "ZORRILLA"}
],
    "Rosco Real 15 ✓": [
  {"letra": "A", "pista": "Con la A: Control de pasajeros y mercancías en las fronteras y puntos de entrada al país.", "respuesta": "ADUANA"},
  {"letra": "B", "pista": "Con la B: Gorra sin visera, redonda y chata, de lana y generalmente de una sola pieza.", "respuesta": "BOINA"},
  {"letra": "C", "pista": "Con la C: Apellido del vocalista y líder de la mítica banda de rock Soda Stereo.", "respuesta": "CERATI"},
  {"letra": "D", "pista": "Con la D: Identificación nacional y oficial de los ciudadanos de un país.", "respuesta": "DNI"},
  {"letra": "E", "pista": "Con la E: Dicho de una actividad o producto que no resulta perjudicial para el entorno natural.", "respuesta": "ECOLÓGICO"},
  {"letra": "F", "pista": "Con la F: Torta delgada de harina de legumbres que se cocina en el horno.", "respuesta": "FAINÁ"},
  {"letra": "G", "pista": "Con la G: Persona encargada de manejar y dirigir la embarcación típica veneciana.", "respuesta": "GONDOLIERO"},
  {"letra": "H", "pista": "Con la H: Instalación destinada al despegue de aeronaves de rotor superior.", "respuesta": "HELIPUERTO"},
  {"letra": "I", "pista": "Con la I: Edificio dedicado al culto cristiano.", "respuesta": "IGLESIA"},
  {"letra": "J", "pista": "Contiene la J: Recipiente de madera donde se deposita un cuerpo sin vida.", "respuesta": "CAJÓN"},
  {"letra": "L", "pista": "Con la L: Objeto metálico que permite activar el mecanismo de apertura de una cerradura.", "respuesta": "LLAVE"},
  {"letra": "M", "pista": "Con la M: Población del sur francés que otorga su nombre al canto nacional de ese país.", "respuesta": "MARSELLA"},
  {"letra": "N", "pista": "Con la N: Corte del cuarto trasero de los vacunos de la parte interna del muslo.", "respuesta": "NALGA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Individuo que se dedica a talar y procesar madera.", "respuesta": "LEÑADOR"},
  {"letra": "O", "pista": "Con la O: Médico especialista en tratar las patologías de la visión.", "respuesta": "OCULISTA"},
  {"letra": "P", "pista": "Con la P: Apellido del actor estadounidense protagonista del filme Se7en.", "respuesta": "PITT"},
  {"letra": "Q", "pista": "Contiene la Q: Reproducción física a tamaño reducido de una estructura o edificio.", "respuesta": "MAQUETA"},
  {"letra": "R", "pista": "Con la R: Ingenio electrónico programable capaz de realizar diversas operaciones.", "respuesta": "ROBOT"},
  {"letra": "S", "pista": "Con la S: Alimento que posee un gusto excesivo por el agregado de cloruro sódico.", "respuesta": "SALADO"},
  {"letra": "T", "pista": "Con la T: Animación sobre felinos cósmicos que se enfrentan a Mumm-Ra.", "respuesta": "THUNDERCATS"},
  {"letra": "U", "pista": "Contiene la U: Persona que ha perdido la visión en uno de sus ojos.", "respuesta": "TUERTO"},
  {"letra": "V", "pista": "Con la V: Espacio techado y cerrado que sirve de hogar para las personas.", "respuesta": "VIVIENDA"},
  {"letra": "X", "pista": "Contiene la X: Aparato que envía documentos a través de la red de telefonía fija.", "respuesta": "FAX"},
  {"letra": "Y", "pista": "Contiene la Y: Apellido del mandatario estadounidense que sufrió un atentado en Dallas en 1963.", "respuesta": "KENNEDY"},
  {"letra": "Z", "pista": "Contiene la Z: Alumno que se está formando en una disciplina técnica o artesanal.", "respuesta": "APRENDIZ"}
],
    "Rosco Real 16 ✓": [
  {"letra": "A", "pista": "Con la A: De gran estatura.", "respuesta": "ALTO"},
  {"letra": "B", "pista": "Con la B: Nombre del paladín de historietas caracterizado como un hombre murciélago que protege a Ciudad Gótica.", "respuesta": "BATMAN"},
  {"letra": "C", "pista": "Con la C: Excremento humano y especialmente el de los niños pequeños.", "respuesta": "CACA"},
  {"letra": "D", "pista": "Con la D: Obra de teatro o de cine en que prevalecen acciones y situaciones tensas y pasiones conflictivas.", "respuesta": "DRAMA"},
  {"letra": "E", "pista": "Con la E: Individuo que realiza un aprendizaje en un establecimiento de enseñanza.", "respuesta": "ESTUDIANTE"},
  {"letra": "F", "pista": "Con la F: Término coloquial para referirse a un cigarrillo.", "respuesta": "FASO"},
  {"letra": "G", "pista": "Con la G: Apellido del legendario ex arquero de Boca Juniors apodado El Loco.", "respuesta": "GATTI"},
  {"letra": "H", "pista": "Con la H: Título del filme de terror de 1978 donde el asesino Michael Myers ataca durante la noche de brujas.", "respuesta": "HALLOWEEN"},
  {"letra": "I", "pista": "Con la I: Que no se puede o no se deja someter o amansar.", "respuesta": "INDOMABLE"},
  {"letra": "J", "pista": "Contiene la J: Enigma o adivinanza que se propone como pasatiempo.", "respuesta": "ACERTIJO"},
  {"letra": "L", "pista": "Con la L: Persona que tiene por oficio hablar por radio o televisión para presentar programas o dar noticias.", "respuesta": "LOCUTOR"},
  {"letra": "M", "pista": "Con la M: Producto obtenido por el batido, amasado y maduración de la nata extraída de la leche.", "respuesta": "MANTECA"},
  {"letra": "N", "pista": "Con la N: Nombre del penúltimo mes del año que cuenta con treinta días.", "respuesta": "NOVIEMBRE"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Mano cerrada.", "respuesta": "PUÑO"},
  {"letra": "O", "pista": "Con la O: Fragilidad de los huesos producida por su descalcificación con formación de poros.", "respuesta": "OSTEOPOROSIS"},
  {"letra": "P", "pista": "Con la P: Placa identificativa que llevan los vehículos para habilitarlos a circular.", "respuesta": "PATENTE"},
  {"letra": "Q", "pista": "Con la Q: Nombre del país de la Península Arábiga donde se celebró el Mundial de Fútbol de 2022.", "respuesta": "QATAR"},
  {"letra": "R", "pista": "Con la R: Paño de cocina o lienzo utilizado para secar la vajilla.", "respuesta": "REPASADOR"},
  {"letra": "S", "pista": "Con la S: Bebida alcohólica de color ambarino que se obtiene por la fermentación del jugo de las manzanas.", "respuesta": "SIDRA"},
  {"letra": "T", "pista": "Con la T: Pieza que se cierra por la parte superior de cajas o recipientes.", "respuesta": "TAPA"},
  {"letra": "U", "pista": "Contiene la U: Repercusión pública de algún hecho.", "respuesta": "RUIDO"},
  {"letra": "V", "pista": "Con la V: Descanso temporal de una actividad habitual, como el trabajo o los estudios.", "respuesta": "VACACIONES"},
  {"letra": "X", "pista": "Contiene la X: Que posee un gran poder de seducción o atracción física.", "respuesta": "SEXUAL - EXCITANTE"},
  {"letra": "Y", "pista": "Contiene la Y: En este día.", "respuesta": "HOY"},
  {"letra": "Z", "pista": "Contiene la Z: Apodo de el cantante de heavy metal, John Osborne, ex-miembro de Black Sabbath.", "respuesta": "OZZY"}
],
    "Rosco Real 17✓": [
  {"letra": "A", "pista": "Con la A: Que posee una combinación de sabores ácidos y azucarados.", "respuesta": "AGRIDULCE"},
  {"letra": "B", "pista": "Con la B: Instrumento para escribir que tiene en su interior un tubo de tinta y en la punta una bolita metálica.", "respuesta": "BOLÍGRAFO"},
  {"letra": "C", "pista": "Con la C: Cubierta del motor del automóvil.", "respuesta": "CAPÓ"},
  {"letra": "D", "pista": "Con la D: Banda argentina de rock integrada por Ricardo Mollo, Diego Arnedo y Catriel Ciavarella.", "respuesta": "DIVIDIDOS"},
  {"letra": "E", "pista": "Con la E: Palo afilado en un extremo para clavarlo.", "respuesta": "ESTACA"},
  {"letra": "F", "pista": "Con la F: Obra cinematográfica.", "respuesta": "FILM - FILME"},
  {"letra": "G", "pista": "Con la G: Lluvia menuda que cae blandamente.", "respuesta": "GARÚA"},
  {"letra": "H", "pista": "Contiene la H: Nombre del personaje de Star Wars que es un Wookie peludo y compañero de Han Solo.", "respuesta": "CHEWBACCA"},
  {"letra": "I", "pista": "Con la I: Tarjeta mediante la cual se convoca a alguien a un evento.", "respuesta": "INVITACIÓN"},
  {"letra": "J", "pista": "Contiene la J: Instrumento que sirve para medir el tiempo.", "respuesta": "RELOJ"},
  {"letra": "L", "pista": "Con la L: Operación estética de estiramiento de la piel de la cara y cuello para suprimir arrugas.", "respuesta": "LIFTING"},
  {"letra": "M", "pista": "Con la M: Que está sin vida.", "respuesta": "MUERTO"},
  {"letra": "N", "pista": "Con la N: Persona oriunda de aquel país de América Central cuya capital es Managua.", "respuesta": "NICARAGÜENSE"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Construcción rústica pequeña de materiales pobres destinada a refugio.", "respuesta": "CABAÑA"},
  {"letra": "O", "pista": "Con la O: Apellido del exfutbolista argentino de River Plate apodado El Burrito.", "respuesta": "ORTEGA"},
  {"letra": "P", "pista": "Con la P: Tenis de mesa.", "respuesta": "PING-PONG"},
  {"letra": "Q", "pista": "Contiene la Q: Caja o maleta para guardar y transportar medicinas.", "respuesta": "BOTIQUÍN"},
  {"letra": "R", "pista": "Con la R: Música de origen jamaicano caracterizada por un ritmo sencillo y repetitivo.", "respuesta": "REGGAE"},
  {"letra": "S", "pista": "Con la S: País europeo de los Alpes reconocido por sus chocolates y cuya capital es Berna.", "respuesta": "SUIZA"},
  {"letra": "T", "pista": "Con la T: Dicho de un jugador que interviene habitualmente en la formación inicial de su equipo.", "respuesta": "TITULAR"},
  {"letra": "U", "pista": "Contiene la U: Persona apasionada por el automovilismo.", "respuesta": "TUERCA"},
  {"letra": "V", "pista": "Con la V: Líquido agrio producido por la fermentación ácida del vino usado como condimento.", "respuesta": "VINAGRE"},
  {"letra": "X", "pista": "Contiene la X: Conocimiento de la vida adquirido por las circunstancias vividas.", "respuesta": "EXPERIENCIA"},
  {"letra": "Y", "pista": "Contiene la Y: Ribera del mar o de un río grande, formada de arenales en superficie casi plana.", "respuesta": "PLAYA"},
  {"letra": "Z", "pista": "Contiene la Z: Nombre del personaje tiracómica argentina creado por Dante Quintero, caracterizado como un cacique te huelche leal y valiente.", "respuesta": "PATORUZÚ"}
],
    "Rosco Real 18✓":[
  {"letra": "A", "pista": "Con la A: País de América del Sur cuya capital es Buenos Aires y es el último campeón de la Copa del Mundo.", "respuesta": "Argentina"},
  {"letra": "B", "pista": "Con la B: Persona que tiene por oficio barrer.", "respuesta": "Barrendero"},
  {"letra": "C", "pista": "Con la C: Uno u otro, sea el que sea.", "respuesta": "Cualquiera"},
  {"letra": "D", "pista": "Con la D: Sacar de su lugar las piezas óseas de la parte posterior del cuello.", "respuesta": "Desnucar"},
  {"letra": "E", "pista": "Con la E: Mamífero insectívoro nocturno de unos 20 centímetros de largo con el dorso y los costados cubiertos de agudas púas que en caso de peligro se enrolla.", "respuesta": "Erizo"},
  {"letra": "F", "pista": "Con la F: Tienda o puesto donde se vende fruta.", "respuesta": "Frutería"},
  {"letra": "G", "pista": "Con la G: Nombre de la cantante estadounidense de apellido Gaynor, intérprete de temas como I Will Survive.", "respuesta": "Gloria"},
  {"letra": "H", "pista": "Con la H: Universidad privada ubicada en Cambridge, Estados Unidos, que fue fundada en 1636.", "respuesta": "Harvard"},
  {"letra": "I", "pista": "Con la I: Representar en la mente la imagen de algo o de alguien.", "respuesta": "Imaginar"},
  {"letra": "J", "pista": "Contiene la J: Recipiente que cubierto con una tapa suelta o unida a la parte principal, sirve para guardar o transportar en él algo.", "respuesta": "Caja"},
  {"letra": "L", "pista": "Con la L: Parte de la espalda comprendida entre la cintura y los glúteos.", "respuesta": "Lumbares"},
  {"letra": "M", "pista": "Con la M: Movimiento periódico alternativo del ascenso y descenso de las aguas del mar producido por la atracción del sol y de la luna.", "respuesta": "Marea"},
  {"letra": "N", "pista": "Con la N: Computadora portátil también llamada laptop.", "respuesta": "Notebook"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Que tiene poco pelo o vello.", "respuesta": "Lampiño"},
  {"letra": "O", "pista": "Con la O: Nombre del actor uruguayo protagonista junto a Soledad Silveyra de la novela Amor en Custodia.", "respuesta": "Osvaldo"},
  {"letra": "P", "pista": "Con la P: Calabaza en forma de fruta pomácea con cuello que sirve para diversos usos, especialmente para cebar mate.", "respuesta": "PORONGO"},
  {"letra": "Q", "pista": "Contiene la Q: Entablado del suelo hecho con madera fina de varios tonos que convenientemente ensambladas forman dibujos geométricos.", "respuesta": "Parquet"},
  {"letra": "R", "pista": "Con la R: Volver a absorber.", "respuesta": "Reabsorber"},
  {"letra": "S", "pista": "Con la S: Natural del sur de África.", "respuesta": "Sudafricano"},
  {"letra": "T", "pista": "Con la T: Artista de circo que trabaja en los aparatos de gimnasia consistentes en una barra horizontal suspendida.", "respuesta": "Trapecista"},
  {"letra": "U", "pista": "Contiene la U: Cazo con mango cuchara grande que sirve para repartir ciertos alimentos en la mesa y para ciertos usos culinarios.", "respuesta": "Cucharón"},
  {"letra": "V", "pista": "Con la V: Sección quirúrgica de un vaso conducto, especialmente de los deferentes, en el aparato genital masculino.", "respuesta": "Vasectomía"},
  {"letra": "X", "pista": "Contiene la X: Quitar el componente vital del aire de una sustancia con la cual estaba combinado.", "respuesta": "Desoxigenar"},
  {"letra": "Y", "pista": "Contiene la Y: Apellido del personaje principal de la trilogía erótica cuya segunda entrega se llama 50 sombras más oscuras.", "respuesta": "Grey"},
  {"letra": "Z", "pista": "Contiene la Z: Golpe dado con la herramienta cortante de madera.", "respuesta": "Hachazo"}
],
    "Rosco Real 19✓": [
  {"letra": "A", "pista": "Con la A: Cada uno de los dos aretes de oro que se ponen para impedir que se cierren los agujeros de las orejas.", "respuesta": "Abridor"},
  {"letra": "B", "pista": "Con la B: Utensilio para la lactancia artificial que consiste en una botella pequeña con una tetina de goma elástica.", "respuesta": "Biberón"},
  {"letra": "C", "pista": "Con la C: Dicho de una situación o de un momento crítico, decisivo.", "respuesta": "Crucial"},
  {"letra": "D", "pista": "Con la D: Quitar los proyectiles de un elemento de fuego.", "respuesta": "Descargar"},
  {"letra": "E", "pista": "Con la E: Pulsera sin adornos y que no se abre.", "respuesta": "Esclava"},
  {"letra": "F", "pista": "Con la F: Nombre del personaje de la película protagonizada por Tom Hanks de apellido Gump.", "respuesta": "Forrest"},
  {"letra": "G", "pista": "Con la G: En atletismo, vara larga de material flexible usada para tomar impulso en el salto de altura.", "respuesta": "Garrocha"},
  {"letra": "H", "pista": "Con la H: ¿Qué puede ser ocupado como vivienda?", "respuesta": "Habitable"},
  {"letra": "I", "pista": "Con la I: Palabra o frase que se emplea para solicitar una información.", "respuesta": "Interrogación - Interrogante"},
  {"letra": "J", "pista": "Con la J: Nombre artístico del cantautor y poeta estadounidense de apellido Morrison, líder de The Doors.", "respuesta": "Jim"},
  {"letra": "L", "pista": "Con la L: Sustancia líquida e incolora que se emplea para fijar el peinado.", "respuesta": "Laca"},
  {"letra": "M", "pista": "Con la M: Instrumento pequeño para reducir a polvo café o semillas.", "respuesta": "Molinillo"},
  {"letra": "N", "pista": "Con la N: Seudónimo del historietista y humorista gráfico argentino, creador de Gaturro.", "respuesta": "Nik"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Salsa que se hace con carne picada, tomate y especias para acompañar la pasta.", "respuesta": "Boloñesa"},
  {"letra": "O", "pista": "Con la O: Que tiene el órgano de la audición de gran tamaño.", "respuesta": "Orejudo"},
  {"letra": "P", "pista": "Con la P: Mazo o atado de plumas u otro material sujeto a un mango que sirve para quitar la suciedad volátil.", "respuesta": "Plumero"},
  {"letra": "Q", "pista": "Contiene la Q: Forma diminutiva de referirse a una pequeña ave psitaciforme.", "respuesta": "Periquito"},
  {"letra": "R", "pista": "Con la R: Instrumento de mango largo con un travesaño armado de púas para recoger hierba o paja.", "respuesta": "Rastrillo"},
  {"letra": "S", "pista": "Con la S: Bolsa hermética descartable que sirve para contener líquidos como la leche.", "respuesta": "Sachet"},
  {"letra": "T", "pista": "Con la T: Carácter o manera de ser y de reaccionar de las personas.", "respuesta": "Temperamento"},
  {"letra": "U", "pista": "Con la U: Sección de los centros médicos en que se atiende a los heridos graves que necesitan cuidados inmediatos.", "respuesta": "Urgencias"},
  {"letra": "V", "pista": "Con la V: Nombre de pila de la actual vicepresidenta de la nación argentina.", "respuesta": "Victoria"},
  {"letra": "X", "pista": "Contiene la X: Noticia conseguida y publicada por un solo medio informativo.", "respuesta": "Exclusiva"},
  {"letra": "Y", "pista": "Contiene la Y: Pronombre posesivo de tercera persona.", "respuesta": "Suyo"},
  {"letra": "Z", "pista": "Contiene la Z: Líquido para quitar la rigidez y dar fragancia a la indumentaria.", "respuesta": "Suavizante"}
],
    "Rosco Real 20✓":[
  {"letra": "A", "pista": "Con la A: Dicho de una persona nacida bajo el signo zodiacal de Acuario.", "respuesta": "ACUARIANA"},
  {"letra": "B", "pista": "Con la B: En los cuentos infantiles o relatos folclóricos, mujer fea y malvada que tiene poderes mágicos y que generalmente puede volar montada en una escoba.", "respuesta": "BRUJA"},
  {"letra": "C", "pista": "Con la C: Que tiene un precio alto o más alto de lo normal.", "respuesta": "COSTOSO"},
  {"letra": "D", "pista": "Con la D: Nombre de pila del chef italiano, miembro del jurado del show de cocina Masterchef y Masterchef Celebrity.", "respuesta": "DONATO"},
  {"letra": "E", "pista": "Con la E: Dedicado al estudio.", "respuesta": "ESTUDIOSO"},
  {"letra": "F", "pista": "Con la F: Olor suave y delicioso.", "respuesta": "FRAGANCIA"},
  {"letra": "G", "pista": "Con la G: Dicho de un color semejante al de la ceniza o el acero y que resulta de mezclar el blanco y el negro.", "respuesta": "GRIS"},
  {"letra": "H", "pista": "Contiene la H: Cerdo.", "respuesta": "CHANCHO"},
  {"letra": "I", "pista": "Con la I: Que no se puede tocar.", "respuesta": "INTOCABLE"},
  {"letra": "J", "pista": "Con la J: Cuarto día de la semana.", "respuesta": "JUEVES"},
  {"letra": "L", "pista": "Con la L: Nombre de la perra de raza collie protagonista de su propio show televisivo que se mantuvo durante 19 temporadas entre 1954 y 1973.", "respuesta": "LASSIE"},
  {"letra": "M", "pista": "Con la M: Habitante imaginario del planeta Marte.", "respuesta": "MARCIANO"},
  {"letra": "N", "pista": "Con la N: Gasolina.", "respuesta": "NAFTA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Porción de cosas sueltas que se puede contener en el puño.", "respuesta": "PUÑADO"},
  {"letra": "O", "pista": "Con la O: Persona que se ocupa de establecer las comunicaciones no automáticas de una central telefónica.", "respuesta": "OPERADORA"},
  {"letra": "P", "pista": "Con la P: País sudamericano ubicado al norte de la República Argentina y cuya capital y ciudad más poblada es Asunción.", "respuesta": "PARAGUAY"},
  {"letra": "Q", "pista": "Contiene la Q: Tienda de ropa de moda.", "respuesta": "BOUTIQUE"},
  {"letra": "R", "pista": "Con la R: Pintalabios.", "respuesta": "ROUGE"},
  {"letra": "S", "pista": "Con la S: Apellido de la actriz argentina apodada La Coca e intérprete de películas como Fuego, Fiebre y Una Vida Descocada.", "respuesta": "SARLI"},
  {"letra": "T", "pista": "Con la T: Nombre artístico de la cantante argentina e intérprete de canciones como Cupido, Miénteme y La Niña de la Escuela.", "respuesta": "TINI"},
  {"letra": "U", "pista": "Contiene la U: Privado de la facultad de hablar.", "respuesta": "MUDO"},
  {"letra": "V", "pista": "Con la V: Hembra del toro.", "respuesta": "VACA"},
  {"letra": "X", "pista": "Contiene la X: Dicho de una persona especializada con grandes conocimientos en una materia.", "respuesta": "EXPERTO"},
  {"letra": "Y", "pista": "Contiene la Y: Condimento originario de la India compuesto por una mezcla de polvo de diversas especias.", "respuesta": "CURRY"},
  {"letra": "Z", "pista": "Contiene la Z: Voz muy fuerte y gruesa.", "respuesta": "VOZARRÓN"}
],
    "Rosco Real 21✓": [
  {"letra": "A", "pista": "Con la A: Golosina compuesta por dos rodajas delgadas de masa adheridas una a otra con dulce y a veces recubierta con chocolate, merengue, etcétera.", "respuesta": "ALFAJOR"},
  {"letra": "B", "pista": "Con la B: Ceremonia mediante la cual se unen en matrimonio dos personas y fiesta con que se celebra.", "respuesta": "BODA"},
  {"letra": "C", "pista": "Con la C: País sudamericano ubicado al otro lado de la cordillera de los Andes y cuya capital es Santiago.", "respuesta": "CHILE"},
  {"letra": "D", "pista": "Con la D: Persona que practica algún deporte por afición o profesionalmente.", "respuesta": "DEPORTISTA"},
  {"letra": "E", "pista": "Con la E: Plato que se toma al principio de una comida.", "respuesta": "ENTRADA"},
  {"letra": "F", "pista": "Con la F: Propio de la mujer o que posee características atribuidas a ella.", "respuesta": "FEMENINO"},
  {"letra": "G", "pista": "Con la G: Apellido del actor argentino de cine tradicional, teatro y televisión famoso por su interpretación de la abuela Mamá Cora.", "respuesta": "GASALLA"},
  {"letra": "H", "pista": "Con la H: Que tiene profundidad.", "respuesta": "HONDO"},
  {"letra": "I", "pista": "Con la I: Máquina que, conectada a una computadora u otro dispositivo electrónico, imprime los resultados de las operaciones.", "respuesta": "IMPRESORA"},
  {"letra": "J", "pista": "Con la J: Nombre del travieso ratoncito de caricaturas que es perseguido por su archienemigo, el gato Tom.", "respuesta": "JERRY"},
  {"letra": "L", "pista": "Con la L: Sitio especialmente dispuesto para lavar la ropa.", "respuesta": "LAVADERO"},
  {"letra": "M", "pista": "Con la M: Apellido del ex entrenador de fútbol argentino apodado El Flaco, campeón con la selección en el Mundial de Argentina 78.", "respuesta": "MENOTTI"},
  {"letra": "N", "pista": "Con la N: Ninguna cosa.", "respuesta": "NADA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Cartera pequeña que se lleva sujeta a la cintura.", "respuesta": "RIÑONERA"},
  {"letra": "O", "pista": "Con la O: Número natural que sigue al 79.", "respuesta": "OCHENTA"},
  {"letra": "P", "pista": "Con la P: Apellido del cantante argentino e intérprete de temas como Porque aún te amo, Como tú y Sin testigos.", "respuesta": "PEREYRA"},
  {"letra": "Q", "pista": "Contiene la Q: Calcetín corto que cubre el pie hasta el tobillo.", "respuesta": "ZOQUETE"},
  {"letra": "R", "pista": "Con la R: Fotografía de una persona.", "respuesta": "RETRATO"},
  {"letra": "S", "pista": "Con la S: Plato compuesto de un caldo y uno o más ingredientes sólidos cocidos en él.", "respuesta": "SOPA"},
  {"letra": "T", "pista": "Con la T: Porción de agua u otro líquido que se bebe o se puede beber de una vez.", "respuesta": "TRAGO"},
  {"letra": "U", "pista": "Contiene la U: Que tiene mucho pelo.", "respuesta": "PELUDO"},
  {"letra": "V", "pista": "Con la V: Persona que recibe un trato especial en ciertos lugares públicos por ser famosa o socialmente relevante.", "respuesta": "VIP"},
  {"letra": "X", "pista": "Contiene la X: Que exige mucho.", "respuesta": "EXIGENTE"},
  {"letra": "Y", "pista": "Con la Y: Añadidura, especialmente la que se da como propina o regalo.", "respuesta": "YAPA"},
  {"letra": "Z", "pista": "Contiene la Z: Ruido fuerte producido con una bocina.", "respuesta": "BOCINAZO"}
],
    "Rosco Real 22✓": [
  {"letra": "A", "pista": "Con la A: Profesión y ejercicio del abogado.", "respuesta": "ABOGACÍA"},
  {"letra": "B", "pista": "Con la B: Bandera pequeña usada como emblema de instituciones o equipos deportivos.", "respuesta": "BANDERÍN"},
  {"letra": "C", "pista": "Con la C: Orilla del mar, de un río o lago y tierra que está cerca de ella.", "respuesta": "COSTA"},
  {"letra": "D", "pista": "Con la D: Conjunto de dientes, muelas y colmillos que tiene en la boca una persona o un animal.", "respuesta": "DENTADURA"},
  {"letra": "E", "pista": "Con la E: Natural de Entre Ríos, provincia de la Argentina.", "respuesta": "ENTRERRIANO"},
  {"letra": "F", "pista": "Con la F: Principio de igualdad de derechos de la mujer y el hombre.", "respuesta": "FEMINISMO"},
  {"letra": "G", "pista": "Con la G: Apellido del ex futbolista argentino conocido como el arquero ataje penales durante la Copa Mundial de Fútbol Italia 1990.", "respuesta": "GOYCOCHEA"},
  {"letra": "H", "pista": "Con la H: Establecimiento destinado al diagnóstico y tratamiento de enfermos donde a menudo se practica la investigación y la docencia.", "respuesta": "HOSPITAL"},
  {"letra": "I", "pista": "Con la I: Cataratas ubicadas en el norte de la provincia de Misiones sobre el río homónimo.", "respuesta": "IGUAZÚ"},
  {"letra": "J", "pista": "Con la J: Cara humana.", "respuesta": "JETA"},
  {"letra": "L", "pista": "Con la L: Depósito natural de agua, generalmente dulce y de menores dimensiones que el lago.", "respuesta": "LAGUNA"},
  {"letra": "M", "pista": "Con la M: Nombre que recibe el bloque económico creado en 1991 por acuerdo entre Argentina, Brasil, Paraguay y Uruguay.", "respuesta": "MERCOSUR"},
  {"letra": "N", "pista": "Con la N: Lugar donde ponen las aves.", "respuesta": "NIDO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Prenda interior femenina para ceñir el pecho.", "respuesta": "CORPIÑO"},
  {"letra": "O", "pista": "Con la O: Punto cardinal del horizonte por donde se pone el sol en los equinoccios.", "respuesta": "OESTE"},
  {"letra": "P", "pista": "Con la P: Salsa preparada con albahaca, piñones y ajo machacados y aceite.", "respuesta": "PESTO"},
  {"letra": "Q", "pista": "Contiene la Q: Muro o construcción para contener las aguas.", "respuesta": "DIQUE"},
  {"letra": "R", "pista": "Con la R: Película de 1982 protagonizada por Sylvester Stallone en el rol de un veterano de la guerra de Vietnam.", "respuesta": "RAMBO"},
  {"letra": "S", "pista": "Con la S: Apellido de la cantante argentina de folclore fallecida en 2009, intérprete de Gracias a la vida.", "respuesta": "SOSA"},
  {"letra": "T", "pista": "Con la T: Tortilla de maíz enrollada con algún alimento dentro, típica de México.", "respuesta": "TACO"},
  {"letra": "U", "pista": "Con la U: Toma de conexión universal de uso frecuente en las computadoras.", "respuesta": "USB"},
  {"letra": "V", "pista": "Con la V: Venganza derivada de las rencillas entre familias, clanes o grupos rivales.", "respuesta": "VENDETTA"},
  {"letra": "X", "pista": "Contiene la X: Sobaco.", "respuesta": "AXILA"},
  {"letra": "Y", "pista": "Con la Y: Conjunto de disciplinas físico-mentales originales de la India.", "respuesta": "YOGA"},
  {"letra": "Z", "pista": "Con la Z: Ciencia que trata de los animales.", "respuesta": "ZOOLOGÍA"}
],
    "Rosco Real 23✓": [
  {"letra": "A", "pista": "Con la A: Sala donde se dan las clases en los centros docentes.", "respuesta": "AULA"},
  {"letra": "B", "pista": "Con la B: Establecimiento generalmente industrial para la elaboración de vinos.", "respuesta": "BODEGA"},
  {"letra": "C", "pista": "Con la C: Persona que por oficio trabaja y labra madera ordinariamente común.", "respuesta": "CARPINTERO"},
  {"letra": "D", "pista": "Con la D: Combate o pelea entre dos a consecuencia de un reto o desafío.", "respuesta": "DUELO"},
  {"letra": "E", "pista": "Con la E: Obra de escultura labrada a imitación del natural.", "respuesta": "ESTATUA"},
  {"letra": "F", "pista": "Con la F: Que da buena imagen fotográfica.", "respuesta": "FOTOGÉNICO"},
  {"letra": "G", "pista": "Con la G: Película romántica de un fantasma que visita a su enamorada a través de un médium.", "respuesta": "GHOST"},
  {"letra": "H", "pista": "Contiene la H: Emparedado de chorizo asado.", "respuesta": "CHORIPAN"},
  {"letra": "I", "pista": "Con la I: Que sirve para matar insectos.", "respuesta": "INSECTICIDA"},
  {"letra": "J", "pista": "Contiene la J: Boleto o billete para un viaje.", "respuesta": "PASAJE"},
  {"letra": "L", "pista": "Con la L: Máquina movida por vapor o motor que arrastra los vagones de un tren.", "respuesta": "LOCOMOTORA"},
  {"letra": "M", "pista": "Con la M: Cubierta de lino o algodón que se pone en la mesa para comer.", "respuesta": "MANTEL"},
  {"letra": "N", "pista": "Con la N: Club italiano de fútbol que contrató a Diego Maradona en 1984.", "respuesta": "NAPOLI"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Apellido de la actriz argentina que encarna a Moni Argento.", "respuesta": "PEÑA"},
  {"letra": "O", "pista": "Con la O: Mar de gran extensión que separa dos o más continentes.", "respuesta": "OCÉANO"},
  {"letra": "P", "pista": "Con la P: Parte inferior cóncava de la mano desde la muñeca hasta los dedos.", "respuesta": "PALMA"},
  {"letra": "Q", "pista": "Contiene la Q: Conjunto de cosas que se llevan en los viajes.", "respuesta": "EQUIPAJE"},
  {"letra": "R", "pista": "Con la R: Rueda giratoria utilizada en juegos de azar.", "respuesta": "RULETA"},
  {"letra": "S", "pista": "Con la S: País africano que fue sede del mundial de fútbol en 2010.", "respuesta": "SUDÁFRICA"},
  {"letra": "T", "pista": "Con la T: Que no está frío ni caliente.", "respuesta": "TIBIO"},
  {"letra": "U", "pista": "Contiene la U: Cama pequeña para niños con bordes altos o barandillas.", "respuesta": "CUNA"},
  {"letra": "V", "pista": "Con la V: Apellido del autor de libros como 20.000 leguas de viaje submarino.", "respuesta": "VERNE"},
  {"letra": "X", "pista": "Contiene la X: Ave fabulosa que los antiguos creyeron que renacía de sus cenizas.", "respuesta": "FÉNIX"},
  {"letra": "Y", "pista": "Contiene la Y: Queso suave de origen suizo fabricado con leche de vaca.", "respuesta": "GRUYÈRE - GRUYER"},
  {"letra": "Z", "pista": "Con la Z: Paso largo que se da con movimiento acelerado.", "respuesta": "ZANCADA"}
],
    "Rosco Real 24✓": [
  {"letra": "A", "pista": "Con la A: Bebida que se toma antes de una comida principal.", "respuesta": "APERITIVO"},
  {"letra": "B", "pista": "Con la B: Prenda larga y estrecha por lo común de lana o seda con que se envuelve y abriga el cuello y la boca.", "respuesta": "BUFANDA"},
  {"letra": "C", "pista": "Con la C: Película de terror de 1976 protagonizada por Sissy Spacek en el papel de una estudiante con telequinesis que se venga de sus compañeros en su graduación.", "respuesta": "CARRIE"},
  {"letra": "D", "pista": "Con la D: De poco vigor o de poca fuerza o resistencia.", "respuesta": "DÉBIL"},
  {"letra": "E", "pista": "Con la E: Que se enamora fácilmente.", "respuesta": "ENAMORADIZO"},
  {"letra": "F", "pista": "Con la F: Natural de Filipinas, país de Asia.", "respuesta": "FILIPINO"},
  {"letra": "G", "pista": "Con la G: Unidad que equivale aproximadamente a mil millones de bytes.", "respuesta": "GIGA"},
  {"letra": "H", "pista": "Con la H: Agua convertida en cuerpo sólido y cristalino por un descenso suficiente de temperatura.", "respuesta": "HIELO"},
  {"letra": "I", "pista": "Con la I: Vigilia, falta de sueño a la hora de dormir.", "respuesta": "INSOMNIO"},
  {"letra": "J", "pista": "Con la J: Nombre artístico de Juan Aristizábal Vázquez, cantante colombiano, intérprete de temas como La camisa negra y Adiós le pido.", "respuesta": "JUANES"},
  {"letra": "L", "pista": "Con la L: Parte del libro opuesta al corte de las hojas en la cual se pone el rótulo.", "respuesta": "LOMO"},
  {"letra": "M", "pista": "Con la M: Grupo de músicos callejeros que interpretan canciones satíricas en los carnavales.", "respuesta": "MURGA"},
  {"letra": "N", "pista": "Con la N: Parte del día comprendido entre la puesta del sol y el amanecer.", "respuesta": "NOCHE"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: En fútbol, acción en la que se sortea un contrario pasándole el balón entre las piernas.", "respuesta": "CAÑO"},
  {"letra": "O", "pista": "Con la O: Abertura. Agujero.", "respuesta": "ORIFICIO"},
  {"letra": "P", "pista": "Con la P: Calvo.", "respuesta": "PELADO"},
  {"letra": "Q", "pista": "Contiene la Q: Ruido o sonido que se hace roncando.", "respuesta": "RONQUIDO"},
  {"letra": "R", "pista": "Con la R: Rotulador de punta ancha y color muy vivo que se usa para resaltar una parte de un texto pasándolo por encima.", "respuesta": "RESALTADOR"},
  {"letra": "S", "pista": "Con la S: Persona asociada con otra u otras para algún fin.", "respuesta": "SOCIO"},
  {"letra": "T", "pista": "Con la T: Nombre de la ciudad más densamente poblada y capital de Japón.", "respuesta": "TOKIO"},
  {"letra": "U", "pista": "Con la U: Mundo.", "respuesta": "UNIVERSO"},
  {"letra": "V", "pista": "Con la V: Dicho de una persona que tiene el arte de modificar su voz de manera que parezca venir de lejos y que imita la de otras personas o diversos sonidos.", "respuesta": "VENTRÍLOCUO"},
  {"letra": "X", "pista": "Con la X: Apodo de origen genovés con el que se conocen los jugadores y seguidores del club atlético Boca Juniors.", "respuesta": "XENEIZES"},
  {"letra": "Y", "pista": "Contiene la Y: Nombre de ratón de animación más popular del cine y la televisión. Vive con su perro Pluto y es novio de Minnie.", "respuesta": "MICKEY"},
  {"letra": "Z", "pista": "Con la Z: Calabaza comestible.", "respuesta": "ZAPALLO"}
],
    "Rosco Real 25✓": [
  {"letra": "A", "pista": "Con la A: Corte de carne que se saca longitudinalmente en tiras del costillar vacuno.", "respuesta": "ASADO"},
  {"letra": "B", "pista": "Con la B: Nombre de la serie estadounidense TV del género western que cuenta las aventuras de la familia Cartwright en el rancho La Ponderosa.", "respuesta": "BONANZA"},
  {"letra": "C", "pista": "Con la C: Gran toldo que cubre un circo o cualquier otro recinto amplio.", "respuesta": "CARPA"},
  {"letra": "D", "pista": "Con la D: Habitación situada en la parte más alta de la casa por lo general aislada.", "respuesta": "DESVÁN"},
  {"letra": "E", "pista": "Con la E: Apellido del físico alemán que formuló la teoría de la relatividad y ganó el premio Nobel de física en 1921.", "respuesta": "EINSTEIN"},
  {"letra": "F", "pista": "Con la F: Plato grande más o menos hondo que se usa para servir los alimentos.", "respuesta": "FUENTE"},
  {"letra": "G", "pista": "Con la G: Apellido del actor y director de cine australiano, protagonista de films como Mad Max, Arma mortal y Corazón valiente.", "respuesta": "GIBSON"},
  {"letra": "H", "pista": "Contiene la H: Caja o estuche que sirve para guardar plumas, lápices, etc.", "respuesta": "CARTUCHERA"},
  {"letra": "I", "pista": "Con la I: Que no puede morir.", "respuesta": "INMORTAL"},
  {"letra": "J", "pista": "Contiene la J: Pimiento.", "respuesta": "AJÍ"},
  {"letra": "L", "pista": "Con la L: Líquido blanco que segregan las mamas de las hembras de los mamíferos para alimento de sus crías.", "respuesta": "LECHE"},
  {"letra": "M", "pista": "Con la M: Pieza que rodea, ciñe o guarnece un cuadro u otra cosa semejante.", "respuesta": "MARCO"},
  {"letra": "N", "pista": "Con la N: País centroamericano famoso por sus playas y volcanes, cuya capital y ciudad más poblada es Managua.", "respuesta": "NICARAGUA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Que escatima excesivamente en el gasto.", "respuesta": "TACAÑO"},
  {"letra": "O", "pista": "Con la O: Producto rebajado de precio.", "respuesta": "OFERTA"},
  {"letra": "P", "pista": "Con la P: Sustancia generalmente líquida que se utiliza para dar buen olor.", "respuesta": "PERFUME"},
  {"letra": "Q", "pista": "Contiene la Q: Dicho de una figura especialmente de un triángulo, que tiene todos sus lados iguales.", "respuesta": "EQUILÁTERO"},
  {"letra": "R", "pista": "Con la R: Apodo de Richard Starkey. Músico y cantante británico famoso por haber sido el baterista de The Beatles.", "respuesta": "RINGO"},
  {"letra": "S", "pista": "Con la S: Excursión de caza mayor que se realiza en algunas regiones de África.", "respuesta": "SAFARI"},
  {"letra": "T", "pista": "Con la T: Prueba psicológica para estudiar alguna función.", "respuesta": "TEST"},
  {"letra": "U", "pista": "Contiene la U: Tiene por oficio cuidar las manos y principalmente cortar y pulir las uñas.", "respuesta": "MANICURA"},
  {"letra": "V", "pista": "Con la V: Ala que tiene por delante las gorras y otras prendas semejantes para resguardar el rostro.", "respuesta": "VISERA"},
  {"letra": "X", "pista": "Contiene la X: Noticia conseguida y publicada por un solo medio informativo que se reserva los derechos de su difusión.", "respuesta": "EXCLUSIVA"},
  {"letra": "Y", "pista": "Contiene la Y: Salsa que se hace batiendo aceite y huevo.", "respuesta": "MAYONESA"},
  {"letra": "Z", "pista": "Contiene la Z: Bebida alcohólica hecha con granos germinados de cebada u otros cereales fermentados en agua y aromatizada con lúpulo.", "respuesta": "CERVEZA"}
],
    "Rosco Real 26✓": [
  {"letra": "A", "pista": "Con la A: Deporte que consiste en escalar montañas.", "respuesta": "ALPINISMO"},
  {"letra": "B", "pista": "Con la B: Voz media entre la de tenor y la de bajo.", "respuesta": "BARÍTONO"},
  {"letra": "C", "pista": "Con la C: Manjar que consiste en huevas de esturión frescas y saladas.", "respuesta": "CAVIAR"},
  {"letra": "D", "pista": "Con la D: Resuelto, audaz, que actúa con decisión.", "respuesta": "DECIDIDO"},
  {"letra": "E", "pista": "Con la E: Mueble cerrado con divisiones en su parte interior para guardar papeles y a veces con un tablero sobre el cual se escribe.", "respuesta": "ESCRITORIO"},
  {"letra": "F", "pista": "Con la F: Acción de frenar súbita y violentamente.", "respuesta": "FRENADA"},
  {"letra": "G", "pista": "Con la G: En el fútbol, regate.", "respuesta": "GAMBETA"},
  {"letra": "H", "pista": "Con la H: La tragedia escrita por William Shakespeare. Nombre del príncipe de Dinamarca que pronuncia su famoso soliloquio, ser o no ser.", "respuesta": "HAMLET"},
  {"letra": "I", "pista": "Con la I: Elevación de nivel general de precios.", "respuesta": "INFLACIÓN"},
  {"letra": "J", "pista": "Contiene la J: Que tiene rojo el pelo.", "respuesta": "PELIRROJO"},
  {"letra": "L", "pista": "Con la L: Ciudad bonaerense en donde se encuentra la basílica de estilo gótico del Santuario de la Virgen visitado normalmente por miles de peregrinos.", "respuesta": "LUJÁN"},
  {"letra": "M", "pista": "Con la M: Barrita de grafito que va en el interior del lápiz.", "respuesta": "MINA"},
  {"letra": "N", "pista": "Con la N: Dicho de un vehículo automóvil, de una máquina o de motor que usa nafta como combustible.", "respuesta": "NAFTERO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Natural de Salta, ciudad y provincia de la Argentina.", "respuesta": "SALTEÑO"},
  {"letra": "O", "pista": "Con la O: Que ocupa en una serie el lugar número 8.", "respuesta": "OCTAVO"},
  {"letra": "P", "pista": "Con la P: Apellido del escritor estadounidense, autor de relatos de terror como El Cuervo, Los Asesinatos de la Calle Morgue y El Corazón Delator.", "respuesta": "POE"},
  {"letra": "Q", "pista": "Contiene la Q: Conducto de las vías respiratorias que va desde la laringe a los bronquios.", "respuesta": "TRÁQUEA"},
  {"letra": "R", "pista": "Con la R: Borde labrado que se hace de las empanadas o pasteles alrededor de la masa.", "respuesta": "REPULGUE"},
  {"letra": "S", "pista": "Con la S: Carencia voluntaria o involuntaria de compañía.", "respuesta": "SOLEDAD"},
  {"letra": "T", "pista": "Con la T: Italiano.", "respuesta": "TANO"},
  {"letra": "U", "pista": "Contiene la U: Operación matemática de sumar.", "respuesta": "SUMA"},
  {"letra": "V", "pista": "Con la V: Dicho de un equipo o de un deportista que compite en el campo o terreno de juego ajeno.", "respuesta": "VISITANTE"},
  {"letra": "X", "pista": "Contiene la X: Apellido del actor estadounidense y ganador de un Oscar por su papel en la película de 2019 Joker.", "respuesta": "PHOENIX"},
  {"letra": "Y", "pista": "Contiene la Y: Chispa eléctrica de gran intensidad producida por descarga entre dos nubes o entre la nube y la tierra.", "respuesta": "RAYO"},
  {"letra": "Z", "pista": "Contiene la Z: Dicho de un hermano.", "respuesta": "MELLIZO"}
],
    "Rosco Real 27✓": [
  {"letra": "A", "pista": "Con la A: Que cultiva o practica sin ser profesional un arte, oficio, ciencia, deporte, etc.", "respuesta": "AMATEUR"},
  {"letra": "B", "pista": "Con la B: Apellido del boxeador argentino de peso pesado asesinado en 1976, recordado por su combate de 1970 frente al campeón Muhammad Ali.", "respuesta": "BONAVENA"},
  {"letra": "C", "pista": "Con la C: Parte más estrecha del tronco del cuerpo humano por arriba de las caderas.", "respuesta": "CINTURA"},
  {"letra": "D", "pista": "Con la D: Local público donde se sirven bebidas y se baila al son de música grabada.", "respuesta": "DISCOTECA"},
  {"letra": "E", "pista": "Con la E: Desecho, broza y cascote que queda de una obra de albañilería o de un edificio arruinado o derribado.", "respuesta": "ESCOMBRO"},
  {"letra": "F", "pista": "Con la F: Apellido del actor estadounidense de origen afroamericano, intérprete de films como Conduciendo a Miss Daisy, Pecados Capitales y Sueño de Libertad.", "respuesta": "FREEMAN"},
  {"letra": "G", "pista": "Con la G: Muy frío.", "respuesta": "GÉLIDO"},
  {"letra": "H", "pista": "Con la H: Inflamación del hígado.", "respuesta": "HEPATITIS"},
  {"letra": "I", "pista": "Con la I: Comienzo.", "respuesta": "INICIO"},
  {"letra": "J", "pista": "Contiene la J: Acto o serie de actos que se celebran en honor de alguien o de algo.", "respuesta": "HOMENAJE"},
  {"letra": "L", "pista": "Con la L: Cuaderno o libro pequeño destinado a escribir anotaciones o cuentas.", "respuesta": "LIBRETA"},
  {"letra": "M", "pista": "Con la M: Banda estadounidense de heavy metal, intérprete de temas como Enter Sandman y Nothing Else Matters.", "respuesta": "METALLICA"},
  {"letra": "N", "pista": "Con la N: Que incluye gran número o muchedumbre de personas o cosas.", "respuesta": "NUMEROSO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Enredo de los hilos o del cabello.", "respuesta": "MARAÑA"},
  {"letra": "O", "pista": "Con la O: Cesación de la memoria que se tenía.", "respuesta": "OLVIDO"},
  {"letra": "P", "pista": "Con la P: Apodo de Waldo Matildo Fillol, ex arquero del club Atlético River Plate y de la Selección Nacional de Fútbol.", "respuesta": "PATO"},
  {"letra": "Q", "pista": "Contiene la Q: Especie de puerta rústica en un alambrado hecha generalmente con trancas.", "respuesta": "TRANQUERA"},
  {"letra": "R", "pista": "Con la R: En el fútbol, golpe al balón con una pierna cruzada por detrás de la otra.", "respuesta": "RABONA"},
  {"letra": "S", "pista": "Con la S: Apellido del cantante estadounidense apodado el Jefe e intérprete de temas como Born in the U.S.A. y Dancing in the Dark.", "respuesta": "SPRINGSTEEN"},
  {"letra": "T", "pista": "Con la T: Persona que da testimonio de algo o lo testigua.", "respuesta": "TESTIGO"},
  {"letra": "U", "pista": "Contiene la U: Lente de aumento, generalmente con un mango.", "respuesta": "LUPA"},
  {"letra": "V", "pista": "Con la V: Nombre de la tercera ciudad más poblada de España, ubicada sobre el mar Mediterráneo, famosa mundialmente por su típica paella.", "respuesta": "VALENCIA"},
  {"letra": "X", "pista": "Contiene la X: Mechón postizo que se agrega al pelo para alargarlo o hacerlo más voluminoso.", "respuesta": "EXTENSIÓN"},
  {"letra": "Y", "pista": "Contiene la Y: El día que antecede inmediatamente al de hoy.", "respuesta": "AYER"},
  {"letra": "Z", "pista": "Contiene la Z: Mujer del emperador.", "respuesta": "EMPERATRIZ"}
],
    "Rosco Programa 5-A (28)✓": [
  {"letra": "A", "pista": "Con la A: Área destinada al aterrizaje y despegue de aviones dotada de instalaciones para el control del tráfico aéreo y de servicios a los pasajeros.","respuesta": "aeropuerto"},
  {"letra": "B", "pista": "Con la B: En un teatro o en un cine, asiento con brazos y respaldos para una persona.","respuesta": "butaca"},
  {"letra": "C", "pista": "Con la C: Persona encargada de llevar los libros de contabilidad.","respuesta": "contador"},
  {"letra": "D", "pista": "Con la D: Mujer noble o distinguida.","respuesta": "dama"},
  {"letra": "E", "pista": "Con la E: Arma de fuego portátil con uno o dos cañones que dispara cartuchos o perdigones y suele utilizarse para cazar.","respuesta": "escopeta"},
  {"letra": "F", "pista": "Con la F: Apellido del piloto argentino de la Fórmula 1 apodado Chueco que hasta el año 2003 fue el máximo ganador de la competencia con cinco coronas.","respuesta": "fangio"},
  {"letra": "G", "pista": "Con la G: Natural del país del Reino Unido ubicado al oeste de la isla de Gran Bretaña.","respuesta": "galés"},
  {"letra": "H", "pista": "Con la H: Disciplina que estudia y narra cronológicamente los acontecimientos pasados.","respuesta": "historia"},
  {"letra": "I", "pista": "Con la I: Que carece de utilidad u obligatoriedad.","respuesta": "innecesario"},
  {"letra": "J", "pista": "Contiene la J: Deuda, falta o pérdida injustificada de dinero en la administración de una entidad.","respuesta": "agujero"},
  {"letra": "L", "pista": "Con la L: Hermoso, bello, grato a la vista.","respuesta": "lindo"},
  {"letra": "M", "pista": "Con la M: Juego parecido al golf que se practica en un campo de dimensiones muy reducidas con obstáculos artificiales.","respuesta": "minigolf"},
  {"letra": "N", "pista": "Con la N: País europeo situado en la región de Escandinavia cuya capital es la ciudad de Oslo.","respuesta": "noruega"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: De dimensiones inferiores a otros de su misma clase.","respuesta": "pequeño"},
  {"letra": "O", "pista": "Con la O: Aptitud para percibir y reproducir los temas y melodías musicales.","respuesta": "oído"},
  {"letra": "P", "pista": "Con la P: Apellido de la cantante argentina de folclore, intérprete de canciones como El Antigal, A don Ata y Que nadie sepa mi sufrir.","respuesta": "pastorutti"},
  {"letra": "Q", "pista": "Contiene la Q: Jugador que en algunos deportes defiende la portería de su bando.","respuesta": "arquero"},
  {"letra": "R", "pista": "Con la R: Jefe espiritual de una comunidad judía.","respuesta": "rabino"},
  {"letra": "S", "pista": "Con la S: Película animada de 2001 protagonizada por un ogro verde que en compañía de su amigo burro va al rescate de la princesa Fiona.","respuesta": "shrek"},
  {"letra": "T", "pista": "Con la T: Macho bovino adulto.","respuesta": "toro"},
  {"letra": "U", "pista": "Con la U: Parte inferior o escalón por lo común de piedra y contrapuesto al dintel en la puerta o entrada de una casa.","respuesta": "umbral"},
  {"letra": "V", "pista": "Con la V: Dicho de un sitio que está con menos gente de la que puede concurrir a él.","respuesta": "vacío"},
  {"letra": "X", "pista": "Contiene la X: Conjunto de seis instrumentos o voces o de sus ejecutantes.","respuesta": "sexteto"},
  {"letra": "Y", "pista": "Contiene la Y: Monarca soberano de un reino.","respuesta": "rey"},
  {"letra": "Z", "pista": "Contiene la Z: Apellido de la conductora, animadora y psicóloga que presenta su magazine en las tardes por la pantalla de Telefe.","respuesta": "lozano"}
],
    "Rosco Programa 5-B (29)✓": [
  {"letra": "A", "pista": "Con la A: Electrodoméstico que sirve para limpiar el polvo absorbiéndolo.","respuesta": "aspiradora"},
  {"letra": "B", "pista": "Con la B: Sustancia espesa y abundante que fluye a veces de la boca humana y de algunos mamíferos.","respuesta": "baba"},
  {"letra": "C", "pista": "Con la C: Película clásica de 1942 protagonizada por Humphrey Bogart e Ingrid Bergman, quien inmortalizó la frase tócala de nuevo Sam.","respuesta": "casablanca"},
  {"letra": "D", "pista": "Con la D: Producto que se utiliza para suprimir el olor corporal o de algún recinto.","respuesta": "desodorante"},
  {"letra": "E", "pista": "Con la E: Unidad monetaria común a los estados de la Unión Económica y Monetaria Europea.","respuesta": "euro"},
  {"letra": "F", "pista": "Con la F: Reunión de gente para celebrar algo o divertirse.","respuesta": "fiesta"},
  {"letra": "G", "pista": "Con la G: Dicho de un sonido que tiene una frecuencia baja de vibraciones por oposición al sonido agudo.","respuesta": "grave"},
  {"letra": "H", "pista": "Contiene la H: Nombre de la ciudad capital de los Estados Unidos de América.","respuesta": "washington"},
  {"letra": "I", "pista": "Con la I: Disco membranoso del ojo de los vertebrados y cefalópodos en cuyo centro está la pupila.","respuesta": "iris"},
  {"letra": "J", "pista": "Contiene la J: Persona que ejerce la cirugía.","respuesta": "cirujano"},
  {"letra": "L", "pista": "Con la L: Plato de carne, papas, maíz y otros ingredientes usado en varios países de América del Sur.","respuesta": "locro"},
  {"letra": "M", "pista": "Con la M: En la serie animada Los Simpson, nombre del iracundo dueño del bar de Springfield en el cual Homero y sus amigos pasan horas bebiendo cerveza.","respuesta": "moe"},
  {"letra": "N", "pista": "Con la N: Hijo del hijo de una persona.","respuesta": "nieto"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Pieza de artillería de gran longitud respecto a su calibre, destinada a lanzar balas, metralla o proyectiles huecos.","respuesta": "cañón"},
  {"letra": "O", "pista": "Con la O: Que presenta oscurecimiento bajo los ojos por falta de descanso.","respuesta": "ojeroso"},
  {"letra": "P", "pista": "Con la P: Apodo del cantante argentino de cumbia ex concursante de MasterChef conocido por sus canciones Deja de llorar y Ya no quiero verte.","respuesta": "polaco"},
  {"letra": "Q", "pista": "Contiene la Q: Soporte que se coloca en el techo de un vehículo para llevar maletas y otros bultos.","respuesta": "portaequipaje"},
  {"letra": "R", "pista": "Con la R: Ondulación en forma de espiral del cabello.","respuesta": "rulo"},
  {"letra": "S", "pista": "Con la S: Sensación que ciertos cuerpos producen en el órgano del gusto.","respuesta": "sabor"},
  {"letra": "T", "pista": "Con la T: Infracción maliciosa de las reglas de un juego o de una competición.","respuesta": "trampa"},
  {"letra": "U", "pista": "Contiene la U: Dicho de un fruto que ha alcanzado el grado de desarrollo adecuado para su consumo.","respuesta": "maduro"},
  {"letra": "V", "pista": "Con la V: Estación del año que sucede a la primavera y precede al otoño.","respuesta": "verano"},
  {"letra": "X", "pista": "Contiene la X: Espacios al aire libre donde se rueda una película.","respuesta": "exteriores"},
  {"letra": "Y", "pista": "Contiene la Y: Apellido de la jugadora de hockey sobre césped, capitana de Las Leonas, elegida la mejor del mundo en ocho ocasiones.","respuesta": "aymar"},
  {"letra": "Z", "pista": "Contiene la Z: Amor que súbitamente se siente o se inspira.","respuesta": "flechazo"}
],
    "Primer Rosco Programa 6-A (30)✓": [
  {"letra": "A", "pista": "Con la A: Lugar donde se corta la madera u otra cosa","respuesta": "ASERRADERO"},
  {"letra": "B", "pista": "Con la B: Tela con marcas y colores distintivos que se utiliza para hacer señales","respuesta": "BANDERA"},
  {"letra": "C", "pista": "Con la C: Vendedor callejero de periódicos","respuesta": "CANILLITA"},
  {"letra": "D", "pista": "Con la D: Nombre del personaje literario creado por Stoker en su novela de terror de 1897 representado como un conde vampiro oriundo de Transilvania","respuesta": "DRÁCULA"},
  {"letra": "E", "pista": "Con la E: Parte posterior del cuerpo humano desde los hombros hasta la cintura","respuesta": "ESPALDA"},
  {"letra": "F", "pista": "Con la F: En la tira cómica Casados con Hijos, nombre del perro dormilón que es la mascota de la familia Argento","respuesta": "FATIGA"},
  {"letra": "G", "pista": "Con la G: Persona que en los juegos del circo romano luchaba con otra o con fieras","respuesta": "GLADIADOR"},
  {"letra": "H", "pista": "Contiene la H: Adiós o hasta luego","respuesta": "CHAU"},
  {"letra": "I", "pista": "Con la I: Que no se debe o puede disculpar","respuesta": "IMPERDONABLE"},
  {"letra": "J", "pista": "Contiene la J: Comida exquisita","respuesta": "MANJAR"},
  {"letra": "L", "pista": "Con la L: Reborde exterior carnoso y móvil de la boca de los mamíferos","respuesta": "LABIO"},
  {"letra": "M", "pista": "Con la M: Imagen, video o texto por lo general distorsionado con fines caricaturescos que se difunde principalmente a través de internet","respuesta": "MEME"},
  {"letra": "N", "pista": "Con la N: Provincia argentina ubicada en la Patagonia que posee atractivos turísticos como el Parque Nacional Los Arrayanes, Villa La Angostura o el volcán Lanín","respuesta": "NEUQUÉN"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Trozo de tela cuadrado o rectangular que se emplea en la cocina para secar la vajilla o para cualquier otro uso","respuesta": "PAÑO"},
  {"letra": "O", "pista": "Con la O: Aplauso ruidoso que colectivamente se tributa a alguien o algo","respuesta": "OVACIÓN"},
  {"letra": "P", "pista": "Con la P: Nombre de pila de la recordada cocinera de televisión que popularizó la frase este plato es un poema","respuesta": "PETRONA"},
  {"letra": "Q", "pista": "Contiene la Q: Técnica de escribir tan deprisa como se habla por medio de ciertos signos y abreviaturas","respuesta": "TAQUIGRAFÍA"},
  {"letra": "R", "pista": "Con la R: Agotado, muy cansado","respuesta": "ROTO"},
  {"letra": "S", "pista": "Con la S: Dicho de un alimento preparado de manera que quede inflado","respuesta": "SUFLÉ"},
  {"letra": "T", "pista": "Con la T: Voz media entre la de contralto y la de barítono","respuesta": "TENOR"},
  {"letra": "U", "pista": "Contiene la U: Objeto con una parte de goma o materia similar en forma de pezón que se da a los niños para que succionen","respuesta": "CHUPETE"},
  {"letra": "V", "pista": "Con la V: Holgazán, perezoso, poco trabajador","respuesta": "VAGO"},
  {"letra": "X", "pista": "Contiene la X: Relajamiento físico o psíquico producido por ejercicios adecuados o por comodidad, bienestar o cualquier otra causa","respuesta": "RELAX"},
  {"letra": "Y", "pista": "Con la Y: Supuesto gigante antropomorfo del cual se dice que vive en el Himalaya","respuesta": "YETI"},
  {"letra": "Z", "pista": "Contiene la Z: Casualidad, caso fortuito","respuesta": "AZAR"}
],
    "Primer Rosco Programa 6-B (31)✓": [
  {"letra": "A", "pista": "Con la A: Dicho de un software que detecta la presencia de código malicioso y puede neutralizar sus efectos","respuesta": "ANTIVIRUS"},
  {"letra": "B", "pista": "Con la B: País sudamericano, el más extenso de la región, reconocido mundialmente por sus carnavales multitudinarios, la samba y la bossa nova","respuesta": "BRASIL"},
  {"letra": "C", "pista": "Con la C: Servicio de suministro de comidas y bebidas a aviones, trenes, colegios, etcétera","respuesta": "CATERING"},
  {"letra": "D", "pista": "Con la D: Secuencia de dos vocales diferentes que se pronuncian en una sola sílaba, por ejemplo aire, puerta","respuesta": "DIPTONGO"},
  {"letra": "E", "pista": "Con la E: Nombre de la ópera rock de 1978 compuesta por Andrew Lloyd Webber en la que se popularizó un icónico tema dedicado a la Argentina","respuesta": "EVITA"},
  {"letra": "F", "pista": "Con la F: De pocas carnes","respuesta": "FLACO - FAMÉLICO"},
  {"letra": "G", "pista": "Con la G: Lugar vallado o cobertizo donde se crían ciertas aves de corral que ponen huevos","respuesta": "GALLINERO"},
  {"letra": "H", "pista": "Con la H: Dormitorio o cuarto de una vivienda","respuesta": "HABITACIÓN"},
  {"letra": "I", "pista": "Con la I: Que es igual a otro con que se compara","respuesta": "IDÉNTICO"},
  {"letra": "J", "pista": "Contiene la J: Camino más corto que el principal para llegar a un lugar","respuesta": "ATAJO"},
  {"letra": "L", "pista": "Con la L: Plancha pequeña y redonda de metal o material brillante que se cose a los vestidos como adorno","respuesta": "LENTEJUELA"},
  {"letra": "M", "pista": "Con la M: Argentino considerado el mejor basquetbolista del país, ganador de cuatro títulos de la asociación norteamericana jugando para San Antonio Spurs","respuesta": "MANU"},
  {"letra": "N", "pista": "Con la N: Periodista encargado de recoger y dar novedades o información para prensa, radio o televisión","respuesta": "NOTERO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Natural de la capital de España o de su comunidad autónoma homónima","respuesta": "MADRILEÑO"},
  {"letra": "O", "pista": "Con la O: Octava hora después del mediodía","respuesta": "OCHO"},
  {"letra": "P", "pista": "Con la P: Apellido del actor estadounidense de ascendencia italiana protagonista de filmes como Perfume de mujer, El Padrino y El Irlandés","respuesta": "PACINO"},
  {"letra": "Q", "pista": "Contiene la Q: Máquina destinada a regular mediante pago el tiempo de estacionamiento de los vehículos","respuesta": "PARQUÍMETRO"},
  {"letra": "R", "pista": "Con la R: Ira, enojo, enfado grande","respuesta": "RABIA"},
  {"letra": "S", "pista": "Con la S: Personaje de cómics creado en 1933 caracterizado como superhéroe volador con fuerza sobrehumana cuyo apodo es el Hombre de Acero","respuesta": "SUPERMAN"},
  {"letra": "T", "pista": "Con la T: Tabla elástica colocada sobre una plataforma y desde la que se lanza al agua el nadador","respuesta": "TRAMPOLÍN"},
  {"letra": "U", "pista": "Contiene la U: Dicho de un sonido que tiene una frecuencia alta de vibraciones por oposición al sonido grave","respuesta": "AGUDO"},
  {"letra": "V", "pista": "Con la V: Persona del sexo masculino","respuesta": "VARÓN"},
  {"letra": "X", "pista": "Contiene la X: Que tiene gran aceptación popular o triunfa en lo que hace","respuesta": "EXITOSO"},
  {"letra": "Y", "pista": "Contiene la Y: Criado principal a cuyo cargo está el gobierno económico de una casa o hacienda","respuesta": "MAYORDOMO"},
  {"letra": "Z", "pista": "Contiene la Z: Dicho festivo y gracioso","respuesta": "CHANZA"}
],
    "Segundo Rosco Programa 6-A (32)✓": [
  {"letra": "A", "pista": "Con la A: Símbolo usado en las direcciones de correo electrónico que separa el nombre del usuario del dominio al que pertenece", "respuesta": "arroba"},
  {"letra": "B", "pista": "Con la B: En una prenda de vestir, pieza generalmente redonda y plana que se introduce en un ojal para abrochar", "respuesta": "botón"},
  {"letra": "C", "pista": "Con la C: Dicho de una persona que come carne humana", "respuesta": "caníbal"},
  {"letra": "D", "pista": "Con la D: Nombre del simpático elefantito de circo de grandes orejas las cuales le permitían volar y que protagonizó la película animada de 1941", "respuesta": "Dumbo"},
  {"letra": "E", "pista": "Con la E: Sello de correos o fiscal", "respuesta": "estampilla"},
  {"letra": "F", "pista": "Con la F: Poseído de ira", "respuesta": "furioso"},
  {"letra": "G", "pista": "Con la G: Alimento compuesto de copos de avena y otros cereales mezclados con frutos secos", "respuesta": "granola"},
  {"letra": "H", "pista": "Con la H: Partidario entusiasta de alguien o algo especialmente de un equipo deportivo", "respuesta": "hincha"},
  {"letra": "I", "pista": "Con la I: Apellido del cantante español de baladas románticas intérprete de canciones como Me olvidé de vivir, Me va me va y Agua dulce, agua salá", "respuesta": "Iglesias"},
  {"letra": "J", "pista": "Contiene la J: Risa impetuosa y ruidosa", "respuesta": "carcajada"},
  {"letra": "L", "pista": "Con la L: Nombre del personaje principal de la saga Star Wars de apellido Skywalker, aprendiz del caballero Jedi discípulo de Obi-Wan", "respuesta": "Luke"},
  {"letra": "M", "pista": "Con la M: Lugar en que se conservan y exponen colecciones de objetos artísticos, científicos, etcétera", "respuesta": "museo"},
  {"letra": "N", "pista": "Con la N: Ninguna persona", "respuesta": "nadie"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Parte de los árboles y matas que cortada y hecha trozos se emplea como combustible", "respuesta": "leña"},
  {"letra": "O", "pista": "Con la O: Mandato que se debe obedecer, observar y ejecutar", "respuesta": "orden"},
  {"letra": "P", "pista": "Con la P: Ciudad de Francia en la que se ubica la Torre Eiffel, el Arco del Triunfo y el Paseo de los Campos Elíseos", "respuesta": "París"},
  {"letra": "Q", "pista": "Contiene la Q: Lance del ajedrez en que un jugador, mediante el movimiento de una pieza, amenaza directamente al rey del otro con obligación de avisarlo", "respuesta": "jaque"},
  {"letra": "R", "pista": "Con la R: Conjunto de uvas sostenidas en un mismo tallo que pende del sarmiento", "respuesta": "racimo"},
  {"letra": "S", "pista": "Con la S: Apellido de la ex tenista argentina ganadora del US Open de 1990 y la medalla de plata de los Juegos Olímpicos de Seúl 1988", "respuesta": "Sabatini"},
  {"letra": "T", "pista": "Con la T: Instrumento de mesa en forma de horca con dos o más púas y que sirve para comer alimentos sólidos", "respuesta": "tenedor"},
  {"letra": "U", "pista": "Contiene la U: Manejo ilícito para conseguir un fin y especialmente para lucrarse", "respuesta": "fraude"},
  {"letra": "V", "pista": "Con la V: Dicho de un color semejante al de la hierba fresca o al de la esmeralda y que ocupa el cuarto lugar en el espectro luminoso", "respuesta": "verde"},
  {"letra": "X", "pista": "Contiene la X: Que no se puede herrumbrar ni corroer", "respuesta": "inoxidable"},
  {"letra": "Y", "pista": "Con la Y: Estadounidense", "respuesta": "yanqui"},
  {"letra": "Z", "pista": "Contiene la Z: Persona o animal que guía o acompaña a otra necesitada de ayuda", "respuesta": "lazarillo"}
],
    "Segundo Rosco Programa 6-B (33)✓": [
  {"letra": "A", "pista": "Con la A: Mueble con puertas y estantes o perchas para guardar ropa y otros objetos", "respuesta": "armario"},
  {"letra": "B", "pista": "Con la B: En el cuento de los Hermanos Grimm, nombre de la bella princesa que vive en el bosque con siete enanitos tras haber huido de su madrastra", "respuesta": "Blancanieves"},
  {"letra": "C", "pista": "Con la C: Tela que por lo común cuelga de puertas y ventanas como adorno o para aislar de la luz y de miradas ajenas", "respuesta": "cortina"},
  {"letra": "D", "pista": "Con la D: Que causa o implica sufrimiento físico o moral", "respuesta": "doloroso"},
  {"letra": "E", "pista": "Con la E: Aparato destinado a calentar un recinto por electricidad o combustión de madera, gas, etcétera", "respuesta": "estufa"},
  {"letra": "F", "pista": "Con la F: Representación de un espectáculo especialmente teatral o proyección de una película", "respuesta": "función"},
  {"letra": "G", "pista": "Con la G: Natural del país heleno ubicado en el sureste de Europa", "respuesta": "griego"},
  {"letra": "H", "pista": "Contiene la H: Cría del perro y algunos mamíferos como el león, el lobo, el oso, etcétera", "respuesta": "cachorro"},
  {"letra": "I", "pista": "Con la I: Apellido del ex delantero sueco de nombre Zlatan", "respuesta": "Ibrahimovic"},
  {"letra": "J", "pista": "Contiene la J: Pieza de cartulina u otro material, generalmente rectangular y de pequeño tamaño, usada para escribir o imprimir algo", "respuesta": "tarjeta"},
  {"letra": "L", "pista": "Con la L: Nombre de la ciudad más poblada y capital del Reino Unido de Gran Bretaña", "respuesta": "Londres"},
  {"letra": "M", "pista": "Con la M: Dicho de un color semejante al de la caja de la castaña o el pelaje de la ardilla", "respuesta": "marrón"},
  {"letra": "N", "pista": "Con la N: Práctica y deporte consistentes en avanzar en el agua moviendo el cuerpo", "respuesta": "natación"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Golpe que se da con el puño cerrado", "respuesta": "piña"},
  {"letra": "O", "pista": "Con la O: Regalo que se hace u ofrenda", "respuesta": "obsequio"},
  {"letra": "P", "pista": "Con la P: Nombre de pila del cantante argentino de rap y freestyle nacido en Córdoba, autor e intérprete de temas como Nena Maldición, Forever Alone y Tenso", "respuesta": "Paulo"},
  {"letra": "Q", "pista": "Contiene la Q: Asiento de tres o cuatro pies y sin respaldo", "respuesta": "banqueta"},
  {"letra": "R", "pista": "Con la R: Dicho de quien compite con otra pugnando por obtener una misma cosa o por superar a aquella", "respuesta": "rival"},
  {"letra": "S", "pista": "Con la S: Juego que practica una sola persona, especialmente si es el de naipes", "respuesta": "solitario"},
  {"letra": "T", "pista": "Con la T: Pieza de felpa, algodón u otro material, por lo general rectangular, para secarse el cuerpo", "respuesta": "toalla"},
  {"letra": "U", "pista": "Con la U: Que requiere atención rápida o apremiante", "respuesta": "urgente"},
  {"letra": "V", "pista": "Con la V: Acelerado, ligero y pronto en el movimiento", "respuesta": "veloz"},
  {"letra": "X", "pista": "Contiene la X: Apellido del actor canadiense actualmente retirado por su papel de Marty McFly en la saga de films Volver al Futuro", "respuesta": "Fox"},
  {"letra": "Y", "pista": "Con la Y: Porción central del huevo de los vertebrados ovíparos", "respuesta": "yema"},
  {"letra": "Z", "pista": "Contiene la Z: Persona que se prende de amor con facilidad de otras", "respuesta": "enamoradizo"}
],
    "Rosco Programa 7-A (34)✓": [
  {"letra": "A", "pista": "Con la A: firma de una persona famosa o notable", "respuesta": "autógrafo"},
  {"letra": "B", "pista": "Con la B: apellido de la actriz argentina conductora de show matutino diario por pantalla", "respuesta": "Barbarossa"},
  {"letra": "C", "pista": "Con la C: servicio público que tiene por objeto el transporte de cartas y paquetes oficiales y privados", "respuesta": "correo"},
  {"letra": "D", "pista": "Con la D: número natural que sigue al ciento noventa y nueve", "respuesta": "doscientos"},
  {"letra": "E", "pista": "Con la E: dicho de una persona que tiene buen gusto y distinción para vestir", "respuesta": "elegante"},
  {"letra": "F", "pista": "Con la F: cubierta generalmente de papel que se pone a un libro o un cuaderno para protegerlo", "respuesta": "folio - forro"},
  {"letra": "G", "pista": "Con la G: manjar delicado generalmente dulce que sirve más para el gusto que para el sustento", "respuesta": "golosina"},
  {"letra": "H", "pista": "Contiene la H: experto en determinada actividad", "respuesta": "canchero"},
  {"letra": "I", "pista": "Con la I: propenso a creer con demasiada facilidad o sin tener en cuenta la realidad", "respuesta": "iluso"},
  {"letra": "J", "pista": "Con la J: apellido del cantante británico líder del legendario grupo de rock The Rolling Stones", "respuesta": "Jagger"},
  {"letra": "L", "pista": "Con la L: agua que cae de las nubes", "respuesta": "lluvia"},
  {"letra": "M", "pista": "Con la M: nombre de la adorable pero macabra esposa de Homero en la famosa familia", "respuesta": "Morticia"},
  {"letra": "N", "pista": "Con la N: caja o estuche con objetos de tocador o costura", "respuesta": "neceser"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: lengua romance que se originó en la Península Ibérica y se habla en gran parte de América", "respuesta": "español"},
  {"letra": "O", "pista": "Con la O: tratamiento de las irregularidades y anomalías en la posición de los dientes y maxilares", "respuesta": "ortodoncia"},
  {"letra": "P", "pista": "Con la P: país europeo que ocupa la parte occidental de la Península Ibérica, su capital es Lisboa", "respuesta": "Portugal"},
  {"letra": "Q", "pista": "Contiene la Q: comida espléndida y exquisita", "respuesta": "banquete"},
  {"letra": "R", "pista": "Con la R: espacio de tiempo especialmente cuando es corto", "respuesta": "rato"},
  {"letra": "S", "pista": "Con la S: persona o equipo que se clasifica en el puesto número dos en un torneo", "respuesta": "subcampeón"},
  {"letra": "T", "pista": "Con la T: parte del día comprendida entre el mediodía y el anochecer", "respuesta": "tarde"},
  {"letra": "U", "pista": "Contiene la U: trozo pequeño de hielo generalmente cuadrado que se añade a una bebida para enfriarla", "respuesta": "cubito"},
  {"letra": "V", "pista": "Con la V: especie de caja provista de un asa que sirve sobre todo en los viajes para transportar ropas", "respuesta": "valija"},
  {"letra": "X", "pista": "Contiene la X: que es adecuado o está destinado tanto para los hombres como para las mujeres", "respuesta": "unisex"},
  {"letra": "Y", "pista": "Contiene la Y: bulto o paquete de equipaje", "respuesta": "bagayo"},
  {"letra": "Z", "pista": "Con la Z: película cómica de 2001 protagonizada en el papel de un modelo lindo pero muy despistado", "respuesta": "Zoolander"}
],
    "Rosco Programa 7-B (35)✓": [
  {"letra": "A", "pista": "Con la A: fruto del olivo", "respuesta": "aceituna"},
  {"letra": "B", "pista": "Con la B: natural del país de América del Sur que limita con Argentina al norte", "respuesta": "boliviano"},
  {"letra": "C", "pista": "Con la C: programa de televisión infantil de la década de 1990 sobre las aventuras de un grupo de niños que jugaban al fútbol", "respuesta": "Cebollitas"},
  {"letra": "D", "pista": "Con la D: apellido del actor estadounidense protagonista de films como Titanic y El Aviador", "respuesta": "DiCaprio"},
  {"letra": "E", "pista": "Con la E: arma defensiva que se lleva embrazada para cubrirse y resguardarse de otras agresiones", "respuesta": "escudo"},
  {"letra": "F", "pista": "Con la F: que tiene la opinión general o la mayor probabilidad de ganar en una competición", "respuesta": "favorito"},
  {"letra": "G", "pista": "Con la G: hombre de campo experimentado en las faenas tradicionales", "respuesta": "gaucho"},
  {"letra": "H", "pista": "Con la H: aparato electrodoméstico, cámara o mueble que produce frío para conservar alimentos", "respuesta": "heladera"},
  {"letra": "I", "pista": "Con la I: fuego grande que destruye lo que no debería quemarse", "respuesta": "incendio"},
  {"letra": "J", "pista": "Contiene la J: local destinado a guardar automóviles", "respuesta": "garaje"},
  {"letra": "L", "pista": "Con la L: bebida compuesta de agua, azúcar y jugo cítrico amarillo", "respuesta": "limonada"},
  {"letra": "M", "pista": "Con la M: apellido del cantante estadounidense que lideró el grupo de rock The Doors", "respuesta": "Morrison"},
  {"letra": "N", "pista": "Con la N: bruma poco espesa y baja", "respuesta": "neblina"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: banda que se pone alrededor del antebrazo para sujetarla o protegerla como adorno", "respuesta": "muñequera"},
  {"letra": "O", "pista": "Con la O: persona que compite o se enfrenta a otra", "respuesta": "oponente"},
  {"letra": "P", "pista": "Con la P: que tiene la piel del rostro más blanca o con menos color de lo normal", "respuesta": "pálido"},
  {"letra": "Q", "pista": "Contiene la Q: persona que ha tomado una casa o parte de ella en alquiler para habitarla", "respuesta": "inquilino"},
  {"letra": "R", "pista": "Con la R: cilindro hueco y perforado al que se arrolla el cabello para rizarlo", "respuesta": "rulero"},
  {"letra": "S", "pista": "Con la S: encargado de velar por la protección del vecindario o de la propiedad", "respuesta": "sereno"},
  {"letra": "T", "pista": "Con la T: historia de ficción filmada y grabada para ser emitida por capítulos en la pantalla chica", "respuesta": "telenovela"},
  {"letra": "U", "pista": "Contiene la U: apellido del exjugador argentino de fútbol que se destacó en el Manchester City y Barcelona", "respuesta": "Agüero"},
  {"letra": "V", "pista": "Con la V: que se hace por espontánea elección y no por obligación o deber", "respuesta": "voluntario"},
  {"letra": "X", "pista": "Contiene la X: conjuro contra el demonio", "respuesta": "exorcismo"},
  {"letra": "Y", "pista": "Contiene la Y: país sudamericano situado al este de la República Argentina, su capital es Montevideo", "respuesta": "Uruguay"},
  {"letra": "Z", "pista": "Contiene la Z: derrota amplia que alguien inflige o padece en una disputa o en cualquier enfrentamiento", "respuesta": "paliza"}
],
    "Rosco Programa 8-A (36)": [
  {"letra": "A", "pista": "Con la A: Técnica terapéutica de la medicina tradicional china consistente en introducir agujas en puntos determinados del cuerpo del paciente.", "respuesta": "acupuntura"},
  {"letra": "B", "pista": "Con la B: Que tiene un precio bajo o más bajo de lo normal.", "respuesta": "barato"},
  {"letra": "C", "pista": "Con la C: Apellido del actor y comediante canadiense estadounidense famoso por sus papeles en los films La Máscara y Tonto y Retonto.", "respuesta": "Carrey"},
  {"letra": "D", "pista": "Con la D: Periódico que se publica cada jornada.", "respuesta": "diario"},
  {"letra": "E", "pista": "Con la E: Punto cardinal del horizonte por donde sale el sol en los equinoccios.", "respuesta": "este"},
  {"letra": "F", "pista": "Con la F: Término y remate de algo.", "respuesta": "final"},
  {"letra": "G", "pista": "Con la G: País europeo ubicado en el mar Mediterráneo cuya capital es la ciudad de Atenas.", "respuesta": "Grecia"},
  {"letra": "H", "pista": "Con la H: Hijo de uno de los cónyuges respecto al hijo del otro.", "respuesta": "hermanastro"},
  {"letra": "I", "pista": "Con la I: Lengua de un pueblo, nación o común a varios.", "respuesta": "idioma"},
  {"letra": "J", "pista": "Con la J: En ningún tiempo o circunstancia.", "respuesta": "jamás"},
  {"letra": "L", "pista": "Con la L: Voz que emite con fuerza el perro, más o menos parecida a la onomatopeya guau.", "respuesta": "ladrido"},
  {"letra": "M", "pista": "Con la M: Apellido del empresario sudafricano de nombre Elon, conocido por sus aportes en el desarrollo del automóvil eléctrico y la industria aeroespacial.", "respuesta": "Musk"},
  {"letra": "N", "pista": "Con la N: Que es susceptible de ser objeto de comercio o transacciones.", "respuesta": "negociable"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Natural de la provincia argentina ubicada en la región del Norte Grande, cuya capital homónima se encuentra a orillas del río Paraguay.", "respuesta": "formoseño"},
  {"letra": "O", "pista": "Con la O: Obra dramática musical cuyo texto se canta total o parcialmente con acompañamiento de orquesta.", "respuesta": "ópera"},
  {"letra": "P", "pista": "Con la P: Apellido del ex futbolista y máximo goleador de Boca Juniors apodado El Loco.", "respuesta": "Palermo"},
  {"letra": "Q", "pista": "Contiene la Q: Persona que tiene por oficio cortar el cabello o hacer y vender postizos, rizos, etcétera.", "respuesta": "peluquero"},
  {"letra": "R", "pista": "Con la R: Espacio limitado por cuerdas y con suelo de lona donde tienen lugar combates de boxeo y de otros tipos de lucha.", "respuesta": "ring"},
  {"letra": "S", "pista": "Con la S: Falta de ruido.", "respuesta": "silencio"},
  {"letra": "T", "pista": "Con la T: Sucesión de actos de violencia ejecutados para infundir pánico o miedo extremo.", "respuesta": "terrorismo"},
  {"letra": "U", "pista": "Contiene la U: Que llega a un lugar o parte a la hora convenida.", "respuesta": "puntual"},
  {"letra": "V", "pista": "Con la V: Banda argentina de rock fundada por los hermanos Moura en 1980, entre sus éxitos figuran Una luna de miel en la mano y Wadu Wadu.", "respuesta": "Virus"},
  {"letra": "X", "pista": "Con la X: Aversión, odio o rechazo hacia las personas nacidas en otros países.", "respuesta": "xenofobia"},
  {"letra": "Y", "pista": "Contiene la Y: Lápiz o barrita de diferentes materias para dibujar, pintar o colorear.", "respuesta": "crayón"},
  {"letra": "Z", "pista": "Con la Z: Que tiene tendencia natural a servirse preferentemente de la mano izquierda o también del pie del mismo lado.", "respuesta": "zurdo"}
],
    "Rosco Programa 8-B (37)": [
  {"letra": "A", "pista": "Con la A: Personaje de Las mil y una noches que encuentra una lámpara mágica que al ser frotada invoca los favores de un poderoso genio.", "respuesta": "aladín - aladino"},
  {"letra": "B", "pista": "Con la B: Tarjeta o papel impresos que dan derecho a viajar en un medio de transporte.", "respuesta": "boleto"},
  {"letra": "C", "pista": "Con la C: Papel escrito y ordinariamente cerrado que una persona envía a otra para comunicarse con ella.", "respuesta": "carta"},
  {"letra": "D", "pista": "Con la D: Conjunto de grabaciones musicales de un autor, un intérprete o un estilo.", "respuesta": "discografía"},
  {"letra": "E", "pista": "Con la E: Ocupación, oficio.", "respuesta": "empleo"},
  {"letra": "F", "pista": "Con la F: Tienda donde se venden arreglos botánicos y plantas de adorno.", "respuesta": "florería - floristería"},
  {"letra": "G", "pista": "Con la G: Aficionado a comer dulces y manjares.", "respuesta": "goloso"},
  {"letra": "H", "pista": "Con la H: Que tiene el esqueleto muy marcado debajo de la piel.", "respuesta": "huesudo"},
  {"letra": "I", "pista": "Con la I: Dicho de un líquido que no se puede tragar o que resulta muy desagradable al gusto.", "respuesta": "imbebible"},
  {"letra": "J", "pista": "Contiene la J: Poco apretado o poco tirante.", "respuesta": "flojo"},
  {"letra": "L", "pista": "Con la L: Nombre artístico de Mariana Espósito, cantante y actriz argentina intérprete de temas como Disciplina y Comprarme un brishito.", "respuesta": "Lali"},
  {"letra": "M", "pista": "Con la M: Facultad psíquica por medio de la cual se retiene y recuerda el pasado.", "respuesta": "memoria"},
  {"letra": "N", "pista": "Con la N: Natural del país soberano de África occidental cuya capital es Abuya.", "respuesta": "nigeriano"},
  {"letra": "Ñ", "pista": "Con la Ñ: Masa hecha con patatas mezcladas con harina de trigo, mantequilla, leche, huevo y queso rallado, dividida en trocitos que se cuecen en agua hirviendo con sal.", "respuesta": "ñoqui"},
  {"letra": "O", "pista": "Con la O: Nombre de pila del protagonista de la serie animada japonesa Los Super Campeones, futbolista prodigio.", "respuesta": "Oliver"},
  {"letra": "P", "pista": "Con la P: Hijo del tío de una persona.", "respuesta": "primo"},
  {"letra": "Q", "pista": "Con la Q: Período temporal equivalente a la mitad de un mes de treinta jornadas.", "respuesta": "quincena"},
  {"letra": "R", "pista": "Con la R: En los colegios, suspensión de la clase para descansar o jugar.", "respuesta": "recreo"},
  {"letra": "S", "pista": "Con la S: Pieza de tela o papel que usa cada comensal para limpiarse los labios y las manos.", "respuesta": "servilleta"},
  {"letra": "T", "pista": "Con la T: Estruendo asociado al rayo producido en las nubes por una descarga eléctrica.", "respuesta": "trueno"},
  {"letra": "U", "pista": "Contiene la U: País de Oceanía famoso en el mundo por ser la tierra de los canguros, su capital es la ciudad de Canberra.", "respuesta": "Australia"},
  {"letra": "V", "pista": "Contiene la V: Mamífero rumiante de cuernos ramificados, cuyo macho tiene astas.", "respuesta": "ciervo"},
  {"letra": "X", "pista": "Contiene la X: Persona que practica ritos religiosos para expulsar entidades malignas.", "respuesta": "exorcista"},
  {"letra": "Y", "pista": "Con la Y: Nombre del gran maestro jedi que entrena a Luke Skywalker en la saga de películas Star Wars.", "respuesta": "Yoda"},
  {"letra": "Z", "pista": "Contiene la Z: Golpe fuerte dado con el cráneo.", "respuesta": "cabezazo"}
],
    "Primer Rosco Programa 9-A (38)": [
  {"letra": "A", "pista": "Con la A: instrumento de agricultura que movido por fuerza animal o mecánica sirve para labrar la tierra abriendo surcos en ella","respuesta": "arado"},
  {"letra": "B", "pista": "Con la B: segunda letra del alfabeto griego que corresponde a la del latino","respuesta": "beta"},
  {"letra": "C", "pista": "Con la C: película argentina de 2010 dirigida por Pablo Trapero y protagonizada por Ricardo Darín en el papel de un abogado que lucra con accidentes de tránsito","respuesta": "carancho"},
  {"letra": "D", "pista": "Con la D: mezcla explosiva de nitroglicerina con otras sustancias","respuesta": "dinamita"},
  {"letra": "E", "pista": "Con la E: que tiene forma de cuerpo geométrico perfectamente redondo","respuesta": "esférico"},
  {"letra": "F", "pista": "Con la F: en el juego de la pelota pared principal contra la cual se lanza la misma","respuesta": "frontón"},
  {"letra": "G", "pista": "Con la G: instrumento de percusión formado por un disco suspendido que vibra al ser golpeado","respuesta": "gong"},
  {"letra": "H", "pista": "Contiene la H: bulto que de resultas de un golpe se hace en el cuero de la cabeza","respuesta": "chichón"},
  {"letra": "I", "pista": "Con la I: apellido del conductor de televisión reconocido por haber sido el presentador y animador de Laten Corazones y Polémica en el bar","respuesta": "iúdica"},
  {"letra": "J", "pista": "Contiene la J: lección o enseñanza que se deduce de un cuento fábula ejemplo anécdota etcétera","respuesta": "moraleja"},
  {"letra": "L", "pista": "Con la L: persona que tiene por oficio limpiar con agua y jabón la ropa","respuesta": "lavandera"},
  {"letra": "M", "pista": "Con la M: criar deficientemente a los hijos condescendiendo demasiado con sus gustos y caprichos","respuesta": "maleducar"},
  {"letra": "N", "pista": "Con la N: bebida hecha con zumo del cítrico homónimo agua y azúcar","respuesta": "naranjada"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: dicho de una persona que siente afecto o amor","respuesta": "cariñosa"},
  {"letra": "O", "pista": "Con la O: cumplir la voluntad de quien manda","respuesta": "obedecer"},
  {"letra": "P", "pista": "Con la P: ciudad capital de la provincia Entre Ríos unida a la ciudad de Santa Fe por el túnel subfluvial","respuesta": "paraná"},
  {"letra": "Q", "pista": "Contiene la Q: ausencia de poder público","respuesta": "anarquía"},
  {"letra": "R", "pista": "Con la R: persona retenida por alguien como garantía para obligar a un tercero a cumplir determinadas condiciones","respuesta": "rehén"},
  {"letra": "S", "pista": "Con la S: apellido del dramaturgo inglés el más importante de la literatura anglosajona autor de Macbeth La Tempestad y Romeo y Julieta","respuesta": "shakespeare"},
  {"letra": "T", "pista": "Con la T: muñeco que se mueve por medio de hilos u otro procedimiento","respuesta": "títere"},
  {"letra": "U", "pista": "Contiene la U: ombligo","respuesta": "pupo"},
  {"letra": "V", "pista": "Con la V: persona que se adelanta a su tiempo o tiene percepción adelantada de futuro","respuesta": "visionario"},
  {"letra": "X", "pista": "Contiene la X: nombre de pila artístico de William Bailey cantante de la banda de Hard Rock californiana Guns and Roses","respuesta": "axl"},
  {"letra": "Y", "pista": "Contiene la Y: carruaje de dos ruedas tirado por un caballo con asiento para dos o tres personas empleado para viajes cortos","respuesta": "sulky"},
  {"letra": "Z", "pista": "Contiene la Z: mentira embuste","respuesta": "saraza"}
],
    "Primer Rosco Programa 9-B (39)": [
  {"letra": "A","pista": "Con la A: que usa con la misma habilidad la mano izquierda y la derecha o el pie izquierdo y el derecho","respuesta": "ambidiestro"},
  {"letra": "B","pista": "Con la B: arrojar explosivos desde una aeronave sobre un lugar","respuesta": "bombardear"},
  {"letra": "C","pista": "Con la C: instrumento hecho de cerdas distribuidas en un armazón que sirve para distintos usos de limpieza","respuesta": "cepillo"},
  {"letra": "D","pista": "Con la D: Río de Europa al cual el compositor austríaco de música clásica Johann Strauss le dedicó su conocido vals","respuesta": "danubio"},
  {"letra": "E","pista": "Con la E: revestimiento de láminas decorativas que cubre la superficie de una pared baúl etcétera","respuesta": "empapelado"},
  {"letra": "F","pista": "Con la F: comida de origen suizo a base de queso que se funde dentro de una cazuela especial en el momento de comer","respuesta": "fondue"},
  {"letra": "G","pista": "Con la G: trío argentino de rock integrado por Willy Iturri Alfredo Toth y Pablo Guyot intérpretes de temas como La calle es su lugar","respuesta": "git"},
  {"letra": "H","pista": "Contiene la H: lucha libre","respuesta": "catch"},
  {"letra": "I","pista": "Con la I: persona que explica a otras en lengua que entienden lo dicho en otra que les es desconocida","respuesta": "intérprete"},
  {"letra": "J","pista": "Contiene la J: descendiente aportado al nuevo matrimonio por el cónyuge de una persona","respuesta": "hijastro"},
  {"letra": "L","pista": "Con la L: apodo o apellido del sindicalista y político que actualmente ocupa el cargo de presidente de la república federativa del Brasil","respuesta": "lula"},
  {"letra": "M","pista": "Con la M: texto redactado a pulso","respuesta": "manuscrito"},
  {"letra": "N","pista": "Con la N: originario en un lugar determinado","respuesta": "nativo - natural"},
  {"letra": "Ñ","pista": "Contiene la Ñ: agrupación de actores cantantes o bailarines unidos para representar espectáculos escénicos","respuesta": "compañía"},
  {"letra": "O","pista": "Con la O: percibir con el sentido auditivo los sonidos","respuesta": "oír"},
  {"letra": "P","pista": "Con la P: vehículo utilizado por el sumo pontífice en sus desplazamientos entre la multitud","respuesta": "papamóvil"},
  {"letra": "Q","pista": "Contiene la Q: cometer una infracción penal o crimen","respuesta": "delinquir"},
  {"letra": "R","pista": "Con la R: película animada de 2007 protagonizada por la simpática rata Remy quien ayuda al aprendiz de cocina Alfredo Linguini a convertirse en un famoso chef","respuesta": "ratatouille"},
  {"letra": "S","pista": "Con la S: apellido artístico del periodista experto en casos policiales autor de los libros No somos ángeles y La historia desconocida llamado Mauro","respuesta": "szeta"},
  {"letra": "T","pista": "Con la T: ola gigantesca producida por un maremoto o una erupción volcánica en el fondo del mar","respuesta": "tsunami"},
  {"letra": "U","pista": "Con la U: conjunto de objetos y enseres que se emplean en un escenario","respuesta": "utilería"},
  {"letra": "V","pista": "Con la V: abertura de la tierra y más comúnmente en una montaña por donde salen de tiempo en tiempo humos llamas y materias encendidas o derretidas","respuesta": "volcán"},
  {"letra": "X","pista": "Contiene la X: que carece de propiedades venenosas o dañinas para la salud","respuesta": "atóxico"},
  {"letra": "Y","pista": "Contiene la Y: programa de televisión que documenta situaciones sin guion protagonizadas por personas desconocidas o famosas","respuesta": "reality"},
  {"letra": "Z","pista": "Contiene la Z: causa u origen de algo","respuesta": "raíz"}
],
    "Segundo Rosco Programa 9-A (40)" : [
  {"letra": "A", "pista": "Con la A: nombre artístico de la cantante británica ganadora de un Oscar intérprete de canciones como skyfold Rolling in the deep", "respuesta": "Adele"},
  {"letra": "B", "pista": "Con la B: empresa dedicada a realizar operaciones financieras con el dinero procedente de sus accionistas y de los depósitos de sus clientes", "respuesta": "Banco"},
  {"letra": "C", "pista": "Con la C: competición de velocidad entre personas que van a pie conducen vehículos o montan animales", "respuesta": "Carrera"},
  {"letra": "D", "pista": "Con la D: sensación molesta y aflictiva de una parte del cuerpo por causa interior o exterior", "respuesta": "Dolor"},
  {"letra": "E", "pista": "Con la E: persona especializada en instalaciones de esta clase de energía", "respuesta": "Electricista"},
  {"letra": "F", "pista": "Con la F: quebradizo y que con facilidad se hace pedazos", "respuesta": "Frágil"},
  {"letra": "G", "pista": "Con la G: cueva o espesura donde se refugian los animales", "respuesta": "Guarida"},
  {"letra": "H", "pista": "Contiene la H: salto violento de una descarga de energía", "respuesta": "Chispazo"},
  {"letra": "I", "pista": "Con la I: burla fina y disimulada", "respuesta": "Ironía"},
  {"letra": "J", "pista": "Contiene la J: postre típico de Uruguay Argentina que consiste en un bizcochuelo recubierto con merengue relleno de crema duraznos y Dulce leche", "respuesta": "Chajá"},
  {"letra": "L", "pista": "Con la L: técnica de extracción localizada de la adiposidad subcutánea mediante una cánula conectada a un aparato aspirador Generalmente con fines estéticos", "respuesta": "Liposucción"},
  {"letra": "M", "pista": "Con la M: en la serie animada de Los Simpsons nombre de la esposa de Homero y madre de Bart", "respuesta": "Marge"},
  {"letra": "N", "pista": "Con la N: aparato para administrar medicamentos en forma de vapor", "respuesta": "Nebulizador"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: cuarto de un edificio con lavabo ducha tina inodoro y otros sanitarios", "respuesta": "Baño"},
  {"letra": "O", "pista": "Con la O: que pierde la memoria de las cosas con facilidad", "respuesta": "Olvidadizo"},
  {"letra": "P", "pista": "Con la P: en algunos juegos de pelota raqueta de madera", "respuesta": "Paleta"},
  {"letra": "Q", "pista": "Contiene la Q: inflamación agudo Crónica de la membrana mucosa de las vías respiratorias", "respuesta": "Bronquitis"},
  {"letra": "R", "pista": "Con la R: instrumento rígido de forma rectangular que sirve para trazar líneas sin desviación o para medir la distancia entre dos puntos", "respuesta": "Regla"},
  {"letra": "S", "pista": "Con la S: apellido la actriz argentina que encarnó el rol Dual de hermanas gemelas en la telecomedia educando a Nina", "respuesta": "Siciliani"},
  {"letra": "T", "pista": "Con la T: cuajada elaborada a partir de leche de soja", "respuesta": "Tofu"},
  {"letra": "U", "pista": "Con la U: lugar en que está situado algo", "respuesta": "Ubicación"},
  {"letra": "V", "pista": "Con la V: canción popular principalmente de asuntos religiosos que se canta Navidad", "respuesta": "Villancico"},
  {"letra": "X", "pista": "Contiene la X: que ocupa una serie lugar número 16", "respuesta": "Decimosexto"},
  {"letra": "Y", "pista": "Con la Y: plantación de Mate", "respuesta": "Yerbatal - Yerbal"},
  {"letra": "Z", "pista": "Contiene la Z: localidad donde se encuentra el Aeropuerto Internacional ministro", "respuesta": "Ezeiza"}
],
    "Segundo Rosco Programa 9-B (41)" : [
  {"letra": "A", "pista": "Con la A: tejido de lana u otras materias y de varios dibujos y colores con que se cubre el piso de las habitaciones escaleras para abrigo y adorno", "respuesta": "Alfombra"},
  {"letra": "B", "pista": "Con la B: lugar donde se tiene considerable el número de volúmenes ordenados para la lectura", "respuesta": "Biblioteca"},
  {"letra": "C", "pista": "Con la C: apellido el piloto de automovilismo argentino que representó a la escudería Williams en el campeonato de Fórmula 1 de 2024", "respuesta": "Colapinto"},
  {"letra": "D", "pista": "Con la D: falto de amabilidad y buenos modales", "respuesta": "Descortés"},
  {"letra": "E", "pista": "Con la E: que asiste a una función pública", "respuesta": "Espectador"},
  {"letra": "F", "pista": "Con la F: hambriento", "respuesta": "Famélico"},
  {"letra": "G", "pista": "Con la G: vehículo automóvil provisto de un sistema de elevación o arrastre destinado a transportar uno o más vehículos", "respuesta": "Grúa"},
  {"letra": "H", "pista": "Con la H: abundancia de gases de combustión", "respuesta": "Humareda"},
  {"letra": "I", "pista": "Con la I: nombre del país peninsular europeo ubicado en el mar Mediterráneo conocido coloquialmente como la bota", "respuesta": "Italia"},
  {"letra": "J", "pista": "Con la J: órgano colectivo que selecciona los más cualificados entre varios candidatos a un premio honor distinción o empleo", "respuesta": "Jurado"},
  {"letra": "L", "pista": "Con la L: nombre del disparatado cómico y músico Que formó parte de Los tres chiflados junto a y curly", "respuesta": "Larry"},
  {"letra": "M", "pista": "Con la M: parte alargada o estrecha con un extremo libre con el cual se puede agarrar un instrumento u utensilio", "respuesta": "Mango"},
  {"letra": "N", "pista": "Con la N: médico especialista en el sistema nervioso", "respuesta": "Neurólogo"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: tienda donde se venden artículos absorbentes y otros objetos relacionados con los cuidados de los bebés", "respuesta": "Pañalera"},
  {"letra": "O", "pista": "Con la O: natural del oeste o del hemisferio oeste", "respuesta": "Occidental"},
  {"letra": "P", "pista": "Con la P: apellido del actor argentino que protagonizó la serie los simuladores y actuó los films tiempo de valientes y el robo de siglo", "respuesta": "Peretti"},
  {"letra": "Q", "pista": "Con la Q: lío, barullo gresca desorden", "respuesta": "Quilombo"},
  {"letra": "R", "pista": "Con la R: nombre artístico de la cantante española de pop latino y flamenco intérprete de canciones como malamente y despechada", "respuesta": "Rosalía"},
  {"letra": "S", "pista": "Con la S: emparedado hecho con dos rebanadas de pan de molde entre las que se coloca jamón queso embutido vegetales u otros alimentos", "respuesta": "Sándwich"},
  {"letra": "T", "pista": "Con la T: plancha dibujada Y coloreada a propósito para jugar a la ajedrez y otros varios juegos", "respuesta": "Tablero"},
  {"letra": "U", "pista": "Con la U: que consta de un solo individuo", "respuesta": "Unipersonal"},
  {"letra": "V", "pista": "Con la V: acera de una calle o Plaza", "respuesta": "Vereda"},
  {"letra": "X", "pista": "Contiene la X: persona dedicada profesionalmente a la elaboración de diccionarios", "respuesta": "Lexicógrafo"},
  {"letra": "Y", "pista": "Contiene la Y: con cavidad u Hondura formada en la tierra", "respuesta": "Hoyo"},
  {"letra": "Z", "pista": "Contiene la Z: acaso O tal vez", "respuesta": "Quizá - Quizás"}
],
    "Primer Rosco Programa 10-A (42)" : [
  {"letra": "A", "pista": "Con la A: persona que recibe enseñanza respecto de un profesor de la escuela, colegio o Universidad donde estudia", "respuesta": "alumno"},
  {"letra": "B", "pista": "Con la B: pieza fina de cerámica mármol o piedra de forma cuadrado rectangular para cubrir suelos o paredes", "respuesta": "baldosa"},
  {"letra": "C", "pista": "Con la C: azúcar fundido y endurecido", "respuesta": "caramelo"},
  {"letra": "D", "pista": "Con la D: operación matemática de fraccionar", "respuesta": "división"},
  {"letra": "E", "pista": "Con la E: que tiene poca salud que padece afecciones con frecuencia", "respuesta": "enfermo"},
  {"letra": "F", "pista": "Con la F: nombre que adoptó el obispo católico Jorge Bergoglio al ser elegido sumo pontífice el año 2013", "respuesta": "Francisco"},
  {"letra": "G", "pista": "Con la G: lucha armada entre dos o más naciones o entre bandos de una misma nación", "respuesta": "guerra"},
  {"letra": "H", "pista": "Contiene la H: cotización de un artista del espectáculo de ciertos profesionales que actúan en público", "respuesta": "caché"},
  {"letra": "I", "pista": "Con la I: país asiático ubicado entre los montes himalayas y océano Índico su capital es la ciudad de Nueva Delhi", "respuesta": "India"},
  {"letra": "J", "pista": "Con la J: superior o cabeza de una corporación partido u oficina", "respuesta": "jefe"},
  {"letra": "L", "pista": "Con la L: permiso para hacer algo", "respuesta": "libertad"},
  {"letra": "M", "pista": "Con la M: especie de bolso cartera que se lleva a la espalda", "respuesta": "mochila"},
  {"letra": "N", "pista": "Con la N: tristeza melancólica originada por el recuerdo de una dicha perdida", "respuesta": "nostalgia"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: lazo de cintas", "respuesta": "moño"},
  {"letra": "O", "pista": "Con la O: apellido del político estadounidense que fue el primer presidente afroamericano del país entre 2009 y 2017", "respuesta": "Obama"},
  {"letra": "P", "pista": "Con la P: insignia distintivo que lleva los agentes de policía para acreditar que lo son", "respuesta": "placa"},
  {"letra": "Q", "pista": "Contiene la Q: peluca pequeña o que solo cubre parte de la cabeza", "respuesta": "peluquín"},
  {"letra": "R", "pista": "Con la R: en un automóvil marcha atrás", "respuesta": "reversa - retroceso"},
  {"letra": "S", "pista": "Con la S: que es bueno para el bienestar del organismo", "respuesta": "sano - saludable"},
  {"letra": "T", "pista": "Con la T: nombre transatlántico insignia británico que colisionó el 15 abril 1912", "respuesta": "Titanic"},
  {"letra": "U", "pista": "Contiene la U: tiempo que vendrá", "respuesta": "futuro"},
  {"letra": "V", "pista": "Con la V: espacio exterior de las tiendas cerrado con cristales donde se exponen las mercancías", "respuesta": "vidriera"},
  {"letra": "X", "pista": "Contiene la X: acostumbrado a hablar y a obrar con meditación y prudencia", "respuesta": "reflexivo"},
  {"letra": "Y", "pista": "Contiene la Y: nombre de pila de la cantante de pop estadounidense intérprete de éxitos como Baby One More Time oops I did it Again y toxic", "respuesta": "Britney"},
  {"letra": "Z", "pista": "Contiene la Z: velo máscara o cosa semejante con que se cubre la cara especialmente la parte que rodea los ojos", "respuesta": "antifaz"}
],
    "Primer Rosco Programa 10-B (43)" : [
  {"letra": "A", "pista": "Con la A: padre o madre de uno de los padres de una persona", "respuesta": "abuelo"},
  {"letra": "B", "pista": "Con la B: tambor muy grande que se toca en una masa y se emplean las orquestas y las bandas militares", "respuesta": "bombo"},
  {"letra": "C", "pista": "Con la C: rollo pequeño de picadura envuelta en papel de fumar", "respuesta": "cigarrillo"},
  {"letra": "D", "pista": "Con la D: dicho de una persona de una parte del cuerpo que no está cubierta por ropa", "respuesta": "desnudo"},
  {"letra": "E", "pista": "Con la E: país ubicado en el noreste de África famoso por sus pirámides y cuya capital y ciudad más poblada es el Cairo", "respuesta": "Egipto"},
  {"letra": "F", "pista": "Con la F: en el juego del póker reunión de trío y pareja", "respuesta": "full"},
  {"letra": "G", "pista": "Con la G: salsa espesa que se prepara con aguacate molido picado al que se agrega cebolla tomate y chile verde", "respuesta": "guacamole"},
  {"letra": "H", "pista": "Contiene la H: perrito caliente", "respuesta": "pancho"},
  {"letra": "I", "pista": "Con la I: que no se puede quebrar o fragmentar", "respuesta": "irrompible"},
  {"letra": "J", "pista": "Contiene la J: mango puño o manubrio de ciertos utensilios y herramientas", "respuesta": "manija"},
  {"letra": "L", "pista": "Con la L: ropa interior femenina", "respuesta": "lencería"},
  {"letra": "M", "pista": "Con la M: apellido del abogado y político rioplatense que ofició de secretario de la primera junta de gobierno 1810 y fue el fundador del periódico La gaceta", "respuesta": "Moreno"},
  {"letra": "N", "pista": "Con la N: dicho de un lugar destinado para practicar deportes acuáticos y zambullirse", "respuesta": "natatorio"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: gran elevación natural del terreno", "respuesta": "montaña"},
  {"letra": "O", "pista": "Con la O: antipatía y aversión hacia algo hacia alguien cuyo mal se desea", "respuesta": "odio"},
  {"letra": "P", "pista": "Con la P: nombre artístico del cantante y músico estadounidense ganador de un Oscar intérprete de temas como Purple Rain cream y Kiss", "respuesta": "Prince"},
  {"letra": "Q", "pista": "Contiene la Q: bebida mexicana semejante a la ginebra que se destila de una especie de maguey", "respuesta": "tequila"},
  {"letra": "R", "pista": "Con la R: apellido de la actriz estadounidense y ganadora de un Oscar por su papel protagónico en el fin del año 2000 Erin Brockovich", "respuesta": "Roberts"},
  {"letra": "S", "pista": "Con la S: que no está envasado o empaquetado", "respuesta": "suelto"},
  {"letra": "T", "pista": "Con la T: en un medio de transporte de pasajeros especialmente en un avión dicho de una clase más económica", "respuesta": "turista"},
  {"letra": "U", "pista": "Contiene la U: dormitorio", "respuesta": "cuarto"},
  {"letra": "V", "pista": "Con la V: raíl de ferrocarril", "respuesta": "vía"},
  {"letra": "X", "pista": "Contiene la X: excesivo que incluye en sí desmesura o desproporción", "respuesta": "exagerado"},
  {"letra": "Y", "pista": "Contiene la Y: en Toy Story nombre del Cowboy de juguete preferido de Andy hasta la aparición del astronauta de quien se hace amigo inseparable", "respuesta": "Woody"},
  {"letra": "Z", "pista": "Contiene la Z: tercer mes del año que tiene 31 días", "respuesta": "marzo"}
],
    "Segundo Rosco Programa 10-A (44)": [
  {"letra": "A", "pista": "Con la A: persona que tripula una nave espacial o que está entrenada para este trabajo", "respuesta": "Astronauta"},
  {"letra": "B", "pista": "Con la B: nombre del pequeño ciervo amigo del conejo Tambor que da nombre a la película animada de 1942", "respuesta": "Bambi"},
  {"letra": "C", "pista": "Con la C: demostración de afecto que consiste en rozar solamente con la mano el cuerpo de una persona, un animal, etcétera", "respuesta": "Caricia"},
  {"letra": "D", "pista": "Con la D: dicho de una persona que sufre alucinaciones o desvaría", "respuesta": "Delirante"},
  {"letra": "E", "pista": "Con la E: en un teatro, el lugar donde se representa la obra o el espectáculo", "respuesta": "Escenario"},
  {"letra": "F", "pista": "Con la F: apodo de Ángel Di María, delantero de la selección argentina de fútbol, autor del segundo gol a Francia en la final del mundial de Qatar 2022", "respuesta": "Fideo"},
  {"letra": "G", "pista": "Con la G: lugar de venta o reparación de neumáticos", "respuesta": "Gomería"},
  {"letra": "H", "pista": "Contiene la H: intelectualmente pobre o corto de miras", "respuesta": "Chato"},
  {"letra": "I", "pista": "Con la I: natural del país europeo cuya capital es Reikiavik", "respuesta": "Islandés"},
  {"letra": "J", "pista": "Con la J: país insular de Asia ubicado en el océano Pacífico cuya capital es Tokio", "respuesta": "Japón"},
  {"letra": "L", "pista": "Con la L: cochinillo que todavía mama", "respuesta": "Lechón"},
  {"letra": "M", "pista": "Con la M: herramienta de percusión compuesta de una cabeza, por lo común de hierro, y un mango, generalmente de madera", "respuesta": "Martillo"},
  {"letra": "N", "pista": "Con la N: nombre del tiránico y despiadado emperador romano del siglo primero después de Cristo, acusado de haber provocado el mayor incendio de la ciudad de Roma", "respuesta": "Nerón"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: periodo de la vida humana que se extiende desde el nacimiento a la pubertad", "respuesta": "Niñez"},
  {"letra": "O", "pista": "Con la O: escondido, ignorado, que no se da a conocer ni se deja ver ni sentir", "respuesta": "Oculto"},
  {"letra": "P", "pista": "Con la P: casa destinada para residencia de los reyes", "respuesta": "Palacio"},
  {"letra": "Q", "pista": "Contiene la Q: gobernante o jefe de una comunidad o pueblo de indios", "respuesta": "Cacique"},
  {"letra": "R", "pista": "Con la R: juego de azar que consiste en frotar la parte de un cartón donde puede aparecer algún premio", "respuesta": "Raspadita"},
  {"letra": "S", "pista": "Con la S: prenda para cubrir la cabeza que consta de copa y ala", "respuesta": "Sombrero"},
  {"letra": "T", "pista": "Con la T: recipiente con cierre hermético que se usa para guardar o llevar alimentos", "respuesta": "Taper - Túper"},
  {"letra": "U", "pista": "Contiene la U: maletero del automóvil", "respuesta": "Baúl"},
  {"letra": "V", "pista": "Con la V: ambulante o que va de un lugar a otro sin asentarse en ninguno", "respuesta": "Vagabundo"},
  {"letra": "X", "pista": "Contiene la X: presión que se ejerce sobre alguien mediante amenazas para obligarlo a actuar de determinada manera y obtener así dinero", "respuesta": "Extorsión"},
  {"letra": "Y", "pista": "Con la Y: producto lácteo obtenido mediante reducción por evaporación y fermentación bacteriana de la leche", "respuesta": "Yogur"},
  {"letra": "Z", "pista": "Contiene la Z: apodo artístico de Gonzalo Conde, DJ y productor musical argentino famoso por sus sesiones musicales con Shakira, Residente y Nicki Nicole", "respuesta": "Bizarrap"}
],
    "Segundo Rosco Programa 10-B (45)": [
  {"letra": "A", "pista": "Con la A: barra pequeña y puntiaguda de metal, hueso o madera, con un ojo por donde se pasa el hilo, cuerda, correa o bejuco", "respuesta": "Aguja"},
  {"letra": "B", "pista": "Con la B: cartera pequeña de bolsillo para llevar dinero, tarjetas, etcétera", "respuesta": "Billetera"},
  {"letra": "C", "pista": "Con la C: parte posterior y prominente de la articulación del brazo con el antebrazo", "respuesta": "Codo"},
  {"letra": "D", "pista": "Con la D: sin ocupación", "respuesta": "Desempleado - Desocupado"},
  {"letra": "E", "pista": "Con la E: que se prolonga muchísimo o excesivamente", "respuesta": "Eterno"},
  {"letra": "F", "pista": "Con la F: fachada o parte primera que se ofrece a la vista en un edificio u otra cosa", "respuesta": "Frente"},
  {"letra": "G", "pista": "Con la G: apellido del actor estadounidense protagonista de filmes como Reto al destino, Chicago y Mujer bonita", "respuesta": "Gere"},
  {"letra": "H", "pista": "Contiene la H: vino espumoso, blanco o rosado, originario de Francia", "respuesta": "Champán - Champaña"},
  {"letra": "I", "pista": "Con la I: falta de castidad o inocencia", "respuesta": "Impureza"},
  {"letra": "J", "pista": "Con la J: terreno donde se cultivan plantas con fines ornamentales", "respuesta": "Jardín"},
  {"letra": "L", "pista": "Con la L: que ha perdido la razón", "respuesta": "Loco"},
  {"letra": "M", "pista": "Con la M: ciudad del norte de Italia ubicada en la región de la Lombardía, reconocida en el mundo por ser la capital de la moda", "respuesta": "Milán"},
  {"letra": "N", "pista": "Con la N: recién hecho o fabricado", "respuesta": "Nuevo"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: natural de la región de las Antillas o de los territorios que bañan el mar homónimo", "respuesta": "Caribeño"},
  {"letra": "O", "pista": "Con la O: límite de la tierra que la separa del mar, de un lago, de un río, etcétera", "respuesta": "Orilla"},
  {"letra": "P", "pista": "Con la P: nombre del simpático cerdito de caricaturas que cerraba cada episodio balbuceando 'Eso es todo, amigos'", "respuesta": "Porky"},
  {"letra": "Q", "pista": "Contiene la Q: tortita que se hace con masa de harina, yemas de huevo batidas y un poco de leche", "respuesta": "Panqueque"},
  {"letra": "R", "pista": "Con la R: nombre artístico del cantante argentino de cuarteto fallecido en 2000, intérprete del tema 'Soy cordobés' y 'Lo mejor del amor'", "respuesta": "Rodrigo"},
  {"letra": "S", "pista": "Con la S: dicho de un día, de una tarde, etcétera, en que brilla el astro rey", "respuesta": "Soleado"},
  {"letra": "T", "pista": "Con la T: acumulación de cerumen en el oído que puede dificultar la audición y producir otros trastornos", "respuesta": "Tapón"},
  {"letra": "U", "pista": "Contiene la U: nombre de la protagonista de la tragedia escrita por William Shakespeare, enamorada de Romeo, por quien muere clavándose una daga", "respuesta": "Julieta"},
  {"letra": "V", "pista": "Con la V: cortometraje en que se registra, generalmente con fines promocionales, una única canción o pieza musical", "respuesta": "Videoclip"},
  {"letra": "X", "pista": "Contiene la X: motivo o pretexto que se invoca para eludir una obligación", "respuesta": "Excusa"},
  {"letra": "Y", "pista": "Contiene la Y: designio o pensamiento de ejecutar algo", "respuesta": "Proyecto"},
  {"letra": "Z", "pista": "Contiene la Z: Ruido fuerte producido con una bocina.", "respuesta": "BOCINAZO"}
],
    "Rosco Programa 11-A (46)" : [
  {"letra": "A", "pista": "Con la A: persona que tripula una nave espacial o que está entrenada para este trabajo", "respuesta": "astronauta"},
  {"letra": "B", "pista": "Con la B: película estadounidense de 2023 protagonizada por Margot Robbie y Ryan Gosling basada en una línea de muñecas de juguete", "respuesta": "Barbie"},
  {"letra": "C", "pista": "Con la C: dicho de una persona que ha contraído nupcias", "respuesta": "casado"},
  {"letra": "D", "pista": "Con la D: nombre artístico de Dylan León Masa, rapero argentino intérprete de temas como 220 y Cirugía", "respuesta": "Dillom"},
  {"letra": "E", "pista": "Con la E: que padece de celos o resentimiento ante el éxito o el bien ajeno", "respuesta": "envidioso"},
  {"letra": "F", "pista": "Con la F: parte inferior de una cosa hueca", "respuesta": "fondo"},
  {"letra": "G", "pista": "Con la G: personaje de historietas cuyo nombre real es Selina Kyle, una ladrona de Ciudad Gótica que viste un traje felino ajustado", "respuesta": "Gatúbela"},
  {"letra": "H", "pista": "Con la H: pasta de garbanzos típica de la cocina árabe aderezada generalmente con aceite de oliva, zumo de limón, crema de sésamo y ajo", "respuesta": "humus"},
  {"letra": "I", "pista": "Con la I: que no puede ser vencido o doblegado", "respuesta": "imbatible"},
  {"letra": "J", "pista": "Contiene la J: pequeña imagen o ícono digital que se usa en las comunicaciones electrónicas para representar una emoción, un objeto, una idea, etcétera", "respuesta": "emoji"},
  {"letra": "L", "pista": "Con la L: utensilio, generalmente una anilla metálica, en el que se agrupan los instrumentos para abrir cerraduras", "respuesta": "llavero"},
  {"letra": "M", "pista": "Con la M: ciudad estadounidense al sur del estado de la Florida famosa en el mundo por sus playas tropicales y su industria del entretenimiento", "respuesta": "Miami"},
  {"letra": "N", "pista": "Con la N: persona diestra en este deporte acuático que avanza en el agua usando brazos y piernas", "respuesta": "nadador"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: natural de la provincia del noroeste de Argentina conocida históricamente como la Madre de Ciudades", "respuesta": "santiagueño"},
  {"letra": "O", "pista": "Con la O: tiene habitualmente marcas oscuras bajo los párpados inferiores", "respuesta": "ojeroso"},
  {"letra": "P", "pista": "Con la P: persona que ejerce o enseña una ciencia o arte", "respuesta": "profesor"},
  {"letra": "Q", "pista": "Contiene la Q: precio que se paga por el arrendamiento de algo", "respuesta": "alquiler"},
  {"letra": "R", "pista": "Con la R: corte de cabello al ras del cuero cabelludo", "respuesta": "rapado"},
  {"letra": "S", "pista": "Con la S: que presume de erudito y entendido sin serlo", "respuesta": "sabiondo"},
  {"letra": "T", "pista": "Con la T: apellido del exparticipante del famoso reality show de encierro que finalizó tercero en su primera edición de 2001 en Argentina", "respuesta": "Trezeguet"},
  {"letra": "U", "pista": "Contiene la U: caja ordinariamente de madera donde se pone un cadáver para sepultarlo o incinerarlo", "respuesta": "ataúd"},
  {"letra": "V", "pista": "Con la V: prenda de una sola pieza usada por la mujer", "respuesta": "vestido"},
  {"letra": "X", "pista": "Contiene la X: prenda interior masculina parecida a un pantalón corto", "respuesta": "bóxer"},
  {"letra": "Y", "pista": "Contiene la Y: que goza de mucho poder o prestigio sobre los demás", "respuesta": "influyente - rey"},
  {"letra": "Z", "pista": "Contiene la Z: persona osada y atrevida", "respuesta": "audaz"}
],
    "Rosco Programa 11-B (47)" : [
  {"letra": "A", "pista": "Con la A: funda rellena de un material blando que sirve para reclinar la cabeza", "respuesta": "almohada"},
  {"letra": "B", "pista": "Con la B: persona en estado de embriaguez", "respuesta": "borracho"},
  {"letra": "C", "pista": "Con la C: infusión oscura que se sirve con una cantidad mínima de lácteo", "respuesta": "cortado"},
  {"letra": "D", "pista": "Con la D: empresa comercial dedicada al reparto y entrega de productos", "respuesta": "distribuidora"},
  {"letra": "E", "pista": "Con la E: fuga de un gas o de un líquido", "respuesta": "escape"},
  {"letra": "F", "pista": "Con la F: instrumento musical de viento de madera u otro material en forma de tubo con varios agujeros circulares que se tapan con los dedos o con piezas metálicas", "respuesta": "flauta"},
  {"letra": "G", "pista": "Con la G: acción falta de educación, torpe o chabacana", "respuesta": "grosería"},
  {"letra": "H", "pista": "Contiene la H: apodo artístico del actor e influencer argentino que fue conductor de un programa de juegos con formas que avanzan hacia una pileta", "respuesta": "Kevsho"},
  {"letra": "I", "pista": "Con la I: que carece de exactitud o validez", "respuesta": "incorrecto"},
  {"letra": "J", "pista": "Con la J: persona que practica una disciplina como el tenis o el fútbol", "respuesta": "jugador"},
  {"letra": "L", "pista": "Con la L: apellido del cantante argentino de trap y pop latino entre cuyas canciones se destacan Adán y Eva, y Nena Maldición", "respuesta": "Londra"},
  {"letra": "M", "pista": "Con la M: película de 2014 protagonizada por Angelina Jolie en el papel de la malvada bruja de un cuento infantil", "respuesta": "Maléfica"},
  {"letra": "N", "pista": "Con la N: situación en la que dos personas mantienen una relación amorosa formal previa al matrimonio", "respuesta": "noviazgo"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: persona que imagina fantasías o anhela cosas improbables", "respuesta": "soñador"},
  {"letra": "O", "pista": "Con la O: dicho de un animal que se alimenta de toda clase de sustancias orgánicas", "respuesta": "omnívoro"},
  {"letra": "P", "pista": "Con la P: lugar de reclusión o sitio donde se encierra y asegura a los condenados", "respuesta": "prisión - penal - penitenciaría - presidio"},
  {"letra": "Q", "pista": "Contiene la Q: deporte de equipo en el que se intenta anotar puntos introduciendo un balón en un aro elevado", "respuesta": "básquet"},
  {"letra": "R", "pista": "Con la R: barrio residencial porteño apodado la París Argentina, donde se ubica la Plaza Francia", "respuesta": "Recoleta"},
  {"letra": "S", "pista": "Con la S: obra radiofónica o televisiva que se difunde en emisiones sucesivas", "respuesta": "serie"},
  {"letra": "T", "pista": "Con la T: parte posterior del pie humano", "respuesta": "talón"},
  {"letra": "U", "pista": "Contiene la U: número que se lee igual de izquierda a derecha que de derecha a izquierda, por ejemplo el 131", "respuesta": "capicúa"},
  {"letra": "V", "pista": "Con la V: disciplina que se ocupa principalmente de prevenir y curar afecciones médicas de los animales", "respuesta": "veterinaria"},
  {"letra": "X", "pista": "Contiene la X: persona que realiza paseos o viajes cortos por afición", "respuesta": "excursionista"},
  {"letra": "Y", "pista": "Contiene la Y: nombre del pequeño canario de animación que siempre exclama que le parece haber visto a un lindo gatito", "respuesta": "Tweety"},
  {"letra": "Z", "pista": "Con la Z: mamífero carnívoro americano conocido por el fétido olor de sus glándulas anales", "respuesta": "zorrino - zorrillo"}
],
    "Rosco Programa 112-A (504)" : [
  {"letra": "A", "pista": "Con la A: Médico especialista encargado de insensibilizar al paciente durante una intervención quirúrgica.", "respuesta": "ANESTESISTA"},
  {"letra": "B", "pista": "Con la B: Estilo de botas de caña alta que cubre la parte superior de la pierna, generalmente por encima de las rodillas.", "respuesta": "BUCANERA"},
  {"letra": "C", "pista": "Con la C: Película de Disney Pixar del año 2017, protagonizada por Miguel, un niño que sueña con ser músico y viaja accidentalmente al mundo de los muertos en México.", "respuesta": "COCO"},
  {"letra": "D", "pista": "Con la D: Género musical bailable que surge en la década de 1970 a partir del soul y otros ritmos.", "respuesta": "DISCO"},
  {"letra": "E", "pista": "Con la E: Mueble compuesto de baldas o anaqueles.", "respuesta": "ESTANTERÍA"},
  {"letra": "F", "pista": "Con la F: Antónimo de verdadero.", "respuesta": "FALSO"},
  {"letra": "G", "pista": "Con la G: Ir delante mostrando el camino.", "respuesta": "GUIAR"},
  {"letra": "H", "pista": "Contiene la H: Prenda de vestir que suele revolear la cantante Soledad Pastorutti cuando se presenta en vivo.", "respuesta": "PONCHO"},
  {"letra": "I", "pista": "Con la I: Que comprende, abarca o tiene virtud y capacidad para integrar a todos.", "respuesta": "INCLUSIVO"},
  {"letra": "J", "pista": "Contiene la J: Entramado de metal, madera u otro material que, generalmente enmarcado en un hueco, permite el paso del aire, la luz o la voz.", "respuesta": "REJILLA"},
  {"letra": "L", "pista": "Con la L: Dicho del pelo, que no tiene rizos.", "respuesta": "LACIO"},
  {"letra": "M", "pista": "Con la M: Nombre de pila de la cantante de apellido Becerra, conocida como La Nena de Argentina, intérprete de temas como Automático.", "respuesta": "MARÍA"},
  {"letra": "N", "pista": "Con la N: Elegir o señalar a alguien para un cargo, un empleo u otra cosa.", "respuesta": "NOMBRAR"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Natural del país centroamericano cuya capital es Tegucigalpa.", "respuesta": "HONDUREÑO"},
  {"letra": "O", "pista": "Con la O: Humillar o herir el amor propio o la dignidad de alguien, o ponerlo en evidencia con palabras o con hechos.", "respuesta": "OFENDER"},
  {"letra": "P", "pista": "Con la P: Noticia o hecho que se da a conocer por primera vez.", "respuesta": "PRIMICIA"},
  {"letra": "Q", "pista": "Contiene la Q: Persona que tiene por oficio aplicar cosméticos y embellecer el rostro de alguien.", "respuesta": "MAQUILLADOR"},
  {"letra": "R", "pista": "Con la R: Apellido de la actriz australiana Margot, famosa por interpretar a Barbie.", "respuesta": "ROBBIE"},
  {"letra": "S", "pista": "Con la S: Calzoncillo ajustado que cubre el cuerpo desde debajo de la cintura hasta las ingles.", "respuesta": "SUSPENSOR - SLIP"},
  {"letra": "T", "pista": "Con la T: Arrojar, lanzar en dirección determinada.", "respuesta": "TIRAR"},
  {"letra": "U", "pista": "Contiene la U: Avenida de los barrios porteños de Belgrano y Villa Urquiza en la que encontramos un importante centro comercial en su cruce con la avenida Cabildo.", "respuesta": "JURAMENTO"},
  {"letra": "V", "pista": "Con la V: Telenovela infanto-juvenil argentina protagonizada por Tini Stoessel, quien representó a una chica con un gran talento musical.", "respuesta": "VIOLETTA"},
  {"letra": "X", "pista": "Contiene la X: Que no forma parte del sueldo o remuneración básica de un trabajador.", "respuesta": "EXTRASALARIAL"},
  {"letra": "Y", "pista": "Contiene la Y: Prestar cooperación o auxilio.", "respuesta": "AYUDAR"},
  {"letra": "Z", "pista": "Contiene la Z: Estrechar a alguien con las extremidades superiores en señal de cariño.", "respuesta": "ABRAZAR"}
],
    "Rosco Programa 111-b (505)" : [
  {"letra": "A", "pista": "Con la A: Palmotear en señal de aprobación o entusiasmo.", "respuesta": "APLAUDIR"},
  {"letra": "B", "pista": "Con la B: Papeleta para votar en unas elecciones.", "respuesta": "BOLETA"},
  {"letra": "C", "pista": "Con la C: Persona que obtiene la primacía en un torneo deportivo.", "respuesta": "CAMPEÓN"},
  {"letra": "D", "pista": "Con la D: Apellido del actor estadounidense Leonardo, protagonista de películas como Titanic y El Lobo de Wall Street.", "respuesta": "DICAPRIO"},
  {"letra": "E", "pista": "Con la E: Que tiene o genera muchas burbujas, aplicado a ciertos vinos.", "respuesta": "ESPUMANTE"},
  {"letra": "F", "pista": "Con la F: Interjección usada para pedir auxilio en un incendio.", "respuesta": "FUEGO"},
  {"letra": "G", "pista": "Con la G: Apasionado de los títulos virtuales y consolas, con profundo conocimiento sobre ese mundo.", "respuesta": "GAMER"},
  {"letra": "H", "pista": "Contiene la H: Localidad de la costa atlántica argentina cercana a Mar del Plata, en la que se encontraban los hoteles de turismo social y es elegida por los jóvenes para vacacionar.", "respuesta": "NECOCHEA"},
  {"letra": "I", "pista": "Con la I: Llave de cabeza regulable usada para apretar o aflojar tuercas y tornillos.", "respuesta": "INGLESA"},
  {"letra": "J", "pista": "Contiene la J: Dicho de un color que tiene tonalidades similares al carmesí o escarlata.", "respuesta": "ROJIZO"},
  {"letra": "L", "pista": "Con la L: Que tiene una dimensión considerable o superior a la habitual en el espacio o en el tiempo.", "respuesta": "LARGO"},
  {"letra": "M", "pista": "Con la M: Mujer en relación con sus hijos.", "respuesta": "MADRE"},
  {"letra": "N", "pista": "Con la N: Persona que mantiene una relación amorosa con otra.", "respuesta": "NOVIO"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Diminutivo para referirse a alguien natural del sur.", "respuesta": "SUREÑITO"},
  {"letra": "O", "pista": "Con la O: Conjunto de ocho personas, animales o cosas de características semejantes o con una función común.", "respuesta": "OCTETO"},
  {"letra": "P", "pista": "Con la P: Recipiente cilíndrico de material flexible en que se expenden cosméticos, fármacos o pinturas de consistencia líquida o cremosa.", "respuesta": "POMO"},
  {"letra": "Q", "pista": "Contiene la Q: Serie infantil de televisión emitida entre 1995 y 2001 que narra la historia de un grupo de huérfanas en el hogar Rincón de Luz.", "respuesta": "CHIQUITITAS"},
  {"letra": "R", "pista": "Con la R: Médico especialista en el uso de imágenes médicas como los rayos X para diagnosticar enfermedades.", "respuesta": "RADIÓLOGO"},
  {"letra": "S", "pista": "Con la S: Bebida de agua gaseosa que contiene ácido carbónico.", "respuesta": "SODA"},
  {"letra": "T", "pista": "Con la T: Palabra o frase con que se da a conocer el nombre o asunto de una obra o de cada una de las partes de un escrito.", "respuesta": "TÍTULO - TEMA"},
  {"letra": "U", "pista": "Contiene la U: Nombre por el que es conocido el músico y compositor estadounidense intérprete de temas como Just the Way You Are y Uptown Funk, de apellido artístico Mars.", "respuesta": "BRUNO"},
  {"letra": "V", "pista": "Con la V: Trayecto que recorre un avión haciendo o no escalas entre el punto de origen y el de destino.", "respuesta": "VUELO"},
  {"letra": "X", "pista": "Contiene la X: Estilo de pantalón cuyas piernas más anchas por la parte de abajo cubren todo el pie.", "respuesta": "OXFORD"},
  {"letra": "Y", "pista": "Contiene la Y: Fruto tropical comestible de forma ovalada, proveniente de un árbol de la familia de las mirtáceas.", "respuesta": "GUAYABA"},
  {"letra": "Z", "pista": "Contiene la Z: Personaje animado de la película de Disney Intensamente quien ve siempre la desventaja de las cosas, es de color azul y lleva grandes gafas redondas.", "respuesta": "TRISTEZA"}
],
    "Rosco Programa 113-A (506)" : [
  {"letra": "A", "pista": "Con la A: Nombre de pila del humorista rosarino apodado el Negro, creador de personajes inolvidables como el Capitán Piluso y Rukuku.", "respuesta": "Alberto"},
  {"letra": "B", "pista": "Con la B: En los cuentos infantiles o relatos folclóricos, mujer fea y malvada, que tiene poderes mágicos y que generalmente puede volar montada en una escoba.", "respuesta": "Bruja"},
  {"letra": "C", "pista": "Con la C: Sustancia que añadida a ciertos alimentos, sirve para darles tonalidad o teñirlos.", "respuesta": "Colorante"},
  {"letra": "D", "pista": "Con la D: Sexta hora después de las 12 del mediodía.", "respuesta": "Dieciocho"},
  {"letra": "E", "pista": "Con la E: Natural del Ecuador, país de América.", "respuesta": "Ecuatoriano"},
  {"letra": "F", "pista": "Con la F: Celebración o reunión de gran magnitud y muy animada.", "respuesta": "Fiestón"},
  {"letra": "G", "pista": "Con la G: Actividad destinada a desarrollar, fortalecer y mantener en buen estado físico el cuerpo por medio de una serie de ejercicios y movimientos reglados.", "respuesta": "Gimnasia"},
  {"letra": "H", "pista": "Contiene la H: Apellido de la escritora y cantautora argentina conocida por sus libros y canciones para niños como Manuelita la Tortuga y El Reino del Revés.", "respuesta": "Walsh"},
  {"letra": "I", "pista": "Con la I: Deseo o motivo afectivo que induce a hacer algo de manera súbita sin reflexionar.", "respuesta": "Impulso"},
  {"letra": "J", "pista": "Contiene la J: Tabla de cristal azogado por la parte posterior y también de acero u otro material bruñido para que se reflejen en él los objetos que estén adelante.", "respuesta": "Espejo"},
  {"letra": "L", "pista": "Con la L: Huevo de piojo que suele estar adherido a los pelos de los animales huéspedes de este parásito.", "respuesta": "Liendre"},
  {"letra": "M", "pista": "Con la M: Ventanillo de la puerta exterior de las casas.", "respuesta": "Mirilla"},
  {"letra": "N", "pista": "Con la N: Especialista en la alimentación y dietética del ser humano.", "respuesta": "Nutricionista"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Cerrar un ojo momentáneamente quedando el otro abierto a veces con disimulo por vía de señal o advertencia.", "respuesta": "Guiño"},
  {"letra": "O", "pista": "Con la O: Aquello que alguien está precisado o forzado a hacer.", "respuesta": "Obligación"},
  {"letra": "P", "pista": "Con la P: Quitar algo, la piel, la cáscara o la corteza.", "respuesta": "Pelar"},
  {"letra": "Q", "pista": "Contiene la Q: Entarimado hecho con maderas finas de varios tonos que convenientemente ensambladas forman dibujos geométricos.", "respuesta": "Parquet"},
  {"letra": "R", "pista": "Con la R: Que profesa un culto o dogma y practica sus normas y preceptos.", "respuesta": "Religioso"},
  {"letra": "S", "pista": "Con la S: Plató cinematográfico o televisivo.", "respuesta": "Set"},
  {"letra": "T", "pista": "Con la T: En un medio de transporte de pasajeros, especialmente en un avión, dicho de una clase más económica.", "respuesta": "Turista"},
  {"letra": "U", "pista": "Contiene la U: Mordedura o punzada de un ave, de un insecto o de ciertos reptiles.", "respuesta": "Picadura"},
  {"letra": "V", "pista": "Con la V: Postre argentino que combina una porción de queso con otra de dulce de membrillo o batata.", "respuesta": "Vigilante"},
  {"letra": "X", "pista": "Contiene la X: Que contiene veneno o produce envenenamiento.", "respuesta": "Tóxico"},
  {"letra": "Y", "pista": "Contiene la Y: Apellido de Horacio, artista argentino de folclore, conocido como el cantor del pueblo, cuya obra retrata la vida gaucha, la naturaleza y la justicia.", "respuesta": "Guarany"},
  {"letra": "Z", "pista": "Contiene la Z: Persona que hace inmersiones bajo el agua con un equipo adecuado para respirar.", "respuesta": "Buzo"}
],
    "Rosco Programa 113-B (57)" : [
  {"letra": "A", "pista": "Con la A: Arma para disparar flechas compuesta por una barra de acero, madera u otro material elástico sujeta por los extremos con una cuerda que la curva al tensarse.", "respuesta": "Arco"},
  {"letra": "B", "pista": "Con la B: Ceremonia mediante la cual se unen en matrimonio dos personas y fiesta con que se celebra.", "respuesta": "Boda"},
  {"letra": "C", "pista": "Con la C: Producto que se usa para abrillantar muebles y suelos.", "respuesta": "Cera"},
  {"letra": "D", "pista": "Con la D: Dicho de una persona en quien se transfiere una facultad o jurisdicción.", "respuesta": "Delegado"},
  {"letra": "E", "pista": "Con la E: Masa comúnmente hecha con harina o almidón que se cuece en agua y sirve para pegar papeles y otras cosas ligeras.", "respuesta": "Engrudo"},
  {"letra": "F", "pista": "Con la F: Aspirar y despedir el humo del tabaco.", "respuesta": "Fumar"},
  {"letra": "G", "pista": "Con la G: Fuerza que sobre todos los cuerpos ejerce la Tierra u otro planeta hacia su centro.", "respuesta": "Gravedad"},
  {"letra": "H", "pista": "Con la H: Especialista en el sistema curativo que aplica a las enfermedades dosis mínimas de sustancias que producirían síntomas iguales a los que se trata de combatir.", "respuesta": "Homeópata"},
  {"letra": "I", "pista": "Con la I: Nombre de pila del personaje de historietas argentino creado por Dante Quinterno que vive de estafas engañando a su tío el coronel Cañones.", "respuesta": "Isidoro"},
  {"letra": "J", "pista": "Contiene la J: Finca dedicada a la cría de animales.", "respuesta": "Granja"},
  {"letra": "L", "pista": "Con la L: Dicho de un producto alimenticio derivado de la leche.", "respuesta": "Lácteo"},
  {"letra": "M", "pista": "Con la M: Variedad de vino dulce que según la tradición popular argentina es el acompañante inseparable de la pizza y la fainá.", "respuesta": "Moscato"},
  {"letra": "N", "pista": "Con la N: Calificación escolar o evaluación.", "respuesta": "Nota"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Diminutivo de algo de corto tamaño o baja estatura.", "respuesta": "Pequeñito"},
  {"letra": "O", "pista": "Con la O: Estación de subte de la línea D que se encuentra entre José Hernández y Ministro Carranza.", "respuesta": "Olleros"},
  {"letra": "P", "pista": "Con la P: Agasajo que sobre el precio convenido y como muestra de satisfacción se da por algún servicio.", "respuesta": "Propina"},
  {"letra": "Q", "pista": "Contiene la Q: Pieza de papel, cartón u otro material semejante, generalmente rectangular, que se coloca en un objeto o una mercancía para identificación, valoración o clasificación.", "respuesta": "Etiqueta"},
  {"letra": "R", "pista": "Con la R: Que canta o baila el género musical urbano caracterizado por rimas habladas.", "respuesta": "Rapero"},
  {"letra": "S", "pista": "Con la S: Panecillo redondo de origen británico preparado con harina, azúcar, manteca, leche y huevos que suele tomarse en el desayuno y la merienda.", "respuesta": "Scone"},
  {"letra": "T", "pista": "Con la T: Ola gigantesca producida por un maremoto o una erupción volcánica en el fondo del mar.", "respuesta": "Tsunami"},
  {"letra": "U", "pista": "Contiene la U: Mezcla de varios ingredientes, líquida o en pasta, que se usa para poner lustroso el calzado, especialmente el de color negro.", "respuesta": "Betún"},
  {"letra": "V", "pista": "Con la V: Lugar cerrado y cubierto construido para ser habitado por personas.", "respuesta": "Vivienda"},
  {"letra": "X", "pista": "Contiene la X: Que goza de gran aceptación, fama o triunfo popular.", "respuesta": "Exitoso"},
  {"letra": "Y", "pista": "Contiene la Y: En el día que precede inmediatamente al de hoy.", "respuesta": "Ayer"},
  {"letra": "Z", "pista": "Contiene la Z: Poner recto o vertical lo que esté inclinado o tendido.", "respuesta": "Enderezar"}
],
    "Rosco Falso 1": [
  {"letra": "A", "pista": "Con la A: Persona licenciada en derecho que ofrece asesoramiento y defensa en juicios.", "respuesta": "ABOGADO"},
  {"letra": "B", "pista": "Con la B: Ejecutar movimientos acompasados con el cuerpo, generalmente al ritmo de la música.", "respuesta": "BAILAR"},
  {"letra": "C", "pista": "Con la C: Apellido del actor estadounidense nacido en 1962, protagonista de la saga Misión Imposible y Top Gun.", "respuesta": "CRUISE"},
  {"letra": "D", "pista": "Con la D: País del norte de Europa cuya capital es Copenhague.", "respuesta": "DINAMARCA"},
  {"letra": "E", "pista": "Con la E: Prestar atención a lo que se oye.", "respuesta": "ESCUCHAR"},
  {"letra": "F", "pista": "Con la F: Género musical y de danza tradicional de Andalucía, en España.", "respuesta": "FLAMENCO"},
  {"letra": "G", "pista": "Con la G: Instrumento musical de cuerda pulsada con una caja de resonancia en forma de ocho.", "respuesta": "GUITARRA"},
  {"letra": "H", "pista": "Con la H: Elemento químico más ligero y abundante del universo, cuyo número atómico es 1.", "respuesta": "HIDROGENO"},
  {"letra": "I", "pista": "Con la I: Nación europea cuya capital es Londres y forma parte del Reino Unido.", "respuesta": "INGLATERRA"},
  {"letra": "J", "pista": "Con la J: Mamífero rumiante de África, el más alto de todos los animales terrestres debido a su largo cuello.", "respuesta": "JIRAFA"},
  {"letra": "L", "pista": "Con la L: Apellido del músico británico nacido en 1940, miembro de The Beatles e intérprete de Imagine.", "respuesta": "LENNON"},
  {"letra": "M", "pista": "Con la M: Natural de Madrid, capital de España.", "respuesta": "MADRILEÑO"},
  {"letra": "N", "pista": "Con la N: Apellido del físico y matemático británico nacido en 1643, descubridor de la ley de gravitación universal.", "respuesta": "NEWTON"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Paso estrecho o garganta profunda entre montañas esculpido por un río.", "respuesta": "CAÑON"},
  {"letra": "O", "pista": "Con la O: Gran extensión de agua salada que cubre la mayor parte de la superficie terrestre.", "respuesta": "OCEANO"},
  {"letra": "P", "pista": "Con la P: Apellido de la actriz nacida en Israel en 1981, ganadora del Oscar por Cisne Negro.", "respuesta": "PORTMAN"},
  {"letra": "Q", "pista": "Contiene la Q: Antigua práctica protocientífica que buscaba la transmutación de los metales en oro.", "respuesta": "ALQUIMIA"},
  {"letra": "R", "pista": "Con la R: Corriente natural de agua que fluye continuamente y desemboca en otra o en el mar.", "respuesta": "RIO"},
  {"letra": "S", "pista": "Con la S: Natural de Suiza, país de Europa central.", "respuesta": "SUIZO"},
  {"letra": "T", "pista": "Con la T: Mamífero carnívoro de Asia, el más grande de los félidos, con pelaje anaranjado y rayas negras.", "respuesta": "TIGRE"},
  {"letra": "U", "pista": "Con la U: Séptimo planeta del sistema solar, conocido por ser un gigante de hielo con un color azul pálido.", "respuesta": "URANO"},
  {"letra": "V", "pista": "Con la V: Persona que se dedica profesionalmente a la medicina de los animales.", "respuesta": "VETERINARIO"},
  {"letra": "X", "pista": "Contiene la X: Automóvil de alquiler con conductor que sirve para el transporte de pasajeros.", "respuesta": "TAXI"},
  {"letra": "Y", "pista": "Con la Y: Lugar donde se hallan restos arqueológicos o minerales de valor.", "respuesta": "YACIMIENTO"},
  {"letra": "Z", "pista": "Con la Z: Calzado de madera de una sola pieza.", "respuesta": "ZUECO"}
],
    "Rosco Falso 2": [
  {"letra": "A", "pista": "Con la A: Natural de Alemania, país de la Unión Europea.", "respuesta": "ALEMAN"},
  {"letra": "B", "pista": "Con la B: Apellido del compositor alemán nacido en 1685, autor de los Conciertos de Brandeburgo y la Pasión según San Mateo.", "respuesta": "BACH"},
  {"letra": "C", "pista": "Con la C: Preparar los alimentos mediante la acción del calor.", "respuesta": "COCINAR"},
  {"letra": "D", "pista": "Con la D: Animal rumiante similar al camello pero que solo posee una giba o joroba.", "respuesta": "DROMEDARIO"},
  {"letra": "E", "pista": "Con la E: Representar las palabras o las ideas con letras u otros signos trazados en papel u otra superficie.", "respuesta": "ESCRIBIR"},
  {"letra": "F", "pista": "Con la F: País europeo cuya capital es la ciudad de París.", "respuesta": "FRANCIA"},
  {"letra": "G", "pista": "Con la G: Persona que profesa la geología o tiene en ella especiales conocimientos.", "respuesta": "GEOLOGO"},
  {"letra": "H", "pista": "Con la H: Apellido del actor estadounidense nacido en 1956, protagonista de Forrest Gump y Náufrago.", "respuesta": "HANKS"},
  {"letra": "I", "pista": "Con la I: Natural de la India, país del sur de Asia.", "respuesta": "INDIO"},
  {"letra": "J", "pista": "Con la J: Archipiélago y país del este de Asia cuya capital es Tokio.", "respuesta": "JAPON"},
  {"letra": "L", "pista": "Con la L: Conjunto de muchas hojas de papel u otro material semejante que, encuadernadas, forman un volumen.", "respuesta": "LIBRO"},
  {"letra": "M", "pista": "Con la M: Apellido del compositor austriaco nacido en 1756, autor de obras maestras como La flauta mágica y su Réquiem.", "respuesta": "MOZART"},
  {"letra": "N", "pista": "Con la N: Masa de vapor de agua suspendida en la atmósfera.", "respuesta": "NUBE"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Fruto de la planta tropical, de forma ovalada y pulpa comestible.", "respuesta": "PIÑA"},
  {"letra": "O", "pista": "Con la O: Órganos de la vista en el ser humano y en los animales.", "respuesta": "OJOS"},
  {"letra": "P", "pista": "Con la P: Persona que se dedica profesionalmente a la psicología.", "respuesta": "PSICOLOGO"},
  {"letra": "Q", "pista": "Contiene la Q: Grupo de trastornos mentales graves caracterizados por alteraciones en la percepción de la realidad.", "respuesta": "ESQUIZOFRENIA"},
  {"letra": "R", "pista": "Con la R: Apellido de la actriz estadounidense nacida en 1967, protagonista de Pretty Woman y Erin Brockovich.", "respuesta": "ROBERTS"},
  {"letra": "S", "pista": "Con la S: Asiento con respaldo, por lo general de cuatro patas y para una sola persona.", "respuesta": "SILLA"},
  {"letra": "T", "pista": "Con la T: Obra dramática cuyo desenlace es funesto y que busca conmover al espectador.", "respuesta": "TRAGEDIA"},
  {"letra": "U", "pista": "Con la U: Parte inferior o escalón en la puerta de entrada de una casa.", "respuesta": "UMBRAL"},
  {"letra": "V", "pista": "Con la V: Estación del año que sigue a la primavera y precede al otoño, caracterizada por el calor.", "respuesta": "VERANO"},
  {"letra": "X", "pista": "Contiene la X: Suspensión o dificultad en la respiración por falta de aire.", "respuesta": "ASFIXIA"},
  {"letra": "Y", "pista": "Con la Y: Planta de raíz comestible muy común en América tropical, también llamada mandioca.", "respuesta": "YUCA"},
  {"letra": "Z", "pista": "Con la Z: Espacio cubierto situado a la entrada de una casa, junto a la puerta de la calle.", "respuesta": "ZAGUAN"}
],
    "Rosco Falso 3": [
  {"letra": "A", "pista": "Con la A: Reservar parte del dinero del que se dispone.", "respuesta": "AHORRAR"},
  {"letra": "B", "pista": "Con la B: Apellido del actor británico nacido en 1974, protagonista de la trilogía de Batman de Christopher Nolan y de la película El prestigio.", "respuesta": "BALE"},
  {"letra": "C", "pista": "Con la C: Segundo país más extenso del mundo", "respuesta": "CANADA"},
  {"letra": "D", "pista": "Con la D: Persona que tiene por oficio realizar dibujos, especialmente de forma profesional.", "respuesta": "DIBUJANTE"},
  {"letra": "E", "pista": "Con la E: Superficie de cristal azogado por la parte posterior para que se reflejen los objetos.", "respuesta": "ESPEJO"},
  {"letra": "F", "pista": "Con la F: Nombre artístico del cantante británico de origen parsi nacido en 1946, líder de Queen e intérprete de Bohemian Rhapsody y We Will Rock You.", "respuesta": "FREDDIE"},
  {"letra": "G", "pista": "Con la G: Natural de Génova, ciudad de Italia.", "respuesta": "GENOVES"},
  {"letra": "H", "pista": "Con la H: Mezcla de gases visibles producida por la combustión de una materia.", "respuesta": "HUMO"},
  {"letra": "I", "pista": "Con la I: Cualidad de los cuerpos cuyas propiedades físicas no dependen de la dirección en que son examinadas.", "respuesta": "ISOTROPIA"},
  {"letra": "J", "pista": "Con la J: Dispensar a alguien de trabajar por haber cumplido la edad o los años de servicio legalmente establecidos.", "respuesta": "JUBILAR"},
  {"letra": "L", "pista": "Con la L: País del sudeste asiático sin salida al mar, cuya capital es Vientián.", "respuesta": "LAOS"},
  {"letra": "M", "pista": "Con la M: Apellido del diplomático y filósofo italiano nacido en 1469, autor de El Príncipe y considerado padre de la ciencia política moderna.", "respuesta": "MAQUIAVELO"},
  {"letra": "N", "pista": "Con la N: Apellido del actor irlandés nacido en 1952, protagonista de La lista de Schindler y de la saga Búsqueda implacable.", "respuesta": "NEESON"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Construcción rústica pequeña hecha de materiales humildes, destinada a vivienda o refugio.", "respuesta": "CABAÑA"},
  {"letra": "O", "pista": "Con la O: Onda de gran amplitud que se forma en la superficie de las aguas.", "respuesta": "OLA"},
  {"letra": "P", "pista": "Con la P: Persona que se dedica a la elaboración de programas informáticos de manera profesional.", "respuesta": "PROGRAMADOR"},
  {"letra": "Q", "pista": "Contiene la Q: Comida de mesa a la que asisten muchas personas para celebrar algún acontecimiento.", "respuesta": "BANQUETE"},
  {"letra": "R", "pista": "Con la R: Natural de la provincia de Río Negro, en Argentina.", "respuesta": "RIONEGRINO"},
  {"letra": "S", "pista": "Con la S: Momento del año en que el Sol se halla en uno de los dos trópicos, lo cual determina la máxima diferencia de duración entre el día y la noche.", "respuesta": "SOLSTICIO"},
  {"letra": "T", "pista": "Con la T: Planeta que habitamos, tercero en distancia al Sol.", "respuesta": "TIERRA"},
  {"letra": "U", "pista": "Con la U: Número entero que sigue al cero.", "respuesta": "UNO"},
  {"letra": "V", "pista": "Con la V: Punto en que concurren los dos lados de un ángulo o las caras de un poliedro.", "respuesta": "VERTICE"},
  {"letra": "X", "pista": "Contiene la X: Enunciado o conjunto de enunciados que forman una unidad con sentido y que son el objeto de una lectura.", "respuesta": "TEXTO"},
  {"letra": "Y", "pista": "Con la Y: Embarcación de gala o de recreo.", "respuesta": "YATE"},
  {"letra": "Z", "pista": "Con la Z: Cuerpo inferior de un edificio u obra que sirve para elevar los basamentos a un mismo nivel.", "respuesta": "ZOCALO"}
],
    "Rosco Falso 4": [
  {"letra": "A", "pista": "Con la A: Especialista en el estudio de las estrellas y el universo.", "respuesta": "ASTRONOMO"},
  {"letra": "B", "pista": "Con la B: Apellido del actor estadounidense nacido en 1924, protagonista de películas como La ley del silencio y El Padrino.", "respuesta": "BRANDO"},
  {"letra": "C", "pista": "Con la C: Natural de Chile, país de América del Sur.", "respuesta": "CHILENO"},
  {"letra": "D", "pista": "Con la D: Apellido del cantautor estadounidense nacido en 1941, ganador del Nobel de Literatura y creador de temas como Like a Rolling Stone y Blowin' in the Wind.", "respuesta": "DYLAN"},
  {"letra": "E", "pista": "Con la E: País de África cuya capital es El Cairo.", "respuesta": "EGIPTO"},
  {"letra": "F", "pista": "Con la F: Acción de sacar una copia de un documento mediante una máquina.", "respuesta": "FOTOCOPIAR"},
  {"letra": "G", "pista": "Con la G: Animal rumiante de cuello muy largo.", "respuesta": "GIRAFA"},
  {"letra": "H", "pista": "Con la H: Persona que hereda los bienes de otra.", "respuesta": "HEREDERO"},
  {"letra": "I", "pista": "Con la I: En gramática, categoría que expresa una orden o ruego.", "respuesta": "IMPERATIVO"},
  {"letra": "J", "pista": "Con la J: Apellido de la actriz estadounidense nacido en 1975, protagonista de películas como Lara Croft: Tomb Raider y Maléfica.", "respuesta": "JOLIE"},
  {"letra": "L", "pista": "Con la L: Líquido blanco que producen las hembras de los mamíferos.", "respuesta": "LECHE"},
  {"letra": "M", "pista": "Con la M: Persona que dirige una orquesta.", "respuesta": "MAESTRO"},
  {"letra": "N", "pista": "Con la N: Apellido del matemático y físico británico nacido en 1642, famoso por la ley de gravitación universal.", "respuesta": "NEWTON"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Persona que tiene mucha destreza con las manos.", "respuesta": "MAÑOSO"},
  {"letra": "O", "pista": "Con la O: Metal precioso de color amarillo.", "respuesta": "ORO"},
  {"letra": "P", "pista": "Con la P: Provincia de Argentina cuya capital es Santa Rosa.", "respuesta": "PAMPA"},
  {"letra": "Q", "pista": "Contiene la Q: Armazón que sostiene el cuerpo humano.", "respuesta": "ESQUELETO"},
  {"letra": "R", "pista": "Con la R: Natural de la ciudad de Roma.", "respuesta": "ROMANO"},
  {"letra": "S", "pista": "Con la S: En química, sustancia que resulta de la unión de dos o más elementos.", "respuesta": "SOLUCION"},
  {"letra": "T", "pista": "Con la T: Tocar un instrumento de cuerda.", "respuesta": "TAÑER"},
  {"letra": "U", "pista": "Con la U: Elemento químico metálico radiactivo.", "respuesta": "URANIO"},
  {"letra": "V", "pista": "Con la V: Estación del año con temperaturas altas.", "respuesta": "VERANO"},
  {"letra": "X", "pista": "Contiene la X: Que existe en la realidad.", "respuesta": "EXISTENTE"},
  {"letra": "Y", "pista": "Con la Y: Parte amarilla del huevo.", "respuesta": "YEMA"},
  {"letra": "Z", "pista": "Con la Z: Calzado de cuero.", "respuesta": "ZAPATO"}
],
    "Rosco Falso 5": [
  {"letra": "A", "pista": "Con la A: Acción y efecto de abandonar algo o a alguien.", "respuesta": "ABANDONO"},
  {"letra": "B", "pista": "Con la B: Barrio porteño donde se encuentra el estadio conocido popularmente como 'La Bombonera'.", "respuesta": "BOCA"},
  {"letra": "C", "pista": "Con la C: Banda británica de rock alternativo liderada por el cantante Chris Martin.", "respuesta": "COLDPLAY"},
  {"letra": "D", "pista": "Con la D: Que no tiene orden o se aparta de él.", "respuesta": "DESORDENADO - DESORGANIZADO"},
  {"letra": "E", "pista": "Con la E: Perteneciente o relativo a las estrellas.", "respuesta": "ESTELAR"},
  {"letra": "F", "pista": "Con la F: Término del lunfardo que refiere a la pereza, desgano o falta de ganas de hacer algo.", "respuesta": "FIACA"},
  {"letra": "G", "pista": "Con la G: Apellido de la cantante estadounidense de pop, intérprete del éxito mundial '7 Rings'.", "respuesta": "GRANDE"},
  {"letra": "H", "pista": "Contiene la H: Bebida alcohólica que se obtiene por la destilación de un cereal fermentado.", "respuesta": "WHISKY"},
  {"letra": "I", "pista": "Con la I: Que no puede ser vencido o derrotado.", "respuesta": "INVENCIBLE"},
  {"letra": "J", "pista": "Contiene la J: Dicho de una persona: Que tiene los ojos de color azul o verde claro.", "respuesta": "OJIZARCO"},
  {"letra": "L", "pista": "Con la L: Nombre de la cantante y actriz argentina protagonista de la serie 'Sky Rojo' y el éxito 'Disciplina'.", "respuesta": "LALI"},
  {"letra": "M", "pista": "Con la M: Ciudad balnearia de la provincia de Buenos Aires, famosa por su arco de entrada y sus playas tranquilas.", "respuesta": "MIRAMAR"},
  {"letra": "N", "pista": "Con la N: Dicho de un color: Semejante al de la fruta de la que toma su nombre.", "respuesta": "NARANJA"},
  {"letra": "Ñ", "pista": "Contiene la Ñ: Instrumento de percusión compuesto por dos piezas de madera que se chocan entre sí, típico de España.", "respuesta": "CASTAÑUELAS"},
  {"letra": "O", "pista": "Con la O: Que tiene propensión a ver y juzgar las cosas en su aspecto más favorable.", "respuesta": "OPTIMISTA"},
  {"letra": "P", "pista": "Con la P: Barrio de la Ciudad de Buenos Aires conocido por sus amplios parques y su gran oferta gastronómica.", "respuesta": "PALERMO"},
  {"letra": "Q", "pista": "Contiene la Q: Conjunto de máquinas que se emplean para un fin determinado en una industria.", "respuesta": "MAQUINARIA"},
  {"letra": "R", "pista": "Con la R: Acción y efecto de recordar algo o a alguien.", "respuesta": "RECUERDO"},
  {"letra": "S", "pista": "Con la S: Apellido de la supermodelo alemana que fue un ícono absoluto de las pasarelas en la década de los 90.", "respuesta": "SCHIFFER"},
  {"letra": "T", "pista": "Con la T: País del sudeste asiático cuya capital y ciudad más poblada es Bangkok.", "respuesta": "TAILANDIA"},
  {"letra": "U", "pista": "Con la U: Toma de conexión universal de uso frecuente en las computadoras.", "respuesta": "USB"},
  {"letra": "V", "pista": "Con la V: Persona que habita con otras en un mismo edificio, barrio o calle.", "respuesta": "VECINO"},
  {"letra": "X", "pista": "Contiene la X: Persona que vive fuera de su patria, generalmente por motivos políticos.", "respuesta": "EXILIADO - EXILIADA"},
  {"letra": "Y", "pista": "Contiene la Y: Nombre del juguete con forma de vaquero que es uno de los protagonistas de la película 'Toy Story'.", "respuesta": "WOODY"},
  {"letra": "Z", "pista": "Contiene la Z: Administrar el sacramento del bautismo a alguien.", "respuesta": "BAUTIZAR"}
],
}

_geometrias_previas = {
    'roscos': None,
    'roscos_fullscreen': False,
    'ctrl1': None,
    'ctrl2': None
}

# ══════════════════════════════════════════════════════════════════════════════
# SISTEMA DE SONIDO
# ══════════════════════════════════════════════════════════════════════════════

class SoundManager:
    BASE_DIR = Path(__file__).resolve().parent
    SOUNDS_DIR = BASE_DIR / "sounds"
    
    FILES = {
        "inicio":      "inicio.mp3",
        "acierto":     "acierto.mp3",
        "error":       "error.mp3",
        "pasapalabra": "pasapalabra.mp3",
        "victoria":    "victoria.mp3",
        "tiempo":      "tiempo.mp3",
        "aplausos":    "aplausos.mp3"
    }

    def __init__(self):
        try:
            pygame.mixer.init()
        except:
            pass
        self.efectos = {}

    def play_background(self):
        archivo = self.FILES.get("inicio")
        ruta_completa = self.SOUNDS_DIR / archivo
        if ruta_completa.exists():
            try:
                pygame.mixer.music.load(str(ruta_completa))
                pygame.mixer.music.play(loops=-1)
            except Exception as e:
                print(f"❌ Error al reproducir música de fondo: {e}")

    def stop_background(self):
        try:
            pygame.mixer.music.stop()
        except: pass

    def play_effect(self, nombre_sonido):
        if nombre_sonido == "inicio":
            self.play_background()
            return
        archivo = self.FILES.get(nombre_sonido)
        if not archivo: return
        ruta_completa = self.SOUNDS_DIR / archivo
        if ruta_completa.exists():
            try:
                if nombre_sonido not in self.efectos:
                    self.efectos[nombre_sonido] = pygame.mixer.Sound(str(ruta_completa))
                self.efectos[nombre_sonido].play()
            except Exception as e:
                print(f"❌ Error al reproducir el efecto {nombre_sonido}: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# RENDERIZADOR VISUAL
# ══════════════════════════════════════════════════════════════════════════════

class RenderRosco:
    W, H = 800, 900
    CX, CY, RADIO = 400, 400, 320
    BG = "#080e28"
    _S: int = 2

    def __init__(self, canvas, offset_x, datos, nombre, color_nombre="#f1c40f"):
        self.canvas = canvas
        self.offset_x = offset_x
        self.datos = datos
        self.posiciones = {}
        self._nombre = nombre
        self._color_nombre = color_nombre
        self._tiempo = 0 
        self._actual = -1
        self._a = 0
        self._e = 0
        
        self.es_victoria_perfecta = False
        self.es_ganador_normal = False
        self.es_segundo_lugar = False
        self.es_empate = False
        
        self.frame_anim = 0
        self.particulas = []
        self._txt_ganador_s = None
        self._txt_ganador = None
        self._txt_nombre_s = None
        self._txt_nombre = None

        self._canvas_img = self.canvas.create_image(self.offset_x, 0, anchor="nw", image=None)
        self._canvas_timer = self.canvas.create_text(self.offset_x + self.CX, self.CY - 60, text="0", font=("Arial", 55, "bold"), fill="white")
        
        n = len(datos)
        for i in range(n):
            ang = (2 * math.pi * i / n) - (math.pi / 2)
            self.posiciones[i] = (int(self.CX + self.RADIO * math.cos(ang)), int(self.CY + self.RADIO * math.sin(ang)))
            
        self._fonts = self._load_fonts()
        self._img_ref = None
        self._render()

    def _load_fonts(self):
        def _try(names, px):
            for n in names:
                try: return ImageFont.truetype(n, px * self._S)
                except: continue
            return ImageFont.load_default()
        return {
            "letra":    _try(["arialbd.ttf"], 38),
            "timer":    _try(["arialbd.ttf"], 75),
            "errores":  _try(["arialbd.ttf"], 40),
            "aciertos": _try(["arialbd.ttf"], 55),
            "nombre":   _try(["segoeuib.ttf", "arialbd.ttf"], 22),
        }

    def _h2r(self, h):
        h = h.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    def _lerp_t(self, c1, c2, t):
        r1, g1, b1 = self._h2r(c1)
        r2, g2, b2 = self._h2r(c2)
        return (int(r1 + (r2 - r1) * t), int(g1 + (g2 - g1) * t), int(b1 + (b2 - b1) * t))

    def _put_text(self, draw, x, y, text, font, fill, stroke_width=0, stroke_fill=None):
        bb = draw.textbbox((0, 0), text, font=font)
        draw.text((x - (bb[2] - bb[0]) // 2 - bb[0], y - (bb[3] - bb[1]) // 2 - bb[1]),
            text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

    def _bubble(self, draw, cx, cy, r, c_base, c_centro, c_borde, es_actual=False):
        S = self._S
        sx, sy, sr = cx * S, cy * S, r * S
        for i in range(18):
            t = i / 17
            cr = sr - i * S
            draw.ellipse([sx - cr, sy - cr, sx + cr, sy + cr], fill=self._lerp_t(c_base, c_centro, t * 0.8))
        rw, rh = int(sr * 0.4), int(sr * 0.25)
        rx, ry = sx - int(sr * 0.15), sy - int(sr * 0.3)
        draw.ellipse([rx - rw, ry - rh, rx + rw, ry + rh], fill=self._lerp_t(c_centro, "#ffffff", 0.5))
        borde = (255, 255, 255) if es_actual else self._h2r(c_borde)
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=borde, width=(4 if es_actual else 1) * S)

    def _draw_bg(self, img_hi, draw):
        S = self._S
        if os.path.exists(PATH_FONDO_ROSCO):
            try:
                bg_img = Image.open(PATH_FONDO_ROSCO).convert("RGB")
                metodo = Image.NEAREST if (self.es_victoria_perfecta or self.es_ganador_normal) else Image.LANCZOS
                bg_img = bg_img.resize((self.W * S, self.H * S), metodo)
                img_hi.paste(bg_img, (0, 0))
                return  
            except Exception as e:
                print(f"Error al abrir {PATH_FONDO_ROSCO}: {e}")

        cx, cy = (self.W // 2) * S, (self.H // 2) * S
        mr = int(math.hypot(self.W, self.H) / 2) * S
        for i in range(30, -1, -1):
            t = i / 30
            draw.ellipse([cx - int(mr * t), cy - int(mr * t), cx + int(mr * t), cy + int(mr * t)], fill=self._lerp_t("#1b4f72", self.BG, t))

    def _draw_letters(self, draw, actual):
        S = self._S
        for i in range(len(self.datos)):
            x, y = self.posiciones[i]
            if getattr(self, 'es_victoria_perfecta', False):
                colors = ("#08750e", "#0eeb15", "#d1f2eb", False)
            else:
                if i == actual:
                    colors = ("#1446db", "#0099ff", "#ffffff", True)
                else:
                    est = self.datos[i].get("estado", "pendiente")
                    if   est == "acierto":    colors = ("#08750e", "#0eeb15", "#d1f2eb", False)
                    elif est == "error":      colors = ("#991214", "#eb0e2f", "#fadbd8", False)
                    elif est == "pasapalabra":colors = ("#ab8013", "#fbff0f", "#fef9e7", False)
                    else:                     colors = ("#293fb7", "#529eff", "#ffffff",  False)
            self._bubble(draw, x, y, 30, colors[0], colors[1], colors[2], colors[3])
            self._put_text(draw, x * S, y * S, self.datos[i]["letra"], self._fonts["letra"], (255, 255, 255))

    def _draw_hud(self, draw):
        if getattr(self, 'es_victoria_perfecta', False) or getattr(self, 'es_ganador_normal', False) or getattr(self, 'es_segundo_lugar', False) or getattr(self, 'es_empate', False):
            return
        S = self._S
        cx, cy = self.CX, self.CY
        self._bubble(draw, cx, cy - 60, 90, "#d41551", "#ff4056", "#fc9fd7")
        self._bubble(draw, cx - 60, cy + 90, 45, "#641e16", "#ed1818", "#c0392b")
        self._put_text(draw, (cx - 60) * S, (cy + 90) * S, str(self._e), self._fonts["errores"], (255, 255, 255))
        self._bubble(draw, cx + 55, cy + 100, 55, "#0b5345", "#2ee60e", "#27ae60")
        self._put_text(draw, (cx + 55) * S, (cy + 100) * S, str(self._a), self._fonts["aciertos"], (255, 255, 255))

    def ocultar_hud_y_mostrar_segundo(self):
        self.es_segundo_lugar = True
        self.canvas.itemconfig(self._canvas_timer, state="hidden")
        self._render()
        cx = self.offset_x + self.CX
        cy = self.CY
        self.canvas.create_text(cx, cy, text="2DO LUGAR", 
                                font=("Arial", 60, "bold"), fill="#808080")

    def activar_victoria_perfecta(self):
        self.es_victoria_perfecta = True
        self.es_ganador_normal = False
        self.canvas.itemconfig(self._canvas_timer, text="") 
        self._render()
        cx = self.offset_x + self.CX
        cy = self.CY
        self._txt_ganador_s = self.canvas.create_text(cx + 4, cy - 50 + 4, text="¡GANADOR!", font=("Arial", 60, "bold"), fill="#110a00")
        self._txt_nombre_s = self.canvas.create_text(cx + 3, cy + 45 + 3, text=self._nombre.upper(), font=("Arial", 44, "bold"), fill="#000000")
        self._txt_ganador = self.canvas.create_text(cx, cy - 50, text="¡GANADOR!", font=("Arial", 60, "bold"), fill="#fff3a1")
        self._txt_nombre = self.canvas.create_text(cx, cy + 45, text=self._nombre.upper(), font=("Arial", 44, "bold"), fill="#ffd700")
        colores_confeti = ["#ff2a6d", "#05d9e8", "#01012b", "#f5a623", "#7ed321", "#b8e986", "#f8e71c"]
        self.particulas = []
        for _ in range(45):
            x = random.randint(self.offset_x + 10, self.offset_x + self.W - 10)
            y = random.randint(-300, 0)
            radio = random.randint(4, 7)
            vel_x = random.uniform(-1.2, 1.2)
            vel_y = random.uniform(3.0, 6.5)
            cid = self.canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill=random.choice(colores_confeti), outline="")
            self.particulas.append({'id': cid, 'vx': vel_x, 'vy': vel_y, 'x': x, 'y': y, 'r': radio})
        self._bucle_animacion()

    def activar_ganador_normal(self):
        self.es_ganador_normal = True
        self.es_victoria_perfecta = False
        self.es_segundo_lugar = False
        self.canvas.itemconfig(self._canvas_timer, text="") 
        self._render()  
        cx = self.offset_x + self.CX
        cy = self.CY
        self._txt_ganador_s = self.canvas.create_text(cx + 4, cy - 50 + 4, text="¡GANADOR!", font=("Arial", 60, "bold"), fill="#110a00")
        self._txt_nombre_s = self.canvas.create_text(cx + 3, cy + 45 + 3, text=self._nombre.upper(), font=("Arial", 44, "bold"), fill="#000000")
        self._txt_ganador = self.canvas.create_text(cx, cy - 50, text="¡GANADOR!", font=("Arial", 60, "bold"), fill="#ffffff")
        self._txt_nombre = self.canvas.create_text(cx, cy + 45, text=self._nombre.upper(), font=("Arial", 44, "bold"), fill="#e0e0e0")
        self.particulas = [] 
        self._bucle_animacion()

    def activar_segundo_lugar(self):
        self.es_segundo_lugar = True
        self.es_ganador_normal = False
        self.es_victoria_perfecta = False
        try:
            self.canvas.itemconfig(self._canvas_timer, state="hidden")
        except:
            pass
        self._render()
        cx = self.offset_x + self.CX
        cy = self.CY
        for attr in ("_txt_ganador", "_txt_nombre", "_txt_ganador_s", "_txt_nombre_s"):
            obj = getattr(self, attr, None)
            if obj:
                try: self.canvas.delete(obj)
                except: pass
        self._txt_ganador_s = self.canvas.create_text(
            cx + 3, cy - 40 + 3, text="2DO LUGAR",
            font=("Arial", 45, "bold"), fill="#110a00")
        self._txt_nombre_s = self.canvas.create_text(
            cx + 2, cy + 35 + 2, text=self._nombre.upper(),
            font=("Arial", 35, "bold"), fill="#000000")
        self._txt_ganador = self.canvas.create_text(
            cx, cy - 40, text="2DO LUGAR",
            font=("Arial", 45, "bold"), fill="#a0a0a0")
        self._txt_nombre = self.canvas.create_text(
            cx, cy + 35, text=self._nombre.upper(),
            font=("Arial", 35, "bold"), fill="#808080")
        for attr in ("_txt_ganador_s", "_txt_ganador", "_txt_nombre_s", "_txt_nombre"):
            obj = getattr(self, attr, None)
            if obj:
                try: self.canvas.tag_raise(obj)
                except: pass
        self.particulas = []

    def activar_empate(self):
        self.es_empate = True
        self.es_ganador_normal = False
        self.es_victoria_perfecta = False
        self.es_segundo_lugar = False
        try:
            self.canvas.itemconfig(self._canvas_timer, state="hidden")
        except:
            pass
        self._render()
        cx = self.offset_x + self.CX
        cy = self.CY
        for attr in ("_txt_ganador", "_txt_nombre", "_txt_ganador_s", "_txt_nombre_s"):
            obj = getattr(self, attr, None)
            if obj:
                try: self.canvas.delete(obj)
                except: pass
        self._txt_ganador_s = self.canvas.create_text(cx + 4, cy - 50 + 4,
            text="¡EMPATE!", font=("Arial", 60, "bold"), fill="#110a00")
        self._txt_nombre_s = self.canvas.create_text(cx + 3, cy + 45 + 3,
            text=self._nombre.upper(), font=("Arial", 44, "bold"), fill="#000000")
        self._txt_ganador = self.canvas.create_text(cx, cy - 50,
            text="¡EMPATE!", font=("Arial", 60, "bold"), fill="#ffffff")
        self._txt_nombre = self.canvas.create_text(cx, cy + 45,
            text=self._nombre.upper(), font=("Arial", 44, "bold"), fill="#ffffff")
        self.canvas.tag_raise(self._txt_ganador_s)
        self.canvas.tag_raise(self._txt_ganador)
        self.canvas.tag_raise(self._txt_nombre_s)
        self.canvas.tag_raise(self._txt_nombre)
        self.particulas = []

    def _bucle_animacion(self):
        if not (self.es_victoria_perfecta or self.es_ganador_normal or getattr(self, 'es_segundo_lugar', False)): return
        self.frame_anim += 1
        if not getattr(self, 'es_segundo_lugar', False):
            escala_pulso = int(math.sin(self.frame_anim * 0.15) * 6)
            self.canvas.itemconfig(self._txt_ganador, font=("Arial", 60 + escala_pulso, "bold"))
            self.canvas.itemconfig(self._txt_ganador_s, font=("Arial", 60 + escala_pulso, "bold"))
            if self.es_victoria_perfecta:
                color_primario = "#fff3a1" if (self.frame_anim // 4) % 2 == 0 else "#ffd700" 
            else:
                color_primario = "#ffffff" if (self.frame_anim // 4) % 2 == 0 else "#e0e0e0" 
            self.canvas.itemconfig(self._txt_ganador, fill=color_primario)
        if self.es_victoria_perfecta and self.particulas:
            for p in self.particulas:
                self.canvas.move(p['id'], p['vx'], p['vy'])
                p['y'] += p['vy']
                p['x'] += p['vx']
                if p['y'] > self.H:
                    p['y'] = random.randint(-50, -10)
                    p['x'] = random.randint(self.offset_x + 10, self.offset_x + self.W - 10)
                    p['vy'] = random.uniform(3.0, 6.5)
                    self.canvas.coords(p['id'], p['x']-p['r'], p['y']-p['r'], p['x']+p['r'], p['y']+p['r'])
        self.canvas.tag_raise(self._txt_ganador_s)
        self.canvas.tag_raise(self._txt_ganador)
        self.canvas.tag_raise(self._txt_nombre_s)
        self.canvas.tag_raise(self._txt_nombre)
        self.canvas.after(33, self._bucle_animacion)

    def _draw_nombre(self, draw):
        if getattr(self, 'es_victoria_perfecta', False) or getattr(self, 'es_ganador_normal', False) or getattr(self, 'es_segundo_lugar', False) or getattr(self, 'es_empate', False):
            return
        S = self._S
        f = self._fonts["nombre"]
        txt = self._nombre.upper()
        cx, cy = 400 * S, 192 * S
        bb = draw.textbbox((0, 0), txt, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        px, py = 28 * S, 13 * S
        x0, y0 = cx - tw // 2 - px, cy - th // 2 - py
        x1, y1 = cx + tw // 2 + px, cy + th // 2 + py
        radius = (y1 - y0) // 2
        r, g, b = self._h2r(self._color_nombre)
        luminancia = 0.299 * r + 0.587 * g + 0.114 * b
        color_texto = (0, 0, 0) if luminancia > 130 else (255, 255, 255)
        color_borde_texto = (255, 255, 255) if luminancia > 130 else (0, 0, 0)
        shadow_offset = 4 * S
        draw.rounded_rectangle([x0 + shadow_offset, y0 + shadow_offset, x1 + shadow_offset, y1 + shadow_offset], radius=radius, fill=(0, 0, 0))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=(r, g, b))
        mid_y = (y0 + y1) // 2
        highlight_color = self._lerp_t(self._color_nombre, "#ffffff", 0.28)
        inner_pad = 4 * S
        draw.rounded_rectangle([x0 + inner_pad, y0 + inner_pad, x1 - inner_pad, mid_y], radius=radius - inner_pad, fill=highlight_color)
        draw.rounded_rectangle([x0 + S, y0 + S, x1 - S, y1 - S], radius=radius - S, outline=(255, 255, 255), width=S)
        self._put_text(draw, cx, cy, txt, f, fill=color_texto, stroke_width=int(1.5 * S), stroke_fill=color_borde_texto)

    def _render(self):
        S = self._S
        img_hi = Image.new("RGB", (self.W * S, self.H * S), self._h2r(self.BG))
        draw = ImageDraw.Draw(img_hi)
        self._draw_bg(img_hi, draw)
        self._draw_letters(draw, self._actual)
        self._draw_hud(draw)
        self._draw_nombre(draw)
        metodo_resize = Image.NEAREST if (self.es_victoria_perfecta or self.es_ganador_normal) else Image.LANCZOS
        img = img_hi.resize((self.W, self.H), metodo_resize)
        self._img_ref = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self._canvas_img, image=self._img_ref)
        self.canvas.tag_raise(self._canvas_timer)

    def refrescar(self, actual, tiempo, a, e):
        self.canvas.itemconfig(self._canvas_timer, text=str(tiempo))
        if actual != self._actual or a != self._a or e != self._e:
            self._actual, self._a, self._e = actual, a, e
            self._render()

# ══════════════════════════════════════════════════════════════════════════════
# GESTOR DE PARTIDA DUAL
# ══════════════════════════════════════════════════════════════════════════════

class GestorPartidaDual:
    def __init__(self, p1_data, p2_data, geometrias_previas=None):
        self.sounds = SoundManager()
        self._boton_reinicio_mostrado = False
        self.estado_jugadores = {1: {"fin": False, "perfecto": False}, 
                                 2: {"fin": False, "perfecto": False}}

        # ── Ventana de roscos: pantalla secundaria en fullscreen ──────────
        self.win_roscos = tk.Toplevel()
        self.win_roscos.title("Roscos - Partida Dual")
        # Posicionar primero en la pantalla secundaria, luego fullscreen
        self.win_roscos.geometry(f"{SECONDARY_W}x{SECONDARY_H}+{SECONDARY_X}+{SECONDARY_Y}")
        self.win_roscos.attributes('-fullscreen', True)
        self.win_roscos.resizable(False, False)
        self.win_roscos.protocol("WM_DELETE_WINDOW", self.cerrar_todo)

        # F11 para alternar fullscreen, Escape para salir de él
        self.win_roscos.bind('<F11>', lambda e: self.win_roscos.attributes(
            '-fullscreen', not self.win_roscos.attributes('-fullscreen')))
        self.win_roscos.bind('<Escape>', lambda e: self.win_roscos.attributes('-fullscreen', False))

        # Detectar si estamos en un único monitor para evitar que los controles se salgan
        self.win_roscos.update_idletasks()
        screen_w = self.win_roscos.winfo_screenwidth()
        screen_h = self.win_roscos.winfo_screenheight()
        single_monitor = (screen_w < PRIMARY_X + CTRL_W or screen_h < PRIMARY_H)

        if single_monitor:
            self.ctrl_area_width = min(CTRL_W, screen_w // 2)
            self.ctrl_area_height = min(CTRL_H, screen_h)
            self.ctrl1_x = 0
            self.ctrl2_x = self.ctrl_area_width
            self.ctrl1_y = self.ctrl2_y = 0
        else:
            self.ctrl_area_width = CTRL_W
            self.ctrl_area_height = CTRL_H
            self.ctrl1_x = PRIMARY_X
            self.ctrl1_y = PRIMARY_Y
            self.ctrl2_x = PRIMARY_X + CTRL_W
            self.ctrl2_y = PRIMARY_Y

        self.canvas_roscos = tk.Canvas(self.win_roscos, width=1600, height=900,
                                       bg="#080e28", highlightthickness=0)
        self.canvas_roscos.pack()
        self.canvas_roscos.create_line(800, 0, 800, 900, fill="#3498db", width=4)
        self.win_roscos.configure(bg="#010521")

        self.r1 = RenderRosco(self.canvas_roscos, 0,   p1_data["preguntas"], p1_data["nombre"], p1_data["color"])
        self.r2 = RenderRosco(self.canvas_roscos, 800, p2_data["preguntas"], p2_data["nombre"], p2_data["color"])

        self.r1.refrescar(-1, p1_data["tiempo"], 0, 0)
        self.r2.refrescar(-1, p2_data["tiempo"], 0, 0)

        # ── Paneles de control: crear primero, posicionar después ─────────
        self.ctrl1 = JuegoPrincipal(tk.Toplevel(), p1_data, self.r1, self, 1)
        self.ctrl2 = JuegoPrincipal(tk.Toplevel(), p2_data, self.r2, self, 2)

        # Jugador 1 → mitad izquierda de la pantalla principal o primer panel en modo mono-monitor
        self.ctrl1.root.geometry(f"{self.ctrl_area_width}x{self.ctrl_area_height}+{self.ctrl1_x}+{self.ctrl1_y}")
        self.ctrl1.root.resizable(False, False)

        # Jugador 2 → mitad derecha de la pantalla principal o segundo panel en modo mono-monitor
        self.ctrl2.root.geometry(f"{self.ctrl_area_width}x{self.ctrl_area_height}+{self.ctrl2_x}+{self.ctrl2_y}")
        self.ctrl2.root.resizable(False, False)

        # Traer los paneles al frente
        self.ctrl1.root.lift()
        self.ctrl2.root.lift()
        self.ctrl1.root.focus_force()

        self.fin_p1 = False
        self.fin_p2 = False
        self.resumen_p1 = None
        self.resumen_p2 = None

    def cerrar_todo(self):
        try:
            self.sounds.stop_background()
            pygame.mixer.quit()
        except: pass
        os._exit(0)

    def reportar_fin(self, jugador_idx, aciertos, errores, pendientes, total_preguntas):
        es_perfecto = (aciertos == total_preguntas and errores == 0)
        self.estado_jugadores[jugador_idx] = {"fin": True, "perfecto": es_perfecto}

        if jugador_idx == 1:
            self.r1_perfecto = es_perfecto
        else:
            self.r2_perfecto = es_perfecto

        if es_perfecto:
            self.sounds.play_effect("victoria")
        else:
            if len(pendientes) == 0:
                self.sounds.play_effect("aplausos")

        debe_mostrar_resumen = len(pendientes) > 0
        retraso = 4000

        if jugador_idx == 1:
            self.fin_p1 = True
            self.resumen_p1 = (aciertos, errores, pendientes)
            if debe_mostrar_resumen:
                self.win_roscos.after(retraso, lambda: self.crear_pantalla_resumen_flotante(
                    1, pendientes, aciertos, errores))
        else:
            self.fin_p2 = True
            self.resumen_p2 = (aciertos, errores, pendientes)
            if debe_mostrar_resumen:
                self.win_roscos.after(retraso, lambda: self.crear_pantalla_resumen_flotante(
                    2, pendientes, aciertos, errores))

        otro_idx = 2 if jugador_idx == 1 else 1
        otro_r = self.r1 if otro_idx == 1 else self.r2
        este_r = self.r1 if jugador_idx == 1 else self.r2

        if self.estado_jugadores[otro_idx]["fin"] and self.estado_jugadores[otro_idx]["perfecto"]:
            este_r.activar_segundo_lugar()

        if es_perfecto and self.estado_jugadores[otro_idx]["fin"]:
            otro_r.activar_segundo_lugar()

        if self.fin_p1 and self.fin_p2:
            self.determinar_ganador()

    def determinar_ganador(self):
        r1_es_perfecto = getattr(self, 'r1_perfecto', False)
        r2_es_perfecto = getattr(self, 'r2_perfecto', False)

        if r1_es_perfecto or r2_es_perfecto:
            if r1_es_perfecto and not r2_es_perfecto:
                self.r2.activar_segundo_lugar()
            elif r2_es_perfecto and not r1_es_perfecto:
                self.r1.activar_segundo_lugar()
            self.win_roscos.after(3000, self._mostrar_boton_reinicio)
            return

        a1, e1, pend1 = self.resumen_p1[:3]
        a2, e2, pend2 = self.resumen_p2[:3]
        
        ganador_1 = False
        ganador_2 = False
        empate = False
        
        if a1 > a2: 
            ganador_1 = True
        elif a2 > a1: 
            ganador_2 = True
        else:
            if e1 < e2: 
                ganador_1 = True
            elif e2 < e1: 
                ganador_2 = True
            else:
                empate = True

        if empate:
            self.r1.activar_empate()
            self.r2.activar_empate()
        else:
            if ganador_1:
                self.r1.activar_ganador_normal()
            else:
                self.r1.activar_segundo_lugar()
            if ganador_2:
                self.r2.activar_ganador_normal()
            else:
                self.r2.activar_segundo_lugar()

        self.win_roscos.after(3000, self._mostrar_boton_reinicio)
  
    def _mostrar_boton_reinicio(self):
        if self._boton_reinicio_mostrado:
            return
        self._boton_reinicio_mostrado = True
        btn = tk.Button(
            self.win_roscos,
            text="🔄  NUEVA PARTIDA",
            font=("Segoe UI", 14, "bold"),
            bg="#27ae60", fg="white",
            padx=20, pady=8,
            command=self._reiniciar,
            cursor="hand2"
        )
        self.canvas_roscos.create_window(800, 865, window=btn)

    def _reiniciar(self):
        try: self.ctrl1.root.destroy()
        except: pass
        try: self.ctrl2.root.destroy()
        except: pass
        try: self.win_roscos.destroy()
        except: pass
        win_ini.deiconify()
        win_ini.lift()
        win_ini.focus_force()

    def crear_pantalla_resumen_flotante(self, jugador_idx, pendientes, aciertos, errores):
        bg_color = "#0a0f24"
        nombre_jugador = self.ctrl1.nombre if jugador_idx == 1 else self.ctrl2.nombre

        win_res = tk.Toplevel(self.win_roscos)
        win_res.title(f"Resumen - {nombre_jugador.upper()}")

        x_offset = 100 if jugador_idx == 1 else 700
        win_res.geometry(f"680x680+{x_offset}+50")
        win_res.configure(bg=bg_color)

        tk.Label(win_res, text=f"FIN DEL JUEGO — {nombre_jugador.upper()}",
                 font=("Arial", 18, "bold"), bg=bg_color, fg="#7f8c8d").pack(pady=(14, 4))

        stats_frame = tk.Frame(win_res, bg=bg_color)
        stats_frame.pack(pady=4)
        tk.Label(stats_frame, text=f"✓  ACIERTOS: {aciertos}",
                 font=("Segoe UI", 14, "bold"), bg=bg_color, fg="#2ecc71").grid(row=0, column=0, padx=25)
        tk.Label(stats_frame, text=f"✗  ERRORES: {errores}",
                 font=("Segoe UI", 14, "bold"), bg=bg_color, fg="#e74c3c").grid(row=0, column=1, padx=25)

        if not pendientes:
            tk.Label(win_res, text="¡Sin preguntas pendientes!",
                     font=("Segoe UI", 13), bg=bg_color, fg="#aaa").pack(pady=30)
            return

        tk.Label(win_res,
                 text="↑ ↓  para navegar  •  Espacio / Enter  para revelar/ocultar  •  R  para revelar/ocultar todas",
                 font=("Segoe UI", 9), bg=bg_color, fg="#566573").pack(pady=(2, 4))

        main_frame = tk.Frame(win_res, bg=bg_color)
        main_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        list_frame = tk.Frame(main_frame, bg=bg_color)
        list_frame.pack(side="left", fill="y", padx=(0, 8))

        tk.Label(list_frame, text="LETRAS", font=("Segoe UI", 9, "bold"),
                 bg=bg_color, fg="#f1c40f").pack()

        lb = tk.Listbox(list_frame, font=("Consolas", 15, "bold"),
                        bg="#111827", fg="#f1c40f",
                        selectbackground="#2563eb", selectforeground="white",
                        highlightthickness=1, highlightcolor="#3498db",
                        width=5, activestyle="none")
        lb.pack(fill="y", expand=True)

        for p in pendientes:
            lb.insert(tk.END, f"  {p['letra']}")

        det_frame = tk.Frame(main_frame, bg="#0d1117", padx=12, pady=10,
                             highlightthickness=1, highlightbackground="#30363d")
        det_frame.pack(side="left", fill="both", expand=True)

        lbl_letra_det = tk.Label(det_frame, text="",
                                  font=("Arial", 22, "bold"),
                                  bg="#0d1117", fg="#f1c40f")
        lbl_letra_det.pack(anchor="w")

        lbl_pista_det = tk.Label(det_frame, text="",
                                  font=("Segoe UI", 11),
                                  bg="#0d1117", fg="white",
                                  wraplength=420, justify="left", anchor="nw")
        lbl_pista_det.pack(anchor="w", pady=(6, 12), fill="x")

        tk.Frame(det_frame, bg="#30363d", height=1).pack(fill="x", pady=6)

        lbl_resp_hint = tk.Label(det_frame,
                                  text="[ Presioná Espacio o Enter para revelar ]",
                                  font=("Segoe UI", 10, "italic"),
                                  bg="#0d1117", fg="#4a6fa5")
        lbl_resp_hint.pack(anchor="w")

        lbl_resp_det = tk.Label(det_frame, text="",
                                 font=("Segoe UI", 14, "bold"),
                                 bg="#0d1117", fg="#5dade2")
        lbl_resp_det.pack(anchor="w", pady=(4, 0))

        resp_visible = [False] * len(pendientes)
        idx_actual = [0]

        def mostrar_detalle(i):
            idx_actual[0] = i
            p = pendientes[i]
            lbl_letra_det.config(text=f"Letra  {p['letra']}")
            lbl_pista_det.config(text=p['pista'])
            if resp_visible[i]:
                lbl_resp_hint.config(text="[ Espacio / Enter para ocultar ]")
                lbl_resp_det.config(text=f"→  {p['respuesta'].upper()}")
            else:
                lbl_resp_hint.config(text="[ Presioná Espacio o Enter para revelar ]")
                lbl_resp_det.config(text="")

        def toggle_respuesta_actual():
            i = idx_actual[0]
            resp_visible[i] = not resp_visible[i]
            mostrar_detalle(i)

        def toggle_todas():
            alguna_oculta = any(not v for v in resp_visible)
            nuevo_estado = alguna_oculta
            for i in range(len(pendientes)):
                resp_visible[i] = nuevo_estado
            if nuevo_estado:
                btn_toggle_todas.config(text="Ocultar todas las respuestas  (R)")
            else:
                btn_toggle_todas.config(text="Revelar todas las respuestas  (R)")
            mostrar_detalle(idx_actual[0])

        def on_select(event):
            sel = lb.curselection()
            if sel:
                mostrar_detalle(sel[0])

        def on_space(event):
            toggle_respuesta_actual()
            return "break"

        def on_enter(event):
            toggle_respuesta_actual()
            return "break"

        def on_r(event):
            toggle_todas()
            return "break"

        lb.bind("<<ListboxSelect>>", on_select)
        lb.bind("<space>",  on_space)
        lb.bind("<Return>", on_enter)
        lb.bind("<r>",      on_r)
        lb.bind("<R>",      on_r)

        btn_toggle_todas = tk.Button(
            win_res,
            text="Revelar todas las respuestas  (R)",
            font=("Segoe UI", 10, "bold"),
            bg="#1a5276", fg="white", bd=0, padx=14, pady=6,
            cursor="hand2",
            command=toggle_todas
        )
        btn_toggle_todas.pack(pady=(0, 10))

        lb.selection_set(0)
        mostrar_detalle(0)
        lb.focus_set()


# ══════════════════════════════════════════════════════════════════════════════
# CONTROL INDIVIDUAL
# ══════════════════════════════════════════════════════════════════════════════

class JuegoPrincipal:
    # ── Dimensiones: cada control ocupa exactamente la mitad de la pantalla principal
    WIN_W = CTRL_W   # 640
    WIN_H = CTRL_H   # 720

    Y_PISTA_ACTUAL   = 175
    Y_PISTA_SIGUIENTE = 260

    # ── Colores de fondo normales y con foco ─────────────────────────────
    _BG_NORMAL  = "#1c1c1c"
    _BG_FOCUSED = "#252535"   # Azulado-oscuro levemente más claro al tener el foco

    # Color del borde de la ventana con/sin foco
    _BORDER_FOCUSED = "#3498db"   # Azul brillante
    _BORDER_NORMAL  = _BG_NORMAL

    def __init__(self, root, p_data, render_rosco, gestor, player_idx):
        self.root = root
        self.gestor = gestor
        self.player_idx = player_idx
        self.v_rosco = render_rosco
        
        self.nombre = p_data["nombre"]
        self.nombre_rosco = p_data["nombre_rosco"]
        self.tiempo = p_data["tiempo"]
        self.preguntas = p_data["preguntas"]
        
        self.root.title(f"Control J{self.player_idx} - {self.nombre.upper()}")
        # La geometría final la aplica GestorPartidaDual; aquí solo un tamaño inicial
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.gestor.cerrar_todo)

        self.idx = 0
        self.aciertos = 0
        self.errores = 0
        self.idx_anterior = None
        self.pausa = False
        self.fin = False
        self.esperando_inicio = True
        self.en_animacion = False  
        self.historial = []
        self.reloj_id = None

        self._tab_activa = "control"
        self._canvas_pistas = None
        self._frame_pistas_inner = None
        self._mw_handler = None

        self._construir_tab_bar()

        self.frame_control = tk.Frame(root, bg=self._BG_NORMAL,
                                      width=self.WIN_W, height=self.WIN_H - 42)
        self.frame_control.pack(fill="both", expand=True)
        self.frame_control.pack_propagate(False)

        self.frame_pistas_tab = tk.Frame(root, bg="#0d1117",
                                          width=self.WIN_W, height=self.WIN_H - 42)

        self._construir_panel_control()
        self._construir_frame_pistas()

        # ── Indicador visual de foco ──────────────────────────────────────
        # Borde exterior de la ventana cambia de color al recibir el foco
        self.root.configure(bg=self._BORDER_NORMAL)
        self.root.bind("<FocusIn>",  self._on_focus_in)
        self.root.bind("<FocusOut>", self._on_focus_out)

        self.actualizar()

    # ── Manejadores de foco ───────────────────────────────────────────────
    def _on_focus_in(self, event=None):
        """Ilumina levemente el panel cuando la ventana gana el foco."""
        # Solo reaccionamos al evento de la ventana raíz (no de widgets hijos)
        if event and str(event.widget) != str(self.root):
            return
        self.root.configure(bg=self._BORDER_FOCUSED)
        self.frame_control.configure(bg=self._BG_FOCUSED)
        self.canvas_ctrl.configure(bg=self._BG_FOCUSED)
        # Actualizar color de los textos que flotan sobre el canvas
        try:
            self.lbl_respuesta.configure(bg=self._BG_FOCUSED)
            self.lbl_feedback_error.configure(bg=self._BG_FOCUSED)
        except Exception:
            pass

    def _on_focus_out(self, event=None):
        """Vuelve al color base cuando la ventana pierde el foco."""
        if event and str(event.widget) != str(self.root):
            return
        self.root.configure(bg=self._BORDER_NORMAL)
        self.frame_control.configure(bg=self._BG_NORMAL)
        self.canvas_ctrl.configure(bg=self._BG_NORMAL)
        try:
            self.lbl_respuesta.configure(bg=self._BG_NORMAL)
            self.lbl_feedback_error.configure(bg=self._BG_NORMAL)
        except Exception:
            pass

    def _construir_tab_bar(self):
        bar = tk.Frame(self.root, bg="#161b22", height=40)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)
        self.btn_tab_ctrl = tk.Button(bar, text="🎮   CONTROL",
            font=("Segoe UI", 10, "bold"), bg="#1c1c1c", fg="white",
            relief="flat", cursor="hand2", padx=22, pady=0, bd=0,
            activebackground="#1c1c1c", activeforeground="white",
            command=lambda: self._switch_tab("control"))
        self.btn_tab_ctrl.pack(side="left", fill="y")
        tk.Frame(bar, bg="#30363d", width=1).pack(side="left", fill="y", pady=6)
        self.btn_tab_pistas = tk.Button(bar, text="📋   TODAS LAS PISTAS",
            font=("Segoe UI", 10, "bold"), bg="#161b22", fg="#6e7681",
            relief="flat", cursor="hand2", padx=22, pady=0, bd=0,
            activebackground="#1c2333", activeforeground="#adbac7",
            command=lambda: self._switch_tab("pistas"))
        self.btn_tab_pistas.pack(side="left", fill="y")
        tk.Frame(self.root, bg="#30363d", height=1).pack(fill="x")

    def _switch_tab(self, tab):
        if tab == self._tab_activa: return
        self._tab_activa = tab
        if tab == "control":
            self.frame_pistas_tab.pack_forget()
            self.frame_control.pack(fill="both", expand=True)
            self.btn_tab_ctrl.config(bg="#1c1c1c",  fg="white",   activebackground="#1c1c1c")
            self.btn_tab_pistas.config(bg="#161b22", fg="#6e7681", activebackground="#1c2333")
        else:
            self.frame_control.pack_forget()
            self.frame_pistas_tab.pack(fill="both", expand=True)
            self.btn_tab_ctrl.config(bg="#161b22",  fg="#6e7681", activebackground="#1c2333")
            self.btn_tab_pistas.config(bg="#0d1117", fg="white",   activebackground="#0d1117")
            self._poblar_frame_pistas()

    def _construir_panel_control(self):
        p = self.frame_control
        self.canvas_ctrl = tk.Canvas(p, width=self.WIN_W, height=self.WIN_H - 42,
                                     bg=self._BG_NORMAL, highlightthickness=0)
        self.canvas_ctrl.pack()
        
        self.canvas_ctrl.create_text(self.WIN_W // 2, 25,
            text=f"JUGADOR: {self.nombre.upper()}",
            font=("Arial", 18, "bold"), fill=COLOR_ACTUAL)
        
        self.txt_cron = self.canvas_ctrl.create_text(
            self.WIN_W // 2, 80, text=str(self.tiempo),
            font=("Consolas", 55, "bold"), fill=COLOR_PASAPALABRA)
        
        self.ctx_pista_actual = self.canvas_ctrl.create_text(
            self.WIN_W // 2, self.Y_PISTA_ACTUAL, text="",
            font=FUENTE_PISTA, fill="white", justify="center", width=520)
        self.ctx_pista_sig = self.canvas_ctrl.create_text(
            self.WIN_W // 2, self.Y_PISTA_SIGUIENTE, text="",
            font=("Arial", 13, "bold"), fill="#7f8c8d",
            justify="center", width=520)

        self.lbl_respuesta = tk.Label(p, text="", font=FUENTE_RESPUESTA,
                                       bg=self._BG_NORMAL, fg=COLOR_RESPUESTA)
        self.canvas_ctrl.create_window(self.WIN_W // 2, 340, window=self.lbl_respuesta)

        self.lbl_feedback_error = tk.Label(p, text="",
            font=("Segoe UI", 12, "bold"), bg=self._BG_NORMAL, fg=COLOR_ERROR,
            wraplength=520, justify="center")
        self.canvas_ctrl.create_window(self.WIN_W // 2, 420, window=self.lbl_feedback_error)

        btn_f = tk.Frame(p, bg=self._BG_NORMAL)
        tk.Button(btn_f, text="CORRECTO (B)", bg=COLOR_ACIERTO, fg="white",
                  width=12, height=2, font=("Arial", 11, "bold"),
                  command=self.do_bien).grid(row=0, column=0, padx=5)
        tk.Button(btn_f, text="REBOBINAR (R)", bg="#7f8c8d", fg="white",
                  width=12, height=2, font=("Arial", 11, "bold"),
                  command=self.do_rebobinar).grid(row=0, column=1, padx=5)
        tk.Button(btn_f, text="ERROR (M)", bg=COLOR_ERROR, fg="white",
                  width=12, height=2, font=("Arial", 11, "bold"),
                  command=self.do_mal).grid(row=0, column=2, padx=5)
        self.canvas_ctrl.create_window(self.WIN_W // 2, 500, window=btn_f)

        self.btn_pasa = tk.Button(p, text="PASAPALABRA (Enter)", bg=COLOR_PASAPALABRA,
            font=("Arial", 14, "bold"), width=35, height=2, command=self.do_pasa)
        self.canvas_ctrl.create_window(self.WIN_W // 2, 570, window=self.btn_pasa)

        self.root.bind('<b>', lambda e: self.do_bien())
        self.root.bind('<m>', lambda e: self.do_mal())
        self.root.bind('<r>', lambda e: self.do_rebobinar())
        self.root.bind('<Return>', lambda e: self.tecla_enter())

    def _construir_frame_pistas(self):
        f = self.frame_pistas_tab
        header = tk.Frame(f, bg="#161b22", pady=8)
        header.pack(fill="x")
        tk.Label(header, text="HISTORIAL DE PISTAS",
                 font=("Segoe UI", 11, "bold"), bg="#161b22", fg="#f1c40f").pack()
        tk.Label(header, text="Usá la rueda del mouse para navegar",
                 font=("Segoe UI", 8), bg="#161b22", fg="#555e6b").pack()
        legend_f = tk.Frame(f, bg="#0d1117", pady=4)
        legend_f.pack(fill="x", padx=10)
        for txt, col in [("▶ Actual","#3498db"),("✓ Correcto","#2ecc71"),
                         ("✗ Error","#e74c3c"),("⟳ Pasapalabra","#f1c40f"),
                         ("  Pendiente","#7f8c8d")]:
            tk.Label(legend_f, text=txt, font=("Segoe UI", 8, "bold"),
                     bg="#0d1117", fg=col).pack(side="left", padx=6)
        tk.Frame(f, bg="#30363d", height=1).pack(fill="x", padx=8, pady=4)

        container = tk.Frame(f, bg="#0d1117")
        container.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        canvas_p = tk.Canvas(container, bg="#0d1117", highlightthickness=0)
        scrollbar_p = tk.Scrollbar(container, orient="vertical", command=canvas_p.yview)
        frame_p = tk.Frame(canvas_p, bg="#0d1117")
        frame_p.bind("<Configure>", lambda e: canvas_p.configure(
            scrollregion=canvas_p.bbox("all")))
        canvas_p.create_window((0, 0), window=frame_p, anchor="nw", width=615)
        canvas_p.configure(yscrollcommand=scrollbar_p.set)
        canvas_p.pack(side="left", fill="both", expand=True)
        scrollbar_p.pack(side="right", fill="y")
        self._canvas_pistas = canvas_p
        self._frame_pistas_inner = frame_p
        def _on_mousewheel(event):
            canvas_p.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas_p.bind("<MouseWheel>", _on_mousewheel)
        self._mw_handler = _on_mousewheel

    def _poblar_frame_pistas(self):
        if not self._frame_pistas_inner: return
        for w in self._frame_pistas_inner.winfo_children(): w.destroy()
        mw = self._mw_handler
        for i, p in enumerate(self.preguntas):
            estado = p.get("estado", "pendiente")
            es_actual = (i == self.idx)
            if es_actual:
                bg_row, bg_borde = "#0e2a5c", "#3498db"
                fg_letra, fg_pista, icono = "#7ec8fc", "#ddeeff", "▶"
            elif estado == "acierto":
                bg_row, bg_borde = "#0b2e1e", "#1f9c54"
                fg_letra, fg_pista, icono = "#2ecc71", "#a9dfbf", "✓"
            elif estado == "error":
                bg_row, bg_borde = "#2e0b0b", "#c0392b"
                fg_letra, fg_pista, icono = "#e74c3c", "#f1948a", "✗"
            elif estado == "pasapalabra":
                bg_row, bg_borde = "#2e2100", "#d4ac0d"
                fg_letra, fg_pista, icono = "#f1c40f", "#fad7a0", "⟳"
            else:
                bg_row, bg_borde = "#161b22", "#30363d"
                fg_letra, fg_pista, icono = "#7f8c8d", "#8b949e", " "
            outer = tk.Frame(self._frame_pistas_inner, bg=bg_borde)
            outer.pack(fill="x", pady=2, padx=3)
            inner = tk.Frame(outer, bg=bg_row, padx=6, pady=5)
            inner.pack(fill="x", padx=(3, 0))
            tk.Label(inner, text=f"{icono} {p['letra']}",
                     font=("Segoe UI", 12, "bold"), bg=bg_row, fg=fg_letra,
                     width=4, anchor="w").pack(side="left", padx=(0, 8))
            tk.Label(inner, text=p["pista"], font=("Segoe UI", 9),
                     bg=bg_row, fg=fg_pista, wraplength=520,
                     justify="left", anchor="w").pack(side="top", fill="x", expand=True)
            tk.Label(inner, text=f"R: {p.get('respuesta', '').upper()}",
                     font=("Segoe UI", 9, "bold"), bg=bg_row, fg=fg_letra,
                     justify="left", anchor="w").pack(side="top", fill="x",
                                                       expand=True, pady=(2, 0))
            for widget in (outer, inner) + tuple(inner.winfo_children()):
                widget.bind("<MouseWheel>", mw)
        self._frame_pistas_inner.update_idletasks()
        total = len(self.preguntas)
        if total > 1:
            self._canvas_pistas.yview_moveto(max(0.0, (self.idx - 2) / total))

    def _refrescar_panel_pistas(self):
        if self._tab_activa == "pistas": self._poblar_frame_pistas()

    def _guardar_estado(self):
        self.historial.append({
            "preguntas": [{**p} for p in self.preguntas],
            "idx": self.idx, "idx_anterior": self.idx_anterior,
            "aciertos": self.aciertos, "errores": self.errores,
            "tiempo": self.tiempo, "pausa": self.pausa,
            "esperando_inicio": self.esperando_inicio,
        })

    def _obtener_siguiente_pendiente(self, desde_idx):
        n = len(self.preguntas)
        for i in range(1, n + 1):
            s = (desde_idx + i) % n
            if not self.preguntas[s].get("respondida", False):
                return self.preguntas[s]
        return None

    def do_rebobinar(self):
        if self.fin or self.en_animacion or not self.historial: return
        self.gestor.sounds.stop_background()
        s = self.historial.pop()
        self.preguntas=s["preguntas"]; self.idx=s["idx"]; self.idx_anterior=s["idx_anterior"]
        self.aciertos=s["aciertos"]; self.errores=s["errores"]; self.tiempo=s["tiempo"]
        self.esperando_inicio=s["esperando_inicio"]; self.pausa=True
        self.v_rosco.datos=self.preguntas
        self.canvas_ctrl.itemconfig(self.txt_cron, text=str(self.tiempo))
        self.actualizar()

    def tecla_enter(self):
        if self.en_animacion: return
        if self.esperando_inicio:
            self._guardar_estado()
            self.esperando_inicio = False
            if self.reloj_id: self.root.after_cancel(self.reloj_id)
            self.gestor.sounds.play_background()
            self.reloj()
        elif self.pausa:
            self._guardar_estado()
            self.pausa = False
            self.gestor.sounds.play_background()
        else:
            self.do_pasa()
        self.actualizar()
    
    def _animar_avance(self, color_origen, callback):
        pasos = 15
        y_inicial_act = self.Y_PISTA_ACTUAL
        y_inicial_sig = self.Y_PISTA_SIGUIENTE
        y_final_act = self.Y_PISTA_ACTUAL - 40
        y_final_sig = self.Y_PISTA_ACTUAL
        self.canvas_ctrl.itemconfig(self.ctx_pista_sig, font=FUENTE_PISTA)

        def lerp_color(c1, c2, f):
            h1 = c1.lstrip("#"); h2 = c2.lstrip("#")
            r1, g1, b1 = int(h1[0:2],16), int(h1[2:4],16), int(h1[4:6],16)
            r2, g2, b2 = int(h2[0:2],16), int(h2[2:4],16), int(h2[4:6],16)
            return f"#{int(r1+(r2-r1)*f):02x}{int(g1+(g2-g1)*f):02x}{int(b1+(b2-b1)*f):02x}"

        # Color de fondo actual (puede ser normal o focused)
        bg_actual = str(self.canvas_ctrl.cget("bg"))

        def paso_frame(step):
            if step <= pasos:
                f = step / pasos
                curr_y_act = y_inicial_act + (y_final_act - y_inicial_act) * f
                curr_y_sig = y_inicial_sig + (y_final_sig - y_inicial_sig) * f
                self.canvas_ctrl.coords(self.ctx_pista_actual, self.WIN_W // 2, curr_y_act)
                self.canvas_ctrl.coords(self.ctx_pista_sig,    self.WIN_W // 2, curr_y_sig)
                col_act = lerp_color(color_origen, bg_actual, f)
                col_sig = lerp_color("#7f8c8d", "#ffffff", f)
                self.canvas_ctrl.itemconfig(self.ctx_pista_actual, fill=col_act)
                self.canvas_ctrl.itemconfig(self.ctx_pista_sig,    fill=col_sig)
                self.root.after(16, lambda: paso_frame(step + 1))
            else:
                self.canvas_ctrl.coords(self.ctx_pista_actual, self.WIN_W // 2, self.Y_PISTA_ACTUAL)
                self.canvas_ctrl.coords(self.ctx_pista_sig,    self.WIN_W // 2, self.Y_PISTA_SIGUIENTE)
                self.canvas_ctrl.itemconfig(self.ctx_pista_actual, font=FUENTE_PISTA, fill="white")
                self.canvas_ctrl.itemconfig(self.ctx_pista_sig, font=("Arial", 14, "bold"), fill="#7f8c8d")
                self.en_animacion = False
                callback()

        paso_frame(0)

    def do_bien(self):
        if self.pausa or self.fin or self.esperando_inicio or self.en_animacion:
            return
        self.en_animacion = True
        self.gestor.sounds.play_effect("acierto")
        self.preguntas[self.idx].update({"respondida": True, "estado": "acierto"})
        self.aciertos += 1
        self.idx_anterior = self.idx
        self.v_rosco.refrescar(self.idx, self.tiempo, self.aciertos, self.errores)
        self.canvas_ctrl.itemconfig(self.ctx_pista_actual, fill=COLOR_ACIERTO)

        if self.aciertos == len(self.preguntas):
            self.fin = True
            self.en_animacion = False
            try:
                pygame.mixer.music.stop()
            except:
                pass
            self.v_rosco.activar_victoria_perfecta()
            pendientes = []
            total_preguntas = len(self.preguntas)
            self.gestor.reportar_fin(
                self.player_idx, self.aciertos, self.errores,
                pendientes, total_preguntas)
            return

        self._animar_avance(COLOR_ACIERTO, lambda: self.avanzar(pausar=False))

    def do_mal(self):
        if self.pausa or self.fin or self.esperando_inicio or self.en_animacion: return
        self.en_animacion = True
        self.gestor.sounds.stop_background()
        self.gestor.sounds.play_effect("error")
        self.preguntas[self.idx].update({"respondida": True, "estado": "error"})
        self.errores += 1
        self.idx_anterior = self.idx
        self.canvas_ctrl.itemconfig(self.ctx_pista_actual, fill=COLOR_ERROR)
        self._animar_avance(COLOR_ERROR, lambda: self.avanzar(pausar=True))

    def do_pasa(self):
        if self.pausa or self.fin or self.esperando_inicio or self.en_animacion: return
        self.en_animacion = True
        self.gestor.sounds.stop_background()
        self.gestor.sounds.play_effect("pasapalabra")
        self.preguntas[self.idx]["estado"] = "pasapalabra"
        self.idx_anterior = self.idx
        self.canvas_ctrl.itemconfig(self.ctx_pista_actual, fill=COLOR_PASAPALABRA)
        self._animar_avance(COLOR_PASAPALABRA, lambda: self.avanzar(pausar=True))

    def avanzar(self, pausar):
        n = len(self.preguntas)
        nxt = -1
        for i in range(1, n + 1):
            s = (self.idx + i) % n
            if not self.preguntas[s].get("respondida", False): nxt = s; break
        if nxt == -1: self.finalizar()
        else: self.idx = nxt; self.pausa = pausar; self.actualizar()

    def actualizar(self):
        if self.fin: return
        self.canvas_ctrl.itemconfig(self.txt_cron, text=str(self.tiempo))
        self.lbl_feedback_error.config(text="")
        
        cx = self.WIN_W // 2
        self.canvas_ctrl.coords(self.ctx_pista_actual, cx, self.Y_PISTA_ACTUAL)
        self.canvas_ctrl.coords(self.ctx_pista_sig,    cx, self.Y_PISTA_SIGUIENTE)
        self.canvas_ctrl.itemconfig(self.ctx_pista_sig, fill="#7f8c8d")

        if self.esperando_inicio:
            p_a = self.preguntas[0]
            self.canvas_ctrl.itemconfig(self.ctx_pista_actual,
                text=f"LISTO - ADELANTO {p_a['letra']}:\n\n{p_a['pista']}",
                fill=COLOR_PASAPALABRA)
            self.lbl_respuesta.config(text=f"RESPUESTA: {p_a['respuesta'].upper()}")
            self.canvas_ctrl.itemconfig(self.ctx_pista_sig, text="")
        elif self.pausa:
            p_next = self.preguntas[self.idx]
            self.canvas_ctrl.itemconfig(self.ctx_pista_actual,
                text=f"PRÓXIMA LECTURA ({p_next['letra']}):\n{p_next['pista']}",
                fill=COLOR_PASAPALABRA)
            self.lbl_respuesta.config(text=f"RESPUESTA: {p_next['respuesta'].upper()}")
            self.canvas_ctrl.itemconfig(self.ctx_pista_sig, text="")
            if self.idx_anterior is not None:
                p_ant = self.preguntas[self.idx_anterior]
                if p_ant["estado"] == "error":
                    self.lbl_feedback_error.config(
                        text=f"❌ ERROR EN {p_ant['letra']}:\n{p_ant['pista']}\nRESPUESTA: {p_ant['respuesta'].upper()}")
        else:
            p = self.preguntas[self.idx]
            self.canvas_ctrl.itemconfig(self.ctx_pista_actual, text=p["pista"], fill="white")
            self.lbl_respuesta.config(text=f"RESPUESTA: {p['respuesta'].upper()}")
            p_s = self._obtener_siguiente_pendiente(self.idx)
            if p_s: self.canvas_ctrl.itemconfig(self.ctx_pista_sig, text=f"{p_s['pista']}")
            else:   self.canvas_ctrl.itemconfig(self.ctx_pista_sig, text="")

        self.v_rosco.refrescar(self.idx, self.tiempo, self.aciertos, self.errores)
        self._refrescar_panel_pistas()

    def reloj(self):
        if self.reloj_id is not None:
            self.root.after_cancel(self.reloj_id)
            self.reloj_id = None
        if not self.pausa and not self.fin and not self.esperando_inicio:
            self.tiempo -= 1
            self.canvas_ctrl.itemconfig(self.txt_cron, text=str(self.tiempo))
            self.v_rosco.refrescar(self.idx, self.tiempo, self.aciertos, self.errores)
            if self.tiempo <= 0: self.finalizar(); return
        self.reloj_id = self.root.after(1000, self.reloj)

    def finalizar(self):
        self.gestor.sounds.stop_background()
        self.fin = True
        self.v_rosco._actual = -1
        self.v_rosco._a = self.aciertos
        self.v_rosco._e = self.errores
        self.v_rosco._render()
        if self.tiempo <= 0:
            self.gestor.sounds.play_effect("tiempo")
        pendientes = [p for p in self.preguntas if not p.get("respondida", False)]
        for widget in self.frame_control.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, tk.Frame):
                try: widget.config(state="disabled")
                except: pass
        total_preguntas = len(self.preguntas)
        self.gestor.reportar_fin(self.player_idx, self.aciertos, self.errores,
                                  pendientes, total_preguntas)


# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA DE INICIO DUAL
# ══════════════════════════════════════════════════════════════════════════════

def crear_panel_jugador(parent, titulo_txt, default_name, bg_color):
    f = tk.Frame(parent, bg=bg_color, padx=10, pady=10)
    tk.Label(f, text=titulo_txt,
             font=("Segoe UI", 16, "bold"), bg=bg_color, fg="#3498db").pack(pady=(0, 10))
    
    tk.Label(f, text="NOMBRE:", font=("Segoe UI", 10, "bold"),
             bg=bg_color, fg="white").pack()
    frame_nom = tk.Frame(f, bg=bg_color)
    frame_nom.pack(pady=5, fill="x")
    ent_nom = tk.Entry(frame_nom, font=("Arial", 12, "bold"), justify="center",
                       bg="#1c1c1c", fg="white", insertbackground="white")
    ent_nom.pack(side="left", fill="x", expand=True)
    ent_nom.insert(0, default_name)
    
    color_var = tk.StringVar(value="#f1c40f")
    btn_color = tk.Button(frame_nom, bg=color_var.get(), width=3,
                          relief="raised", bd=2, cursor="hand2")
    btn_color.pack(side="left", padx=(6, 0))
    def elegir_color(var=color_var, btn=btn_color):
        nuevo = colorchooser.askcolor(color=var.get(), title="Color")[1]
        if nuevo: var.set(nuevo); btn.config(bg=nuevo)
    btn_color.config(command=elegir_color)
    
    tk.Label(f, text="ROSCO:", font=("Segoe UI", 10, "bold"),
             bg=bg_color, fg="white").pack(pady=(10, 0))
    frame_lista = tk.Frame(f, bg=bg_color)
    frame_lista.pack(pady=5, fill="both", expand=True)
    sb = tk.Scrollbar(frame_lista)
    sb.pack(side="right", fill="y")
    lista = tk.Listbox(frame_lista, font=("Segoe UI", 13, "bold"),
                       bg="#1c1c1c", fg="#f1c40f", selectbackground="#3498db",
                       highlightthickness=0, yscrollcommand=sb.set,
                       height=4, exportselection=False)
    lista.pack(side="left", fill="both", expand=True)
    sb.config(command=lista.yview)
    for nombre in BIBLIOTECA_ROSCOS.keys(): lista.insert(tk.END, nombre)
    
    tk.Label(f, text="TIEMPO (SEGS):", font=("Segoe UI", 10, "bold"),
             bg=bg_color, fg="white").pack(pady=(10, 0))
    ent_tiempo = tk.Entry(f, font=("Arial", 12, "bold"), justify="center",
                          bg="#1c1c1c", fg="white", insertbackground="white")
    ent_tiempo.pack(pady=5, fill="x")
    ent_tiempo.insert(0, "200")
    
    return f, ent_nom, lista, ent_tiempo, color_var

def iniciar_juego():
    def get_data(ent_nom, lista, ent_tiempo, color_var):
        jugador = ent_nom.get()
        seleccion = lista.curselection()
        if not jugador or not seleccion: return None
        try: tiempo = int(ent_tiempo.get())
        except ValueError: return None
        n_rosco = lista.get(seleccion[0])
        return {
            "nombre": jugador,
            "nombre_rosco": n_rosco,
            "preguntas": [dict(p) for p in BIBLIOTECA_ROSCOS[n_rosco]],
            "tiempo": tiempo,
            "color": color_var.get()
        }

    d1 = get_data(nom1, list1, t1, col1)
    d2 = get_data(nom2, list2, t2, col2)

    if not d1 or not d2:
        messagebox.showwarning("Atención",
            "Revisá que ambos jugadores tengan nombre, rosco y tiempo válido.")
        return

    win_ini.withdraw()
    GestorPartidaDual(d1, d2)

if __name__ == "__main__":
    win_ini = tk.Tk()
    win_ini.title("Configuración Dual")
    win_ini.geometry("1280x700")
    win_ini.configure(bg="#0a0f24")
    
    tk.Label(win_ini, text="PASAPALABRA - PARTIDA DUAL",
             font=("Segoe UI", 20, "bold"),
             bg="#0a0f24", fg="#3498db").pack(pady=15)
    
    frame_jugadores = tk.Frame(win_ini, bg="#0a0f24")
    frame_jugadores.pack(fill="both", expand=True, padx=20)
    
    p1, nom1, list1, t1, col1 = crear_panel_jugador(
        frame_jugadores, "JUGADOR 1", "Jugador 1", "#0d1b2a")
    p1.pack(side="left", fill="both", expand=True, padx=10)
    
    p2, nom2, list2, t2, col2 = crear_panel_jugador(
        frame_jugadores, "JUGADOR 2", "Jugador 2", "#1b263b")
    p2.pack(side="right", fill="both", expand=True, padx=10)
    
    btn_iniciar = tk.Button(win_ini, text="INICIAR PARTIDA DUAL",
        font=("Segoe UI", 14, "bold"), bg="#3498db", fg="white",
        command=iniciar_juego, cursor="hand2")
    btn_iniciar.pack(pady=20, padx=50, fill="x")

    win_ini.mainloop()