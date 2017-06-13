import math


class ArtsDiffFast:
    """
    ARTS algorithm with default values as described in:
    Adaptive response-time-based category sequencing in perceptual learning
    by Everett Mettler and Philip J. Kellman

    a: Constant - general weight
    D: Constant - enforced delay (trials)
    b: Constant - weight for the response time
    d: Constant - weight for the standard deviation (inside log)
    w: Constant - priority increment for an error. Higher values let incorrect items appear quicker again
    """

    def __init__(self, a=0.1, D=2, b=1.1, d=1.7, w=20):
        self.a = a
        self.D = D
        self.b = b
        self.d = d
        self.w = w

    def calculate(self, N, alpha, sd):
        return self.a \
               * (N - self.D) \
               * (
                   (1 - alpha) * self.b * (math.e ** (self.d * sd))
                   + (alpha * self.w)
               )
