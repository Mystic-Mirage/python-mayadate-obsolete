import datetime


CORRELATION_GMT = 584283
CORRELATION_TL = 584285

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


def _date2longcount(gregorian_date, correlation=CORRELATION_GMT):
    if not isinstance(gregorian_date, datetime.date):
        raise ValueError(
            "argument must be 'datetime.date' object",
            type(gregorian_date).__name__
        )
    ordinal = gregorian_date.toordinal() + 1721425 - correlation
    return _ord2longcount(ordinal)


def _longcount2ord(*args):
    longcount = _longcount(*args)
    piktun, baktun, katun, tun, winal, kin = longcount
    ordinal = piktun
    ordinal = 20 * ordinal + baktun
    ordinal = 20 * ordinal + katun
    ordinal = 20 * ordinal + tun
    ordinal = 18 * ordinal + winal
    ordinal = 20 * ordinal + kin
    return ordinal


def _longcount(*args):
    args_len = len(args)
    if args_len == 5:
        piktun = 0
        baktun, katun, tun, winal, kin = args
    elif args_len == 6:
        piktun, baktun, katun, tun, winal, kin = args
    else:
        raise ValueError(
            'long count # of arguments must be 5 or 6',
            args_len
        )
    return piktun, baktun, katun, tun, winal, kin


def _maya2date(maya_date):
    ordinal = maya_date.daynum - 1721425 + maya_date.correlation
    return datetime.date.fromordinal(ordinal)


def _ord2longcount(ordinal):
    dividend = ordinal
    longcount = []
    for ratio in (2880000, 144000, 7200, 360, 20, 1):
        quotient, dividend = divmod(dividend, ratio)
        longcount.append(quotient)
    return tuple(longcount)


def _ord2haab(ordinal):
    haab = divmod((ordinal + 348) % 365, 20)
    return haab[0] + 1, haab[1]


def _ord2tzolkin(ordinal):
    return (ordinal + 19) % 20 + 1, (ordinal + 3) % 13 + 1


class date:

    __slots__ = (
        '_piktun',
        '_baktun',
        '_katun',
        '_tun',
        '_winal',
        '_kin',
    )

    correlation = CORRELATION_GMT

    @classmethod
    def fromdaynum(cls, ordinal):
        longcount = _ord2longcount(ordinal)
        return cls(*longcount)

    @classmethod
    def fromgregorian(cls, gregorian_date, correlation=None):
        if correlation is None:
            correlation_init = CORRELATION_GMT
        else:
            correlation_init = correlation
        longcount = _date2longcount(gregorian_date, correlation_init)
        maya = cls(*longcount)
        if correlation is not None:
            maya.correlation = correlation
        return maya

    def __new__(cls, *args):
        piktun, baktun, katun, tun, winal, kin = _longcount(*args)
        _check_longcount_fields(piktun, baktun, katun, tun, winal, kin)
        self = object.__new__(cls)
        self._piktun = piktun
        self._baktun = baktun
        self._katun = katun
        self._tun = tun
        self._winal = winal
        self._kin = kin
        return self

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
            self.ybearerstr,
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
    def haabsrt(self):
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
