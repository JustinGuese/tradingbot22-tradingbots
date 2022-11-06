def getDecision(dfrow):
    if dfrow['momentum_rsi'] <= 49.93:
        if dfrow['trend_cci'] <= -16.52:
            return 0
        else:  # if dfrow['trend_cci'] > -16.52
            return 1
    else:  # if dfrow['momentum_rsi'] > 49.93
        if dfrow['momentum_ao'] <= 0.0:
            return 1
        else:  # if dfrow['momentum_ao'] > 0.0
            if dfrow['volume_vwap'] <= 169.4:
                return 1
            else:  # if dfrow['volume_vwap'] > 169.4
                return 1
