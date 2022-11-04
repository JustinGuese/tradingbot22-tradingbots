def getDecision(dfrow):
    if dfrow['volume'] <= 97917.0:
        if dfrow['high'] <= 72.03:
            if dfrow['low'] <= 53.05:
                if dfrow['low'] <= 44.47:
                    if dfrow['open'] <= 44.44:
                        if dfrow['volume'] <= 55776.0:
                            return 1
                        else:  # if dfrow['volume'] > 55776.0
                            return 0
                    else:  # if dfrow['open'] > 44.44
                        return 0
                else:  # if dfrow['low'] > 44.47
                    return 1
            else:  # if dfrow['low'] > 53.05
                if dfrow['close'] <= 65.72:
                    return 1
                else:  # if dfrow['close'] > 65.72
                    if dfrow['open'] <= 66.29:
                        return 0
                    else:  # if dfrow['open'] > 66.29
                        return 1
        else:  # if dfrow['high'] > 72.03
            if dfrow['adj_close'] <= 72.4:
                return 0
            else:  # if dfrow['adj_close'] > 72.4
                if dfrow['adj_close'] <= 78.03:
                    return 1
                else:  # if dfrow['adj_close'] > 78.03
                    return 1
    else:  # if dfrow['volume'] > 97917.0
        if dfrow['open'] <= 67.3:
            if dfrow['low'] <= 44.39:
                return 0
            else:  # if dfrow['low'] > 44.39
                if dfrow['volume'] <= 235556.0:
                    return 1
                else:  # if dfrow['volume'] > 235556.0
                    return 0
        else:  # if dfrow['open'] > 67.3
            if dfrow['low'] <= 76.64:
                return 0
            else:  # if dfrow['low'] > 76.64
                return 1
