curl --location --request POST "https://${SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1" \
--header "Ocp-Apim-Subscription-Key: ${SPEECH_KEY}" \
--header 'Content-Type: application/ssml+xml' \
--header 'X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3' \
--header 'User-Agent: curl' \
--data-raw '<speak version='\''1.0'\'' xml:lang='\''en-US'\''>
    <voice xml:lang='\''zh-CN'\'' xml:gender='\''Female'\'' name='\'zh-CN-XiaochenNeural''\''>
        <prosody rate="0" pitch="0">
		你好!
        </prosody>
    </voice>
</speak>' # > output.mp3
