import graphene

import communitymanager_3.members.schema as MembersSchema


class Query(MembersSchema.Query, graphene.ObjectType):
    pass


class Mutation(MembersSchema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
