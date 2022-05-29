def is_admin(ctx):
    for role in ctx.author.roles:
        if 969962769854128240 == role.id:
            return True
    return False
