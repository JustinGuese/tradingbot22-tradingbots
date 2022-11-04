def getDecision(dfrow):
    if dfrow['volume'] <= 3067300.0:
        if dfrow['adj_close'] <= 284.6:
            return 1
        else:  # if dfrow['adj_close'] > 284.6
            if dfrow['close'] <= 533.15:
                if dfrow['open'] <= 515.77:
                    if dfrow['volume'] <= 1923000.0:
                        return 1
                    else:  # if dfrow['volume'] > 1923000.0
                        if dfrow['low'] <= 297.19:
                            return 0
                        else:  # if dfrow['low'] > 297.19
                            return 1
                else:  # if dfrow['open'] > 515.77
                    if dfrow['adj_close'] <= 518.42:
                        return 0
                    else:  # if dfrow['adj_close'] > 518.42
                        return 0
            else:  # if dfrow['close'] > 533.15
                return 1
    else:  # if dfrow['volume'] > 3067300.0
        if dfrow['low'] <= 235.6:
            if dfrow['high'] <= 214.57:
                return 1
            else:  # if dfrow['high'] > 214.57
                return 0
        else:  # if dfrow['low'] > 235.6
            if dfrow['close'] <= 505.35:
                if dfrow['low'] <= 381.56:
                    if dfrow['high'] <= 352.91:
                        return 1
                    else:  # if dfrow['high'] > 352.91
                        return 1
                else:  # if dfrow['low'] > 381.56
                    if dfrow['low'] <= 471.47:
                        return 0
                    else:  # if dfrow['low'] > 471.47
                        if dfrow['open'] <= 505.41:
                            return 1
                        else:  # if dfrow['open'] > 505.41
                            return 0
            else:  # if dfrow['close'] > 505.35
                return 1
