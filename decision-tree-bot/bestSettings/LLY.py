def getDecision(dfrow):
    if dfrow['adj_close'] <= 71.09:
        return 0
    else:  # if dfrow['adj_close'] > 71.09
        if dfrow['adj_close'] <= 321.2:
            if dfrow['low'] <= 288.41:
                if dfrow['high'] <= 262.46:
                    if dfrow['high'] <= 230.04:
                        if dfrow['adj_close'] <= 185.15:
                            if dfrow['low'] <= 179.58:
                                if dfrow['close'] <= 156.71:
                                    if dfrow['open'] <= 148.07:
                                        if dfrow['close'] <= 118.49:
                                            if dfrow['high'] <= 107.3:
                                                if dfrow['adj_close'] <= 78.74:
                                                    return 1
                                                else:  # if dfrow['adj_close'] > 78.74
                                                    return 1
                                            else:  # if dfrow['high'] > 107.3
                                                if dfrow['close'] <= 110.17:
                                                    return 0
                                                else:  # if dfrow['close'] > 110.17
                                                    return 1
                                        else:  # if dfrow['close'] > 118.49
                                            return 1
                                    else:  # if dfrow['open'] > 148.07
                                        return 0
                                else:  # if dfrow['close'] > 156.71
                                    return 1
                            else:  # if dfrow['low'] > 179.58
                                return 0
                        else:  # if dfrow['adj_close'] > 185.15
                            return 1
                    else:  # if dfrow['high'] > 230.04
                        if dfrow['volume'] <= 1997900.0:
                            return 1
                        else:  # if dfrow['volume'] > 1997900.0
                            return 0
                else:  # if dfrow['high'] > 262.46
                    return 1
            else:  # if dfrow['low'] > 288.41
                return 0
        else:  # if dfrow['adj_close'] > 321.2
            return 1
