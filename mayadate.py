import datetime
import struct


CORRELATION_GMT = 584283
CORRELATION_TL = 584285

_MAXORDINAL = 57599999

_TZOLKINNAMES = (
    None,
    "Imix'",
    "Ik'",
    "Ak'b'al",
    "K'an",
    "Chikchan",
    "Kimi",
    "Manik'",
    "Lamat",
    "Muluk",
    "Ok",
    "Chuwen",
    "Eb'",
    "B'en",
    "Ix",
    "Men",
    "K'ib'",
    "Kab'an",
    "Etz'nab'",
    "Kawak",
    "Ajaw"
)

_HAABNAMES = (
    None,
    "Pop",
    "Wo",
    "Sip",
    "Sotz'",
    "Tzek",
    "Xul",
    "Yaxk'",
    "Mol",
    "Ch'en",
    "Yax",
    "Sac",
    "Keh",
    "Mak",
    "K'ank'in",
    "Muwan",
    "Pax",
    "K'ayab'",
    "Kumk'u",
    "Wayeb'"
)

_LORDOFNIGHTNAMES = (
    None,
    'G1',
    'G2',
    'G3',
    'G4',
    'G5',
    'G6',
    'G7',
    'G8',
    'G9'
)


def _check_longcount_fields(piktun, baktun, katun, tun, winal, kin):
    if not all([
        isinstance(piktun, int),
        isinstance(baktun, int),
        isinstance(katun, int),
        isinstance(tun, int),
        isinstance(winal, int),
        isinstance(kin, int),
    ]):
        raise TypeError('int expected')
    if not 0 <= piktun <= 19:
        raise ValueError('piktun must be in 0..19', piktun)
    if not 0 <= baktun <= 19:
        raise ValueError('baktun must be in 0..19', baktun)
    if not 0 <= katun <= 19:
        raise ValueError('katun must be in 0..19', katun)
    if not 0 <= tun <= 19:
        raise ValueError('tun must be in 0..19', tun)
    if not 0 <= winal <= 17:
        raise ValueError('winal must be in 0..17', winal)
    if not 0 <= kin <= 19:
        raise ValueError('kin must be in 0..19', kin)


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def _date2longcount(gdate, correlation):
    if not isinstance(gdate, datetime.date):
        raise ValueError(
            "argument must be 'datetime.date' object",
            type(gdate).__name__
        )
    o = gdate.toordinal() + 1721425 - correlation
    return _ord2longcount(o)


_DAYS_IN_MONTH = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

_DAYS_AFTER_MONTH = []
dbm = 0
for dim in reversed(_DAYS_IN_MONTH[1:]):
    _DAYS_AFTER_MONTH.append(dbm)
    dbm += dim
del dbm, dim
_DAYS_AFTER_MONTH.append(None)
_DAYS_AFTER_MONTH.reverse()


def _is_leap(year):
    y = year + 1
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def _days_after_year(year):
    y = year + 1
    return -(y * 365 + y // 4 - y // 100 + y // 400)


def _days_in_month(year, month):
    assert 1 <= month <= 12, month
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


def _days_after_month(year, month):
    assert 1 <= month <= 12, 'month must be in 1..12'
    return _DAYS_AFTER_MONTH[month] - (month < 2 and _is_leap(year))


def _days_after_day(year, month, day):
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, ('day must be in 1..%d' % dim)
    return dim - day


def _bc2gregorianord(year, month, day):
    return -(
        _days_after_year(year) +
        _days_after_month(year, month) +
        _days_after_day(year, month, day)
    )


def _bc2longcount(year, month, day, correlation):
    o = _bc2gregorianord(year, month, day) + 1721425 - correlation
    return _ord2longcount(o)


def _longcount2ord(*args):
    l = _longcount(*args)
    piktun, baktun, katun, tun, winal, kin = l
    o = piktun
    o = 20 * o + baktun
    o = 20 * o + katun
    o = 20 * o + tun
    o = 18 * o + winal
    o = 20 * o + kin
    return o


def _longcount(*args):
    len_args = len(args)
    if len_args == 5:
        piktun = 0
        baktun, katun, tun, winal, kin = args
    elif len_args == 6:
        piktun, baktun, katun, tun, winal, kin = args
    else:
        raise ValueError(
            'long count # of arguments must be 5 or 6',
            len_args
        )
    return piktun, baktun, katun, tun, winal, kin


def _maya2date(mdate):
    o = mdate.daynum - 1721425 + mdate.correlation
    return datetime.date.fromordinal(o)


def _ord2longcount(o):
    assert 0 <= o <= _MAXORDINAL, 'ordinal must be in 1..%d' % (_MAXORDINAL)
    d = o
    l = []
    for r in (2880000, 144000, 7200, 360, 20, 1):
        q, d = divmod(d, r)
        l.append(q)
    return tuple(l)


def _ord2haab(o):
    haab = divmod((o + 348) % 365, 20)
    return haab[0] + 1, haab[1]


def _ord2tzolkin(o):
    return (o + 19) % 20 + 1, (o + 3) % 13 + 1


class date:

    __slots__ = (
        '_piktun',
        '_baktun',
        '_katun',
        '_tun',
        '_winal',
        '_kin',
        'correlation'
    )

    default_correlation = CORRELATION_GMT

    @classmethod
    def fromdaynum(cls, ordinal):
        longcount = _ord2longcount(ordinal)
        return cls(*longcount)

    @classmethod
    def fromgregorian(cls, *args, **kwargs):
        if 'correlation' in kwargs:
            correlation = kwargs['correlation']
        else:
            correlation = cls.default_correlation
        len_args = len(args)
        if len_args == 1:
            if isinstance(args[0], tuple):
                if len(args[0]) != 3:
                    raise ValueError('tuple must consist of 3 elements')
                year, month, day = args[0]
                if year < 0:
                    longcount = _bc2longcount(year, month, day, correlation)
                else:
                    gdate = datetime.date(year, month, day)
                    longcount = _date2longcount(gdate, correlation)
            elif isinstance(args[0], datetime.date):
                longcount = _date2longcount(args[0], correlation)
            else:
                raise ValueError(
                    "argument must be tuple or 'datetime.date' object"
                )
        elif len_args == 3:
            year, month, day = args
            if year < 0:
                longcount = _bc2longcount(year, month, day, correlation)
            else:
                gdate = datetime.date(year, month, day)
                longcount = _date2longcount(gdate, correlation)
        else:
            raise ValueError('argument # must be 1 or 3')
        return cls(*longcount, correlation=correlation)

    @classmethod
    def today(cls, correlation=None):
        today = datetime.date.today()
        return cls.fromgregorian(today, correlation)

    def __init__(self, *args, **kwargs):
        piktun, baktun, katun, tun, winal, kin = _longcount(*args)
        _check_longcount_fields(piktun, baktun, katun, tun, winal, kin)
        self._piktun = piktun
        self._baktun = baktun
        self._katun = katun
        self._tun = tun
        self._winal = winal
        self._kin = kin
        if 'correlation' in kwargs:
            self.correlation = kwargs['correlation']
        else:
            self.correlation = self.__class__.default_correlation

    def __repr__(self):
        if self._piktun > 0:
            return '%s(%d, %d, %d, %d, %d, %d)' % (
                'mayadate.' + self.__class__.__name__,
                self._piktun,
                self._baktun,
                self._katun,
                self._tun,
                self._winal,
                self._kin
            )
        else:
            return '%s(%d, %d, %d, %d, %d)' % (
                'mayadate.' + self.__class__.__name__,
                self._baktun,
                self._katun,
                self._tun,
                self._winal,
                self._kin
            )

    def __str__(self):
        return '%s | %s | %s | %s | %s' % (
            self.longcountstr,
            self.tzolkinstr,
            self.haabstr,
            self.yearbearerstr,
            self.lordofnightstr
        )

    @property
    def daynum(self):
        return _longcount2ord(
            self._piktun,
            self._baktun,
            self._katun,
            self._tun,
            self._winal,
            self._kin
        )

    @property
    def piktun(self):
        return self._piktun

    @property
    def baktun(self):
        return self._baktun

    @property
    def katun(self):
        return self._katun

    @property
    def tun(self):
        return self._tun

    @property
    def winal(self):
        return self._winal

    @property
    def kin(self):
        return self._kin

    @property
    def longcount(self):
        if self._piktun > 0:
            return (
                self._piktun,
                self._baktun,
                self._katun,
                self._tun,
                self._winal,
                self._kin
            )
        else:
            return (
                self._baktun,
                self._katun,
                self._tun,
                self._winal,
                self._kin
            )

    @property
    def longcountstr(self):
        if self._piktun > 0:
            return '%d.%d.%d.%d.%d.%d' % (
                self._piktun,
                self._baktun,
                self._katun,
                self._tun,
                self._winal,
                self._kin
            )
        else:
            return '%d.%d.%d.%d.%d' % (
                self._baktun,
                self._katun,
                self._tun,
                self._winal,
                self._kin
            )

    @property
    def tzolkin(self):
        return _ord2tzolkin(self.daynum)

    @property
    def tzolkinstr(self):
        tzolkin = self.tzolkin
        return '%d %s' % (tzolkin[1], _TZOLKINNAMES[tzolkin[0]])

    @property
    def haab(self):
        return _ord2haab(self.daynum)

    @property
    def haabstr(self):
        haab = self.haab
        return '%d %s' % (haab[1], _HAABNAMES[haab[0]])

    @property
    def yearbearer(self):
        daynum = self.daynum
        yearbearer = daynum - (daynum + 348) % 365
        return _ord2tzolkin(yearbearer)

    @property
    def yearbearerstr(self):
        ybearer = self.yearbearer
        return '%d %s' % (ybearer[1], _TZOLKINNAMES[ybearer[0]])

    @property
    def lordofnight(self):
        return (self.daynum + 8) % 9 + 1

    @property
    def lordofnightstr(self):
        return _LORDOFNIGHTNAMES[self.lordofnight]

    def togregorian(self):
        try:
            return _maya2date(self)
        except:
            raise OverflowError("can't convert to gregorian date")

    def _cmp(self, other):
        assert isinstance(other, date)
        piktun = self._piktun
        baktun = self._baktun
        katun = self._katun
        tun = self._tun
        winal = self._winal
        kin = self._kin
        piktun2 = other._piktun
        baktun2 = other._baktun
        katun2 = other._katun
        tun2 = other._katun
        winal2 = other._winal
        kin2 = other._winal
        return _cmp(
            (piktun, baktun, katun, tun, winal, kin),
            (piktun2, baktun2, katun2, tun2, winal2, kin2)
        )

        if isinstance(other, date):
            return self._cmp(other) == 0
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, date):
            return self._cmp(other) != 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, date):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, date):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) > 0
        return NotImplemented

    def __hash__(self):
        return hash(self._getstate())

    def __add__(self, other):
        if isinstance(other, delta):
            o = self.daynum + other.days
            if 0 <= o <= _MAXORDINAL:
                return date.fromdaynum(o)
            raise OverflowError("result out of range")
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, delta):
            return delta(-other.days) + self
        if isinstance(other, date):
            daynum1 = self.daynum
            daynum2 = other.daynum
            return delta(daynum1 - daynum2)
        return NotImplemented

    def _getstate(self):
        return struct.pack(
            'BBBBBB',
            self._piktun,
            self._baktun,
            self._katun,
            self._tun,
            self._winal,
            self._kin
        )


delta = datetime.timedelta
