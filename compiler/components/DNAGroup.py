import struct


class DNAGroup:
    COMPONENT_CODE = 1

    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        self.visGroup = None

    def setName(self, name):
        self.name = name

    def add(self, child):
        self.children.append(child)

    def setVisGroup(self, visGroup):
        self.visGroup = visGroup

    def getVisGroup(self):
        return self.visGroup

    def setParent(self, parent):
        self.parent = parent
        self.visGroup = parent.getVisGroup()

    def getParent(self):
        return self.parent

    def clearParent(self):
        self.parent = None
        self.visGroup = None

    def debug(self, message):
        if self.verbose:
            print 'DNAGroup:', message

    def traverse(self, recursive=True, verbose=False):
        self.verbose = verbose

        self.debug('created... prop code: {0}'.format(self.COMPONENT_CODE))
        data = struct.pack('<B', self.COMPONENT_CODE)  # Component code

        self.debug('packing... name length: {0}'.format(len(self.name)))
        data += struct.pack('<B', len(self.name))  # Name length
        self.debug('packing... name: {0}'.format(self.name))
        data += self.name  # Name

        if self.parent:
            parentName = self.parent.name
        else:
            parentName = None
        if parentName is None:
            self.debug('skipped... parent name length')
            self.debug('skipped... parent name')
            data += struct.pack('<B', 0)  # Parent name length
        else:
            self.debug('packing... parent name length: {0}'.format(len(parentName)))
            data += struct.pack('<B', len(parentName))  # Parent name length
            self.debug('packing... parent name: {0}'.format(parentName))
            data += parentName  # Parent name

        if self.visGroup:
            visGroupName = self.visGroup.name
        else:
            visGroupName = None
        if visGroupName is None:
            self.debug('skipped... DNAVisGroup name length')
            self.debug('skipped... DNAVisGroup name')
            data += struct.pack('<B', 0)  # DNAVisGroup name length
        else:
            self.debug('packing... DNAVisGroup name length: {0}'.format(len(visGroupName)))
            data += struct.pack('<B', len(visGroupName))  # DNAVisGroup name length
            self.debug('packing... DNAVisGroup name: {0}'.format(visGroupName))
            data += visGroupName  # DNAVisGroup name

        if recursive:
            data += self.traverseChildren(verbose=verbose)

        return data

    def traverseChildren(self, verbose=False):
        data = ''
        for child in self.children:
            data += child.traverse(recursive=True, verbose=verbose)

        # The following code makes the PDNA reader move the parent level up:
        data += struct.pack('B', 255)

        return data
