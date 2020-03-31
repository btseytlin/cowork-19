import json
import random
import itertools
from uuid import uuid4
from pytest import mark
import uuid

from cowork_site.models import Posting, User


class TestPostingList:
    def test_list_empty(self, client, session):
        assert session.query(Posting).all() == []

        res = client.get('/')
        assert b'<article class="posting-card" id="posting-' not in res.data

    def test_list_many(self, client, session):
        user = User()
        session.add(user)
        session.commit()

        posting_1 = Posting(user=user,
                            name='name',
                            description='description',
                            cv_url='cv_url',
        )

        posting_2 = Posting(user=user,
                            name='name2',
                            description='description',
                            cv_url='cv_url')

        posting_3 = Posting(user=user,
                           name='name2',
                           description='description',
                           cv_url='cv_url',
                           display=False)

        session.add(posting_1)
        session.add(posting_2)
        session.add(posting_3)
        session.commit()

        session.refresh(posting_1)
        session.refresh(posting_2)
        session.refresh(posting_3)

        res = client.get('/')
        assert f'<article class="posting-card" id="posting-{posting_1.id}' in str(res.data)
        assert f'<article class="posting-card" id="posting-{posting_2.id}' in str(res.data)
        assert f'<article class="posting-card" id="posting-{posting_3.id}' not in str(res.data)

    def test_search_name(self, client, session):
        user = User()
        session.add(user)
        session.commit()

        posting_1 = Posting(user=user,
                            name='valid post',
                            description='',
                            cv_url='cv_url',
                            )

        posting_2 = Posting(user=user,
                            name='wtf',
                            description='wtf',
                            cv_url='cv_url')

        posting_3 = Posting(user=user,
                            name='utf8 пост пост',
                            description='',
                            cv_url='cv_url')

        session.add(posting_1)
        session.add(posting_2)
        session.add(posting_3)
        session.commit()

        session.refresh(posting_1)
        session.refresh(posting_2)
        session.refresh(posting_3)

        # search first post
        res = client.get('/?search_string=valid')
        assert f'<article class="posting-card" id="posting-{posting_1.id}' in str(
            res.data)
        assert f'<article class="posting-card" id="posting-{posting_2.id}' not in str(
            res.data)
        assert f'<article class="posting-card" id="posting-{posting_3.id}' not in str(
            res.data)

        # search third post
        res = client.get('/?search_string=пост')
        assert f'<article class="posting-card" id="posting-{posting_1.id}' not in str(
            res.data)
        assert f'<article class="posting-card" id="posting-{posting_2.id}' not in str(
            res.data)
        assert f'<article class="posting-card" id="posting-{posting_3.id}' in str(
            res.data)

