# -*- coding: utf-8 -*-

import datetime
import pytz
import time
from datetime import date
from datetime import time
from time import tzname
from .pyzk import zk
from odoo import models, fields, api

def _tz_get(self):
    # put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
    return [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_id = fields.Char(string='Attendance ID')


class BiometricDevices(models.Model):
    _name = 'biometric.devices'

    name = fields.Char(string='Device Name')
    ip_address = fields.Char(string='IP Address')
    port = fields.Integer(string='Port Number')
    timezone = fields.Selection(_tz_get, string='Timezone', default=lambda self: self._context.get('tz'),
                          help="The partner's timezone, used to output proper date and time values "
                               "inside printed reports. It is important to set a value for this field. "
                               "You should use the same timezone that is otherwise used to pick and "
                               "render date and time values: your computer's timezone.")
    tz_offset = fields.Char(compute='_compute_tz_offset', string='Timezone offset', invisible=True)
    description = fields.Text(string='Device Description')
    # lines = fields.One2many('device.attendance.log', 'dev_id', string='Attendance Logs')
    active = fields.Boolean(default=True)
    notes = fields.Text()
    timeout = fields.Integer(default=5)
    force_udp = fields.Boolean(default=False)
    ommit_ping = fields.Boolean(default=False)
    password = fields.Char(default=0)

    def test_device(self):
        device = zk.ZK(self.ip_address, port=self.port, timeout=self.timeout, password=self.password,
                       force_udp=self.force_udp, ommit_ping=self.ommit_ping)
        try:
            conn = device.connect()
        except Exception as e:
            pass
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Barameg Biometric Attendance'),
                    'message': e,
                    'type': 'danger',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification
        else:
            pass
        finally:
            pass
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Barameg Biometric Attendance'),
                    'message': 'Connected Successfully',
                    'type': 'success',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification

    def get_attendance_log(self):
        device = zk.ZK(self.ip_address, port=self.port, timeout=self.timeout, password=self.password,
                       force_udp=self.force_udp, ommit_ping=self.ommit_ping)
        try:
            conn = device.connect()
            attendances = conn.get_attendance()
            print(attendances)
        except Exception as e:
            pass
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Barameg Biometric Attendance'),
                    'message': e,
                    'type': 'danger',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification


class DeviceAttendance(models.Model):
    _name = 'device.attendance'

    device = fields.Many2one('biometric.devices')
    employee_code = fields.Char(string='Employee Code')
    timestamp = fields.Datetime(string='Punch Time')
    # check = fields.Selection([
    #     ('in', 'Check-In'),
    #     ('out', 'Check-Out'),
    # ])

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def import_attendance(self):
        pass
        # employees = self.env['hr.employee'].sudo().search([])
        # for employee in employees:
        #     if employee.attendance_id:
        #         attendances = self.env['device.attendance'].sudo().search([('employee_code', '=', employee.attendance_id)])
        #         for attendance in attendances:
        #             if employee.attendance_id == attendance.employee_code:



