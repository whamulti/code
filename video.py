import requests

url = "https://cdnst68.tokyvideo.com/videos/581/581087/mp4/47d4c549946774e8c89cdcf44b5947254b21eb1df4bf1da8c0976eab04ae7758.mp4?secure=xhSw_vWIiGEqbS6YwfypfQ%3D%3D%2C1773540768"
response = requests.get(url)

with open("video.mp4", "wb") as f:
    f.write(response.content)