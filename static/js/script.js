// Ajax request example
document.getElementById('inputForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    document.getElementById('loader').style.display = 'block'; // Show loader
    document.getElementById('responseSection').innerHTML = ''; // Clear previous response
    const userInput = document.getElementById('userInput').value;
    

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: userInput })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loader').style.display = 'none'; // Hide loader
        const { message, status } = data || {};       
        if (status) {
            document.getElementById('responseSection').innerHTML = `<h2>Response:</h2><p>${message}</p>`; 
            document.getElementById('userInput').value = ''; // Clear the textarea

        }
    })
    .catch(error => console.error('Error:', error));
});
