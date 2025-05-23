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

document.getElementById("tree-recommendation-btn").addEventListener("click", function () {
  if (!selectedGeometry) {
    alert("Please draw a region first.");
    return;
  }
  const farmDetails = document.getElementById("farm-details");

  const farmData = {
    farmId: farmDetails.dataset.farmId,
    farmName: farmDetails.dataset.farmName,
    farmLocation: farmDetails.dataset.farmLocation
  };

  showLoading("Generating Tree Recommendation...");

  const payload = {
    geometry: selectedGeometry,
    start_date: document.getElementById("start-date").value,
    end_date: document.getElementById("end-date").value,
    farm_details: farmData,
    farm_id: farmData.farmId
  };
  console.log(payload.farm_id)

  fetch("/map/recommend-tree/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify(payload)
  })
    .then(res => {
      if (!res.ok) throw new Error("Network error");
      return res.text();  // 后端返回 HTML 部分
    })
    .then(html => {
      hideLoading();
      document.getElementById("tree-recommendation-result").innerHTML = html;
    })
    .catch(err => {
      hideLoading();
      console.error(err);
      alert("Failed to fetch tree recommendation.");
    });
});
