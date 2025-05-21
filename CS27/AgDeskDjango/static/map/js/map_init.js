const map = L.map('map').setView([-33.8688, 151.2093], 10);

const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

const sentinelLayer = L.tileLayer.wms(`https://services.sentinel-hub.com/ogc/wms/${sentinel_instance_id}`, {
  layers: '3_NDVI',
  format: 'image/png',
  transparent: true,
  SHOWLOGO: false,
  attribution: '&copy; Sentinel Hub',
  updateWhenIdle: true,
  reuseTiles: true
});

const baseMaps = { "OpenStreetMap": osmLayer };
const overlayMaps = { "Sentinel-2 Imagery": sentinelLayer };
L.control.layers(baseMaps, overlayMaps).addTo(map);

const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);
