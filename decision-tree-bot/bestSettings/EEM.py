def getDecision(dfrow):
    if dfrow['close'] <= 39.91:
        if dfrow['adj_close'] <= 35.11:
            if dfrow['low'] <= 34.89:
                return 0
            else:  # if dfrow['low'] > 34.89
                return 1
        else:  # if dfrow['adj_close'] > 35.11
            return 0
    else:  # if dfrow['close'] > 39.91
        if dfrow['volume'] <= 58618950.0:
            if dfrow['low'] <= 55.06:
                if dfrow['high'] <= 51.18:
                    if dfrow['volume'] <= 39346100.0:
                        return 1
                    else:  # if dfrow['volume'] > 39346100.0
                        if dfrow['adj_close'] <= 49.3:
                            return 1
                        else:  # if dfrow['adj_close'] > 49.3
                            return 1
                else:  # if dfrow['high'] > 51.18
                    return 0
            else:  # if dfrow['low'] > 55.06
                return 1
        else:  # if dfrow['volume'] > 58618950.0
            if dfrow['high'] <= 46.33:
                if dfrow['low'] <= 44.09:
                    if dfrow['adj_close'] <= 41.15:
                        return 0
                    else:  # if dfrow['adj_close'] > 41.15
                        return 0
                else:  # if dfrow['low'] > 44.09
                    return 1
            else:  # if dfrow['high'] > 46.33
                if dfrow['low'] <= 48.07:
                    return 0
                else:  # if dfrow['low'] > 48.07
                    if dfrow['adj_close'] <= 47.57:
                        if dfrow['adj_close'] <= 45.27:
                            return 0
                        else:  # if dfrow['adj_close'] > 45.27
                            return 1
                    else:  # if dfrow['adj_close'] > 47.57
                        return 0
