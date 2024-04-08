document.addEventListener('DOMContentLoaded', function() {
    // Función para obtener el token de autenticación del almacenamiento local
    const getAuthToken = () => localStorage.getItem('authToken');

    // Función interceptor para añadir el token de autenticación a las solicitudes
    const fetchWithAuth = (url, options = {}) => {
        const token = getAuthToken();
        if (token) {
            options.headers = options.headers || {};
            options.headers.Authorization = `Bearer ${token}`;
        }
        return fetch(url, options);
    };

    // Realiza una solicitud GET a la ruta /perfil/ cuando la página se cargue
    fetchWithAuth("/perfil/")
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Respuesta del servidor:', data);
            // Aquí puedes procesar la respuesta del servidor y actualizar la página de perfil según sea necesario
        })
        .catch((error) => {
            console.error('Error:', error);
        });

    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Create a FormData object from the form
        const formData = new FormData(form);

        // Send the HTTP request with the Authorization header using fetchWithAuth
        fetchWithAuth("/citas", {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            console.log('Token from local storage:', localStorage.getItem('authToken'));
            // Handle the server response here
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});