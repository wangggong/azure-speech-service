curl --location --request POST "https://${SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1" \
--header "Ocp-Apim-Subscription-Key: ${SPEECH_KEY}" \
--header 'Content-Type: application/ssml+xml' \
--header 'X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3' \
--header 'User-Agent: curl' \
--data-raw '<speak version='\''1.0'\'' xml:lang='\''en-US'\''>
    <voice xml:lang='\''zh-CN'\'' xml:gender='\''Female'\'' name='\'zh-CN-XiaochenNeural''\''>
        <prosody rate="20%" pitch="0%">
            第十名，这我家祖传的面板就是我的不沾面垫，拥有祖传面板和不沾面垫。两位之间的对决到底谁更胜一筹，让我们拭目以待。哎呀，这我的面板也太粘了，粘的到处都是看我的，一点儿都不沾。第九名，这套硅胶锅铲我们已经用了快一年了，终于又有活动了。红色和黑色我都买过，都没有异味。它是食品级硅胶材质，在二百三十度高温，我们家煎炒烹炸。主帅用的都是它，它四边是软的，中间是硬的，是用各种锅具用了这么久也没有遇到脱色、起泡、变形等问题，质量还是蛮好的。第八名，妈，我和你说了多少次，别再这样蒸馒头了，馒头沾掉皮，纱布不好洗，还滋生细菌。用这个新款的蒸笼布吧，一包里面有三十片，用的时候抽一张，剩下的密封起来，甚至要铺在蒸锅里。它这个透气性很好，不粘连，还可以反复使用。第七名比赛开始，我可以防水，我也可以防水，我可以放歌，我一割就坏。我自带硅胶软刷，洗碗特别干净，我没带硅胶软刷，洗碗很烂。第六名给你们看一下，我们家厨房平时是怎么防烫隔热的，用的就是这种耐高温的隔热垫，可以直接做锅垫，也可以做防烫的。手电图案很可爱，像水杯、水壶、餐具放在上面都不担心它会烫坏桌面了。第五名，平常煮东西很容易出来，但是盖上这个防溢盖中间花瓣遇到蒸汽会自己睁开，再也不怕溢出来了，还能用来蒸东西。硅胶材质耐热不变形，清洗也不麻烦，用完可直接挂起来。第四名，婆婆每次做饭，非要用草鞋把锅拿下来，我就给她买了这个小黄鸭防烫加热锅，用它拿取不会烫手，用来拿蒸玉米的盘子，方便又卫生，用完吸附在墙面上还不占空间。第三名，家里有冰箱的，一定要买一个这样的硅胶保鲜盖，吃不完的剩菜剩饭，密封性很好。不错喽，放冰箱里即保鲜，还不串味，家里大小碗盘都可用。食品级硅胶沸水消毒也没事。第二名，这个果蔬刷你家里整一个平常清洗土豆红薯，钢丝球太硬，土手又洗不干净，这个小玩意就很好。它可以弯折包裹住食材表面带刺的黄瓜，清洗起来就不会扎手了。难洗的毛头也不在话下，垃圾脚旮旯的生姜，还有带网格的蒸蛋器漏勺，它比洗锅刷更有力，但不会破坏锅的涂层。用完水冲冲就干净了。第一名想不到还有这么好用的东西，硅胶刷毛轻松刷洗杯子，使脚超长手柄，在线的杯子都能刷干净。想要点左下方购物车。
        </prosody>
    </voice>
</speak>' > output.mp3
