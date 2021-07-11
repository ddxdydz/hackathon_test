from ursina import *

app = Ursina()
descr = dedent('<scale:1>Summon').strip()
Text.default_resolution = 1080 * Text.size
test = Text(text=descr, origin=(0, 0))

window.fps_counter.enabled = True
print('....', Text.get_width('yolo'))
app.run()
