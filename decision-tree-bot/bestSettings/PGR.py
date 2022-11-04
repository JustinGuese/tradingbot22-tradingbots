def getDecision(dfrow):
    if dfrow['volume'] <= 2205400.0:
        if dfrow['open'] <= 58.76:
            return 1
        else:  # if dfrow['open'] > 58.76
            if dfrow['high'] <= 125.59:
                return 1
            else:  # if dfrow['high'] > 125.59
                return 1
    else:  # if dfrow['volume'] > 2205400.0
        if dfrow['volume'] <= 4550550.0:
            if dfrow['high'] <= 59.15:
                if dfrow['volume'] <= 4282250.0:
                    return 1
                else:  # if dfrow['volume'] > 4282250.0
                    return 0
            else:  # if dfrow['high'] > 59.15
                if dfrow['adj_close'] <= 51.71:
                    return 0
                else:  # if dfrow['adj_close'] > 51.71
                    if dfrow['adj_close'] <= 82.12:
                        if dfrow['high'] <= 81.24:
                            return 1
                        else:  # if dfrow['high'] > 81.24
                            return 1
                    else:  # if dfrow['adj_close'] > 82.12
                        if dfrow['close'] <= 123.72:
                            if dfrow['high'] <= 89.22:
                                return 0
                            else:  # if dfrow['high'] > 89.22
                                if dfrow['volume'] <= 2285600.0:
                                    return 0
                                else:  # if dfrow['volume'] > 2285600.0
                                    if dfrow['open'] <= 123.49:
                                        if dfrow['adj_close'] <= 112.95:
                                            return 1
                                        else:  # if dfrow['adj_close'] > 112.95
                                            return 1
                                    else:  # if dfrow['open'] > 123.49
                                        return 0
                        else:  # if dfrow['close'] > 123.72
                            return 1
        else:  # if dfrow['volume'] > 4550550.0
            return 0
