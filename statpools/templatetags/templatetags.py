from django import template

register = template.Library()

@register.filter
def in_game(things, gameid):
    return things.filter(gameid=gameid)

@register.filter
def in_market(things, marketkey):
    return things.filter(marketkey=marketkey)

@register.filter
def in_outcome(things, outcome):
    return things.filter(outcome=outcome)

@register.filter
def in_option(things, option):
    return things.filter(option=option)

@register.filter
def sub(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def double(value):
    try:
        return float(value)*2
    except (ValueError, TypeError):
        return ''
    
@register.filter
def score_dif(value, arg):
    try:
        dif = float(value) - float(arg)
        return abs(dif)
    except (ValueError, TypeError):
        return ''