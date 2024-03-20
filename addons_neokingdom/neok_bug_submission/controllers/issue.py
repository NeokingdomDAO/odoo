# -*- coding: utf-8 -*-
import base64
import logging

from odoo import api, http
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Issue(http.Controller):
    @http.route('/issue', type='http', auth='public', website=True)
    def issue_page(self):
        vals = {
            'email': '',
            'name': '',
            'dao_name': '',
            'recaptcha_site_key': request.env['ir.config_parameter'].sudo().get_param('recaptcha_public_key', '')
        }

        # check if user is logged in
        if request.session.uid and request.env.user.exists():
            vals.update(
                email=request.env.user.email,
                name=request.env.user.name,
                dao_name=request.env.user.company_id.name
            )

        return http.request.render('neok_bug_submission.issue_page', vals)

    @http.route('/issue/submit', type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def issue_submit(self, **post):
        try:
            # do recaptcha verification
            if not request.params.get('recaptcha_token_response', False) or not request.env['ir.http']._verify_request_recaptcha_token('submit'):
                raise ValidationError('Recaptcha verification failed')

            # Extract data from the post request
            dao_name = post.get('dao_name', False)
            description = post.get('description', '')
            email = post.get('email', False)
            name = post.get('name', False)
            title = post.get('title', False)

            # wrong request, or refresh. redirect to the issue page
            if not dao_name or not email or not name or not title:
                return request.redirect('/issue')

            # Assuming you have a 'bug.submission' model
            su_bug_submission = request.env['neok.helpdesk.bug.submission'].sudo()
            su_ir_attachment = request.env['ir.attachment'].sudo()
            su_res_partner = request.env['res.partner'].sudo()

            # check if partner already exists
            partner = request.env['res.partner'].search([('email', '=', email)], limit=1)

            # create a new partner
            if not partner.exists():
                partner_vals = {
                    'name': name,
                    'email': email,
                }
                partner = su_res_partner.create(partner_vals)

            # Create a new record in the 'bug.submission' model
            submission_vals = {
                'dao_name': dao_name,
                'description': description,
                'title': title,
                'partner_id': partner.id,
            }
            new_submission = su_bug_submission.create(submission_vals)

            # Save files as attachments
            if post.get('files'):
                attached_files = request.httprequest.files.getlist('files')

                for file in attached_files:
                    new_att = su_ir_attachment.create({
                        'name': file.filename,
                        'datas': base64.b64encode(file.read()),
                        'res_model': 'neok.helpdesk.bug.submission',
                        'res_id': new_submission.id
                    })
                    new_submission.attachment_ids += new_att

            # result page
            return http.request.render('neok_bug_submission.issue_page_response', {
                'res_title': 'Issue Submitted',
                'res_subtitle': 'Thank you!',
                'msg': 'Identifier: {0}'.format(new_submission.name),
                'success': True
            })

        except Exception as e:
            _logger.error('Error while submitting issue: %s', e)
            return http.request.render('neok_bug_submission.issue_page_response', {
                'res_title': 'Issue Submission Failed',
                'res_subtitle': 'Try again, or use our social channels to contact us. (Links below)',
                'msg': 'Seems like an unlucky day..',
                'success': False
            })
