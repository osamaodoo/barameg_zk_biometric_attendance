odoo.define('barameg_zk_biometric_attendance.ListController', function (require) {
"use strict";

    /**
     * The List Controller controls the list renderer and the list model.  Its role
     * is to allow these two components to communicate properly, and also, to render
     * and bind all extra buttons/pager in the control panel.
     */

    var core = require('web.core');
    var BasicController = require('web.BasicController');
    var DataExport = require('web.DataExport');
    var Dialog = require('web.Dialog');
    var ListConfirmDialog = require('web.ListConfirmDialog');
    var session = require('web.session');
    const viewUtils = require('web.viewUtils');

    var _t = core._t;
    var qweb = core.qweb;
    var rpc = require('web.rpc')

    var ListController = require('web.ListController')
    ListController.include({
        /**
         * This key contains the name of the buttons template to render on top of
         * the list view. It can be overridden to add buttons in specific child views.
         */
        renderButtons: function($node) {

            this._super.apply(this, arguments);
            console.log('tttttttt')
            if(this.modelName == 'hr.attendance'){
                if (this.$buttons) {
                    let import_attendance_button = this.$buttons.find('.o_import_attendance_button');
                    import_attendance_button && import_attendance_button.click(this.proxy('import_attendance')) ;
                }

            } else {
                let import_attendance_button = this.$buttons.find('.o_import_attendance_button');
                import_attendance_button.hide()
            }

        },

        import_attendance: function () {

            console.log(this)
            return this._rpc({model: 'hr.attendance', method: 'import_attendance'})

            //implement your click logic here

        }
    })

})