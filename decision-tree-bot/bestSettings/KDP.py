def getDecision(dfrow):
    if dfrow['adj_close'] <= 13.14:
        return 0
    else:  # if dfrow['adj_close'] > 13.14
        if dfrow['close'] <= 38.15:
            if dfrow['volume'] <= 4810600.0:
                if dfrow['high'] <= 29.2:
                    if dfrow['close'] <= 23.07:
                        return 0
                    else:  # if dfrow['close'] > 23.07
                        if dfrow['volume'] <= 2373550.0:
                            if dfrow['volume'] <= 1296950.0:
                                return 0
                            else:  # if dfrow['volume'] > 1296950.0
                                return 1
                        else:  # if dfrow['volume'] > 2373550.0
                            return 0
                else:  # if dfrow['high'] > 29.2
                    if dfrow['volume'] <= 3691050.0:
                        return 1
                    else:  # if dfrow['volume'] > 3691050.0
                        return 1
            else:  # if dfrow['volume'] > 4810600.0
                if dfrow['open'] <= 37.31:
                    if dfrow['close'] <= 35.5:
                        return 0
                    else:  # if dfrow['close'] > 35.5
                        if dfrow['high'] <= 36.68:
                            return 1
                        else:  # if dfrow['high'] > 36.68
                            if dfrow['adj_close'] <= 37.2:
                                return 0
                            else:  # if dfrow['adj_close'] > 37.2
                                return 1
                else:  # if dfrow['open'] > 37.31
                    if dfrow['adj_close'] <= 37.39:
                        return 0
                    else:  # if dfrow['adj_close'] > 37.39
                        if dfrow['open'] <= 38.55:
                            return 1
                        else:  # if dfrow['open'] > 38.55
                            return 0
        else:  # if dfrow['close'] > 38.15
            return 1
