# A list of activation functions!

def linear(weighted_sum):
    return weighted_sum


def leakyReLU(weighted_sum):
    if(weighted_sum < 0):
        return (weighted_sum * 0.1)
    else:
        return weighted_sum