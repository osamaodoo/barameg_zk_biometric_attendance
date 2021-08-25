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
    biometric_check_window = fields.Integer(default=5)
    biometric_last_check_in = fields.Datetime()
    biometric_last_check_out = fields.Datetime()


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
            count = 0
            attendances = str(attendances).split('<Attendance>:')
            for attendance in attendances:
                try:
                    uid = attendance.split(' : ')[0].strip()
                    timestamp = attendance.split(' : ')[1].split(' (')[0]
                except:
                    pass
                else:
                    log = self.env['device.attendance']
                    # record_exist = log.search([('employee_code', '=', uid), ('timestamp', '=', timestamp)])
                    # if not record_exist:
                    log.create({
                        'device': self.id,
                        'employee_code': uid,
                        'timestamp': timestamp,
                        # 'check': attendance.punch
                    })
                    count = count + 1
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Barameg Biometric Attendance'),
                    'message': str(count) + ' records have been imported!',
                    'type': 'success',  # types: success,warning,danger,info
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

class PreparedAttendance(models.Model):
    _name = 'prepared.attendance'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
    worked_time = fields.Float(compute='calc_worked_time')

    @api.depends('check_in','check_out')
    def calc_worked_time(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                diff = (rec.check_out - rec.check_in).total_seconds() / 60 / 60
                rec.worked_time = diff
            else:
                rec.worked_time = 0

    @api.model
    def prepare_attendance(self):
        employees = self.env['hr.employee'].search([])
        attendances = self.env['device.attendance'].search([])
        for attendance in attendances:
            for employee in employees:
                if employee.attendance_id == attendance.employee_code:
                    # employee never checked before
                    if not employee.biometric_last_check_in and not employee.biometric_last_check_out:
                        print('employee never checked in')
                        self.create({
                            'employee_id': employee.id,
                            'check_in': attendance.timestamp,
                        })
                        employee.biometric_last_check_in = attendance.timestamp
                    # checked in employee
                    if employee.biometric_last_check_in and not employee.biometric_last_check_out:
                        # pass
                        print('employee checked in')
                        if attendance.timestamp > employee.biometric_last_check_in:
                            diff = (attendance.timestamp - employee.biometric_last_check_in).total_seconds() / 60
                            if diff > employee.biometric_check_window:
                                pass
                                record = self.search([('employee_id', '=', employee.id),('check_in', '=', employee.biometric_last_check_in)])
                                record.write({
                                    'check_out': attendance.timestamp
                                })
                                employee.biometric_last_check_in = False
                    #checked out employee
                    if employee.biometric_last_check_out and not employee.biometric_last_check_in:
                        pass
                        print('employee checked out')
                        if attendance.timestamp > employee.biometric_last_check_out:
                            diff = (attendance.timestamp - employee.biometric_last_check_out).total_seconds() / 60
                            if diff > employee.biometric_check_window:
                                self.create({
                                    'employee_id': employee.id,
                                    'check_in': attendance.timestamp,
                                })
                                employee.biometric_last_check_in = attendance.timestamp

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def import_attendance(self):
        pass
        employees = self.env['hr.employee'].sudo().search([])
        for employee in employees:
            if employee.attendance_id:
                attendances = self.env['device.attendance'].sudo().search([('employee_code', '=', employee.attendance_id)])
                for attendance in attendances:
                    if employee.attendance_id == attendance.employee_code:
                        pass


