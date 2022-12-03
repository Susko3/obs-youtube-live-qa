# How to use

1. Install [OBS](https://obsproject.com/)
2. Download this repository by clicking the green `Code` button, and then `Download ZIP`
3. Extract the downloaded `.zip`
4. Follow the steps below for the CSS theme and the script

## CSS theme

1. In the extracted `.zip`, right click on `youtube-live-qa.css` and select `Edit`
2. Select all and copy the CSS
3. In OBS, create a new `Browser` source
4. Set it up with the following recommended defaults:
   - Name: `Live Q&A`
   - URL: `https://www.youtube.com/live_chat?is_popout=1&dark_theme=1&v=jfKfPfyJRdk`
     - Set the video ID to the ID of your livestream, you can use the [Script](#script) below to update this value later
   - Width: `1000`
   - Height: `500`
   - Custom CSS: Paste from `youtube-live-qa.css`

Until you start the Q&A session, the source will be entirely invisible. (Keep in mind that pinned messages might be visible, so it's best to hide the source when not using Live Q&A.)

Advanced usage: You can customise the font and appearance by manually editing the CSS or combining it with [Chat v2.0 Style Generator](https://chatv2.septapus.com/).

## Script

### First-time setup

1. Download and instal the latest version of Python **3.10** from [python.org](https://www.python.org/downloads/)
2. In OBS studio, click on `Tools` &rarr; `Scripts`
3. Navigate to `Python settings`
4. Click on `Browse`
5. For the `Folder`, copy and paste exactly `%localappdata%\Programs\Python\Python310` (if you used the defaults while installing Python)
6. Click on `Select folder`
   - you should see `Loaded Python Version 3.10` in OBS
7. Navigate to `Scripts`
8. Click on the `+` to add a new script
9. Navigate to where you extracted the `.zip` and select `update-youtube-chat-url.py`
10. Select the newly added script `update-youtube-chat-url.py`
11. Paste in your stream URL
    - This URL is only generated once you start streaming, so you can fill it in later
    - Hover over the `(?)` to see what URLs are supported
12. Click on `Update sources` to update all YouTube chat browser sources (the button is disabled if the URL is invalid)
    - When you use `Update sources`, all YouTube chat Browser sources will conveniently update to the new URL (even if they're displaying regular chat and not Live Q&A)

### Subsequent usages

1. In OBS studio, click on `Tools` &rarr; `Scripts`
2. Select the script `update-youtube-chat-url.py`
3. Paste in your stream URL
4. Click on `Update sources`

# Caveats

Doesn't properly work when there is a pinned message in chat. Unpin all messages before starting a Live Q&A session for best results.

