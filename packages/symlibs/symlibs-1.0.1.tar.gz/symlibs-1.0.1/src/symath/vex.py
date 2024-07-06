#!/usr/bin/python
# coding=utf-8

class Vec:
    def __init__ (self, *val, ln = 0):
        self.__val = []
        if ln > 0:
            for i in range(ln):
                if i >= len(val):
                    self.__val.append(None)
                else:
                    self.__val.append(val[i])
        else:
            for v in val:
                self.__val.append(v)
    def __del__ (self):
        del self.__val
    def __setitem__ (self, idx, val):
        _idx = self.__getIdx(idx)
        try:
            self.__val[_idx] = val
            return self.__val[_idx]
        except IndexError as e:
            self.__out_indexerr(idx, _idx, e)
    def __getitem__ (self, idx):
        _idx = self.__getIdx(idx)
        try:
            return self.__val[_idx]
        except IndexError as e:
            self.__out_indexerr(idx, _idx, e)
    def __len__ (self):
        return len(self.__val)
    def __add__ (self, val):
        ret = Vec(ln = self.__len())
        if type(val) == Vec:
            for i in range(min(len(val), self.__len())):
                ret[i] = self.__val[i] + val[i]
        else:
            for i in range(self.__len()):
                ret[i] = self.__val[i] + val
        return ret
    def __sub__ (self, val):
        ret = Vec(ln = self.__len())
        if type(val) == Vec:
            for i in range(min(len(val), self.__len())):
                ret[i] = self.__val[i] - val[i]
        else:
            for i in range(self.__len()):
                ret[i] = self.__val[i] - val
        return ret
    def __mul__ (self, val):
        ret = Vec(ln = self.__len())
        if type(val) == Vec:
            for i in range(min(len(val), self.__len())):
                ret[i] = self.__val[i] * val[i]
        else:
            for i in range(self.__len()):
                ret[i] = self.__val[i] * val
        return ret
    def __truediv__ (self, val):
        ret = Vec(ln = self.__len())
        if type(val) == Vec:
            for i in range(min(len(val), self.__len())):
                ret[i] = self.__val[i] / val[i]
        else:
            for i in range(self.__len()):
                ret[i] = self.__val[i] / val
        return ret
    def __mod__ (self, val):
        ret = Vec(ln = self.__len())
        if type(val) == Vec:
            for i in range(min(len(val), self.__len())):
                ret[i] = self.__val[i] % val[i]
        else:
            for i in range(self.__len()):
                ret[i] = self.__val[i] % val
        return ret
    def __pow__ (self, val):
        ret = Vec(ln = len(self))
        if type(val) == Vec:
            for i in range(min(len(val), len(self))):
                ret[i] = self.__val[i] ** val[i]
        else:
            for i in range(len(self)):
                ret[i] = self.__val[i] ** val
        return ret
    def __cmp__ (self, val):
        if type(val) == Vec:
            if len(self) > len(val): return 1
            elif len(self) < len(val): return -1
            else:
                for i in range(len(self)):
                    try:
                        if val[i] < self[i]: return 1
                        elif val[i] > self[i]: return -1
                    except TypeError:
                        if type(val[i]) == type(self[i]): 
                            try:
                                if not val[i] == self[i]: return 2
                            except TypeError:
                                try:
                                    if val[i] != self[i]: return 2
                                except TypeError:
                                    return 2
                            return 0
                        else:
                            return 2
                    return 0
        else:
            raise TypeError(f"Try comparing Vec with {type(val)}.")
        return ret
    def __eq__ (self, val):
        return self.__cmp__(val) == 0
    def __nq__ (self, val):
        return not self == val
    def __lt__ (self, val):
        return self.__cmp__(val) == -1
    def __le__ (self, val):
        return self < val or self == val
    def __gt__ (self, val):
        return self.__cmp__(val) == 1
    def __ge__ (self, val):
        return self > val or self == val
    def tuple (self):
        return tuple(self.__val)
    def __getIdx (self, x):
        def err ():
            raise IndexError("The index must be an integer within the length "
                +"or one of \"x\", \"y\", \"z\", or \"w\" (case insensitive).")
        if type(x) == int:
            if x >= 0: return x
        if type(x) == str:
            match(x.low()):
                case 'x': return 0;
                case 'y': return 1;
                case 'z': return 2;
                case 'w': return 4;
        err()
    def __out_indexerr(self, idx, _idx, e):
        if type(idx) == int:
            raise IndexError("Access out of bounds! Vec has a dimension"
                + f"of {len(self.__val)}, but attempting to access "
                + f"{idx}.") from e
        else:
            raise IndexError("Access out of bounds! Vec has a dimension"
                + f"of {len(self.__val)}, but attempting to access "
                + f"{_idx} ({idx}).") from e
class Vec2:
    def __init__ (self):
        self = Vec(ln = 2)
class Vec3:
    def __init__ (self):
        self = Vec(ln = 3)

