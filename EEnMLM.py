class EEnMLM(object):
    # Engset Multirate Loss Model calculations using the approximate Stasiak-Glabowski method
    def __init__(self, c, t, k, nList, bList, aEngList = None, tList = None, lEngList = None, mEngList = None):
        self._c = c  # set total capacity of the system
        self._t = t
        self._k = k # set the number of service classes
        self._nList = nList
        self._bList = bList # set the bandwidth requirement of service classes
        if aEngList != None:
            self._aEngList = aEngList # set the Engset traffic loads
        else:
            self._lEngList = lEngList # set the Engset arrival rates
            self._mEngList = mEngList # set the Engset service times
            self._aEngList = self._calc_ak() # calculate the Engset traffic loads
        if tList != None:
            self._tList = tList # set the trunk reservation values
        else:
            self._tList = [0] * self._k # set trunk reservation values equal to 0
        self._aList = [0] * self._k # initialize (set to zero) the corresponding Erlang traffic loads
        for i in range(0, self._k):
            self._aList[i] = self._aEngList[i] * self._nList[i] # calculate the corresponding Erlang traffic loads
        self._qErlList = self._calc_qj_erl() # calculate the corresponding Erlang unnormalized q values
        self._qErlNormList = self._calc_erl_norm_qj() # calculate the corresponding Erlang normalized q values
        self._erl_ykjList = self._calc_erl_ykj() # calculate the ykj values
        self._qEngList = self._calc_qj_engset() # calculate the (Engset) q values
        self._qEngNormList = self._calc_eng_norm_qj() # calculate the normalized (Engset) q values
        self._pbk = self._calc_pbk() # calculate the congestion probabilities
        self._u = self._calc_u() # calculate the link utilization

    def _calc_ak(self):
        # Calculate the traffic loads when the arrival rates and service times are given
        aList = []
        for i in range (0, self._k):
            a = self._lEngList[i] / self._mEngList[i]
            aList.append(a)
        return aList

    def _calc_qj_erl(self):
        # Calculate the unnormalized values of qj's using the exact recursive Kaufman-Roberts formula
        qErlList = []
        for j in range(0, self._t + 1):
            if j == 0:
                qj = 1.0
            else:
                qj = 0
                for i in range(0, self._k):
                    if (j - self._bList[i]) >= 0 and j <= self._t - self._tList[i]:
                        qj += self._aList[i] * self._bList[i] * qErlList[j - self._bList[i]]
                coef = min(self._c, j)
                qj *= 1.0 / coef
            qErlList.append(qj)
        return qErlList

    def _calc_erl_norm_qj(self):
        # Calculate the corresponding EMLM normalized values of qj's
        qErlNormList = []
        g = sum(self._qErlList)
        for j in range(0, self._t + 1):
            qErlNorm = self._qErlList[j] / g
            qErlNormList.append(qErlNorm)
        return qErlNormList

    def _calc_erl_ykj(self):
        # Calculate the values of yk(j)'s and store them in a two-dimensional list
        ykjList = []
        for i in range (0, self._k):
            yjList = []
            for j in range(0, self._t + 1):
                y = 0
                if (j - self._bList[i]) >= 0 and self._qErlList[j] > 0:
                    y = self._aList[i] * self._bList[i] * self._qErlList[j - self._bList[i]] * (1 + yjList[j - self._bList[i]])
                    coef = min(self._c, j)
                    y *= 1.0 / (coef * self._qErlList[j])
                    
                    sum = 0
                    for n in range (0, self._k):
                        if n != i and j - self._bList[n] >= 0:
                            sum += self._aList[n] * self._bList[n] * self._qErlList[j - self._bList[n]] * yjList[j - self._bList[n]]
                    coef = min(self._c, j)
                    y += (1.0 / (coef * self._qErlList[j])) * sum
                yjList.append(y)
            ykjList.append(yjList)
        return ykjList

    def _calc_qj_engset(self):
        # Calculate the EnMLM unnormalized values of qj's using the approximate recursive formula of Stasiak-Glabowski
        qErlList = []
        for j in range(0, self._t + 1):
            if j == 0:
                qj = 1.0
            else:
                qj = 0
                for i in range(0, self._k):
                    if (j - self._bList[i]) >= 0 and j <= self._t - self._tList[i]:
                        qj += (self._nList[i] - self._erl_ykjList[i][j - self._bList[i]]) * self._aEngList[i] * self._bList[i] * qErlList[j - self._bList[i]]
                coef = min(self._c, j)
                qj *= 1.0 / coef
            qErlList.append(qj)
        return qErlList

    def _calc_eng_norm_qj(self):
        # Calculate the normalized values of qj's
        qEngNormList = []
        g = sum(self._qEngList)
        for j in range(0, self._t + 1):
            qEngNorm = self._qEngList[j] / g
            qEngNormList.append(qEngNorm)
        return qEngNormList

    def _calc_pbk(self):
        # Calculate the Congestion Probabilities 
        pbList = []
        for i in range (0, self._k):
            pb = 0
            minj = self._t - self._bList[i] - self._tList[i] + 1
            for j in range (minj, self._t + 1):
                pb += self._qEngNormList[j]
            pbList.append(pb)
        return pbList

    def _calc_u(self):
        # Calculate the link utilization
        u = 0
        for j in range(1, self._c + 1):
            u += j * self._qEngNormList[j]
        for j in range(self._c + 1, self._t + 1):
            u += self._c * self._qEngNormList[j]
        return u
    
    def _update_obj(self):
        # Update the object when an instance variable changes
        for i in range(0, self._k):
            self._aList[i] = self._aEngList[i] * self._nList[i]
        self._qErlList = self._calc_qj_erl()
        self._qErlNormList = self._calc_erl_norm_qj()
        self._erl_ykjList = self._calc_erl_ykj()
        self._qEngList = self._calc_qj_engset()
        self._qEngNormList = self._calc_eng_norm_qj()
        self._pbk = self._calc_pbk()
        self._u = self._calc_u()
    
    #----------------
    # Setters/Getters
    #----------------
    def set_c(self, c):
        # Set the total capacity of the system (after the object instantiation) and update the object
        self._c = c
        self._update_obj()
    
    def set_k(self, k):
        # Set the number of service classes (after the object instantiation) and update the object
        self._k = k
        self._update_obj()
        
    def set_nList(self, nList):
        # Set number of sources and update the object
        self._nList = nList
        self._update_obj()

    def set_bList(self, bList):
        # Set the bandwidth requirement (in units) of service classes and update the object
        self._bList = bList
        self._update_obj()
        
    def set_aEngList(self, aEngList):
        # Set the traffic loads and update the object. Empty the lEngList and mEngList
        self._aEngList = aEngList
        self._lEngList = None
        self._mEngList = None
        self._update_obj()

    def set_tList(self, tList):
        # Set the trunk reservation of service classes and update the object
        self._tList = tList
        self._update_obj()
        
    def set_lEngList_mEngList(self, lEngList, mEngList):
        # Set the arrival rates and service times and update the object
        self._lEngList = lEngList
        self._mEngList = mEngList
        self._aEngList = self._calc_ak()
        self._update_obj()
        
    def get_qErl(self):
        # Get Erlang q values
        return self._qErlList
    
    def get_qErlNorm(self):
        # Get Erlang q normalized values
        return self._qErlNormList
    
    def get_erl_ykj(self):
        # Get Erlang ykj values
        return self._erl_ykjList
    
    def get_qEng(self):
        # Get q values
        return self._qEngList

    def get_qEngNorm(self):
        # Get q normalized values
        return self._qEngNormList

    def get_pbk(self):
        # Get call blocking probabilities
        return self._pbk
    
    def get_u(self):
        # Get link utilization value
        return self._u