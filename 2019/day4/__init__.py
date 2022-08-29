import common
import re

def valid(num_str):
    if num_str[1] < num_str[0] or num_str[2] < num_str[1] or num_str[3] < num_str[2] or num_str[4] < num_str[3] or num_str[5] < num_str[4]:
        return False

    y = re.sub('(?P<d>[0-9])(?P=d){2,}', '-', num_str)
    if not re.match('.*(?P<d>[0-9])(?P=d).*', y):
        return False

    return True

def main(session=None):
    min_num = 172851
    max_num = 675869
    
    x = min_num
    allowed = []

    while x <= max_num:
        y = str(x)

        if valid(y):
            print(x)
            allowed.append(x)

        x += 1

    return allowed
