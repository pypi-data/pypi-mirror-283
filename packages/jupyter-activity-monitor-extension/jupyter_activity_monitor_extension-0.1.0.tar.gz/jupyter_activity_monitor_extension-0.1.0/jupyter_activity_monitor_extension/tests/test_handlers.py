import json
import pytest


@pytest.fixture
def jp_server_config(jp_template_dir):
    return {
        "ServerApp": {
            "jpserver_extensions": {"jupyter_activity_monitor_extension": True}
        },
    }


async def test_get_without_sessions_and_terminal(jp_fetch):
    response = await jp_fetch("api", "idle", method="GET")

    assert response.code == 200


# TODO: Write tests for get with sessions and terminals mocked.
