function saveNDVIRegion() {
  if (!drawnPolygon) {
    alert("Please draw a region first.");
    return;
  }

  const farmDetails = document.getElementById("farm-details");
  const farmId = farmDetails?.dataset?.farmId;

  if (!farmId) {
    alert("Farm ID not found.");
    return;
  }

  showLoading("Saving NDVI Region...");

  // ✅ 关键：将 drawnPolygon 转换为 GeoJSON 格式
  const geometry = drawnPolygon.toGeoJSON().geometry;

  const payload = {
    geometry: geometry, // ✅ 不是原始对象，而是纯净的 GeoJSON
    farm_id: farmId,
    start_date: document.getElementById("start-date").value,
    end_date: document.getElementById("end-date").value,
  };

  fetch("/map/api/save-ndvi/", {
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

document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("save-ndvi-btn");
  if (btn) {
    btn.addEventListener("click", saveNDVIRegion);
  }
});
