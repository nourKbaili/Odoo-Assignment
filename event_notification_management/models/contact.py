from odoo import api, fields, models
from odoo.exceptions import UserError


class contact(models.Model):
    _inherit = 'res.partner'

    # I have added an explicit contact type, we could have taken advantage of existing fields in the contact also
    contact_type = fields.Selection([('customer', 'Customer'), ('lead', 'Lead'),('vendor','Vendor'),
                                     ('employee','Employee')], string='Participant Type')

    # this action will be completed according to the desired contact method,
    def action_start_communication(self):
        raise UserError("This will redirect to a chat method, once specified ")


