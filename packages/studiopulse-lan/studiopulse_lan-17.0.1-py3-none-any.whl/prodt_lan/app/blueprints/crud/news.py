from prodt_lan.app.models.news import News

from prodt_lan.app.blueprints.crud.base import BaseModelResource, BaseModelsResource


class NewssResource(BaseModelsResource):
    def __init__(self):
        BaseModelsResource.__init__(self, News)


class NewsResource(BaseModelResource):
    def __init__(self):
        BaseModelResource.__init__(self, News)
