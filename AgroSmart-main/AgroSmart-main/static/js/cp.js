document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("prediction-form");
  const resultContainer = document.getElementById("prediction-result");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    // Retrieve form values
    const state = document.getElementById("state").value;
    const district = document.getElementById("district").value;
    const cropYear = document.getElementById("crop-year").value;
    const season = document.getElementById("season").value;
    const crop = document.getElementById("crop").value;
    const area = document.getElementById("area").value;

    // Perform the prediction logic (this is a placeholder, replace with actual logic)
    const predictedYield = (Math.random() * 100).toFixed(2); // Dummy prediction result

    // Display the prediction result
    resultContainer.innerHTML = `
        <h2>Prediction Result</h2>
        <p><strong>State:</strong> ${state}</p>
        <p><strong>District:</strong> ${district}</p>
        <p><strong>Crop Year:</strong> ${cropYear}</p>
        <p><strong>Season:</strong> ${season}</p>
        <p><strong>Crop:</strong> ${crop}</p>
        <p><strong>Area:</strong> ${area} hectares</p>
        <p><strong>Predicted Yield:</strong> ${predictedYield} tonnes</p>
      `;
    resultContainer.style.display = "block";
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
