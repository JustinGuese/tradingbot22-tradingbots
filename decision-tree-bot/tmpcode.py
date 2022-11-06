def getDecision(dfrow):
    if dfrow['volume'] <= 2239600.0:
        if dfrow['open'] <= 80.69:
            return 0
        else:  # if dfrow['open'] > 80.69
            if dfrow['close'] <= 109.79:
                if dfrow['close'] <= 90.45:
                    if dfrow['adj_close'] <= 83.76:
                        return 1
                    else:  # if dfrow['adj_close'] > 83.76
                        return 0
                else:  # if dfrow['close'] > 90.45
                    return 1
            else:  # if dfrow['close'] > 109.79
                if dfrow['volume'] <= 1323950.0:
                    return 1
                else:  # if dfrow['volume'] > 1323950.0
                    if dfrow['close'] <= 171.12:
                        if dfrow['open'] <= 141.89:
                            if dfrow['close'] <= 117.64:
                                return 1
                            else:  # if dfrow['close'] > 117.64
                                return 1
                        else:  # if dfrow['open'] > 141.89
                            if dfrow['close'] <= 148.06:
                                return 0
                            else:  # if dfrow['close'] > 148.06
                                if dfrow['high'] <= 156.11:
                                    return 1
                                else:  # if dfrow['high'] > 156.11
                                    return 1
                    else:  # if dfrow['close'] > 171.12
                        return 1
    else:  # if dfrow['volume'] > 2239600.0
        if dfrow['volume'] <= 3842650.0:
            if dfrow['close'] <= 89.31:
                return 0
            else:  # if dfrow['close'] > 89.31
                if dfrow['open'] <= 108.58:
                    return 1
                else:  # if dfrow['open'] > 108.58
                    return 0
        else:  # if dfrow['volume'] > 3842650.0
            return 0
