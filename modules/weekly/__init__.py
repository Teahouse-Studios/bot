import json
import re

from graia.application import MessageChain
from graia.application.message.elements.internal import Image, Plain

from core.template import sendMessage
from core.utils import get_url


async def weekly(kwargs: dict):
    try:
        result = json.loads(await get_url(
            'https://minecraft.fandom.com/zh/api.php?action=parse&page=Minecraft_Wiki/weekly&prop=text|revid&format=json'))
        html = result['parse']['text']['*']
        text = re.sub(r'<p>', '\n', html)  # 分段
        text = re.sub(r'<(.*?)>', '', text, flags=re.DOTALL)  # 移除所有 HTML 标签
        text = re.sub(r'\n\n\n', '\n\n', text)  # 移除不必要的空行
        text = re.sub(r'\n*$', '', text)
        img = re.findall(r'(?<=src=")(.*?)(?=/revision/latest/scale-to-(width|height)-down/\d{3}\?cb=\d{14}?")', html)
        page = re.findall(r'(?<=<b><a href=").*?(?=")', html)
        sended_img = Image.fromNetworkAddress(img[0][0]) if img else Plain('\n（发生错误：图片获取失败）')
        msg = '发生错误：本周页面已过期，请联系中文 Minecraft Wiki 更新。' if page[
                                                             0] == '/zh/wiki/%E7%8E%BB%E7%92%83' else '本周的每周页面：\n\n' + text + '\n图片：' + \
                                                                                                      img[0][
                                                                                                          0] + '?format=original\n\n页面链接：https://minecraft.fandom.com' + \
                                                                                                      page[
                                                                                                          0] + '\n每周页面：https://minecraft.fandom.com/zh/wiki/?oldid=' + str(
            result['parse']['revid'])
        await sendMessage(kwargs, MessageChain.create([Plain(msg), sended_img]))

    except Exception as e:
        await sendMessage(kwargs, '发生错误：' + str(e))


command = {'weekly': weekly}
help = {'weekly': {'module': '获取中文 Minecraft Wiki 的每周页面。', 'help': '''~weekly - 获取中文 Minecraft Wiki 的每周页面。'''}}
