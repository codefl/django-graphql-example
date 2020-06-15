import graphene
from graphene.relay import ClientIDMutation
from graphql_relay import from_global_id
from ..types.response_types import CategoryResponseType
from ...common.common_types import ErrorType
from ....product.models import CategoryModel
from graphql_jwt.decorators import staff_member_required


class CategoryCreateInput(graphene.InputObjectType):
    name = graphene.String()


class CategoryUpdateInput(graphene.InputObjectType):
    name = graphene.String()


class CreateCategoryMutation(ClientIDMutation):

    class Arguments:
        category_data = graphene.Argument(CategoryCreateInput, required=True)
        parent_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    response = graphene.Field(CategoryResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, parent_id, category_data):
        parent_id = from_global_id(parent_id)[1]
        cnt = CategoryModel.objects.filter(name__exact=category_data.name).count()
        if cnt > 0:
            r = ErrorType(error_code="DUPLICATE_CATEGORY",
                          error_message="Category with name {} already exists".format(category_data.name))

            return CreateCategoryMutation(ok=False, response=r)

        parent = None
        if parent_id is not None:
            try:
                parent = CategoryModel.objects.get(pk=parent_id)
            except CategoryModel.DoesNotExist:
                r = ErrorType(error_code="PARENT_CATEGORY_NOT_EXIST",
                              error_message="Parent category {} does not exists".format(parent_id))

        c = CategoryModel(name=category_data.name, parent=parent)
        c.save()
        return CreateCategoryMutation(ok=True, response=c)


class UpdateCategoryMutation(ClientIDMutation):

    class Input:
        category_id = graphene.ID(required=True)
        category_data = graphene.Argument(CategoryUpdateInput, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(CategoryResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, category_id, category_data):
        category_id = from_global_id(category_id)[1]
        if category_data.name is not None:
            cnt = CategoryModel.objects.filter(name__exact=category_data.name).count()
            if cnt > 0:
                r = ErrorType(error_code="DUPLICATE_CATEGORY",
                              error_message="Category with name {} already exists".format(category_data.name))

                return UpdateCategoryMutation(ok=False, response=r)

        try:
            c = CategoryModel.objects.get(pk=category_id)
            if category_data.name is not None:
                c.name = category_data.name
            c.save()
            return UpdateCategoryMutation(ok=True, response=c)
        except CategoryModel.DoesNotExist:
            r = ErrorType(error_code="CATEGORY_NOT_EXIST",
                          error_message="Category {} does not exist".format(category_id))

            return UpdateCategoryMutation(ok=False, response=r)


class DeleteCategoryMutation(ClientIDMutation):

    class Arguments:
        category_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    response = graphene.Field(CategoryResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, category_id):
        try:
            category_id = from_global_id(category_id)[1]
            c = CategoryModel.objects.get(pk=category_id)
            c.delete()
            c.id = category_id
            return DeleteCategoryMutation(ok=True, response=c)
        except CategoryModel.DoesNotExist:
            r = ErrorType(error_code="CATEGORY_NOT_EXIST",
                          error_message="Category {} does not exist".format(category_id))

            return DeleteCategoryMutation(ok=False, response=r)
