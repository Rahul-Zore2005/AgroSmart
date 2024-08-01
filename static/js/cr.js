document
  .getElementById("recommendationForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    // Retrieve form values
    const nitrogen = document.getElementById("nitrogen").value;
    const phosphorus = document.getElementById("phosphorus").value;
    const potassium = document.getElementById("potassium").value;
    const temperature = document.getElementById("temperature").value;
    const humidity = document.getElementById("humidity").value;
    const phValue = document.getElementById("phValue").value;
    const rainfall = document.getElementById("rainfall").value;

    // Prepare the data to send
    const data = {
      nitrogen: nitrogen,
      phosphorus: phosphorus,
      potassium: potassium,
      temperature: temperature,
      humidity: humidity,
      phValue: phValue,
      rainfall: rainfall
    };

    // Send the data to the Flask API
    fetch('/recommend_crop', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      // Display recommendation
      const resultDiv = document.getElementById("recommendationResult");
      resultDiv.style.display = "block";
      resultDiv.innerHTML = `<h2>Recommended Crop: ${data.recommendation}</h2>`;
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });

// Toggle user dropdown menu
function toggleUserMenu() {
  const userDropdown = document.getElementById("user-dropdown");
  userDropdown.classList.toggle("show");
}

function logout() {
  window.location.href = "index.html";
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
  if (!event.target.matches(".user-icon")) {
    const dropdowns = document.getElementsByClassName("user-dropdown");
    for (let i = 0; i < dropdowns.length; i++) {
      const openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
};
