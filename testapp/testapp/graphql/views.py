from graphene_django.views import GraphQLView
from .context import GQLContext


class CustomGraphQLView(GraphQLView):

    def get_context(self, request):
        context = super().get_context(request)
        setattr(context, 'appcontext', GQLContext(request))
        return context
