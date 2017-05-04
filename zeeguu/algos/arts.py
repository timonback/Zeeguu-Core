import math


class ARTS:
    """ Constant: enforced delay (trials) """
    D = 1

    """ Constant: weight """
    a = 2

    """ Constant: weight """
    b = 4

    """ Constant: weight """
    r = 8

    """ Constant: priority increment for an error """
    w = 16

    """ Calculate the ARTS priority
    
    Parameters:
     N: number of trials since item was presented
     alpha: 0, if item was last answered correct; 1 otherwise
     RT: response time on most recent presentation
    """

    def calculate(self, N, alpha, RT):
        return self.a \
               * (N - self.D) \
               * (
                   (1 - alpha) * self.b * math.log(RT / self.r)
                   + (alpha * self.w)
               )
