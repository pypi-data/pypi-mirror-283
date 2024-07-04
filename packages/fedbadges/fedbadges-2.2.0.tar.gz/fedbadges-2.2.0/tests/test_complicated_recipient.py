from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fedora_messaging.message import Message

from .utils import get_rule


class MockQuery:
    def count(self):
        return float("inf")  # Master tagger


@pytest.fixture
def user_exists(fasjson_client):
    fasjson_client.get_user.return_value = SimpleNamespace(result={"username": "dummy-user"})


@pytest.fixture
def above_threshold():
    with patch("fedbadges.rules.get_cached_messages_count") as get_cached_messages_count:
        get_cached_messages_count.return_value = float("inf")
        yield


def test_complicated_recipient_real(
    cache_configured,
    rules,
    tahrir_client,
    user_exists,
    above_threshold,
):
    rule = get_rule(rules, "Speak Up!")
    msg = Message(
        topic="org.fedoraproject.prod.meetbot.meeting.complete",
        body={
            "meeting_topic": "testing",
            "attendees": {"fasuser": 2, "threebean": 2},
            "chairs": {},
            "topic": "",
            "url": "fedora-meeting.2013-06-24-19.52",
            "owner": "threebean",
            "channel": "#fedora-meeting",
        },
    )
    assert rule.matches(msg, tahrir_client) == {"fasuser", "threebean"}


def test_complicated_recipient_pagure(
    rules,
    tahrir_client,
    user_exists,
    above_threshold,
):
    rule = get_rule(rules, "Long Life to Pagure (Pagure I)")
    msg = Message(
        topic="io.pagure.prod.pagure.git.receive",
        body={
            "authors": [
                {"fullname": "Pierre-YvesChibon", "name": "pingou"},
                {"fullname": "Lubom\\u00edr Sedl\\u00e1\\u0159", "name": "lsedlar"},
            ],
            "total_commits": 2,
            "start_commit": "da090b8449237e3878d4d1fe56f7f8fcfd13a248",
        },
    )

    assert rule.matches(msg, tahrir_client) == {"pingou", "lsedlar"}
