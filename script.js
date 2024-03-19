let localCounter = 0;
let isInitialLoad = false;

function setLocalCounter(value) {
    localCounter = value;
    document.getElementById('clickCount').innerText = localCounter;
}

function incrementCounter() {
    // Check if it's the initial load
    if(isInitialLoad) {
        // Only fetch the global counter on initial load and not increment
        fetchGlobalCounter().then(() => {
            isInitialLoad = false; // After initial load, set to false
        });
    } else {
        // After initial load, increment locally and update the global counter
        setLocalCounter(localCounter + 1);
        updateGlobalCounter();
    }
}

function fetchGlobalCounter() {
    return fetch('http://127.0.0.1:5000/counter',{ method: 'GET'}) 
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            setLocalCounter(data.counter);
        })
        .catch(error => console.error('Failed to fetch global counter:', error));
}

function updateGlobalCounter() {
    fetch('http://127.0.0.1:5000/click', { method: 'POST' }) 
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // This is where you could handle a successful counter update
            // For example, you could update some state to indicate the global counter was updated
        })
        .catch(error => console.error('Failed to update global counter:', error));
}

// incrementCounter function to the button click event
document.getElementById('clickBtn').addEventListener('click', incrementCounter);

// Fetching the global counter on page load
document.addEventListener('DOMContentLoaded', function() {
    fetchGlobalCounter();
});
