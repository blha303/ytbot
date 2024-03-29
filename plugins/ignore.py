import json
from util import hook
from fnmatch import fnmatch


@hook.sieve
def ignore_sieve(bot, input, func, type, args):
    """ blocks input from ignored channels/hosts """
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    mask = input.mask.lower()

    # don't block input to event hooks
    if type == "event":
        return input

    if ignorelist:
        for pattern in ignorelist:
            if pattern.startswith("#") and pattern in ignorelist:
                if input.command == "PRIVMSG" and input.lastparam[1:] == "unignore":
                    return input
                else:
                    return None
            elif fnmatch(mask, pattern):
                if input.command == "PRIVMSG" and input.lastparam[1:] == "unignore":
                    return input
                else:
                    return None

    return input


@hook.command(permissions=["ignore"])
def ignore(inp, notice=None, bot=None, config=None):
    """ignore <channel|nick|host> -- Makes the bot ignore <channel|user>."""
    target = inp.lower()
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    if target in ignorelist:
        notice("{} is already ignored.".format(target))
    else:
        notice("{} has been ignored.".format(target))
        ignorelist.append(target)
        ignorelist.sort()
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return


@hook.command(permissions=["ignore"])
def unignore(inp, notice=None, bot=None, config=None):
    """unignore <channel|user> -- Makes the bot listen to
    <channel|user>."""
    target = inp.lower()
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    if target in ignorelist:
        notice("{} has been unignored.".format(target))
        ignorelist.remove(target)
        ignorelist.sort()
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    else:
        notice("{} is not ignored.".format(target))
    return
