from nonebot import on_command,CommandSession

@on_command('echo',only_to_me=False,shell_like=True,aliases='复读')
async def echo(session:CommandSession):
    await session.send(session.state.get('message') or session.current_arg)