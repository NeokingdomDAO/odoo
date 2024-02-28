# -*- coding: utf-8 -*-
import logging
import json

from odoo import http, _
from odoo.http import request, Response
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class WebsiteHrRecruitment(http.Controller):
    @http.route('/neok-api/positions', auth="public", csrf=False, methods=['GET'], type='json')
    def neok_api_positions(self):
        try:
            job_ids = request.env['hr.job'].sudo().search([('website_published', '=', True)], order="sequence, create_date desc")

            return [{
                'id': _job.id,
                'title': _job.name or '',
                'department': _job.department_id.name or '',
                'location': _job.address_id.name or '',
                'contract_type': _job.contract_type_id.name or '',
                'recruiter': _job.user_id.name or ''
            } for _job in job_ids]
        except Exception as e:
            _logger.error('Error while fetching positions: %s', str(e))
            return Response(
                json.dumps({'msg': 'Error while fetching positions. Please try again later.'}),
                status=500,
                mimetype='application/json'
            )

    @http.route('/neok-api/position/details', auth="public", csrf=False, methods=['POST'], type='json')
    def neok_api_position_details(self):
        try:
            _data = json.loads(request.httprequest.data)
            job_id = _data.get('job_id', False)

            if not job_id:
                return Response(
                    json.dumps({'msg': 'Position not found.'}),
                    status=404,
                    mimetype='application/json'
                )

            job_id = request.env['hr.job'].sudo().browse(int(job_id))

            if not job_id.exists():
                return Response(
                    json.dumps({'msg': 'Position not found.'}),
                    status=404,
                    mimetype='application/json'
                )
            if not job_id.website_published:
                return Response(
                    json.dumps({'msg': 'Position is closed!'}),
                    status=400,
                    mimetype='application/json'
                )

            return {
                'id': job_id.id,
                'title': job_id.name or '',
                'department': job_id.department_id.name or '',
                'location': job_id.address_id.name or '',
                'contract_type': job_id.contract_type_id.name or '',
                'recruiter': job_id.user_id.name or '',
                'description': job_id.description or '',
            }
        except Exception as e:
            _logger.error('Error while fetching position details: %s', str(e))
            return Response(
                json.dumps({'msg': 'Error while fetching position details. Please try again later.'}),
                status=500,
                mimetype='application/json'
            )

    @http.route('/neok-api/position/apply', auth="public", csrf=False, methods=['POST'], type='json')
    def neok_api_position_apply(self):
        try:
            vals = {}
            _data = json.loads(request.httprequest.data)

            # check if applied job exists and open
            job_id = _data.get('job_id', False)

            if not job_id:
                return Response(
                    json.dumps({'msg': 'Position not found.'}),
                    status=404,
                    mimetype='application/json'
                )

            job_id = request.env['hr.job'].sudo().browse(int(job_id))

            if not job_id.exists():
                return Response(
                    json.dumps({'msg': 'Position not found.'}),
                    status=404,
                    mimetype='application/json'
                )
            if not job_id.website_published:
                return Response(
                    json.dumps({'msg': 'Position is closed!'}),
                    status=400,
                    mimetype='application/json'
                )

            # get required fields
            for key, value in _data.items():
                if key in ['partner_name', 'email_from', 'partner_phone', 'description']:
                    if not value or (value == ''):
                        raise ValidationError(_('Please fill all the required fields.'))

                    vals[key] = value

            # set job related fields
            vals['job_id'] = job_id.id
            vals['name'] = '{0}\'s application for {1}'.format(vals['partner_name'], job_id.name)

            # get optional fields
            linkedin_profile = _data.get('linkedin_profile', False)
            source_id = _data.get('source', False)

            if linkedin_profile:
                vals['linkedin_profile'] = linkedin_profile
            if source_id:
                source_id = request.env['utm.source'].sudo().search([('name', 'ilike', source_id)], limit=1)

                if source_id.exists():
                    vals['source_id'] = source_id.id

            request.env['hr.applicant'].sudo().create(vals)
        except Exception as e:
            _logger.error('Error while applying for a position: %s', str(e))
            return Response(
                json.dumps({'msg': 'Error while applying for the position. Please try again later.'}),
                status=500,
                mimetype='application/json'
            )

        return Response(
            json.dumps({'msg': 'Sent. Thank you! We will get back to you soon.'}),
            status=200,
            mimetype='application/json'
        )
