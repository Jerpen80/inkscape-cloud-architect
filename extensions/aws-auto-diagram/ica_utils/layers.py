from inkex.elements import Group

INKSCAPE_NS = "http://www.inkscape.org/namespaces/inkscape"


def get_or_create_layer(inkdoc, name):
    """Get or create a named Inkscape layer. Returns the Group element."""
    # Search for existing layer with this label
    for elem in inkdoc.svg:
        if (isinstance(elem, Group)
                and elem.get(f'{{{INKSCAPE_NS}}}groupmode') == 'layer'
                and elem.get(f'{{{INKSCAPE_NS}}}label') == name):
            return elem

    # Create new layer
    layer = Group()
    layer.set(f'{{{INKSCAPE_NS}}}groupmode', 'layer')
    layer.set(f'{{{INKSCAPE_NS}}}label', name)
    inkdoc.svg.append(layer)
    return layer
