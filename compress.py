from color import color_shortcut


def combine_blocks(blocks):
    # Map of property stringification to list of containing blocks
    #property_locations = {}

    return blocks


def _filter_property(basename, properties):
    prefix = basename + '-'
    filtered = []

    for prop in list(properties):
        name, value = prop

        if name == basename or name[:len(prefix)] == prefix:
            filtered.append(properties.remove(prop))

    return filtered


def compress_color(properties):
    for i, (name, value) in enumerate(properties):
        if name in ('color', 'background-color', 'border-color'):
            properties[i] = (name, color_shortcut(value))


def compress_font(properties):
    #fonts = _filter_property('font', properties)
    pass


def compress_dimension(properties):
    #margins = _filter_property('margin', properties)
    #paddings = _filter_property('padding', properties)
    pass
