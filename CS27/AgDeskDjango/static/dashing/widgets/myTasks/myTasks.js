/* global $, rivets, Dashing, Dashboard */

Dashing.widgets.myTasks = function(dashboard) {
    var self = this, widget;
    this.__init__ = Dashing.utils.widgetInit(dashboard, 'myTasks');
    this.row = 2,
    this.col = 1,
    this.scope = {
        title:"My Tasks",
    };
    this.getWidget = function () {
        return widget;
    };
    this.getData = function () {};
};