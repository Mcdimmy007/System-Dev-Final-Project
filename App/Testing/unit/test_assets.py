from unittest.mock import Mock
from app import compile_static_assets

def test_compile_static_assets():
    app = Mock()
    compile_static_assets(app)

    # Check that the assets are registered
    assert "account_less_bundle" in app.jinja_env.assets_environment
    assert "dashboard_less_bundle" in app.jinja_env.assets_environment
    assert "js_all" in app.jinja_env.assets_environment

    # Check that the bundles are built
    assert app.jinja_env.assets_environment["account_less_bundle"].urls()[0].endswith("dist/css/account.css")
    assert app.jinja_env.assets_environment["dashboard_less_bundle"].urls()[0].endswith("dist/css/dashboard.css")
    assert app.jinja_env.assets_environment["js_all"].urls()[0].endswith("dist/js/main.min.js")
