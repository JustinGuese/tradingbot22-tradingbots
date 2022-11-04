def getDecision(dfrow):
    if dfrow['adj_close'] <= 198.92:
        if dfrow['volume'] <= 42567900.0:
            if dfrow['close'] <= 140.57:
                if dfrow['volume'] <= 26142500.0:
                    if dfrow['open'] <= 125.1:
                        return 1
                    else:  # if dfrow['open'] > 125.1
                        return 1
                else:  # if dfrow['volume'] > 26142500.0
                    return 1
            else:  # if dfrow['close'] > 140.57
                return 1
        else:  # if dfrow['volume'] > 42567900.0
            if dfrow['low'] <= 162.77:
                return 0
            else:  # if dfrow['low'] > 162.77
                return 1
    else:  # if dfrow['adj_close'] > 198.92
        if dfrow['volume'] <= 26313000.0:
            if dfrow['high'] <= 267.65:
                if dfrow['high'] <= 263.86:
                    return 1
                else:  # if dfrow['high'] > 263.86
                    return 0
            else:  # if dfrow['high'] > 267.65
                return 1
        else:  # if dfrow['volume'] > 26313000.0
            if dfrow['high'] <= 233.07:
                return 1
            else:  # if dfrow['high'] > 233.07
                if dfrow['adj_close'] <= 297.42:
                    return 0
                else:  # if dfrow['adj_close'] > 297.42
                    if dfrow['high'] <= 316.23:
                        if dfrow['close'] <= 303.69:
                            return 0
                        else:  # if dfrow['close'] > 303.69
                            return 1
                    else:  # if dfrow['high'] > 316.23
                        if dfrow['close'] <= 331.1:
                            return 0
                        else:  # if dfrow['close'] > 331.1
                            return 1
