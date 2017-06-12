import math


class ArtsRT:
    """
    ARTS algorithm with default values as described in:
    Adaptive response-time-based category sequencing in perceptual learning
    by Everett Mettler and Philip J. Kellman
    a: Constant - general weight
    D: Constant - enforced delay (trials)
    b: Constant - weight for the response time
    r: Constant - weight for the response time (inside log)
    w: Constant - priority increment for an error. Higher values let incorrect items appear quicker again
    """

    def __init__(self, a=0.1, D=2, b=1.1, r=1.7, w=20):
        self.a = a
        self.D = D
        self.b = b
        self.r = r
        self.w = w

    def __eq__(self, other):
        return self.a == other.a \
               and self.D == other.D \
               and self.b == other.b \
               and self.r == other.r \
               and self.w == other.w

    def calculate(self, args):
        """ Calculate the ARTS priority
        Parameters:
            args: Contains the following parameters:
                N: number of trials since item was presented
                alpha: 0, if item was last answered correct; 1 otherwise
                RT: response time on most recent presentation
        """
        N, alpha, RT = args
        return self.a \
               * (N - self.D) \
               * (
                   (1 - alpha) * self.b * math.log(RT / self.r)
                   + (alpha * self.w)
               )