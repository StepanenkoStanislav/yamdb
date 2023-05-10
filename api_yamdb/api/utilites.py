from django.template.loader import render_to_string
from django.core.signing import Signer
from django.db.models import Avg
from rest_framework.generics import get_object_or_404

from yamdb.models import Title

signer = Signer()


def send_confirm_code(user):
    context = {
        'user': user,
        'sign': signer.sign(user.username),
    }
    subject = render_to_string(
        'email/confirmation_code_subject.txt',
        context,
    )
    body = render_to_string(
        'email/confirmation_code_body.txt',
        context,
    )

    user.email_user(subject, body)


def update_title_rating(title_id):
    title = Title.objects.filter(id=title_id)
    if not title.exists():
        return
    title = title[0]
    rating = int(title.reviews.aggregate(Avg("score"))['score__avg'])
    title.rating = rating if rating > 0 else None
    title.save()


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['request'].parser_context[
            'kwargs']['title_id']
        title = get_object_or_404(Title, id=title_id)
        return title

    def __repr__(self):
        return '%s()' % self.__class__.__name__
