def getDecision(dfrow):
    if dfrow['adj_close'] <= 261.74:
        return 0
    else:  # if dfrow['adj_close'] > 261.74
        if dfrow['high'] <= 466.13:
            if dfrow['low'] <= 415.08:
                if dfrow['low'] <= 372.23:
                    if dfrow['volume'] <= 1116950.0:
                        if dfrow['adj_close'] <= 285.77:
                            return 1
                        else:  # if dfrow['adj_close'] > 285.77
                            if dfrow['close'] <= 309.49:
                                return 0
                            else:  # if dfrow['close'] > 309.49
                                if dfrow['low'] <= 342.76:
                                    if dfrow['adj_close'] <= 321.93:
                                        return 1
                                    else:  # if dfrow['adj_close'] > 321.93
                                        return 1
                                else:  # if dfrow['low'] > 342.76
                                    if dfrow['open'] <= 367.79:
                                        if dfrow['adj_close'] <= 328.96:
                                            return 1
                                        else:  # if dfrow['adj_close'] > 328.96
                                            return 0
                                    else:  # if dfrow['open'] > 367.79
                                        return 1
                    else:  # if dfrow['volume'] > 1116950.0
                        if dfrow['close'] <= 323.41:
                            return 0
                        else:  # if dfrow['close'] > 323.41
                            return 1
                else:  # if dfrow['low'] > 372.23
                    return 1
            else:  # if dfrow['low'] > 415.08
                if dfrow['high'] <= 449.82:
                    return 0
                else:  # if dfrow['high'] > 449.82
                    if dfrow['open'] <= 454.04:
                        return 1
                    else:  # if dfrow['open'] > 454.04
                        return 0
        else:  # if dfrow['high'] > 466.13
            return 1
