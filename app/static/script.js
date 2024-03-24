// Initialize local counter variable
let localCounter = 0;

function setLocalCounter(value) {
    localCounter = value;
    document.getElementById('clickCount').innerText = localCounter;
    document.getElementById('clickBtn').disabled = false;
}

// Function to increment local counter and trigger global counter update
function incrementCounter() {
    setLocalCounter(localCounter + 1);
    updateGlobalCounter();
}

// Function to fetch global counter value from the server
function fetchGlobalCounter() {
    return fetch('https://4ifqmulwvl.execute-api.us-east-1.amazonaws.com/testing/counter', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            setLocalCounter(data.counter);
            
        })
        .catch(error => console.error('Failed to fetch global counter:', error));
}

// Function to update global counter value on the server
function updateGlobalCounter() {
    fetch('https://4ifqmulwvl.execute-api.us-east-1.amazonaws.com/testing/click', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Option to handle response
        })
        .catch(error => console.error('Failed to update global counter:', error));
}

// Event listener for click button to increment counter
document.getElementById('clickBtn').addEventListener('click', incrementCounter);

// Event listener for DOMContentLoaded event to initialize and fetch global counter
document.addEventListener('DOMContentLoaded', function() {

    // Disabling the click when loading the page
    document.getElementById('clickBtn').disabled = true;
    fetchGlobalCounter();
    setInterval(fetchGlobalCounter, 5000);

});


