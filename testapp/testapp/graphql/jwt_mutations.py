import graphene
import graphql_jwt


class UserType(graphene.ObjectType):
    user_id = graphene.Field(graphene.String, required=True)
    first_name = graphene.Field(graphene.String)
    last_name = graphene.Field(graphene.String)
    email = graphene.Field(graphene.String, required=True)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType, required=True)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        _user = info.context.user
        user = UserType(user_id=_user.id, first_name=_user.first_name,
                        last_name=_user.last_name, email=_user.email)
        return cls(user=user)


class JwtMutations(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
