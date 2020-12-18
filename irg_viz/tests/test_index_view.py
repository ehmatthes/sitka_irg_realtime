from django.contrib.auth.models import AnonymousUser

from irg_viz import views


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