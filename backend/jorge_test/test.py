from datetime import datetime as d


now = d.now().strftime("%d%m%y-%H%M%S")
name = now + ".mp4"
print(d.now())
print(now)
print(name)