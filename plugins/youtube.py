import re
import time

from util import hook, http, timeformat


youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)'
              '([-_a-zA-Z0-9]+)', re.I)

base_url = 'http://gdata.youtube.com/feeds/api/'
api_url = base_url + 'videos/{}?v=2&alt=jsonc'
search_api_url = base_url + 'videos?v=2&alt=jsonc&max-results=1'
video_url = "http://youtu.be/%s"


def plural(num=0, text=''):
    return "{:,} {}{}".format(num, text, "s"[num==1:])





def get_video_description(video_id):
    request = http.get_json(api_url.format(video_id))

    if request.get('error'):
        return

    data = request['data']

    out = u'\x02{}\x02'.format(data['title'])

    if not data.get('duration'):
        return out

    length = data['duration']
    out += u' - length \x02{}\x02'.format(timeformat.format_time(length, simple=True))

    if 'ratingCount' in data:
        # format
        likes = plural(int(data['likeCount']), "like")
        dislikes = plural(data['ratingCount'] - int(data['likeCount']), "dislike")

        percent = 100 * float(data['likeCount'])/float(data['ratingCount'])
        out += u' - {}, {} (\x02{:.1f}\x02%)'.format(likes,
                                                    dislikes, percent)

    if 'viewCount' in data:
        views = data['viewCount']
        out += u' - \x02{:,}\x02 view{}'.format(views, "s"[views==1:])

    try:
        uploader = http.get_json(base_url + "users/{}?alt=json".format(data["uploader"]))["entry"]["author"][0]["name"]["$t"]
    except:
        uploader = data["uploader"]

    upload_time = time.strptime(data['uploaded'], "%Y-%m-%dT%H:%M:%S.000Z")
    out += u' - \x02{}\x02 on \x02{}\x02'.format(uploader,
                                                time.strftime("%Y.%m.%d", upload_time))

    if 'contentRating' in data:
        out += u' - \x034NSFW\x02'

    return out


@hook.regex(*youtube_re)
def youtube_url(match):
    return get_video_description(match.group(1))
