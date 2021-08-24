# -*- coding: utf-8 -*-
# from odoo import http


# class BaramegZkBiometricAttendance(http.Controller):
#     @http.route('/barameg_zk_biometric_attendance/barameg_zk_biometric_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/barameg_zk_biometric_attendance/barameg_zk_biometric_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('barameg_zk_biometric_attendance.listing', {
#             'root': '/barameg_zk_biometric_attendance/barameg_zk_biometric_attendance',
#             'objects': http.request.env['barameg_zk_biometric_attendance.barameg_zk_biometric_attendance'].search([]),
#         })

#     @http.route('/barameg_zk_biometric_attendance/barameg_zk_biometric_attendance/objects/<model("barameg_zk_biometric_attendance.barameg_zk_biometric_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('barameg_zk_biometric_attendance.object', {
#             'object': obj
#         })
