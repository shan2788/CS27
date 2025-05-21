document.getElementById("generate-report-btn").addEventListener("click", function () {
  if (!drawnPolygon) return alert("Please draw a region first.");
  showLoading("Generating NDVI Report...");

  const geojson = drawnPolygon.toGeoJSON();
  const farmDetails = document.getElementById("farm-details");

  const farmData = {
    farmId: farmDetails.dataset.farmId,
    farmName: farmDetails.dataset.farmName,
    farmLocation: farmDetails.dataset.farmLocation
  };

  fetch("/map/api/generate-report/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({
      geometry: geojson.geometry,
      start_date: document.getElementById("start-date").value,
      end_date: document.getElementById("end-date").value,
      farm_details: farmData
    })
  })
    .then(res => res.blob())
    .then(blob => {
      hideLoading();
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
    })
    .catch(err => {
      hideLoading();
      alert("Error generating NDVI report.");
      console.error(err);
    });
});

document.getElementById("carbon-credit-btn").addEventListener("click", function () {
  if (!drawnPolygon) return alert("Please draw a region first.");
  showLoading("Generating Carbon Credit Report...");

  const geojson = drawnPolygon.toGeoJSON();
  const farmDetails = document.getElementById("farm-details");

  const farmData = {
    farmId: farmDetails.dataset.farmId,
    farmName: farmDetails.dataset.farmName,
    farmLocation: farmDetails.dataset.farmLocation
  };

  fetch("/map/api/carbon-credit/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({
      geometry: geojson.geometry,
      start_date: document.getElementById("start-date").value,
      end_date: document.getElementById("end-date").value,
      farm_details: farmData
    })
  })
    .then(res => res.blob())
    .then(blob => {
      hideLoading();
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
    })
    .catch(err => {
      hideLoading();
      alert("Error generating carbon credit report.");
      console.error(err);
    });
});
