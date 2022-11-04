def getDecision(dfrow):
    if dfrow['volume'] <= 34445000.0:
        if dfrow['close'] <= 84.34:
            if dfrow['adj_close'] <= 60.44:
                if dfrow['high'] <= 51.86:
                    return 1
                else:  # if dfrow['high'] > 51.86
                    if dfrow['low'] <= 51.56:
                        return 0
                    else:  # if dfrow['low'] > 51.56
                        return 1
            else:  # if dfrow['adj_close'] > 60.44
                if dfrow['high'] <= 72.12:
                    return 1
                else:  # if dfrow['high'] > 72.12
                    if dfrow['low'] <= 71.06:
                        return 0
                    else:  # if dfrow['low'] > 71.06
                        return 1
        else:  # if dfrow['close'] > 84.34
            if dfrow['volume'] <= 19300000.0:
                return 1
            else:  # if dfrow['volume'] > 19300000.0
                if dfrow['low'] <= 137.58:
                    if dfrow['high'] <= 130.17:
                        if dfrow['close'] <= 115.1:
                            return 0
                        else:  # if dfrow['close'] > 115.1
                            return 1
                    else:  # if dfrow['high'] > 130.17
                        return 0
                else:  # if dfrow['low'] > 137.58
                    return 1
    else:  # if dfrow['volume'] > 34445000.0
        if dfrow['low'] <= 55.43:
            return 0
        else:  # if dfrow['low'] > 55.43
            if dfrow['low'] <= 101.18:
                return 1
            else:  # if dfrow['low'] > 101.18
                if dfrow['adj_close'] <= 136.28:
                    return 0
                else:  # if dfrow['adj_close'] > 136.28
                    return 1
