from nonebot import on_command,CommandSession
import base64
from Crypto.Cipher import AES

aes_key = "35303735363736373639343236663734" #必须32位 
aes_mode = AES.MODE_ECB

def aes_enc(text):
    key = bytes(aes_key, encoding = "utf8")
    cryptos = AES.new(key, aes_mode)
    length = 16
    count = len(text.encode('utf-8'))             
    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 0
    text = text + ('\0' * add)
    text = text.encode('utf-8')
    cipher_text = cryptos.encrypt(text)
    cipher_text = base64.b64encode(cipher_text)
    return str(cipher_text,'utf8')

def aes_dec(text):
    key = bytes(aes_key, encoding = "utf8")
    cryptos = AES.new(key, aes_mode)
    plain_text = cryptos.decrypt(base64.b64decode(text))
    result = str(plain_text,'utf8')
    result = result.replace('\0','')
    return result



@on_command('decrypter',only_to_me=False,shell_like=True,aliases='普吉一下')
async def decrypter(session:CommandSession):
    if session.ctx['message_type'] == 'group':
        await session.finish('密文消息请私聊使用')
    else:
        try:
            text = session.argv[0].strip()
            result = aes_dec(text)

            await session.send(result)
            await session.send('对加密消息严格保密，请勿分享给任何第三方，谢谢配合')
        except:
            await session.finish()


@on_command('encrypter',only_to_me=False,aliases='一下普吉')
async def encrypter(session:CommandSession):
    text = session.get('text',prompt='请输入想要加密的文本信息')
    try:
        result = aes_enc(text)
        await session.send(result)

    except:
        await session.finish()