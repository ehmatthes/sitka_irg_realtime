import pytest

from django.contrib.auth.models import AnonymousUser

from irg_viz import views

from accounts.models import CustomUser

from make_groups import build_all_groups
from make_sample_users import make_sample_users


# --- Tests for anonymous viewers ---

# Make sure site is available, and actual data is unavailable.

def test_anonymous_available(rf):
    """Test that anonymous users do see an index page.
    - See appropriate message.
    Test they don't see sensitive data.
    - No image.
    - No admin tools.

    Note: This may fail, because response.content.decode() sometimes
      breaks lines up in unexpected ways.
    """

    request = rf.get('/')
    request.user = AnonymousUser()
    response = views.index(request)

    assert response.status_code == 200

    response_text = response.content.decode()

    # Make assertions about what should be on anonymous page.
    required_strings = [
        "This is an experimental project",
        "you must be logged in",
    ]
    for s in required_strings:
        assert s in response_text

    # Make assertions about regular user content that shouldn't be on
    #   anonymous page.
    regular_user_strings = [
        'When are we most at risk for landslides',
        'The red shaded region represents',
        'Log out',
        'Data source',
        'plot_images/irg_critical_forecast_plot_current_extended.png',
    ]

    for s in regular_user_strings:
        assert s not in response_text

    # Make asserts about admin content that shouldn't be on
    #   anonymous page.
    admin_strings = [
        'Admin Tools',
        'Create new notification',
        'Invite a new user',
    ]

    for s in admin_strings:
        assert s not in response_text


# --- Tests for regular users ---

# Make sure site is available, and actual data is available.

@pytest.mark.django_db
def test_index_regular_user(rf):
    """Test that regular users see the content they're supposed to see.
    - Main text
    - plot image
    Test that they don't see admin data.
    - text of admin links.
    """
    build_all_groups()
    make_sample_users()
    regular_user = CustomUser.objects.get(username='sample_user')

    request = rf.get('/')
    request.user = regular_user
    response = views.index(request)

    assert response.status_code == 200

    response_text = response.content.decode()

    # Make assertions about content that should be available to a regular
    #   user.
    regular_user_strings = [
        'When are we most at risk for landslides',
        'The red shaded region represents',
        'Log out',
        'Data source',
        'plot_images/irg_critical_forecast_plot_current_extended.png',
    ]

    for s in regular_user_strings:
        assert s in response_text

    # Make asserts about admin content that shouldn't be available to a
    #   regular user.
    admin_strings = [
        'Admin Tools',
        'Create new notification',
        'Invite a new user',
    ]

    for s in admin_strings:
        assert s not in response_text

@pytest.mark.skip
def test_index_plot():
    """Test that the main plot on the index page is correct.
    """
    pass


# --- Tests for admin users ---

# Make sure site is available, and admin links are available.

@pytest.mark.django_db
def test_index_admin_user(rf):
    """Test that admin users see the content they're supposed to see.
    - Main text
    - plot image
    - text of admin links
    """
    build_all_groups()
    make_sample_users()
    admin_user = CustomUser.objects.get(username='sample_admin')

    request = rf.get('/')
    request.user = admin_user
    response = views.index(request)

    assert response.status_code == 200

    response_text = response.content.decode()

    # Make assertions about content that should be available to an admin
    #   user. They should be able to see all regular user content.
    regular_user_strings = [
        'When are we most at risk for landslides',
        'The red shaded region represents',
        'Log out',
        'Data source',
        'plot_images/irg_critical_forecast_plot_current_extended.png',
    ]

    for s in regular_user_strings:
        assert s in response_text

    # Make asserts about admin content that shouldn't be available to a
    #   regular user.
    admin_strings = [
        'Admin Tools',
        'Create new notification',
        'Invite a new user',
    ]

    for s in admin_strings:
        assert s in response_text