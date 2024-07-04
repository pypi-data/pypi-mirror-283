import logging
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from fedora_messaging.message import Message

from .utils import get_rule


@pytest.fixture
def rule(rules):
    return get_rule(rules, "Junior Tagger (Tagger I)")


@pytest.fixture
def message():
    return Message(
        topic="org.fedoraproject.prod.fedoratagger.tag.create",
    )


def test_complicated_trigger_against_empty(rule, message):
    assert rule.matches(message, Mock(name="tahrir")) == set()


def test_complicated_trigger_against_partial(rule, message):
    message.body = {"user": {}}
    assert rule.matches(message, Mock(name="tahrir")) == set()


def test_complicated_trigger_against_partial_mismatch(rule, message, tahrir_client, caplog):
    caplog.set_level(logging.ERROR)
    message.body = {"user": None}
    assert rule.matches(message, tahrir_client) == set()
    print(caplog.messages)
    print(caplog.text)
    assert len(caplog.messages) == 1


def test_complicated_trigger_against_full_match(rule, message, tahrir_client, fasjson_client):
    message.body = {
        "tag": {
            "dislike": 0,
            "like": 1,
            "package": "mattd",
            "tag": "awesome",
            "total": 1,
            "votes": 1,
        },
        "user": {"anonymous": False, "rank": -1, "username": "ralph", "votes": 4},
        "vote": {
            "like": True,
            "tag": {
                "dislike": 0,
                "like": 1,
                "package": "mattd",
                "tag": "awesome",
                "total": 1,
                "votes": 1,
            },
            "user": {"anonymous": False, "rank": -1, "username": "ralph", "votes": 4},
        },
    }

    # Set up some mock stuff
    class MockQuery:
        def count(self):
            return float("inf")  # Master tagger

    fasjson_client.get_user.return_value = SimpleNamespace(result={"username": "dummy-user"})
    with patch("fedbadges.rules.get_cached_messages_count") as get_cached_messages_count:
        get_cached_messages_count.return_value = float("inf")
        assert rule.matches(message, tahrir_client) == {"ralph"}
