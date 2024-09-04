async function detectAnemia() {
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const hemoglobin = parseFloat(document.getElementById('hemoglobin').value);
    const mcv = parseFloat(document.getElementById('mcv').value);

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hemoglobin, gender, mcv })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const result = data.prediction === 1 ? 'Anemic' : 'Non Anemic';
        document.getElementById('result').innerText = `The person is likely to be ${result}`;

        if (mcv < 80.0) {
            document.getElementById('type').innerText = "Type is likely to be microcytic anemia";
        } else if (mcv > 100.0) {
            document.getElementById('type').innerText = "Type is likely to be macrocytic anemia. Please consult your doctor.";
        } else {
            document.getElementById('type').innerText = "";
        }
    } catch (error) {
        document.getElementById('result').innerText = 'Error: Unable to process the request.';
        console.error('There was a problem with the fetch operation:', error);
    }
}

function showInfo() {
    const info = "The dataset consists of 1421 samples with attributes such as gender, hemoglobin, MCV, etc. Random Forest was selected due to its performance.";
    document.getElementById('info').innerHTML = `Get the complete code at <a href='https://github.com/Rahul20915/Anemia-detection-of-patient-using-machine-learning'>GitHub Repo</a><br>${info}`;
}
