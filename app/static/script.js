let localCounter = 0;
let isInitialLoad = true;

function setLocalCounter(value) {
    localCounter = value;
    document.getElementById('clickCount').innerText = localCounter;
    document.getElementById('clickBtn').disabled = false;
}

function incrementCounter() {
    setLocalCounter(localCounter + 1);
    updateGlobalCounter();
}

function fetchGlobalCounter() {
    return fetch('http://3.89.220.49:5000/counter', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            setLocalCounter(data.counter);
            if (isInitialLoad) {
                isInitialLoad = false;
            }
        })
        .catch(error => console.error('Failed to fetch global counter:', error));
}

function updateGlobalCounter() {
    fetch('http://3.89.220.49:5000/click', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // setLocalCounter(data.counter);
        })
        .catch(error => console.error('Failed to update global counter:', error));
}

document.getElementById('clickBtn').addEventListener('click', incrementCounter);

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('clickBtn').disabled = true;
    fetchGlobalCounter();
    setInterval(fetchGlobalCounter, 5000);

});


