import cv2
import numpy as np
import face_recognition
import base64
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import Usuario, Asistencia
from .forms import UsuarioForm  # Asegúrate de importar correctamente el formulario
from django.core.files.base import ContentFile

def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'asistencia/index.html', {'usuarios': usuarios})

def capturar(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        # Procesar la imagen capturada y guardarla temporalmente
        image_data = image_data.split(',')[1]
        image_data = base64.b64decode(image_data)
        with open('temp.jpg', 'wb') as f:
            f.write(image_data)

        # Leer la imagen capturada y detectar rostros
        captured_image = face_recognition.load_image_file('temp.jpg')
        captured_face_encodings = face_recognition.face_encodings(captured_image)

        if len(captured_face_encodings) == 0:
            return JsonResponse({'message': "No se detectó ningún rostro en la imagen"})

        # Obtener las imágenes de los alumnos y sus codificaciones faciales
        usuarios = Usuario.objects.all()
        known_face_encodings = []
        known_user_ids = []
        for usuario in usuarios:
            user_image = face_recognition.load_image_file(usuario.imagen.path)
            user_encodings = face_recognition.face_encodings(user_image)
            if user_encodings:
                user_encoding = user_encodings[0]
                known_face_encodings.append(user_encoding)
                known_user_ids.append(usuario.id)

        # Comparar las codificaciones faciales de la imagen capturada con las de los alumnos
        for i, captured_face_encoding in enumerate(captured_face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, captured_face_encoding)
            if True in matches:
                user_id = known_user_ids[matches.index(True)]
                usuario = Usuario.objects.get(id=user_id)
                asistencia = Asistencia(usuario=usuario)
                asistencia.imagen_capturada.save('asistencia.jpg', ContentFile(image_data))
                asistencia.save()
                return JsonResponse({'message': f"Asistencia marcada para {usuario.nombre}"})

        return JsonResponse({'message': "Ningún alumno reconocido en la imagen"})
    return HttpResponse("Método no permitido", status=405)


def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('asistencia/')  # Redirige a la página deseada después de guardar el usuario
    else:
        form = UsuarioForm()
    return render(request, 'asistencia/agregar_usuario.html', {'form': form})


def vista_alumnos(request):
    if request.method == 'POST':
        # Verificar si se ha enviado un formulario de eliminación de usuario
        usuario_id = request.POST.get('usuario_id')
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                usuario.delete()
                # Redirigir a la misma página después de la eliminación
                return redirect('alumnos')
            except Usuario.DoesNotExist:
                pass  # Puedes manejar el caso donde el usuario no existe si lo deseas

    usuarios = Usuario.objects.all()
    return render(request, 'asistencia/alumnos.html', {'usuarios': usuarios})



