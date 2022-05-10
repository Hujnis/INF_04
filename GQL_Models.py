import graphene
from requests import session
from sqlalchemy import extract

from Alfa import BlockModel, FormModel, ItemModel, SectionModel

from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from fastapi import FastAPI

class FormGQL(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    
    sections = graphene.List(lambda: SectionGQL)
    def resolve_section(children,info):
        return children.sections


class SectionGQL(graphene.ObjectType): 
    id = graphene.ID()
    name = graphene.String()
    
    form = graphene.Field(lambda: FormGQL)
    def resolve_form(parent, info):
        return parent.form

    blocks = graphene.List(lambda: BlockGQL)
    def resolve_block(children, info):
        return children.blocks


class BlockGQL(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    section = graphene.Field(lambda: SectionGQL)
    def resolve_section(parent, info):
        return parent.section

    items = graphene.List(lambda: ItemGQL)
    def resolve_item(children, info):
        return children.items


class ItemGQL(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    block = graphene.Field(lambda: BlockGQL)
    def resolve_block(parent,info):
        return parent.block


class QueryGQL():
    form = graphene.Field(FormGQL, id=graphene.ID(required=True))
    section = graphene.Field(SectionGQL, id=graphene.ID(required=True))
    block = graphene.Field(BlockGQL, id=graphene.ID(required=True))
    item = graphene.Field(ItemGQL, id=graphene.ID(required=True))

    def resolve_form(root, info, id):
        session = extractSession(info)
        result = session.query(FormModel).filter(FormModel.id == id).first()
        return result

    def resolve_section(root, info, id):
        session = extractSession(info)
        result = session.query(SectionModel).filter(SectionModel.id==id).first()
        return result    

    def resolve_block(root, info, id):
        session = extractSession(info)
        result = session.query(BlockModel).filter(BlockModel.id==id).first()
        return result
    
    def resolve_item(root, info, id):
        session = extractSession(info)
        result = session.query(ItemModel).filter(ItemModel.id==id).first()
        return result



#connection establishment
dbSessionData = {}

def defineStartupAndShutdown(app, SessionMaker):
    @app.on_event("startup")
    async def startup_event():
        session = SessionMaker()
        dbSessionData['session'] = session

    @app.on_event("shutdown")
    def shutdown_event():
        session = dbSessionData.get('session', None)
        if not session is None:
            session.close()

def extractSession(info):
    session = dbSessionData.get('session', None)
    assert not session is None, 'session is not awailable'
    return session

##########################################
#App
graphql_app = GraphQLApp(
    schema=graphene.Schema(query=QueryGQL), 
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')

defineStartupAndShutdown(app, SessionMaker)

app.add_route('/gql/', graphql_app)
start_api(app=app, port=9992, runNew=True)
###########################################