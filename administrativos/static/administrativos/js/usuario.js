function confirmDelete(userId) {
    if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
        fetch(`/administrativo/eliminar_usuario/${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })        
        .then(response => {
            if (response.ok) {
                alert('Usuario eliminado correctamente');
                location.reload();  
            } else {
                alert('Error al eliminar el usuario');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Abrir el modal de edición y cargar los datos del usuario
function openEditModal(userId) {
    fetch(`/administrativo/obtener_usuario/${userId}/`)
        .then(response => {
            if (!response.ok) throw new Error('Error al obtener los datos del usuario');
            return response.json();
        })
        .then(data => {
            document.getElementById('userId').value = data.id;
            document.getElementById('nombre').value = data.nombres;
            document.getElementById('correo').value = data.correo;
            // Agrega aquí otros campos según sea necesario
            document.getElementById('editModal').style.display = 'block';
        })
        .catch(error => console.error('Error al abrir el modal de edición:', error));
}

// Cerrar el modal de edición
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Manejar el envío del formulario de edición
document.getElementById('editUserForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío por defecto

    const formData = new FormData(this);
    const userId = formData.get('userId');

    fetch(`/administrativo/editar_usuario/${userId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (response.ok) {
            alert('Usuario actualizado correctamente');
            closeEditModal();
            location.reload();  // Recargar la página para reflejar los cambios
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Error al actualizar el usuario');
            });
        }
    })
    .catch(error => {
        console.error('Error en la actualización del usuario:', error);
        alert('Hubo un problema al actualizar el usuario.');
    });
});
