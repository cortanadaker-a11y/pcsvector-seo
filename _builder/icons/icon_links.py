"""Shared favicon link tags (compass emoji, Noto Color Emoji SVG, Apache-2.0)."""
TAGS = [
    '<link rel="icon" href="/favicon.ico" sizes="any">',
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
    '<link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48">',
    '<link rel="icon" href="/favicon-192x192.png" type="image/png" sizes="192x192">',
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">',
]
INLINE = ''.join(TAGS)            # sub-pages: head is one line
HOME = '\n'.join(TAGS)            # home: one tag per line
# the only line ever replaced on the home page
HOME_OLD = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'%3E'
            '%3Ctext y=\'.9em\' font-size=\'90\'%3E%F0%9F%A7%AD%3C/text%3E%3C/svg%3E">')
SUB_OLD = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
