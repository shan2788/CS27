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

function saveNDVIRegion() {
  if (!drawnPolygon) {
    alert("Please draw a region first.");
    return;
  }

  showLoading("Saving NDVI Region...");

  const payload = {
    geometry: drawnPolygon,
    start_date: document.getElementById("start-date").value,
    end_date: document.getElementById("end-date").value,
  };

  fetch("/map/save-ndvi/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify(payload)
  })
    .then(res => {
      if (!res.ok) throw new Error("Network error");
      return res.json();
    })
    .then(data => {
      hideLoading();
      alert("NDVI region saved successfully!");
    })
    .catch(err => {
      hideLoading();
      console.error(err);
      alert("Failed to save NDVI region.");
    });
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
window.saveNDVIRegion = saveNDVIRegion;