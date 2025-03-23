/* global $, rivets, Dashing, Dashboard */

Dashing.widgets.myCheckouts = function(dashboard) {
    var self = this, widget;
    this.__init__ = Dashing.utils.widgetInit(dashboard, 'myCheckouts');
    this.row = 1,
    this.col = 2,
    this.scope = {
        title:"My Checkouts",
    };
    this.getWidget = function () {
        return widget;
    };
    this.getData = function () {};
};