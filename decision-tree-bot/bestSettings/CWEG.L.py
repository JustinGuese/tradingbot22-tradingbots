def getDecision(dfrow):
    if dfrow['high'] <= 15895.82:
        return 0
    else:  # if dfrow['high'] > 15895.82
        if dfrow['adj_close'] <= 33535.0:
            if dfrow['low'] <= 33215.57:
                if dfrow['low'] <= 28603.25:
                    if dfrow['volume'] <= 1.5:
                        if dfrow['close'] <= 18775.0:
                            return 1
                        else:  # if dfrow['close'] > 18775.0
                            return 0
                    else:  # if dfrow['volume'] > 1.5
                        if dfrow['close'] <= 23888.75:
                            return 1
                        else:  # if dfrow['close'] > 23888.75
                            return 1
                else:  # if dfrow['low'] > 28603.25
                    if dfrow['low'] <= 29951.78:
                        if dfrow['high'] <= 29532.43:
                            if dfrow['close'] <= 28811.25:
                                return 0
                            else:  # if dfrow['close'] > 28811.25
                                if dfrow['adj_close'] <= 29443.75:
                                    return 1
                                else:  # if dfrow['adj_close'] > 29443.75
                                    if dfrow['adj_close'] <= 30012.5:
                                        return 0
                                    else:  # if dfrow['adj_close'] > 30012.5
                                        return 1
                        else:  # if dfrow['high'] > 29532.43
                            if dfrow['adj_close'] <= 29913.75:
                                return 0
                            else:  # if dfrow['adj_close'] > 29913.75
                                return 1
                    else:  # if dfrow['low'] > 29951.78
                        if dfrow['volume'] <= 383.0:
                            return 1
                        else:  # if dfrow['volume'] > 383.0
                            return 0
            else:  # if dfrow['low'] > 33215.57
                return 0
        else:  # if dfrow['adj_close'] > 33535.0
            return 1
