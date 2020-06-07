import graphene
from ..types.response_types import CategoryResponseType
from ...common.common_types import ErrorType
from ....product.models import CategoryModel


class CategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    parent_id = graphene.ID()


class CreateCategoryMutation(graphene.Mutation):

    class Arguments:
        category_data = graphene.Argument(CategoryInput)

    ok = graphene.Boolean()
    response = graphene.Field(CategoryResponseType)

    @staticmethod
    def mutate(root, info, category_data):
        cnt = CategoryModel.objects.filter(name__exact=category_data.name).count()
        if cnt > 0:
            r = ErrorType(error_code="DUPLICATE_CATEGORY",
                          error_message="Category with name {} already exists".format(category_data.name))

            return CreateCategoryMutation(ok=False, response=r)

        parent = None
        if category_data.parent_id is not None:
            try:
                parent = CategoryModel.objects.get(pk=category_data.parent_id)
            except CategoryModel.DoesNotExist:
                r = ErrorType(error_code="PARENT_CATEGORY_NOT_EXIST",
                              error_message="Parent category {} does not exists".format(category_data.parent_id))

        c = CategoryModel(name=category_data.name, parent=parent)
        c.save()
        return CreateCategoryMutation(ok=True, response=c)


class UpdateCategoryMutation(graphene.Mutation):

    class Arguments:
        category_id = graphene.ID()
        category_name = graphene.Argument(graphene.String, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(CategoryResponseType)

    @staticmethod
    def mutate(root, info, category_id, category_name):
        cnt = CategoryModel.objects.filter(name__exact=category_name).count()
        if cnt > 0:
            r = ErrorType(error_code="DUPLICATE_CATEGORY",
                          error_message="Category with name {} already exists".format(category_name))

            return UpdateCategoryMutation(ok=False, response=r)

        try:
            c = CategoryModel.objects.get(pk=category_id)
            c.name = category_name
            c.save()
            return UpdateCategoryMutation(ok=True, response=c)
        except CategoryModel.DoesNotExist:
            r = ErrorType(error_code="CATEGORY_NOT_EXIST",
                          error_message="Category {} does not exist".format(category_id))

            return UpdateCategoryMutation(ok=False, response=r)


class DeleteCategoryMutation(graphene.Mutation):

    class Arguments:
        category_id = graphene.ID()

    ok = graphene.Boolean()
    response = graphene.Field(CategoryResponseType)

    @staticmethod
    def mutate(root, info, category_id):
        try:
            c = CategoryModel.objects.get(pk=category_id)
            c.delete()
            c.id = category_id
            return DeleteCategoryMutation(ok=True, response=c)
        except CategoryModel.DoesNotExist:
            r = ErrorType(error_code="CATEGORY_NOT_EXIST",
                          error_message="Category {} does not exist".format(category_id))

            return DeleteCategoryMutation(ok=False, response=r)