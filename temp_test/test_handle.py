import datetime


_shares = {}


def _handle(f_type):
    def wrapper(method):
        _shares[f_type] = method

        def wrapped(self, *args, **kwargs):
            return method(self, *args, **kwargs)

        return wrapped
    return wrapper


class KlineFinance():

    _shares = {

    }

    # @property
    # def trident(self):
    #     return Environment.get_instance().mod_dict["trident"]
    #
    # def fixed_factor(self, factor: Factor, instruments: list, start_time: datetime, end_time: datetime,
    #                  fqc=None, output: np.ndarray = None) -> np.ndarray:
    #
    #     pass

    @_handle("type1")
    def mv(self, instruments, start_time, end_time, output):
        print(instruments)
        print(start_time)
        print(end_time)
        print(output)


if __name__ == "__main__":
    codes = ["code1", "code2", "code3", "code4"]
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime(2019, 1, 1)
    output = None
    kf = KlineFinance()
    kf.mv(codes, start, end, output)
    print(_shares)

    pass



