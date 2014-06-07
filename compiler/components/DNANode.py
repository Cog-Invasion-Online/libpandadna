import struct

import DNAGroup


class DNANode(DNAGroup.DNAGroup):
    COMPONENT_CODE = 3

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)

        self.pos = (0, 0, 0)
        self.hpr = (0, 0, 0)
        self.scale = (1, 1, 1)

    def setPos(self, pos):
        self.pos = pos

    def setHpr(self, hpr):
        self.hpr = hpr

    def setScale(self, scale):
        self.scale = scale

    def debug(self, message):
        if self.verbose:
            print 'DNANode:', message

    def traverse(self, recursive=True, verbose=False):
        data = DNAGroup.DNAGroup.traverse(self, recursive=False, verbose=verbose)

        for component in self.pos:
            self.debug('packing... position: {0}'.format(component))
            data += struct.pack('<i', int(component * 100))  # Position

        for component in self.hpr:
            self.debug('packing... rotation: {0}'.format(component))
            data += struct.pack('<h', int(component * 100))  # Rotation

        for component in self.scale:
            self.debug('packing... scale: {0}'.format(component))
            data += struct.pack('<h', int(component * 100))  # Scale

        if recursive:
            data += self.traverseChildren(verbose=verbose)

        return data
