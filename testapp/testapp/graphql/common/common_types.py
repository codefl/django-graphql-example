import graphene


class ErrorType(graphene.ObjectType):
    error_code = graphene.String()
    error_message = graphene.String()
