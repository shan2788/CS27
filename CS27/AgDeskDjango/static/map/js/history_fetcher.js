document.getElementById("view-history-btn").addEventListener("click", function () {
  const historySection = document.getElementById("history-section");
  const historyContent = document.getElementById("history-content");
  const farmId = document.getElementById("farm-details").dataset.farmId;

  if (historySection.style.display === "none") {
    historySection.style.display = "block";
    fetch(`/map/api/region-history/${farmId}/`)
      .then(res => res.text())
      .then(html => {
        historyContent.innerHTML = html;
      })
      .catch(err => {
        console.error(err);
        historyContent.innerHTML = "<p>Error loading history.</p>";
      });
  } else {
    historySection.style.display = "none";
  }
});

document.getElementById("view-carbon-credit-history-btn")?.addEventListener("click", function () {
  const section = document.getElementById("carbon-credit-history-section");
  const content = document.getElementById("carbon-credit-history-content");
  const farmId = document.getElementById("farm-details").dataset.farmId;

  if (section.style.display === "none") {
    section.style.display = "block";
    fetch(`/map/api/carbon-credit-history/${farmId}/`)
      .then(res => res.text())
      .then(html => {
        content.innerHTML = html;
      })
      .catch(err => {
        console.error(err);
        content.innerHTML = "<p>Error loading carbon credit history.</p>";
      });
  } else {
    section.style.display = "none";
  }
});
