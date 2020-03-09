from flask import request
from flask_restful import Resource

from models import db
from models.link import LinksModel, LinksSchema

link_schema = LinksSchema()
links_schema = LinksSchema(many=True)


class LinksListResource(Resource):
    def get(self):
        links = LinksModel.query.order_by(LinksModel.source_id).all()
        return links_schema.dump(links)

    def post(self):
        new_link = LinksModel(
            source_id=request.json['source_id'],
            target_id=request.json['target_id'],
            source_direction=request.json['source_direction'],
            target_direction=request.json['target_direction']
        )
        db.session.add(new_link)
        db.session.commit()
        return link_schema.dump(new_link)


class LinksResource(Resource):
    def get(self, link_id):
        link = LinksModel.query.get_or_404(link_id)
        return link_schema.dump(link)

    def patch(self, link_id):
        req = request.json
        link = LinksModel.query.get_or_404(link_id)

        if 'source_id' in req:
            link.source_id = req['source_id']

        if 'target_id' in req:
            link.target_id = req['target_id']

        if 'source_direction' in req:
            link.source_direction = req['source_direction']

        if 'target_direction' in req:
            link.target_direction = req['target_direction']

        db.session.commit()
        return link_schema.dump(link)

    def delete(self, link_id):
        link = LinksModel.query.get_or_404(link_id)
        db.session.delete(link)
        db.session.commit()
        return '', 204
