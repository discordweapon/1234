import asyncio
import os
import random
import random as ran
import smtplib
import sys
import time
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import discord
import openpyxl
from captcha.image import ImageCaptcha
from discord import channel
from discord.embeds import Embed

client = discord.Client()



idA,  timeA, expA, expB, expC, levelA , give, ID, TIME =  [], [], [], [], [], [], 0, 0, 0

try: #만약 파일이 없으면 새로 만듦
    f = open("UserData.txt", "r")
except:
    f = open("UserData.txt", "w")
    f.close()
    f = open("UserData.txt", "r")
while True: #유저들 데이터를 읽음 데이터 형식 : 유저ID,가지고 있는 돈,돈받은 시간
    line = f.readline()
    if not line: break
    line = line.split(",")
    idA.append(line[0])
    timeA.append(int(line[1]))
    expA.append(int(line[2]))
    expB.append(int(line[3]))
    expC.append(int(line[4]))
    levelA.append(int(line[5]))
f.close()

@client.event
async def on_ready(): #봇이 켜지면
    print("봇 아이디: ", client.user.id)
    print("봇 준비 완료")
    game = discord.Game("/도움말")
    await client.change_presence(status=discord.Status.online, activity=game)
    
@client.event
async def on_message(message):
        

    if message.content == "!임베드":
        embed = discord.Embed(title = "테스트봇의 도움말", description = '''
        예시''', color = 0x8258FA)

        await message.author.send(embed = embed)
    
    if message.content.startswith('역할'):
        for i in message.author.roles:
            if i.name == '역할이름':
                await message.channel.send('역할을 가지고 계십니다.')
                break
    
    if message.content.startswith('/실험'):
        msg1 = message.content[4:] 
        ran1 = random.randint(1, 9)
        ran2 = random.randint(10, 90)
        ran3 = random.randint(100, 900)
        ran4 = random.randint(1000, 9000)
        ran5 = random.randint(10000, 90000)
        ran6 = random.randint(100000, 900000)
        ran7 = random.randint(1000000, 9000000)
        ranran = ran1 + ran2 + ran3 + ran4 + ran5 + ran6 + ran7
        to = ('+8210%s' %msg1)
        print(to)
        print(ranran)


    if message.content.startswith("/인증"):
        ID = str(message.author.id)
        Image_captcha = ImageCaptcha()
        msg = ""
        a = ""
        for i in range(6):
            a += str(random.randint(0, 9))

        name = "Captcha.png"
        Image_captcha.write(a, name)

        await message.channel.send(file=discord.File(name))
        await message.channel.send("**30초안에 답안을 적어주세요!**")

        def check(msg):
            return msg.author == message.author 

        try:
            msg = await client.wait_for("message", timeout=30, check=check)
        except:
            await message.channel.send("**시간 초과입니다.**")
            return

        if msg.content != a:
            await message.channel.send("**오답입니다.**")
            raise ValueError
        else:
            await message.channel.send("**정답입니다.")
            embed = discord.Embed(title='', description="", color=0x00FF00)
            embed.add_field(name="**적는 요령**", value="**/이메일 1234567@gmail.com", inline=True)
            idA.append(ID)
            timeA.append(1)
            expA.append(0)
            expB.append(0)
            expC.append(0)
            levelA.append(1)
            f = open("UserData.txt", "w") 
            for i in range(0,len(idA),1):
                f.write(str(idA[i])+","+str(timeA[i])+","+str(expA[i])+","+str(expB[i])+","+str(expC[i])+","+str(levelA[i])+"\n")
            f.close()
            await message.channel.send(embed = embed)
    
    if message.content.startswith("/이메일"):
        ID = str(message.author.id)
        msg1 = message.content[5:]
        msg2 = message.content[-9:]
        msg3 = 'gmail.com'
        if timeA[idA.index(ID)] < 1:
            await message.channel.send("먼저 인증을 완료한 뒤, /이메일을 쳐주세요!")
            raise ValueError
        elif timeA[idA.index(ID)] == 1:
            if msg3 != msg2:
                await message.channel.send("이메일을 정확하게 적어주세요!")
                timeA[idA.index(ID)] -= 1
                f = open("UserData.txt", "w") 
                for i in range(0,len(idA),1):
                    f.write(str(idA[i])+","+str(timeA[i])+","+str(expA[i])+","+str(expB[i])+","+str(expC[i])+","+str(levelA[i])+"\n")
                f.close()
                raise ValueError
            elif msg3 == msg2:
                ranran = random.randint(1000000, 9000000)
                from_user = "qazwsxedcrfvqwer7@gmail.com"
                pw = 'ejsohznzptybcuru'

                subject = u'test'
                text = u'인증코드 : [%s]' % (ranran)
        
                msg = MIMEText(text, _charset = 'UTF-8')
                msg['Subject'] = subject
                msg["To"] = msg1
                
                s = smtplib.SMTP("smtp.gmail.com" , 587)
                s.starttls()
                s.login(from_user, pw)
                s.sendmail(from_user, msg1, msg.as_string())
                s.quit()

                timeA[idA.index(ID)] -= 1
                f = open("UserData.txt", "w") 
                for i in range(0,len(idA),1):
                    f.write(str(idA[i])+","+str(timeA[i])+","+str(expA[i])+","+str(expB[i])+","+str(expC[i])+","+str(levelA[i])+"\n")
                f.close()

                txt = '{}.txt'.format(ID)
                f = open(txt , mode= "w")
                f.write(str(ranran))
                f.close()
                embed = discord.Embed(title='**인증번호가 발신되었습니다**', description="**인증번호 7자리를 채팅에다 적어주세요!**", color=0x00FF00)
                embed.add_field(name="**적는 요령**", value="**/번호 1234567", inline=True)
                await message.channel.send(embed = embed)

    if message.content.startswith('/번호'):
        ID = str(message.author.id)
        msg4 = message.content[4:]
        txt2 = '{}.txt'.format(ID)
        f = open(txt2 , mode= "r")
        content = f.read()
        f.close()
        if msg4 != content:
            await message.channel.send("인증번호가 맞지 않습니다")
            os.remove('{0}.txt'.format(ID))
            raise ValueError
        else:
            os.remove('{0}.txt'.format(ID))
            await message.channel.send("인증을 완료했습니다! \n #인증채널 로 돌아가 /확인을 쳐주세요!") 



    if message.content == 'test':
        if message.channel.id == 820867967004835870:
            await message.channel.send('오류가 안나!')
        else:
            await message.channel.send('오류나..........')
            

    if message.content == '/test' and message.channel.id == 820867967004835870:
        await message.channel.send('오옹')




    if message.content.startswith(" ") and message.channel.id == 820867967004835870:
        ID = str(message.author.id)
        exp = [0, 10 , 20 , 30 , 40 , 50]
        while True:
            expA[idA.index(ID)] = expA[idA.index(ID)] + 5
            f = open("UserData.txt", "w") 
            for i in range(0,len(idA),1):
                f.write(str(idA[i])+","+str(timeA[i])+","+str(expA[i])+","+str(expB[i])+","+str(expC[i])+","+str(levelA[i])+"\n")
            f.close()
            if expA[idA.index(ID)] >= exp[levelA[idA.index(ID)]]:
                levelA[idA.index(ID)] == levelA[idA.index(ID)] + 1
                f = open("UserData.txt", "w") 
                for i in range(0,len(idA),1):
                    f.write(str(idA[i])+","+str(timeA[i])+","+str(expA[i])+","+str(expB[i])+","+str(expC[i])+","+str(levelA[i])+"\n")
                f.close()
                expC[idA.index(ID)] = expC[idA.index(ID)] + exp[{}.format(levelA[idA.index(ID)])]
                f = open("UserData.txt", "w") 
                for i in range(0,len(idA),1):
                    f.write(str(idA[i])+","+str(timeA[i])+","+str(expA[i])+","+str(expB[i])+","+str(expC[i])+","+str(levelA[i])+"\n")
                f.close()
                expB[idA.index(ID)] = expB[idA.index(ID)] + expC[idA.index(ID)]
                f = open("UserData.txt", "w") 
                for i in range(0,len(idA),1):
                    f.write(str(idA[i])+","+str(timeA[i])+","+str(expA[i])+","+str(expB[i])+","+str(expC[i])+","+str(levelA[i])+"\n")
                f.close()
                embed=discord.Embed(title='레벨이 올랐습니다!' , description='level : ' + str(levelA[idA.index(ID)]) + 'exp : ' + str(expA[idA.index(ID)]) + '/' + str(expB[idA.index(ID)]))
                await message.channel.send(embed = embed)

                
        




        








client.run(os.environ['token'])
