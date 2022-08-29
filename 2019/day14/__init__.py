import common
import math
from collections import defaultdict


def parse(raw):
    lines = raw.splitlines()
    out = {}
    for line in lines:
        pieces = line.split(' => ')
        right = pieces[1].split(' ')
        out[right[1]] = {
            'output_qty': int(right[0]),
            'inputs': []
        }
        for ingredient in pieces[0].split(', '):
            print(ingredient)
            (qty, src) = ingredient.split(' ')
            out[right[1]]['inputs'].append({
                'ingredient': src,
                'input_qty': int(qty)
            })

    return out


def calc(recipes, leftovers=None, fuel_needed=1):
    needs = ['FUEL']
    needed_qty = defaultdict(int, {
        'FUEL': fuel_needed
    })
    if leftovers == None:
        leftovers = defaultdict(int, {})

    while len(needs) > 0:
        need = needs.pop(0)
        need_qty = needed_qty[need]
        needed_qty[need] = 0

        avail = leftovers[need]

        if avail > need_qty:
            leftovers[need] = avail - need_qty
            continue

        need_qty -= avail
        leftovers[need] = 0
        recipe = recipes[need]
        qty_needed = math.ceil(need_qty/recipe['output_qty'])
        leftovers[need] += (qty_needed * recipe['output_qty']) - need_qty

        for inp in recipe['inputs']:
            if inp['ingredient'] not in needs and inp['ingredient'] != 'ORE':
                needs.append(inp['ingredient'])
            needed_qty[inp['ingredient']] += inp['input_qty'] * qty_needed 
        
    return (needed_qty['ORE'], leftovers)


def main(session=None):
    raw = common.load_input(14, session)
    recipes = parse(raw)

    (pt1, leftovers) = calc(recipes)
    print(f"Pt1 {pt1}")

    min_guess = math.floor(1000000000000 / pt1)
    max_guess = min_guess * 2

    while min_guess < max_guess - 1:
        guess = math.floor(min_guess + (max_guess-min_guess)/2)
        (needed, leftovers) = calc(recipes, fuel_needed=guess)

        if needed > 1000000000000:
            max_guess = guess
        else:
            min_guess = guess

        print(max_guess, min_guess)

    print(f"Pt2 {min_guess}")
