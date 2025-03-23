/* global $, rivets, Dashing, Dashboard */

Dashing.widgets.weatherWidgetWeek = function(dashboard) {
    var self = this, widget;
    this.__init__ = Dashing.utils.widgetInit(dashboard, 'weatherWidgetWeek');
    this.row = 1,
    this.col = 2,
    this.scope = {
        title:"Weather Week",
    };
    this.getWidget = function () {
        return widget;
    };
    this.getData = function () {};
};