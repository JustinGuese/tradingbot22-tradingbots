def getDecision(dfrow):
    if dfrow['low'] <= 42.28:
        return 0
    else:  # if dfrow['low'] > 42.28
        if dfrow['close'] <= 106.55:
            if dfrow['volume'] <= 160690800.0:
                if dfrow['open'] <= 46.98:
                    if dfrow['adj_close'] <= 43.1:
                        return 1
                    else:  # if dfrow['adj_close'] > 43.1
                        return 0
                else:  # if dfrow['open'] > 46.98
                    return 1
            else:  # if dfrow['volume'] > 160690800.0
                if dfrow['low'] <= 74.17:
                    return 0
                else:  # if dfrow['low'] > 74.17
                    return 1
        else:  # if dfrow['close'] > 106.55
            if dfrow['volume'] <= 67360252.0:
                return 1
            else:  # if dfrow['volume'] > 67360252.0
                if dfrow['adj_close'] <= 171.77:
                    if dfrow['open'] <= 151.1:
                        if dfrow['high'] <= 148.15:
                            if dfrow['open'] <= 138.13:
                                if dfrow['close'] <= 130.29:
                                    return 1
                                else:  # if dfrow['close'] > 130.29
                                    return 1
                            else:  # if dfrow['open'] > 138.13
                                if dfrow['high'] <= 143.12:
                                    return 0
                                else:  # if dfrow['high'] > 143.12
                                    if dfrow['open'] <= 143.79:
                                        return 1
                                    else:  # if dfrow['open'] > 143.79
                                        return 0
                        else:  # if dfrow['high'] > 148.15
                            return 1
                    else:  # if dfrow['open'] > 151.1
                        return 0
                else:  # if dfrow['adj_close'] > 171.77
                    return 1
