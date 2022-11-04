def getDecision(dfrow):
    if dfrow['high'] <= 117.28:
        if dfrow['low'] <= 37.74:
            return 0
        else:  # if dfrow['low'] > 37.74
            if dfrow['adj_close'] <= 67.06:
                if dfrow['volume'] <= 60680400.0:
                    if dfrow['volume'] <= 28860400.0:
                        return 1
                    else:  # if dfrow['volume'] > 28860400.0
                        return 1
                else:  # if dfrow['volume'] > 60680400.0
                    return 0
            else:  # if dfrow['adj_close'] > 67.06
                return 1
    else:  # if dfrow['high'] > 117.28
        if dfrow['volume'] <= 43603750.0:
            if dfrow['close'] <= 132.18:
                return 0
            else:  # if dfrow['close'] > 132.18
                if dfrow['high'] <= 194.31:
                    return 1
                else:  # if dfrow['high'] > 194.31
                    if dfrow['volume'] <= 38175650.0:
                        if dfrow['close'] <= 221.01:
                            return 0
                        else:  # if dfrow['close'] > 221.01
                            return 1
                    else:  # if dfrow['volume'] > 38175650.0
                        return 0
        else:  # if dfrow['volume'] > 43603750.0
            if dfrow['adj_close'] <= 244.76:
                if dfrow['open'] <= 216.13:
                    if dfrow['volume'] <= 77591152.0:
                        if dfrow['adj_close'] <= 169.78:
                            return 0
                        else:  # if dfrow['adj_close'] > 169.78
                            return 0
                    else:  # if dfrow['volume'] > 77591152.0
                        return 1
                else:  # if dfrow['open'] > 216.13
                    return 0
            else:  # if dfrow['adj_close'] > 244.76
                return 1
