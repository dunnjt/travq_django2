import graphene
from graphene_django import DjangoObjectType

from .models import User, Question, Answer, Tag, Skill, Badge


class UserType(DjangoObjectType):
    class Meta:
        model = User

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer

class SkillType(DjangoObjectType):
    class Meta:
        model = Skill

class BadgeType(DjangoObjectType):
    class Meta:
        model = Badge

class TagType(DjangoObjectType):
    class Meta:
        model = Tag

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.String())
    question = graphene.Field(QuestionType, id=graphene.String())
    all_questions = graphene.List(QuestionType)
    answer = graphene.Field(AnswerType, id=graphene.String())
    tag = graphene.List(TagType)
    badge = graphene.List(BadgeType)
    skill = graphene.List(SkillType)

    def resolve_user(self, info, id, **kwargs):
        return User.objects.get(id=id)

    def resolve_question(self, info, id, **kwargs):
        return Question.objects.get(id=id)

    def resolve_all_questions(self, info, **kwards):
        return Question.objects.all()

    def resolve_tag(self, info, **kwargs):
        return Tag.objects.all()

    def resolve_answer(self, info, id, **kwargs):
        return Answer.objects.get(id=id)

    def resolve_skill(self, info, **kwargs):
        return Skill.objects.all()

    def resolve_badge(self, info, **kwargs):
        return Badge.objects.all()


class CreateUser(graphene.Mutation):
    id = graphene.String()
    name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    points = graphene.String()
    skills = graphene.List(graphene.String)
    badge = graphene.List(graphene.String)

    #2
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()
        skills = graphene.List(graphene.String)
        points = graphene.Int()
        badge = graphene.List(graphene.String)

    #3
    def mutate(self, info, name, email, password, skills, points, badge):
        user = User(
            name=name,
            email=email,
            password=password,
            points=points
            )
        user.save()

        for s in skills:
            temp = Skill(skill=s)
            temp.save()
            user.skills.add(temp)
            user.save()

        for b in badge:
            temp = Badge(badge=b)
            temp.save()
            user.badge.add(temp)
            user.save()

        return CreateUser(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            skills=user.skills,
            points=user.points
        )

class CreateAnswer(graphene.Mutation):
    id = graphene.Int()
    user = graphene.String()
    votes = graphene.Int()
    createdOn = graphene.Date()
    answer = graphene.String()

    #2
    class Arguments:
        votes = graphene.Int()
        answer = graphene.String()
        user = graphene.String()
        question = graphene.String()

    #3
    def mutate(self, info, answer, votes, user, question):
        u = User.objects.get(id=user)
        q = Question.objects.get(id=question)
        answer = Answer(
            answer=answer,
            votes=votes,
            user=u,
            question=q
            )
        answer.save()

        return CreateAnswer(
            id=answer.id,
        )

class CreateVote(graphene.Mutation):
    id=graphene.Int()
    vote=graphene.Int()

    class Arguments:
        vote = graphene.Int()
        id = graphene.Int()

    def mutate(self, info, id, vote):
        answer = Answer.objects.get(id=id)
        answer.votes+=vote
        answer.save()

        return CreateVote(
            id=answer.id
        )

class CreateLogon(graphene.Mutation):
    id=graphene.String()
    password=graphene.String()
    email=graphene.String()

    class Arguments:
        password=graphene.String()
        email=graphene.String()

    def mutate(self, info, password, email):
        user = User.objects.get(password=password, email=email)

        return CreateLogon(
            id=user.id
        )


class CreateQuestion(graphene.Mutation):
    id = graphene.Int()
    user = graphene.String()
    question = graphene.String()
    tags = graphene.List(graphene.String)
    createdOn = graphene.Date()

    #2
    class Arguments:
        question = graphene.String()
        tags = graphene.List(graphene.String)
        user = graphene.String()

    #3
    def mutate(self, info, question, tags, user):
        u = User.objects.get(id=user)
        question = Question(
            question=question,
            user=u
            )
        question.save()

        for t in tags:
            temp = Tag(tag=t)
            temp.save()
            question.tag.add(temp)
            question.save()

        return CreateQuestion(
            id=question.id,
            createdOn=question.createdOn
        )

class CreateSkill(graphene.Mutation):
    id = graphene.Int()
    user = graphene.String()
    skill = graphene.String()

    #2
    class Arguments:
        user = graphene.String()
        skill = graphene.String()

    #3
    def mutate(self, info, user, skill):
        skill = Skill(
            skill=skill,
            user=user
            )
        skill.save()

        return CreateSkill(
            id=skill.id,
        )

class CreateBadge(graphene.Mutation):
    id = graphene.Int()
    user = graphene.String()
    badge = graphene.String()

    #2
    class Arguments:
        user = graphene.String()
        badge = graphene.String()

    #3
    def mutate(self, info, user, badge):
        skill = Skill(
            skill=badge,
            user=user
            )
        badge.save()

        return CreateBadge(
            id=badge.id,
        )

class CreateTag(graphene.Mutation):
    id = graphene.Int()
    tag = graphene.String()

    #2
    class Arguments:
        tag = graphene.String()

    #3
    def mutate(self, info, tag):
        tag = Tag(
            tag=tag
            )
        tag.save()

        return CreateTag(
            id=tag.id,
        )

#4
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_question = CreateQuestion.Field()
    create_answer = CreateAnswer.Field()
    create_skill = CreateSkill.Field()
    create_badge = CreateBadge.Field()
    create_tag = CreateTag.Field()
    create_vote = CreateVote.Field()
    create_logon = CreateLogon.Field()
