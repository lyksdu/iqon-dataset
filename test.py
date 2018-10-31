import re

src = "<div>¥10,152</div>"
price = re.compile(r"¥[\d,]+")
string = "8,999"
for i in price.findall(src):
    print(i)
print(int(''.join(string.split(','))))