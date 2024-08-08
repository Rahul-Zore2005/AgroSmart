document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".fertilizer-section form");
  const resultContainer = document.querySelector(".fertilizer-result");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Collect form data
    const formData = new FormData(form);
    const data = {
      temperature: formData.get("temperature"),
      humidity: formData.get("humidity"),
      soilMoisture: formData.get("soilMoisture"),
      soilType: formData.get("soilType"),
      cropType: formData.get("cropType"),
      nitrogen: formData.get("nitrogen"),
      potassium: formData.get("potassium"),
      phosphorous: formData.get("phosphorous"),
    };

    // Send the data to the backend endpoint
    fetch("your-backend-endpoint-url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        // Display the recommendation result
        resultContainer.innerHTML = `
                <h2>Fertilizer Recommendation</h2>
                <p><strong>Recommended Fertilizer:</strong> ${data.fertilizer}</p>
                <p><strong>Details:</strong> ${data.details}</p>
            `;
        resultContainer.style.display = "block";
      })
      .catch((error) => {
        console.error("Error:", error);
        resultContainer.innerHTML =
          "<p>There was an error processing your request. Please try again later.</p>";
        resultContainer.style.display = "block";
      });
  });
});
function toggleUserMenu() {
  const userDropdown = document.getElementById("user-dropdown");
  userDropdown.classList.toggle("show");
}

function logout() {
  window.location.href = "index.html";
}

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
