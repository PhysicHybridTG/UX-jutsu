import os
from userge import userge, Message
from userge.utils.tools import post_to_telegraph

_T_LIMIT = 5242880

@userge.on_cmd("op", about={
    'header': "Pasting some files content",
    'types': ['.json', '.html', '.txt', '.py'],
    'usage': "Reply to media with extension mentioned above : limit 5MB for media"})
async def te_(message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.err("reply to media")
        return
    if not ((replied.document
            and replied.document.file_name.endswith(
                ('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.html', '.txt', '.py', '.json'))
            and replied.document.file_size <= _T_LIMIT)):
        await message.err("not supported!")
        return
    await message.edit("`Processing...`")
    if (replied.text
        or (replied.document
            and replied.document.file_name.endswith(
            ('.html', '.txt', '.py', '.json')))):
        if replied.document:
            a = await replied.download()
            with open(a,"r") as f:
                body_text = "<code>" + f.read() + "</code>"
            link = post_to_telegraph('Heading',body_text)
            await message.edit(text=f"**Check [URL]({link})**", disable_web_page_preview=True)
            os.remove(a)