async function getMajor() {
    const userPrompt = document.getElementById('userPrompt').value;
    const resultElement = document.getElementById('result');

    resultElement.innerHTML = '';

    if (!userPrompt) {
        resultElement.innerHTML = 'Please describe your interests.';
        return;
    }

    try {
        // Sending a POST request to the backend (Flask API)
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userPrompt }),
        });

        if (!response.ok) {
            // Handle non-200 status codes
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // If we get course recommendations
        if (data.courses && data.courses.trim() !== "") {
            resultElement.innerHTML = `<h2>Recommended Majors/Courses:</h2><p>${data.courses}</p>`;
        } else {
            resultElement.innerHTML = 'No recommendations found. Please try again with a different description.';
        }
    } catch (error) {
        resultElement.innerHTML = `Error: ${error.message}. Please try again later.`;
    }
}
