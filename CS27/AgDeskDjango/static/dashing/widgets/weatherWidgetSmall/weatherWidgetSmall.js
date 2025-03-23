/* global $, rivets, Dashing, Dashboard */

Dashing.widgets.weatherWidgetSmall = function(dashboard) {
    var self = this, widget;
    this.__init__ = Dashing.utils.widgetInit(dashboard, 'weatherWidgetSmall');
    this.row = 1,
    this.col = 1,
    this.scope = {
        title:"Weather (Small)",
    };
    this.getWidget = function () {
        return widget;
    };
    this.getData = function () {};
};