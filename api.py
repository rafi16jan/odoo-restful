from json import dumps as json
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception
class Api(http.Controller):

    @http.route('/api/restful', type='http', auth='none', csrf=False)
    @serialize_exception
    def restful(self, **post):
        filecontent = {}
        if post.get('login') and post.get('password'):
           if not post.get('database'): #If no database is passed on the ajax post, get one random database
              from odoo.service.db import list_dbs
              post['database'] = list_dbs()[0]
           login = request.session.authenticate(post['database'], post['login'], post['password'])
           if not login: #If login doesn't return uid, return json with status denied
              filecontent['status'] = 'denied'
              return request.make_response(json(filecontent), [('Access-Control-Allow-Origin', '*')])
           filecontent = request.env['res.users'].search([]).read() #If login successful, you can execute functions and access datas
        if not filecontent: #If no data filled in the dict, return error
           filecontent = {'status': 'error'}
        return request.make_response(json(filecontent), [('Access-Control-Allow-Origin', '*')])
