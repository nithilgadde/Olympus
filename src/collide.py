def overlap(a, b):
    ax, ay, aw, ah, = a
    bx, by, bw, bh = b
    return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)

def hits_any(box, boxes):
    for b in boxes:
        if overlap(box, b):
            return True
    return False