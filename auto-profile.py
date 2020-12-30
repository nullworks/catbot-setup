#!/usr/bin/env python3

# This script automatically sets community profile pictures for bots.
# You do not have to "set up" a steam profile on each account for this to work, evidently.
# Simply copy your accounts.txt and bot-profile.jpg here and run: ./auto-profile.py
# Image format can be PNG, this script just expects the filename to be .jpg

# Make sure you install dependencies first:
# pip3 install -U steam[client]

import steam.client
import json

f = open('accounts.txt', 'r')
data = f.read()
f.close()

data = data.replace('\r\n', '\n')
accounts = data.split('\n')
accounts.remove('')
profile = open('bot-profile.jpg', 'rb')

enable_debugging = False
enable_extra_info = False
dump_response = False

def debug(message):
    if enable_debugging:
        print(message)

def extra(message):
    if enable_extra_info:
        print(message)

for index, account in enumerate(accounts):
    username, password = account.split(':')
    print(f'Logging in as user #{index + 1}/{len(accounts)} ({username})...')

    client = steam.client.SteamClient()
    eresult = client.login(username, password=password)
    status = 'OK' if eresult == 1 else 'FAIL'
    print(f'Login status: {status} ({eresult})')
    if status == 'FAIL':
        raise RuntimeError('Login failed; bailing out. See https://steam.readthedocs.io/en/stable/api/steam.enums.html#steam.enums.common.EResult for the relevant error code.')

    print(f'Logged on as: {client.user.name}')
    print(f'Community profile: {client.steam_id.community_url}')
    extra(f'Last logon (UTC): {client.user.last_logon}')
    extra(f'Last logoff (UTC): {client.user.last_logoff}')

    print('Getting web_session...')
    session = client.get_web_session()
    debug(f'session.cookies: {session.cookies}')

    url = 'https://steamcommunity.com/actions/FileUploader'
    id64 = client.steam_id.as_64 # type int
    data = {
        'MAX_FILE_SIZE': '1048576',
        'type': 'player_avatar_image',
        'sId': f'{id64}',
        'sessionid': session.cookies.get('sessionid', domain='steamcommunity.com'),
        'doSub': '1',
    }
    post_cookies = {
        'steamLogin': session.cookies.get('steamLogin', domain='steamcommunity.com'),
        'steamLoginSecure': session.cookies.get('steamLoginSecure', domain='steamcommunity.com'),
        'sessionid': session.cookies.get('sessionid', domain='steamcommunity.com')
    }
    debug(f'post_cookies: {post_cookies}')

    print('Setting profile picture...')

    r = session.post(url=url, params={'type': 'player_avatar_image', 'sId':str(id64)}, files={'avatar': profile}, data=data, cookies=post_cookies)
    content = r.content.decode('ascii')
    if dump_response: print(f'response: {content}')
    if not content.startswith('<!DOCTYPE html'):
        response = json.loads(content)
        raise RuntimeError(f'Error setting profile: {response["message"]}')

    print('Done; logging out.')
    client.logout()

    # Seek to beginning; reuse file
    profile.seek(0)

    # Spacing between accounts
    print()

profile.close()

print('All done.')
