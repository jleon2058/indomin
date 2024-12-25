from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.addons.sale_timesheet_enterprise.models.sale import DEFAULT_INVOICED_TIMESHEET


class AnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    def _is_updatable_timesheet(self):
        return not self.validated