from odoo import api, fields, models,_

from datetime import datetime, time

from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class Event(models.Model):
    _inherit = 'event.event'

    # This field differentiates CRM events from other events.
    is_crm_event = fields.Boolean(string="CRM event", default=False)
    # The date when communication should start.
    communication_starts_before = fields.Date(string = 'Communication Start Date')
    # Participants who are either leads or customers.
    participant_ids = fields.Many2many('res.partner', string='Participants',domain = "[ ('contact_type', 'in', ['lead', 'customer'])]")

    @api.constrains('communication_starts_before', 'date_begin')
    def _check_communication_starts_before(self):
        """
        Ensure that the communication_starts_before date is before the event's date_begin.
        """
        for event in self:
            if event.communication_starts_before and event.date_begin:
                event_start_date = event.date_begin.date()
                if event.communication_starts_before >= event_start_date:
                    raise ValidationError(_("The Final Communication Date must be before the Event Start Date."))

    def _cron_send_email_notification(self):
        """
        This method executes daily to notify salespeople about upcoming events.
        """
        today = datetime.combine(fields.Date.today(), time(0, 0, 0))
        # here we couldhave compared with date <= , instead of contacting on the same day that is defined
        # but this will require marking the events that have been checked
        events = self.search([('communication_starts_before', '=', today), ('is_crm_event','=',True)])

        for event in events:
            self._send_email(event)



    def _send_email(self, event):
        """
        This method forms and sends email notifications to salespeople responsible
        for the event's participants.
        """
        get_template = self.env.ref('event_notification_management.Notify_sales_people')
        template = self.env['mail.template'].browse(get_template.id)

        if not template:
            raise UserError(_("Mail template not found!"))

        # Collect unique salesperson IDs to avoid duplicate notifications.
        salesperson_ids = set()
        if event.participant_ids:
            for participant in event.participant_ids:
                if participant.user_id:
                    salesperson_ids.add(participant.user_id.id)

        sales_people = self.env['res.users'].browse(salesperson_ids)
        if sales_people:
            for salesperson in sales_people:
                if not salesperson.email:
                    raise UserError(_("Cannot send email: user %s has no email address.", salesperson.name))
                print('user',salesperson.email,salesperson.name)
                template.with_context(
                    email=salesperson.email,
                    name = salesperson.display_name,
                    event_name=event.name,
                    event_date=event.date_begin,
                    event_url=f"/web#id={event.id}&view_type=form&model=event.event"

                ).send_mail(event.id, force_send=True)

                _logger.info("A Notification has been sent to <%s> at <%s>", salesperson.login, salesperson.email)






