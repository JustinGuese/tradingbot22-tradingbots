def getDecision(dfrow):
    if dfrow['volume'] <= 1067634048.0:
        if dfrow['high'] <= 3.75:
            return 0
        else:  # if dfrow['high'] > 3.75
            if dfrow['adj_close'] <= 50.09:
                if dfrow['high'] <= 37.12:
                    if dfrow['open'] <= 13.88:
                        if dfrow['volume'] <= 66569404.0:
                            if dfrow['open'] <= 3.9:
                                return 1
                            else:  # if dfrow['open'] > 3.9
                                if dfrow['low'] <= 11.12:
                                    return 0
                                else:  # if dfrow['low'] > 11.12
                                    if dfrow['volume'] <= 55466532.0:
                                        return 1
                                    else:  # if dfrow['volume'] > 55466532.0
                                        return 0
                        else:  # if dfrow['volume'] > 66569404.0
                            return 1
                    else:  # if dfrow['open'] > 13.88
                        if dfrow['adj_close'] <= 17.84:
                            return 0
                        else:  # if dfrow['adj_close'] > 17.84
                            return 0
                else:  # if dfrow['high'] > 37.12
                    return 1
            else:  # if dfrow['adj_close'] > 50.09
                if dfrow['adj_close'] <= 107.91:
                    if dfrow['close'] <= 61.5:
                        return 0
                    else:  # if dfrow['close'] > 61.5
                        if dfrow['high'] <= 66.7:
                            return 1
                        else:  # if dfrow['high'] > 66.7
                            return 0
                else:  # if dfrow['adj_close'] > 107.91
                    return 1
    else:  # if dfrow['volume'] > 1067634048.0
        if dfrow['low'] <= 86.49:
            return 1
        else:  # if dfrow['low'] > 86.49
            return 1
