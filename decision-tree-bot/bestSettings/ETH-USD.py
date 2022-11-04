def getDecision(dfrow):
    if dfrow['volume'] <= 2595545088.0:
        if dfrow['volume'] <= 1077244992.0:
            return 1
        else:  # if dfrow['volume'] > 1077244992.0
            if dfrow['low'] <= 206.53:
                return 0
            else:  # if dfrow['low'] > 206.53
                if dfrow['open'] <= 231.49:
                    return 1
                else:  # if dfrow['open'] > 231.49
                    if dfrow['close'] <= 620.09:
                        return 0
                    else:  # if dfrow['close'] > 620.09
                        return 1
    else:  # if dfrow['volume'] > 2595545088.0
        if dfrow['adj_close'] <= 135.05:
            if dfrow['volume'] <= 4250621568.0:
                return 1
            else:  # if dfrow['volume'] > 4250621568.0
                return 0
        else:  # if dfrow['adj_close'] > 135.05
            if dfrow['open'] <= 1048.14:
                if dfrow['volume'] <= 7683760384.0:
                    if dfrow['volume'] <= 5441296384.0:
                        return 1
                    else:  # if dfrow['volume'] > 5441296384.0
                        if dfrow['low'] <= 230.96:
                            return 0
                        else:  # if dfrow['low'] > 230.96
                            return 1
                else:  # if dfrow['volume'] > 7683760384.0
                    if dfrow['adj_close'] <= 389.07:
                        return 1
                    else:  # if dfrow['adj_close'] > 389.07
                        return 1
            else:  # if dfrow['open'] > 1048.14
                if dfrow['volume'] <= 28023304192.0:
                    if dfrow['high'] <= 3179.42:
                        return 0
                    else:  # if dfrow['high'] > 3179.42
                        return 1
                else:  # if dfrow['volume'] > 28023304192.0
                    return 1
