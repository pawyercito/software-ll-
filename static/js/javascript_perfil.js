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

    // Ejemplo de uso de fetchWithAuth para una solicitud GET
    fetchWithAuth("/perfil/")
        .then(response => response.json())
        .then(data => {
            console.log('Respuesta del servidor:', data);
            // Manejar la respuesta del servidor aquí
        })
        .catch((error) => {
            console.error('Error:', error);
        });

    // Aquí puedes añadir más solicitudes usando fetchWithAuth
    // Por ejemplo, para una solicitud POST:
    // fetchWithAuth("/ruta/protegida", {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ clave: 'valor' }),
    // })
    // .then(response => response.json())
    // .then(data => console.log(data))
    // .catch(error => console.error(error));
});