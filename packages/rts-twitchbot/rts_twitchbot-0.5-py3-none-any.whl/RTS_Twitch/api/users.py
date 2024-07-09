from ExtraDecorators import validatetyping
from RTS_Twitch.toolset import paginate, single
from ExtraUtils.validate_dict import validate_dict

@validatetyping
async def get_users_by_id(channel_id:int,user_ids:list)->dict:
    '''Twitch official example response:
{
  "data": [
    {
      "id": "141981764",
      "login": "twitchdev",
      "display_name": "TwitchDev",
      "type": "",
      "broadcaster_type": "partner",
      "description": "Supporting third-party developers building Twitch integrations from chatbots to game integrations.",
      "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png",
      "offline_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png",
      "view_count": 5980557,
      "email": "not-real@email.com",
      "created_at": "2016-12-14T20:32:28Z"
    }
  ]
}
    '''

    if len(user_ids) == 0:
        user_ids = [channel_id]
    if len(user_ids) > 100:
        user_ids = user_ids[:100]
    ids = ""
    for ident in user_ids:
        if isinstance(ident,int):
            ids += f"id={ident}&"
    ids = ids[:-1]
    url= f"https://api.twitch.tv/helix/users?{ids}"
    return await single(channel_id,url)

@validatetyping
async def get_users_by_login(channel_id:int,user_names:list)->dict:
    '''Twitch official example response:
{
  "data": [
    {
      "id": "141981764",
      "login": "twitchdev",
      "display_name": "TwitchDev",
      "type": "",
      "broadcaster_type": "partner",
      "description": "Supporting third-party developers building Twitch integrations from chatbots to game integrations.",
      "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png",
      "offline_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png",
      "view_count": 5980557,
      "email": "not-real@email.com",
      "created_at": "2016-12-14T20:32:28Z"
    }
  ]
}
    '''

    if len(user_ids) == 0:
        return {"error":"not_enough_user_names @users.py(get_users_by_login)"}
    if len(user_ids) > 100:
        user_ids = user_ids[:100]
    login = ""
    for ident in user_ids:
        if isinstance(ident,str):
            login += f"login={ident}&"
    login = login[:-1]
    url= f"https://api.twitch.tv/helix/users?{login}"
    return await single(channel_id,url)

@validatetyping
async def update_user(channel_id:int,description:str)->dict:
    '''Twitch official example response:
{
  "data":[{
    "id": "44322889",
    "login": "dallas",
    "display_name": "dallas",
    "type": "staff",
    "broadcaster_type": "affiliate",
    "description": "BaldAngel",
    "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/4d1f36cbf1f0072d-profile_image-300x300.png",
    "offline_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/dallas-channel_offline_image-2e82c1df2a464df7-1920x1080.jpeg",
    "view_count": 6995,
    "email": "not-real@email.com",
    "created_at": "2013-06-03T19:12:02.580593Z"
  }]
}
    '''
    if len(description) > 300:
        return {"error":"description_too_long > 300 @users.py(update_user)"}
    url= f"https://api.twitch.tv/helix/users?description={description}"
    return await single(channel_id,url,"PUT")

@validatetyping
async def get_user_block_list(channel_id:int)->dict:
    '''Twitch official example response:
    {
  "data": [
    {
      "user_id": "135093069",
      "user_login": "bluelava",
      "display_name": "BlueLava"
    },
    {
      "user_id": "27419011",
      "user_login": "travistyoj",
      "display_name": "TravistyOJ"
    }
  ]
}'''
    url= f"https://api.twitch.tv/helix/users/blocks?broadcaster_id={channel_id}"
    return await paginate(channel_id,url)


@validatetyping
async def block_user(channel_id:int,user_id:int, source_context:str=None, reason:str=None)->dict:
    append = ""
    if source_context in ["chat","whisper"]:
        append = f"&source_context={source_context}"
    if reason in ["spam","harassment","other"]:
        append += f"&reason={reason}"
    url= f"https://api.twitch.tv/helix/users/blocks?broadcaster_id={channel_id}&target_user_id={user_id}"
    return await single(channel_id,url,"PUT")

@validatetyping
async def unblock_user(channel_id:int,user_id:int)->dict:
    url= f"https://api.twitch.tv/helix/users/blocks?broadcaster_id={channel_id}&target_user_id={user_id}"
    return await single(channel_id,url,"DELETE")

@validatetyping
async def get_user_extensions(channel_id:int)->dict:
    '''Twitch official example response:
{
  "data": [
    {
      "id": "wi08ebtatdc7oj83wtl9uxwz807l8b",
      "version": "1.1.8",
      "name": "Streamlabs Leaderboard",
      "can_activate": true,
      "type": [
        "panel"
      ]
    },
    {
      "id": "d4uvtfdr04uq6raoenvj7m86gdk16v",
      "version": "2.0.2",
      "name": "Prime Subscription and Loot Reminder",
      "can_activate": true,
      "type": [
        "overlay"
      ]
    },
    {
      "id": "rh6jq1q334hqc2rr1qlzqbvwlfl3x0",
       "version": "1.1.0",
      "name": "TopClip",
      "can_activate": true,
      "type": [
        "mobile",
        "panel"
      ]
    },
    {
      "id": "zfh2irvx2jb4s60f02jq0ajm8vwgka",
      "version": "1.0.19",
      "name": "Streamlabs",
      "can_activate": true,
      "type": [
        "mobile",
        "overlay"
      ]
    },
    {
      "id": "lqnf3zxk0rv0g7gq92mtmnirjz2cjj",
      "version": "0.0.1",
      "name": "Dev Experience Test",
      "can_activate": true,
      "type": [
        "component",
        "mobile",
        "panel",
        "overlay"
      ]
    }
  ]
}
    '''
    url= f"https://api.twitch.tv/helix/users/extensions/list"
    return await single(channel_id,url)

@validatetyping
async def get_user_active_extensions(channel_id:int)->dict:
    '''Twitch official example response:
{
  "data": {
    "panel": {
      "1": {
        "active": true,
        "id": "rh6jq1q334hqc2rr1qlzqbvwlfl3x0",
        "version": "1.1.0",
        "name": "TopClip"
      },
      "2": {
        "active": true,
        "id": "wi08ebtatdc7oj83wtl9uxwz807l8b",
        "version": "1.1.8",
        "name": "Streamlabs Leaderboard"
      },
      "3": {
        "active": true,
        "id": "naty2zwfp7vecaivuve8ef1hohh6bo",
        "version": "1.0.9",
        "name": "Streamlabs Stream Schedule & Countdown"
      }
    },
    "overlay": {
      "1": {
        "active": true,
        "id": "zfh2irvx2jb4s60f02jq0ajm8vwgka",
        "version": "1.0.19",
        "name": "Streamlabs"
      }
    },
    "component": {
      "1": {
        "active": true,
        "id": "lqnf3zxk0rv0g7gq92mtmnirjz2cjj",
        "version": "0.0.1",
        "name": "Dev Experience Test",
        "x": 0,
        "y": 0
      },
      "2": {
        "active": false
      }
    }
  }
}
    '''
    url= f"https://api.twitch.tv/helix/users/extensions?user_id={channel_id}"
    return await single(channel_id,url)

@validatetyping
async def update_user_extensions(channel_id:int,dataset:dict)->dict:
    '''Twitch official example rersponse see get_user_active_extensions()

Twitch official example request dataset:
{
  "data": {
    "panel": {
      "1": {
        "active": true,
        "id": "rh6jq1q334hqc2rr1qlzqbvwlfl3x0",
        "version": "1.1.0"
      },
      "2": {
        "active": true,
        "id": "wi08ebtatdc7oj83wtl9uxwz807l8b",
        "version": "1.1.8"
      },
      "3": {
        "active": true,
        "id": "naty2zwfp7vecaivuve8ef1hohh6bo",
        "version": "1.0.9"
      }
    },
    "overlay": {
      "1": {
        "active": true,
        "id": "zfh2irvx2jb4s60f02jq0ajm8vwgka",
        "version": "1.0.19"
      }
    },
    "component": {
      "1": {
        "active": true,
        "id": "lqnf3zxk0rv0g7gq92mtmnirjz2cjj",
        "version": "0.0.1",
        "x": 0,
        "y": 0
      },
      "2": {
        "active": false
      }
    }
  }
}
    '''
    url= f"https://api.twitch.tv/helix/users/extensions"
    return await single(channel_id,url,"PUT",data=dataset)