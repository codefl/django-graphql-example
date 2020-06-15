import graphene
from graphene.relay import ClientIDMutation
from graphql_relay import from_global_id
from ..types.response_types import TagResponseType
from ...common.common_types import ErrorType
from ....product.models import TagModel, ProductModel
from graphql_jwt.decorators import staff_member_required


class TagCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()


class TagUpdateInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()


class CreateTagMutation(ClientIDMutation):

    class Input:
        tag_data = graphene.Argument(TagCreateInput, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(TagResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, tag_data):
        cnt = TagModel.objects.filter(name__exact=tag_data.name).count()
        if cnt > 0:
            r = ErrorType(error_code="DUPLICATE_TAG",
                          error_message="Tag with name {} already exists".format(tag_data.name))
            return CreateTagMutation(ok=False, response=r)

        c = TagModel(name=tag_data.name, description=tag_data.description)
        c.save()
        return CreateTagMutation(ok=True, response=c)


class UpdateTagMutation(ClientIDMutation):

    class Arguments:
        tag_id = graphene.ID(required=True)
        tag_data = graphene.Argument(TagUpdateInput, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(TagResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, tag_id, tag_data):
        tag_id = from_global_id(tag_id)[1]
        if tag_data.name is not None:
            cnt = TagModel.objects.filter(name__exact=tag_data.name).count()
            if cnt > 0:
                r = ErrorType(error_code="DUPLICATE_TAG",
                              error_message="Tag with name {} already exists".format(tag_name))
                return UpdateTagMutation(ok=False, response=r)

        try:
            c = TagModel.objects.get(pk=tag_id)
            if tag_data.name is not None:
                c.name = tag_data.name
            if tag_data.description is not None:
                c.description = tag_data.description
            c.save()

            return UpdateTagMutation(ok=True, response=c)
        except TagModel.DoesNotExist:
            r = ErrorType(error_code="TAG_NOT_EXIST",
                          error_message="Tag {} does not exist".format(tag_id))
            return UpdateTagMutation(ok=False, response=r)


class DeleteTagMutation(ClientIDMutation):

    class Input:
        tag_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    response = graphene.Field(TagResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, tag_id):
        try:
            tag_id = from_global_id(tag_id)[1]
            cnt = ProductModel.objects.filter(tags__id=tag_id).count()
            if cnt > 0:
                r = ErrorType(error_code="TAG_IN_USE",
                              error_message="Tag {} still in use. Cannot delete.".format(tag_id))
                return DeleteTagMutation(ok=False, response=r)

            c = TagModel.objects.get(pk=tag_id)
            c.delete()
            c.id = tag_id
            return DeleteTagMutation(ok=True, response=c)
        except TagModel.DoesNotExist:
            r = ErrorType(error_code="TAG_NOT_EXIST",
                          error_message="Tag {} does not exist".format(tag_id))
            return DeleteTagMutation(ok=False, response=r)
