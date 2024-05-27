def concat(a, b):
    return a + b

def reverse(s):
    return s[::-1]

def init(config=None, context=None):
    pass

exports = {
    "concat": concat,
    "reverse": reverse,
}
