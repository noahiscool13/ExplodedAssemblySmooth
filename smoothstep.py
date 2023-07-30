def smoothstep(x, edge0=0, edge1=1):
    x = clamp((x - edge0) / (edge1 - edge0))

    return x * x * (3 - 2 * x)

def smootherstep(x, edge0 = 0, edge1 = 1) :
  x = clamp((x - edge0) / (edge1 - edge0))

  return x * x * x * (3 * x * (2 * x - 5) + 10)


def clamp(x, lowerlimit=0, upperlimit=1):
    if x < lowerlimit:
        return lowerlimit
    if x > upperlimit:
        return upperlimit
    return x
