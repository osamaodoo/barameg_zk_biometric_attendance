odoo.define('barameg_zk_biometric_attendance.ListView', function (require) {
    "use strict";

    /**
     * The list view is one of the core and most basic view: it is used to look at
     * a list of records in a table.
     *
     * Note that a list view is not instantiated to display a one2many field in a
     * form view. Only a ListRenderer is used in that case.
     */

    var BasicView = require('web.BasicView');
    var core = require('web.core');
    var ListModel = require('web.ListModel');
    var ListRenderer = require('web.ListRenderer');
    var ListController = require('web.ListController');
    var pyUtils = require('web.py_utils');

    var _lt = core._lt;

    var ListView = BasicView.include({
//        init: function (viewInfo, params) {
//            this._super.apply(this, arguments);
//            console.log('ttttttttttttttttt')
//            console.log(this)
//            var headerButtons = this.arch.children[0].children
//            if (headerButtons.length > 0){
//                for(const button of headerButtons){
//                    if (button.attrs.name == 'import_countries'){
//                        this.$headerButtons.push(button);
//                    }
//                }
//            }
//        },
//        _extractHeaderButtons: function(node) {
//            node.children.forEach(child => {
//                if (child.tag === 'button' && !child.attrs.modifiers.invisible) {
//                    this.headerButtons.push(child);
//                    console.log('buttoooooooot')
//                }
//            });
//        },

    })

})