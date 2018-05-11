from graphs.utils import is_mobile_app_user_agent


def test_is_android_app():
    assert is_mobile_app_user_agent('starwars/2.9.6 (Android: 24)') is True
    assert is_mobile_app_user_agent('terraria/2.9.5 (Android: 24)') is True
    assert is_mobile_app_user_agent('gta/2.9.6 (Android: 27)') is True
    assert is_mobile_app_user_agent('foobar/2.9.6 (Android: 27)') is True

    assert is_mobile_app_user_agent('Mozilla/5.0 (Linux; Android 7.0; LG-K550 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36') is False


def test_is_ios_app():
    assert is_mobile_app_user_agent('FandomEnterpriseApp/1.5.5 (iPhone; iOS 11.2; Scale/2.00)') is True
    assert is_mobile_app_user_agent('foobar/2.9 (iPhone; iOS 11.4; Scale/2.00)') is True
    assert is_mobile_app_user_agent('Fallout 4/2.10 (iPhone; iOS 11.2; Scale/2.00)') is True

    assert is_mobile_app_user_agent('Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 YJApp-IOS jp.co.yahoo.ipn.appli/4.9.4') is False
