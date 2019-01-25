import discord
from collections import defaultdict
import re
import random


TOKEN = ''
with open('.TOKEN','r') as fin: TOKEN = fin.readline().strip()

class DNDClient(discord.Client):

    RollingPattern = re.compile('(\d*d\d+[-\+]?([-\+]\d+)?)')

    def __init__(self, *args, **kwargs):
        discord.Client.__init__(self, *args, **kwargs)
        self.run(TOKEN)

    async def on_message(self, message):
        content = message.content.strip()
        if self.isARoll(content):
            await self.handleRoll(content, message.channel)
        
    
    async def handleRoll(self, content, channel):
        rolls = self.roll(r[0] for r in re.findall(self.RollingPattern, content))

        leftColSize = max(map(len, [str(v) for v in rolls.keys()]))
        response = '\n'.join(['{}: {}'.format(k.ljust(leftColSize), ', '.join(map(str, v))) for k,v in sorted(rolls.items())])
        response = '```\n{}```'.format(response)
        await self.send_message(channel, response)
        

    @classmethod
    def isARoll(cls, s):
        for roll in re.split('\W*', s):
            if not re.match(cls.RollingPattern, roll): return False
        return True

    @classmethod
    def roll(cls, rolls):
        ret = defaultdict(list)
        for roll in rolls:
            n, d = roll.split('d')
            if n == '': n = 1
            advantage = 0
            if '+' in d: advantage = 1
            elif '-' in d: advantage = -1
            
            die = int(d[:-1] if advantage != 0 else d)
            for _ in range(int(n)):
                result = random.randint(1, die)
                if advantage == 1:
                    result = max(result, random.randint(1, die))
                elif advantage == -1:
                    result = min(result, random.randint(1, die))
                ret['d' + d].append(result)
        return ret

        
        
client = DNDClient()