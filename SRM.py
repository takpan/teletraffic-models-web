class SRM(object):
    # Erlang Multirate Loss Model calculations using the exact recursive formula of Kaufman-Roberts
    def __init__(self, c, k, bList, brList, aList = None, arList = None, tList = None, lList = None, mList = None, mrList = None):
        self._c = c  # total capacity of the system
        self._k = k # number of service classes
        self._bList = bList # bandwidth requirement (in units) of service classes
        self._brList = brList
        if aList != None:
            self._aList = aList
            self._arList = arList
        else:
            self._lList = lList # arrival rates
            self._mList = mList # service times
            self._mrList = mrList
            self._aList = self._calc_ak(self._mList) # traffic loads
            self._arList = self._calc_ak(self._mrList)
        if tList != None:
            self._tList = tList
        else:
            self._tList = [0] * self._k
        self._qList = self._calc_qj() # unnormalized q values
        self._qNormList = self._calc_norm_qj() # normalized q values
        self._ykj = self._calc_ykj()
        self._pbk = self._calc_pbk()
        self._u = self._calc_u()
        # The length of the list must be equal to k, else raise an exception
    
    def _calc_ak(self, mList):
        # Calculate the traffic loads when the arrival rates and service times are given
        aList = []
        for i in range (0, self._k):
            a = self._lList[i] / mList[i]
            aList.append(a)
        return aList
    
    def _calc_qj(self):
        # Calculate the unnormalized values of qj's using the exact recursive Kaufman-Roberts formula
        qList = []
        for j in range(0, self._c + 1):
            if j == 0:
                qj = 1.0
            else:
                qj = 0
                for i in range(0, self._k):
                    if (j - self._bList[i]) >= 0 and j <= self._c - self._tList[i]:
                        qj += self._aList[i] * self._bList[i] * qList[j - self._bList[i]]
                for i in range(0, self._k):
                    if (j - self._bList[i]) >= 0 and j <= self._c - self._tList[i] and j > self._c - (self._bList[i] - self._brList[i]):
                        qj += self._arList[i] * self._brList[i] * qList[j - self._brList[i]]
                qj *= 1.0/j
            qList.append(qj)
        return qList
    
    def _calc_norm_qj(self):
        # Calculate the normalized values of qj's
        qNormList = []
        g = sum(self._qList)
        for j in range(0, self._c + 1):
            qNorm = self._qList[j] / g
            qNormList.append(qNorm)
        return qNormList

    def _calc_ykj(self):
        # Calculate the values of yk(j)'s and store them in a two-dimensional list
        ykjList = []
        for i in range (0, self._k):
            yjList = []
            for j in range(0, self._c + 1):
                y = 0
                if (j > self._c - (self._bList[i] - self._brList[i]) and j - self._brList[i]) >= 0 and self._qList[j] > 0:
                    y = self._arList[i] * self._qList[j - self._brList[i]] / self._qList[j]
                yjList.append(y)
            ykjList.append(yjList)
        return ykjList

    def _calc_pbk(self):
        # Calculate the Time Congestion Probabilities = Call Blocking Probabilities
        pbList = []
        for i in range (0, self._k):
            pb = 0
            minj = self._c - self._bList[i] - self._tList[i] + 1
            for j in range (minj, self._c + 1):
                pb += self._qNormList[j]
            pbList.append(pb)
        return pbList

    def _calc_u(self):
        # Calculate the link utilization
        u = 0
        for j in range(1, self._c + 1):
            u += j * self._qNormList[j]
        return u
    
    def _update_obj(self):
        # Update the object when an instance variable changes
        self._qList = self._calc_qj()
        self._qNormList = self._calc_norm_qj()
        self._ykj = self._calc_ykj()
        self._pbk = self._calc_pbk()
        self._u = self._calc_u()
    
    # Setters/Getters
    def set_c(self, c):
        # Set the total capacity of the system (after the object instantiation) and update the object
        self._c = c
        self._update_obj()
    
    def set_k(self, k):
        # Set the number of service classes (after the object instantiation) and update the object
        self._k = k
        self._update_obj()

    def set_bList(self, bList):
        # Set the bandwidth requirement (in units) of service classes and update the object
        self._bList = bList
        self._update_obj()

    def set_aLists(self, aList, arList):
        # Set the traffic loads and update the object. Empty the lList and mList
        self._aList = aList
        self._arList = aList
        self._lList = None
        self._mList = None
        self._update_obj()

    def set_tList(self, tList):
        # Set the trunk reservation of service classes and update the object
        self._tList = tList
        self._update_obj()
        
    def set_lList_mLists(self, lList, mList, mrList):
        # Set the arrival rates and service times and update the object
        self._lList = lList
        self._mList = mList
        self._mrList = mrList
        self._aList = self._calc_ak(mList)
        self._arList = self._calc_ak(mrList)
        self._update_obj()
        
    def get_q(self):
        # Get q values
        return self._qList
    
    def get_qNorm(self):
        # Get q normalized values
        return self._qNormList
    
    def get_ykj(self):
        # Get ykj values
        return self._ykj
    
    def get_pbk(self):
        # Get call blocking probabilities
        return self._pbk
    
    def get_u(self):
        # Get link utilization value
        return self._u
