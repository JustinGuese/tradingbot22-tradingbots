def getDecision(dfrow):
    if dfrow['adj_close'] <= 21.76:
        if dfrow['high'] <= 17.53:
            if dfrow['close'] <= 14.55:
                return 0
            else:  # if dfrow['close'] > 14.55
                return 1
        else:  # if dfrow['high'] > 17.53
            if dfrow['volume'] <= 71838000.0:
                return 1
            else:  # if dfrow['volume'] > 71838000.0
                return 0
    else:  # if dfrow['adj_close'] > 21.76
        if dfrow['volume'] <= 124977000.0:
            if dfrow['low'] <= 342.22:
                if dfrow['adj_close'] <= 309.87:
                    if dfrow['volume'] <= 49256250.0:
                        return 1
                    else:  # if dfrow['volume'] > 49256250.0
                        if dfrow['open'] <= 23.3:
                            return 1
                        else:  # if dfrow['open'] > 23.3
                            if dfrow['low'] <= 222.07:
                                return 0
                            else:  # if dfrow['low'] > 222.07
                                if dfrow['high'] <= 252.57:
                                    if dfrow['low'] <= 235.72:
                                        return 1
                                    else:  # if dfrow['low'] > 235.72
                                        return 1
                                else:  # if dfrow['high'] > 252.57
                                    if dfrow['adj_close'] <= 279.85:
                                        return 0
                                    else:  # if dfrow['adj_close'] > 279.85
                                        return 1
                else:  # if dfrow['adj_close'] > 309.87
                    return 0
            else:  # if dfrow['low'] > 342.22
                return 1
        else:  # if dfrow['volume'] > 124977000.0
            if dfrow['open'] <= 198.21:
                return 1
            else:  # if dfrow['open'] > 198.21
                return 1
