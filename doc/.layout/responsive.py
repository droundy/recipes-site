#!/usr/bin/python2

import types, string

def dist(x):
    if isinstance(x, types.StringTypes):
        return x
    return '%gem' % x

def cssrule(name, width, leftmargin, rightmargin, floatme='left', clear='none', padding=0):
    if name == '':
        return ''
    if leftmargin == '':
        leftmargin = '-100%'
    if rightmargin == '':
        rightmargin = '-100%'
    if width == '':
        width = 'auto'
    if width == 0 or width == '0%':
        return """%s {
    display: none;
}\n""" % (name)
    return """%s {
    width: %s;
    margin-left: %s;
    margin-right: %s;
    float: %s;
    clear: %s;
    padding: %s;
    display: block;
    position: relative;
}\n""" % (name, dist(width), dist(leftmargin), dist(rightmargin), floatme, clear, padding)


class Column(object):
    def __init__(self, name, minwidth=0):
        self._name = name
        self._minwidth = minwidth
    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name

    def widths(self):
        return [self._minwidth]
    def css(self, actualwidth, leftmargin="", width="", rightmargin="",
            floatme='left', clear='none'):
        return cssrule(self._name, width, leftmargin, rightmargin,
                       floatme=floatme, clear=clear, padding='0 .5em')

class Optional(Column):
    def widths(self):
        return [0, self._minwidth]

class Fixed(Column):
    def widths(self):
        return [0, self._minwidth]
    def _always(self):
        return """
    z-index: 1000;
    overflow-y: auto;
    top: 0;
    bottom: 0;
    -webkit-overflow-scrolling: touch;
    position: fixed;"""
    def css(self, actualwidth, leftmargin="", width="", rightmargin="",
            floatme='left', clear='none'):
        if width == 0 or width == '0%':
            return """%s {
    display: none;
}\n""" % (self._name)
        if leftmargin != '' and width != '':
            return """%s {%s
    width: %s;
    left: %s;
    display: block;
}\n""" % (self._name, self._always(), dist(width), dist(leftmargin))
        if rightmargin != '' and width != '':
            return """%s {%s
    width: %s;
    right: %s;
    display: block;
}\n""" % (self._name, self._always(), dist(width), dist(rightmargin))

class FixedOrWide(Fixed):
    def __init__(self, name, minwidth=0, widecss='', fixedcss=''):
        self._name = name
        self._minwidth = minwidth
        self._widecss = widecss
        self._fixedcss = fixedcss
    def css(self, actualwidth, leftmargin="", width="", rightmargin="",
            floatme='left', clear='none'):
        if actualwidth != 0:
            css = Fixed.css(self, actualwidth,leftmargin,width,rightmargin,floatme,clear)
            return  css + """%s {
%s
}\n""" % (self._name, self._fixedcss)
        return """%s {
%s
}\n""" % (self._name, self._widecss)

def _all_groupings(xs):
    if len(xs) < 2:
        return [[xs]]
    groups = [[xs]]
    for n in range(1,len(xs)):
        groups += map(lambda r: [xs[:n]]+r, _all_groupings(xs[n:]))
    return sorted(groups)

def _sublist_choices(xs):
    if len(xs) == 0:
        return []
    if len(xs) == 1:
        return [[x] for x in xs[0]]
    rest = _sublist_choices(xs[1:])
    return [[x] + r for x in xs[0] for r in rest]

class Container(object):
    def __init__(self, name, children):
        self._name = name
        self._children = children
    def __str__(self):
        return self._name+str(self._children)
    def __repr__(self):
        return self._name+str(self._children)

    def widths(self):
        childrenwidths = [c.widths() for c in self._children]
        choices = _sublist_choices(childrenwidths)
        groupings = [g for gs in [_all_groupings(cs) for cs in choices] for g in gs]
        return sorted(list(set([max([sum(group) for group in grouping]) for grouping in groupings])))
    def css(self, actualwidth, leftmargin="", width="", rightmargin="",
            floatme='left', clear='none'):
        myself = cssrule(self._name, width, leftmargin, rightmargin,
                         floatme=floatme, clear=clear)
        options = _sublist_choices([c.widths() for c in self._children])
        groupings = [g for gs in [_all_groupings(cs) for cs in options] for g in gs]
        okay = [g for g in groupings
                if max([sum(group) for group in g]) == actualwidth]
        if len(okay) == 0:
            return cssrule(self._name, 0, 0, 0)
        childcss = ''
        i = 0
        for row in okay[-1]:
            rowsize = float(sum(row))
            def percent(x):
                return '%g%%' % (100*x/rowsize)
            childcss += '/* row %s %s */\n' % (row, self._children[i:i+len(row)])
            childcss += self._children[i].css(row[0],
                                              leftmargin=0,
                                              width=percent(row[0]),
                                              clear='both')
            leftmargin = row[0]
            i += 1
            for c in row[1:]:
                childcss += self._children[i].css(c, leftmargin=percent(leftmargin),
                                                  width=percent(c))
                leftmargin += c
                i += 1
        return myself + childcss

class EmContainer(object):
    def __init__(self, name, left, middle, right):
        self._name = name
        self._left = left
        self._middle = middle
        self._right = right
    def __str__(self):
        return self._name+str(self._left)+str(self._middle)+str(self._right)
    def __repr__(self):
        return self.__str__(self)
    def _options(self):
        childrenwidths = [c.widths() for c in self._left + [self._middle] + self._right]
        choices = _sublist_choices(childrenwidths)
        choices = sorted(choices, key = lambda c: sum(c))
        careful = [choices[0]]
        nzeros = 100
        for n in range(1,len(choices)):
            badone = False
            for i in range(len(choices[0])):
                if choices[n][i] == 0 and choices[n-1][i] != 0:
                    badone = True
                    break
            if not badone:
                careful.append(choices[n])
        return careful
    def widths(self):
        return sorted(list(set([sum(c) for c in self._options()])))
    def css(self, actualwidth, leftmargin="", width="", rightmargin="",
            floatme='left', clear='none'):
        myself = cssrule(self._name, width, leftmargin, rightmargin,
                         floatme=floatme, clear=clear)
        options = _sublist_choices([c.widths() for c in
                                    self._left + [self._middle] + self._right])
        okay = sorted([o for o in options if sum(o) == actualwidth],
                      key = lambda o: len([x for x in o if x == 0]))
        if len(okay) == 0:
            return cssrule(self._name, 0, 0, 0)
        widths = okay[0]
        childcss = ''
        i = 0
        leftmargin = 0
        for c in self._left:
            childcss += c.css(widths[i], leftmargin=leftmargin,
                              width=widths[i], floatme='left')
            leftmargin += widths[i]
            i += 1
        rightmargin = 0
        i=1
        for c in self._right:
            childcss += c.css(widths[-i], rightmargin=rightmargin,
                              width=widths[-i], floatme='right')
            rightmargin += widths[-i]
            i += 1
        i = len(self._left)
        childcss += self._middle.css(widths[i], leftmargin=leftmargin,
                                     rightmargin=rightmargin, floatme='left')
        return myself + childcss

def indent(str):
    lines = string.split(str, '\n')
    if lines[-1] == '':
        return '    '+string.join(lines[:-1], '\n    ')+'\n'
    return '    '+string.join(lines, '\n    ')

def total_css(container, usercss):
    css = """
@input 'normalize.css'
html {
    padding: 0;
    margin: 0;
}
body {
    padding: 0;
    margin: 0;
}
*, *:after, *:before {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}
"""
    allwidths = sorted(container.widths())
    css += usercss
    css += container.css(allwidths[0], leftmargin=0, rightmargin=0)
    for width in allwidths[1:]:
        css += '/* width %g */' % width
        css += """@media screen and (min-width: %gem) {
""" % (width)
        css += indent(container.css(width, leftmargin=0, rightmargin=0))
        css += """}
"""
    return css
