from odoo import _, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_register_payment(self):
        """ Open the account.payment.register wizard to pay the selected journal entries.
        :return: An action opening the account.payment.register wizard.
        """
        order = self.env['sale.order'].search([('invoice_ids.id', '=', self.id)])
        cod_collection = self.env['cod.payment.collection'].search([('sale_order_id.id', '=', order.id)])
        if order.order_cod_available:
            if cod_collection.ids:
                for record in cod_collection:
                    if not record.state == 'done':
                        raise ValidationError(_('You can not register payment because COD payment are still pending.'))
                    else:
                        return {
                            'name': _('Register Payment'),
                            'res_model': 'account.payment.register',
                            'view_mode': 'form',
                            'context': {
                                'active_model': 'account.move',
                                'active_ids': self.ids,
                            },
                            'target': 'new',
                            'type': 'ir.actions.act_window',
                        }
            else:
                raise ValidationError(_('You can not register payment because COD payment are still pending.'))
        else:
            return {
                'name': _('Register Payment'),
                'res_model': 'account.payment.register',
                'view_mode': 'form',
                'context': {
                    'active_model': 'account.move',
                    'active_ids': self.ids,
                },
                'target': 'new',
                'type': 'ir.actions.act_window',
            }
