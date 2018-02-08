from discord.ext import commands

class admin_only(commands.CommandError):
    pass

class mod_only(commands.CommandError):
    pass

class dev_only(commands.CommandError):
    pass

admin_role_ids = [321747479047569409, 321808415120687104]

mod_role_id = 321747496319844364

def is_dev():
    def predicate(ctx):
        if ctx.message.author.id in [169597963507728384, 117678528220233731]:
            return True
        else:
            raise dev_only
    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        for role in ctx.author.roles:
            if role.id in admin_role_ids:
                return True
        raise admin_only
    return commands.check(predicate)

def is_mod():
    def predicate(ctx):
        for role in ctx.message.author.roles:
            if role.id in admin_role_ids or role.id == mod_role_id:
                return True
        raise mod_only
    return commands.check(predicate)