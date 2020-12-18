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
    """

    request = rf.get('/')
    request.user = AnonymousUser()
    response = views.index(request)

    assert response.status_code == 200
