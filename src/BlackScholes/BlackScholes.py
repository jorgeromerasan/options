import numpy as np
from src.dates.date import Date, Days
from src.utils.distributions import cdf, cdf_p




class European:

    def __init__(self, BuySell:str,S:float, K:float, Rf:float,sessionDate:Date, maturityDate:Date, vola:float, CP:str, Div:float, typeDiv='Cont'):

        self.BuySell = 1 if BuySell == "Buy" else -1

        self.S           = S
        self.K           = K
        self.Rf          = Rf
        self.sDate       = sessionDate
        self.mDate       = maturityDate
        self.vola        = vola
        self.CP          = CP
        self.typeDiv     = typeDiv


        self.daysmaturity = self.mDate - self.sDate
        self.daysYear = 365 if self.daysmaturity > 365 else 360
        self.MT = self.daysmaturity / self.daysYear

        if self.typeDiv == 'Cont':
            self.y = Div
            self.Div = self.S*(1 - np.exp(-self.y * self.MT))
        else:
            self.Div = Div
            self.y = -(1 / self.MT) * np.log(1 - self.Div / self.S)




        self.D1 = (np.log(self.S / self.K) + (self.Rf - self.y + 0.5 * self.vola ** 2) * self.MT) / (self.vola * np.sqrt(self.MT))
        self.D2 = self.D1 - (self.vola * np.sqrt(self.MT))


    def Price(self):

        if self.CP == "C":
            return self.BuySell * round(max((self.S * np.exp(-self.y * self.MT)), 0.00000001) * cdf(x=self.D1) - self.K * np.exp((-self.Rf) * self.MT) * cdf(x=self.D2),4)
        elif self.CP == "P":
            return self.BuySell * round(-max((self.S * np.exp(-self.y * self.MT)), 0.00000001) * cdf(x=-self.D1) + self.K * np.exp((-self.Rf) * self.MT) * cdf(x=-self.D2),4)
        else:
            raise ValueError('The Option must be "C" or "P" ')
    def intrinsic(self):

        if self.CP == "C":
            return self.BuySell * round(max(self.S - self.K,0),4)
        elif self.CP == "P":
            return self.BuySell * round(max(self.K - self.S, 0),4)
        else:
            raise ValueError('The Option must be "C" or "P" ')

    def Delta(self):
        if self.CP == "C":
            return self.BuySell * round(cdf(x=self.D1) * np.exp(-self.y * self.MT),4)
        elif self.CP == "P":
            return self.BuySell * round(-cdf(x=-self.D1) * np.exp(-self.y * self.MT),4)
        else:
            raise ValueError('The Option must be "C" or "P" ')

    def Gamma(self):

        return self.BuySell * round((np.exp(-self.y * self.MT) / (self.S * self.vola * np.sqrt(self.MT))) * cdf_p(self.D1),5)

    def Theta(self):

        if self.CP == "C":
            return self.BuySell * round(100 * ((self.y * self.S * np.exp(-self.y * self.MT) * cdf(x=self.D1))\
                   - ((self.S * np.exp(-self.y * self.MT) * self.vola * cdf_p(x=self.D1)) / (2 * np.sqrt(self.MT)))\
                   - (self.Rf * self.K * np.exp(-self.Rf * self.MT) * cdf(x=self.D2))),4)
        elif self.CP == "P":
            return self.BuySell * round(100 * (-(self.y * self.S * np.exp(-self.y * self.MT) * cdf(x=-self.D1))\
                   - ((self.S * np.exp(-self.y * self.MT) * self.vola * cdf_p(x=self.D1)) / (2 * np.sqrt(self.MT)))\
                   + (self.Rf * self.K * np.exp(-self.Rf * self.MT) * cdf(x=-self.D2))),4)
        else:
            raise ValueError('The Option must be "C" or "P" ')

    def Vega(self):

        return  self.BuySell * round(self.S * np.exp(-self.y * self.MT) * np.sqrt(self.MT) * cdf_p(x=self.D1),4)

    def Rho(self):
        if self.CP == "C":
            return self.BuySell * round(self.K * self.MT * np.exp(-self.Rf * self.MT) * cdf(x=self.D2),4)
        elif self.CP == "P":
            return self.BuySell * round(-self.K * self.MT * np.exp(-self.Rf * self.MT) * cdf(x=-self.D2),4)
        else:
            raise ValueError('The Option must be "C" or "P" ')

    def sk(self):
        return round(self.S - self.K * np.exp(-(self.Rf - self.y) * self.MT),4)





if __name__ == "__main__":



    OptionC = European(BuySell="Buy",
                       S=4.9,
                      K= 4.9,
                      Rf = 0.03,
                      sessionDate=Date(day=11, month=2, year =2018),
                      maturityDate=Date(day=11, month=3, year =2018),
                      vola = 0.25,
                      CP = "C",
                      Div= 0.025,#0.01981857442,#0.190423182809269,
                      typeDiv = 'Cont')



    OptionP = European(BuySell="Buy",
                       S=4.9,
                       K=4.9,
                       Rf=0.03,
                       sessionDate=Date(day=11, month=2, year=2018),
                       maturityDate=Date(day=11, month=3, year=2018),
                       vola=0.25,
                       CP="P",
                       Div= 0.025,#0.01981857442,  # 0.190423182809269,
                       typeDiv = 'Cont')



    print("----------------- CALL ----------")
    print(OptionC.Price())
    print("----------------- PUT ----------")
    print(OptionP.Price())
    print("----------------- CALL DELTA ----------")
    print(OptionC.Delta())
    print("----------------- PUT DELTA ----------")
    print(OptionP.Delta())
    print("----------------- CALL GAMMA ----------")
    print(OptionC.Gamma())
    print("----------------- PUT GAMMA ----------")
    print(OptionP.Gamma())
    print("----------------- CALL VEGA ----------")
    print(OptionC.Vega())
    print("----------------- PUT VEGA ----------")
    print(OptionP.Vega())
    print("----------------- CALL THETA ----------")
    print(OptionC.Theta())
    print("----------------- PUT THETA ----------")
    print(OptionP.Theta())
    print("----------------- CALL RHO ----------")
    print(OptionC.Rho())
    print("----------------- PUT RHO ----------")
    print(OptionP.Rho())

    print("----------------- ###### ----------")
    print("----------------- CHECKS ----------")
    print(OptionC.Delta() - OptionP.Delta())