def getDecision(dfrow):
    if dfrow['high'] <= 69.75:
        if dfrow['volume'] <= 42870000.0:
            return 0
        else:  # if dfrow['volume'] > 42870000.0
            return 1
    else:  # if dfrow['high'] > 69.75
        if dfrow['adj_close'] <= 171.94:
            if dfrow['adj_close'] <= 124.2:
                if dfrow['adj_close'] <= 118.59:
                    if dfrow['high'] <= 103.76:
                        if dfrow['low'] <= 92.67:
                            if dfrow['volume'] <= 132973612.0:
                                if dfrow['high'] <= 86.34:
                                    return 1
                                else:  # if dfrow['high'] > 86.34
                                    if dfrow['close'] <= 88.56:
                                        return 0
                                    else:  # if dfrow['close'] > 88.56
                                        return 1
                            else:  # if dfrow['volume'] > 132973612.0
                                return 0
                        else:  # if dfrow['low'] > 92.67
                            return 1
                    else:  # if dfrow['high'] > 103.76
                        return 0
                else:  # if dfrow['adj_close'] > 118.59
                    return 1
            else:  # if dfrow['adj_close'] > 124.2
                if dfrow['close'] <= 157.83:
                    if dfrow['high'] <= 144.8:
                        if dfrow['close'] <= 130.76:
                            return 0
                        else:  # if dfrow['close'] > 130.76
                            return 1
                    else:  # if dfrow['high'] > 144.8
                        return 0
                else:  # if dfrow['close'] > 157.83
                    if dfrow['volume'] <= 62855000.0:
                        return 0
                    else:  # if dfrow['volume'] > 62855000.0
                        return 1
        else:  # if dfrow['adj_close'] > 171.94
            return 1
