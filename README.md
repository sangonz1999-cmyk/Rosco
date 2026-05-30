
Sigue estos pasos en esa computadora (La primera vez):

	Entra a la carpeta:

		cd C:\Ruta\A\Tu\Carpeta\Rosco

	Inicializa el repositorio (solo una vez):

		git init

	Conéctalo a tu repositorio de GitHub:

		git remote add origin [EL-LINK-DE-TU-REPOSITORIO]

	Trae todo lo que está en la nube:

		git pull origin main


El ciclo de vida diario (Lo que harás siempre)



	En la computadora donde editaste:

		Entra a la carpeta:

			cd C:\Ruta\A\Tu\Carpeta\Rosco

		Para incluir todos los cambios que hiciste

			git add .

		Ej: "Agregué una pregunta nueva"

			git commit -m "Nueva versión"

		Para enviar el cambio a la nube

			git push .

En la otra computadora (antes de empezar a trabajar):

	Para descargar automáticamente esos cambios desde la nube

		git pull 
    
