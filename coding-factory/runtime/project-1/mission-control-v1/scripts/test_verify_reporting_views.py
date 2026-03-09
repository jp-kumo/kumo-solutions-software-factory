#!/usr/bin/env python3

from verify_reporting_views import REQUIRED_VIEWS


def test_required_views_list():
    assert "vw_project_summary" in REQUIRED_VIEWS
    assert "vw_owner_decisions" in REQUIRED_VIEWS
    assert len(REQUIRED_VIEWS) == 6
