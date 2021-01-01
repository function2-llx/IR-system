lines = open('dep.txt').readlines()
for i in range(0, len(lines), 4):
    name, abbr = map(str.strip, lines[i:i + 2])
    print(f'<option value={abbr}>{name}</option>')
