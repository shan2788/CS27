function showNDVIImage(blob) {
  const imageUrl = URL.createObjectURL(blob);
  document.getElementById("ndvi-image").src = imageUrl;
}

function submitPolygon() {
  if (!drawnPolygon) return alert("Please draw a region first.");
  showLoading("Getting NDVI Image...");
  fetch("/map/api/ndvi/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({
      geometry: drawnPolygon.toGeoJSON().geometry,
      start_date: document.getElementById("start-date").value,
      end_date: document.getElementById("end-date").value
    })
  })
    .then(res => res.blob())
    .then(blob => {
      hideLoading();
      showNDVIImage(blob);
    })
    .catch(err => {
      hideLoading();
      alert("Error fetching NDVI image");
      console.error(err);
    });
}

let debounceTimer = null;
function debounceSubmitPolygon() {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(submitPolygon, 300);
}

function fetchMonthlyNDVI() {
  if (!drawnPolygon) return alert("Please draw a region.");
  showLoading('Fetching Monthly NDVI Data...');
  fetch("/map/api/ndvi-monthly/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({
      geometry: drawnPolygon.toGeoJSON().geometry,
      start_date: document.getElementById("start-date").value,
      end_date: document.getElementById("end-date").value
    })
  })
    .then(res => res.json())
    .then(data => {
      hideLoading();
      const container = document.getElementById("monthly-ndvi-container");
      container.innerHTML = "";
      data.forEach(item => {
        container.insertAdjacentHTML("beforeend", `
          <div class="card mb-3">
            <div class="card-header">${item.month}</div>
            <img src="data:image/png;base64,${item.image_base64}" class="card-img-top" />
            <div class="card-body">
              <p><strong>Mean NDVI:</strong> ${item.ndvi_mean}</p>
              <p><strong>Max NDVI:</strong> ${item.ndvi_max}</p>
              <p><strong>Min NDVI:</strong> ${item.ndvi_min}</p>
            </div>
          </div>
        `);
      });
    })
    .catch(err => {
      hideLoading();
      alert("Failed to fetch monthly NDVI summary.");
      console.error(err);
    });
}
