def getDecision(dfrow):
    if dfrow['volume'] <= 2917500.0:
        if dfrow['close'] <= 248.75:
            if dfrow['adj_close'] <= 189.42:
                if dfrow['close'] <= 161.09:
                    if dfrow['low'] <= 151.6:
                        return 1
                    else:  # if dfrow['low'] > 151.6
                        if dfrow['high'] <= 156.63:
                            return 0
                        else:  # if dfrow['high'] > 156.63
                            if dfrow['adj_close'] <= 153.18:
                                return 1
                            else:  # if dfrow['adj_close'] > 153.18
                                return 0
                else:  # if dfrow['close'] > 161.09
                    return 1
            else:  # if dfrow['adj_close'] > 189.42
                if dfrow['close'] <= 213.15:
                    return 0
                else:  # if dfrow['close'] > 213.15
                    if dfrow['open'] <= 237.02:
                        if dfrow['volume'] <= 2321950.0:
                            return 1
                        else:  # if dfrow['volume'] > 2321950.0
                            return 0
                    else:  # if dfrow['open'] > 237.02
                        if dfrow['adj_close'] <= 239.29:
                            return 0
                        else:  # if dfrow['adj_close'] > 239.29
                            return 1
        else:  # if dfrow['close'] > 248.75
            return 1
    else:  # if dfrow['volume'] > 2917500.0
        if dfrow['adj_close'] <= 225.46:
            if dfrow['high'] <= 192.94:
                if dfrow['volume'] <= 3762350.0:
                    return 1
                else:  # if dfrow['volume'] > 3762350.0
                    return 0
            else:  # if dfrow['high'] > 192.94
                return 0
        else:  # if dfrow['adj_close'] > 225.46
            return 1
