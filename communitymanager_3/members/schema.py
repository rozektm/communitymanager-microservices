import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from communitymanager_3.members.models import (
    Community,
    CommunityAttributes,
    Member,
    Membership,
    Metadata,
)


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        interfaces = (relay.Node,)
        filter_fields = ["email", "name", "membership"]


class CreateMember(relay.ClientIDMutation):
    member = graphene.Field(MemberType)

    class Input:
        name = graphene.String()
        email = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        member = Member(name=input.get("name"), email=input.get("email"))
        member.save()
        return CreateMember(member=member)


class UpdateMember(relay.ClientIDMutation):
    member = graphene.Field(MemberType)

    class Input:
        id = graphene.String()
        name = graphene.String()
        email = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        member = Member.objects.get(pk=from_global_id(input.get("id"))[1])
        member.name = input.get("name")
        member.email = input.get("email")
        member.save()
        return UpdateMember(member=member)


class MembershipType(DjangoObjectType):
    class Meta:
        model = Membership
        interfaces = (relay.Node,)
        filter_fields = {
            "community__abreviation": ["exact"],
            "member__email": ["exact", "icontains"],
            "level__value": ["exact"],
        }


class CommunityType(DjangoObjectType):
    class Meta:
        model = Community
        interfaces = (relay.Node,)
        filter_fields = ["name", "abreviation"]


class CreateCommunity(relay.ClientIDMutation):
    community = graphene.Field(CommunityType)

    class Input:
        name = graphene.String()
        abreviation = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        community = Community(
            name=input.get("name"),
            abreviation=input.get("abreviation"),
        )
        community.save()
        return CreateCommunity(community=community)


class UpdateCommunity(relay.ClientIDMutation):
    community = graphene.Field(CommunityType)

    class Input:
        id = graphene.String()
        name = graphene.String()
        abreviation = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        community = Community.objects.get(pk=from_global_id(input.get("id"))[1])
        community.name = input.get("name")
        community.abreviation = input.get("abreviation")
        community.save()
        return UpdateCommunity(community=community)


class CommunityAttributesType(DjangoObjectType):
    class Meta:
        model = CommunityAttributes
        interfaces = (relay.Node,)
        filter_fields = []


class CreateAttribute(relay.ClientIDMutation):
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pass


class UpdateAttribute(relay.ClientIDMutation):
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pass


class MetaDataType(DjangoObjectType):
    class Meta:
        model = Metadata
        interfaces = (relay.Node,)
        filter_fields = []


class CreateMetaData(relay.ClientIDMutation):
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pass


class UpdateMetaData(relay.ClientIDMutation):
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pass


class Query(graphene.ObjectType):
    member = relay.Node.Field(MemberType)
    all_members = DjangoFilterConnectionField(MemberType)

    membership = relay.Node.Field(MembershipType)
    all_memberships = DjangoFilterConnectionField(MembershipType)

    community = relay.Node.Field(CommunityType)
    all_communities = DjangoFilterConnectionField(CommunityType)

    metadata = relay.Node.Field(MetaDataType)
    all_metadatas = DjangoFilterConnectionField(MetaDataType)

    community_attribute = relay.Node.Field(CommunityAttributesType)
    all_community_attributes = DjangoFilterConnectionField(CommunityAttributesType)


class Mutation(graphene.ObjectType):
    create_member = CreateMember.Field()
    update_member = UpdateMember.Field()

    create_community = CreateCommunity.Field()
    update_community = UpdateCommunity.Field()
