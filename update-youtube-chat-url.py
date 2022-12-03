# Copyright(c) Susko3 <susko3@protonmail.com>. Licensed under the MIT Licence.
# See the LICENCE file in the repository root for full licence text.

from datetime import datetime

import obspython as obs


def debug(*args):
    # print(*args)
    ...


PROPERTIES_YOUTUBE_VIDEO_URL = "url"
PROPERTIES_INFO_LOGS = "logs"
PROPERTIES_UPDATE_BUTTON = "update_button"
PROPERTIES_UPDATE_BUTTON_TEXT = "Update sources"

YOUTUBE_VIDEO_ID_LENGTH = 11

properties_youtube_video_url = ""

log_text = LOG_INITIAL_TEXT = f"""
Ready. Click `{PROPERTIES_UPDATE_BUTTON_TEXT}` to update.
""".lstrip()


def reset_log():
    global log_text
    log_text = ""


def log(text: str = '', print_date: bool=False):
    global log_text
    print(text)

    if print_date:
        log_text += f"[{datetime.now().strftime('%H:%M:%S')}] "

    log_text += text + '\n'


def script_description():
    return "Updates all YouTube chat browser sources to match the specified URL"


def is_valid_video_id(id: str) -> bool:
    if len(id) != YOUTUBE_VIDEO_ID_LENGTH:
        return False

    VALID_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXZYabcdefghijklmnopqrstuvwxyz-_"
    return all(c in VALID_CHARS for c in id)


URL_HELP_TEXT = """
ℹ YouTube video ID or URL copied from the livestream,
creator dashboard, or chat poput.

✅ Accepted formats:
- jfKfPfyJRdk
- https://youtu.be/dQw4w9WgXcQ
- https://www.youtube.com/watch?v=dQw4w9WgXcQ
- https://www.youtube.com/live_chat?is_popout=1&v=jfKfPfyJRdk
- https://studio.youtube.com/video/jfKfPfyJRdk/edit
- https://studio.youtube.com/video/jfKfPfyJRdk/livestreaming
""".strip()


def parse_video_id(url: str) -> str | None:
    """
    Parses a youtube video ID from a youtube live URL.
    """

    if is_valid_video_id(url):
        return url

    for prefix in "youtu.be/", "watch?v=", "studio.youtube.com/video/", "youtube.com/live_chat?is_popout=1&v=":
        if (index := url.find(prefix)) != -1:
            if is_valid_video_id(id := url[index + len(prefix):][:YOUTUBE_VIDEO_ID_LENGTH]):
                return id

    return None


"https://www.youtube.com/live_chat?is_popout=1&v=nSDdBKp_nF0"


YOUTUBE_LIVE_CHAT_URL_PREFIX = "https://www.youtube.com/live_chat"

BROWSER_SOURCE_SETTING_URL = "url"


def update_browser_url(browser_source, youtube_live_video_id) -> tuple[bool, str, str]:
    """
    Returns: (success, name, new_url)
    https://www.youtube.com/live_chat?is_popout=1&v=_HyYrpy6hM4
    """

    settings = obs.obs_source_get_settings(browser_source)
    url = obs.obs_data_get_string(settings, BROWSER_SOURCE_SETTING_URL)

    if not url.startswith(YOUTUBE_LIVE_CHAT_URL_PREFIX):
        return False, None, None

    # index of video id moniker
    index = url.find("&v=")

    if index == -1:
        index = url.find("?v=")

    if index == -1:
        log(f"⚠ Failed to find youtube video ID in url '{url}' of source '{obs.obs_source_get_name(browser_source)}'")
        return False, None, None

    url = url[:index + 3] + youtube_live_video_id + url[index + 3 + YOUTUBE_VIDEO_ID_LENGTH:]

    obs.obs_data_set_string(settings, BROWSER_SOURCE_SETTING_URL, url)
    obs.obs_source_update(browser_source, settings)

    return True, obs.obs_source_get_name(browser_source), url


def update_all_chat_browser_sources():
    youtube_live_video_id = parse_video_id(properties_youtube_video_url)

    reset_log()

    if not youtube_live_video_id:
        log(f"⚠️ YouTube live video ID not valid: {properties_youtube_video_url}", True)
        return

    print("update_all_chat_browser_sources", youtube_live_video_id)

    sources = obs.obs_enum_sources()
    if sources is None:
        return

    log('✅ Updated sources:  (Name – New URL)', True)

    for source in sources:
        if obs.obs_source_get_id(source) == "browser_source":
            success, name, new_url = update_browser_url(source, youtube_live_video_id)
            if success:
                log(f'"{name}" – {new_url}')


def on_update_button(props, prop):
    global log_text

    update_all_chat_browser_sources()
    obs.obs_property_set_long_description(obs.obs_properties_get(props, PROPERTIES_INFO_LOGS), log_text)
    return True


def on_url_changed(props, property, settings):
    debug("on_url_changed")
    return check_update_button_enabled(obs.obs_properties_get(props, PROPERTIES_UPDATE_BUTTON))


def check_update_button_enabled(update_button):
    global properties_youtube_video_url

    debug(f"check_update_button_enabled({repr(properties_youtube_video_url)})")

    was_valid = obs.obs_property_enabled(update_button)
    is_valid = parse_video_id(properties_youtube_video_url) is not None

    if was_valid != is_valid:
        obs.obs_property_set_enabled(update_button, is_valid)
        obs.obs_property_set_long_description(update_button, None if is_valid else "URL not valid.")
        print("is valid", is_valid, "button", update_button)
        return True

    return False


def script_defaults(settings):
    debug("script_defaults")
    obs.obs_data_set_default_string(settings, PROPERTIES_YOUTUBE_VIDEO_URL, "")
    obs.obs_data_set_default_string(settings, PROPERTIES_INFO_LOGS, "")


# cleanup_func = None

def script_update(settings):
    global properties_youtube_video_url

    debug("script_update")
    properties_youtube_video_url = obs.obs_data_get_string(settings, PROPERTIES_YOUTUBE_VIDEO_URL)


def script_properties():
    debug("script_properties")
    props = obs.obs_properties_create()

    url = obs.obs_properties_add_text(props, PROPERTIES_YOUTUBE_VIDEO_URL, "URL", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(url, URL_HELP_TEXT)
    update_button = obs.obs_properties_add_button(
        props, PROPERTIES_UPDATE_BUTTON, PROPERTIES_UPDATE_BUTTON_TEXT, on_update_button)
    check_update_button_enabled(update_button)

    logs = obs.obs_properties_add_text(props, PROPERTIES_INFO_LOGS, "Info", obs.OBS_TEXT_INFO)
    obs.obs_property_set_description(logs, "Info: ")
    obs.obs_property_set_long_description(logs, LOG_INITIAL_TEXT)

    obs.obs_property_set_modified_callback(url, on_url_changed)

    return props


def script_unload():
    debug("script_unload")
#     global cleanup_func
#     if cleanup_func is not None:
#         cleanup_func()
