let drawnPolygon = null;
let selectedGeometry = null;

const polygonDrawer = new L.Draw.Polygon(map, { shapeOptions: { color: '#97009c', fillOpacity: 0.1 } });
const rectangleDrawer = new L.Draw.Rectangle(map, { shapeOptions: { color: '#ff7800', fillOpacity: 0.1 } });

L.Draw.Triangle = L.Draw.SimpleShape.extend({
  statics: { TYPE: 'triangle' },
  options: {
    shapeOptions: {
      color: '#007bff', fillOpacity: 0.2, weight: 2
    }
  },
  initialize(map, options) {
    this.type = L.Draw.Triangle.TYPE;
    L.Draw.SimpleShape.prototype.initialize.call(this, map, options);
  },
  _drawShape(latlng) {
    const points = this._getTrianglePoints(this._startLatLng, latlng);
    if (!this._shape) {
      this._shape = L.polygon(points, this.options.shapeOptions);
      this._map.addLayer(this._shape);
    } else {
      this._shape.setLatLngs(points);
    }
  },
  _getTrianglePoints(start, end) {
    return [[start.lat, start.lng], [end.lat, end.lng], [end.lat, start.lng]];
  },
  _fireCreatedEvent() {
    const triangle = L.polygon(this._shape.getLatLngs(), this.options.shapeOptions);
    L.Draw.SimpleShape.prototype._fireCreatedEvent.call(this, triangle);
  }
});
const triangleDrawer = new L.Draw.Triangle(map, { shapeOptions: { color: '#007bff', fillOpacity: 0.1 } });

function disableAllDrawers() {
  polygonDrawer.disable();
  rectangleDrawer.disable();
  triangleDrawer.disable();
}

document.getElementById("start-draw").addEventListener("click", () => {
  disableAllDrawers();
  const shape = document.getElementById("draw-shape").value;
  if (shape === "polygon") polygonDrawer.enable();
  else if (shape === "rectangle") rectangleDrawer.enable();
  else if (shape === "triangle") triangleDrawer.enable();
});

document.getElementById("end-draw").addEventListener("click", disableAllDrawers);

map.on(L.Draw.Event.CREATED, (event) => {
  if (drawnPolygon) map.removeLayer(drawnPolygon);
  drawnPolygon = event.layer;
  selectedGeometry = drawnPolygon.toGeoJSON().geometry;
  drawnPolygon.addTo(map);
});
