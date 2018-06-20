import graphene
from datetime import datetime

from graphene_django.types import DjangoObjectType

from .models import FooBar as FooBarModel


class FooBar(DjangoObjectType):
    class Meta:
        model = FooBarModel


class AllFoobarsQuery(graphene.ObjectType):
    all_foobars = graphene.List(FooBar)

    def resolve_all_foobars(self, info, **kwargs):
        return FooBarModel.objects.all()


class FoobarQuery(graphene.ObjectType):
    foobar = graphene.Field(FooBar, name=graphene.String())

    def resolve_foobar(self, info, name):
        return FooBarModel.objects.get(name=name)


class IntroduceFoobar(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    foobar = graphene.Field(FooBar)

    def mutate(self, info, name):
        foobar = FooBarModel(name=name)
        foobar.save()
        return IntroduceFoobar(foobar=foobar, ok=True)


class TouchFoobar(graphene.Mutation):
    class Arguments:
        uid = graphene.String()

    ok = graphene.Boolean()
    foobar = graphene.Field(FooBar)

    def mutate(self, info, uid):
        foobar = FooBarModel.objects.get(id=uid)
        foobar.updated_at = datetime.now()
        foobar.save()
        return IntroduceFoobar(foobar=foobar, ok=True)


# Combine multiple query objects into a single one to expose them all
class Queries(AllFoobarsQuery, FoobarQuery):
    pass


class Mutations(graphene.ObjectType):
    introduce_foobar = IntroduceFoobar.Field()
    touch_foobar = TouchFoobar.Field()


schema = graphene.Schema(query=Queries, mutation=Mutations)
