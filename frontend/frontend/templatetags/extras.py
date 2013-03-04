from django import template

register = template.Library()

@register.filter(name='get_image')
def get_image(images, size_name):
    mega = ('mega', 'extralarge', 'large', 'medium', 'small')
    extralarge = ('extralarge', 'large', 'medium', 'small')
    large = ('large', 'medium', 'small')
    medium = ('medium', 'small')
    small = ('small',)
    generic = 'http://cdn.lst.fm/flatness/imageheader/default_artist_256.png'

    sizes = locals()[size_name]
    for s in sizes:
        if s in images and images[s] != '':
            return images[s]
    return generic

@register.filter(name='icon_split')
def get_icon_split(icon, desired):
    # Take an icon string in the form code#000000
    split = icon.split('#')

    if (desired == 'code'):
        return split[0]
    elif (desired == 'colour'):
        return '#' + split[1]
