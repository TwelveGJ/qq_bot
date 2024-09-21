async def reply_message(message, reply_content):
    messageResult = await message._api.post_group_message(
        group_openid=message.group_openid,
        msg_type=0,
        msg_id=message.id,
        content=reply_content)
    return messageResult


def get_group_openid(message):
    return message.group_openid


def get_member_openid(message):
    return message.author.member_openid


def get_message_images_url_list(message):
    attachments = message.attachments
    images_url = [item.url for item in attachments if item.content_type.startswith('image')]
    return images_url
