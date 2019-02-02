import discord
from collections import defaultdict
import re
import random


TOKEN = ''
with open('.TOKEN','r') as fin: TOKEN = fin.readline().strip()

class DNDClient(discord.Client):
    RollingPattern = re.compile('(((\d*)d(\d+))([-\+](?!\d))?([-\+]\d+)?)')

    def __init__(self, *args, **kwargs):
        discord.Client.__init__(self, *args, **kwargs)
        self.run(TOKEN)

    async def on_message(self, message):
        content = message.content.strip()
        if self.isARoll(content):
            await self.handleRoll(content, message.channel)


    async def handleRoll(self, content, channel):
        rolls = self.roll(re.findall(self.RollingPattern, content))

        leftColSize = max(map(len, [str(v) for v in rolls.keys()]))
        response = '\n'.join(['{}: {}'.format(k.ljust(leftColSize), ', '.join(map(str, v))) for k,v in sorted(rolls.items())])
        response = '```\n{}```'.format(response)
        await self.send_message(channel, response)


    @classmethod
    def isARoll(cls, s):
        for roll in s.split():
            if not re.match(cls.RollingPattern, roll): return False
        return True

    @classmethod
    def roll(cls, rolls):
        ret = defaultdict(list)
        for roll in rolls:
            _, _, n, d, advantage, mod = roll
            if n == '': n = 1
            else: n = int(n)

            d = int(d)

            if '+' == advantage: advantage = 1
            elif '-' == advantage: advantage = -1
            else: advantage = 0

            mod = int(mod) if mod != '' else 0

            for _ in range(n):
                result = random.randint(1, d)
                if advantage == 1:
                    result = max(result, random.randint(1, d))
                elif advantage == -1:
                    result = min(result, random.randint(1, d))
                ret[f'd{d}'].append(result + mod)
        return ret

client = DNDClient()