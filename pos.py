# for val, pos in map(lambda x: x.split('/'), r"""n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
# m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
# v/动词 vm/能愿动词 vd/趋向动词 a/形容词 d/副词
# h/前接成分 k/后接成分 i/习语 j/简称
# r/代词 c/连词 p/介词 u/助词 y/语气助词
# e/叹词 o/拟声词 g/语素 w/标点 x/其它""".replace('\n', ' ').split(' ')):
#     print(f'<option value={val}>{pos}</option>')
lines = open('pos.txt').readlines()
for i in range(0, len(lines), 3):
    abbr, name, example = map(str.strip, lines[i:i + 3])
    # print(abbr, name, example)
    print(f'<option value={abbr}>{name}</option>')
