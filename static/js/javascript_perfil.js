document.addEventListener('DOMContentLoaded', function() {
    // Function to retrieve the authentication token from local storage
    const getAuthToken = () => {
        console.log('Local storage object:', localStorage);
        const token = localStorage.getItem('access_token');
        console.log('Token from local storage:', token); // Log the token for debugging
        return token;
    };

    const fetchWithAuth = (url, options = {}) => {
        const token = getAuthToken();
        if (token) {
            options.headers = {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            };
        }
        console.log('Fetch options:', options); // Log the fetch options for debugging
        return fetch(url, options);
    };

    // Wait for 2 seconds before making the request
    setTimeout(() => {
        // Example of using fetchWithAuth for a GET request
        console.log('Fetching data from /perfil/');
        fetchWithAuth("/perfil/", {
            method: 'GET',
        })
       .then(response => {
            console.log('Response status:', response.status);
            if (response.status === 401) {
                // If the response status is 401, refresh the page to force the user to log in again
                location.reload();
            }
            return response.json();
        })
       .then(data => {
            console.log('Server response:', data);
            // Handle the server response here
        })
       .catch((error) => {
            console.error('Error:', error);
        });
    }, 2000);

    // You can add more requests using fetchWithAuth here
    // For example, for a POST request:
    // fetchWithAuth("/ruta/protegida", {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ key: 'value' }),
    // })
    //.then(response => response.json())
    //.then(data => console.log(data))
    //.catch(error => console.error(error));
});