from functions import get_basenumber_from_int, get_int_from_basenumber, split, cut, onlycontains, reverse

#change path name
#_handler = DataBaseHandler("macAddressDatas/", [], 0)
#_handler.verify()

#_handler.add("", "", [], False, "b")
#_hanlder.add("", "", [], False, "b")
#..add the constructors ids an their datas.
#download from 
#..
#http://standards-oui.ieee.org/oui.txt
#....

MAC48 = 48
MAC64 = 60

#Format : unicast(bool), globbaly, oui, nic, clearmac, bin
#TODO -> OUI with organization name in a table/dict

def mac_address(address):
    try:
        return Mac48Address(address)
    except:
        try:
            return Mac64Address(address)
        except:
            msg = "Unable to create an mac 48 or mac 64 address with address {0}".format(address)
            raise MacAddressValueError(msg)

def get_organization_from_organization_unique_identifier(oui=""):
    if oui != "": pass    
    raise OUIValueError("Can't get the name of an organization from an empty string")

class MacAddressValueError(ValueError):
    pass

class OUIValueError(ValueError):
    pass

class _MacBase:
    @property
    def version(self):
        msg = "Version not implemented"
        raise NotImplementedError(msg)
    @property
    def address(self):
        msg = "Address not implemented"
        raise NotImplementedError(msg)
    @property
    def unicast(self):
        msg = "Address not implemented, no unicast"
        raise NotImplementedError(msg)
    @property
    def organization_unique_identifier(self):
        msg = "Address not implemented, no OUI"
        raise NotImplementedError(msg)
    @property
    def nic(self):
        msg = "Address not implemented, no NIC"
        raise NotImplementedError(msg)
    @property
    def globally_unique(self):
        msg = "Address not implemented, no global/non-global"
        raise NotImplementedError(msg)
    @property
    def reversed(self):
        msg = "Address not implemented, can't reverse it"
        raise NotImplementedError(msg)
    def _check_int_adress(self, address):
        if onlycontains(address, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
            if int(address) > 2**MAC48-1 and int(address) > 2**MAC64-1:
                msg = "Address {0} has too high value".format(address)
                raise MacAddressValueError(msg)
        if not onlycontains(address, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
            msg = "Address {0} contains invalid characters for an integer".format(address)
            raise MacAddressValueError(msg)
    
    def _check_binary_address(self, address):
        if len(address) > MAC48 and len(address) > MAC64:
            msg = "Binary address {0} is too long".format(address)
            raise MacAddressValueError(msg)
        if not onlycontains(address, ["0", "1"]):
            msg = "Invalid binary address {0}".format(address)
            raise MacAddressValueError(msg)

    def _check_string_address(self, address):
        splittedwith2 = split(address, [":"])
        splittedwithone = split(address, ["-"])
        splitted = None
        if len(splittedwith2) >= len(splittedwithone):
            splitted = split(address, [":"])
        if len(splittedwith2) < len(splittedwithone):
            splitted = split(address, ["-"])
        hexa_values = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ,"a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F")
        if len(splitted) != 6 and len(splitted) != 8:
            msg = "Address {0} has invalid length"
            raise MacAddressValueError(msg)
        for x in range(0, len(splitted)):
            if len(splitted[x]) > 2:
                msg = "Address {0} has at {1} an invalid value".format(address, x+1)
                raise MacAddressValueError(msg)
            if not onlycontains(splitted[x], hexa_values):
                msg = "Address {0} has an invalid character in {1} for hexadecimal".format(address, splitted[x])
                raise MacAddressValueError(msg)

class _Mac48Base(_MacBase):
    @property
    def version():
        return 48

    def _get_address_from_int(self, address):
        self._check_int_adress(address)
        a = get_basenumber_from_int(address, 2)
        if len(a) < MAC48:
            for x in range(0, MAC48-len(a)):
                a = "0" + a
        b_oui = a[0 : 24]
        b_nic = a[24 : 48]
        oui = ""
        nic = ""
        cutted = cut(b_oui, 8)
        for x in range(0, len(cutted)):
            oui += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
        cutted = cut(b_nic, 8)
        for x in range(0, len(cutted)):
            nic += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
        datas = [bool(int(a[7])), bool(int(a[6])), oui, nic, "", a]
        cutted = cut(a, 8)
        for x in range(0, len(cutted)):
            datas[4] += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
            if x != len(cutted)-1:
                datas[4] += ":"
        return tuple(datas)
        
    def _get_address_from_string(self, address):
        self._check_string_address(address)
        splittedwith2 = split(address, [":"])
        splittedwithone = split(address, ["-"])
        splitted = None
        if len(splittedwith2) >= len(splittedwithone):
            splitted = split(address, [":"])
        if len(splittedwith2) < len(splittedwithone):
            splitted = split(address, ["-"])
        v = ""
        for spl in splitted:
            a = str(get_basenumber_from_int(get_int_from_basenumber(spl, 16), 2))
            for x in range(0, 8-len(a)):
                a = "0" + a
            v += a
        b_oui = v[0 : 24]
        b_nic = v[24 : 48]
        oui = ""
        nic = ""
        cutted = cut(b_oui, 8)
        for x in range(0, len(cutted)):
            oui += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
        cutted = cut(b_nic, 8)
        for x in range(0, len(cutted)):
            nic += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
        datas = [bool(int(v[7])), bool(int(v[6])), oui, nic, address, v]
        return tuple(datas)

    def _get_address_from_binary(self, address):
        self._check_binary_address(address)
        a = str(address)
        if len(address) < MAC48:
            for b in range(0, MAC48-len(address)):
                a = "0" + a
        oui = ""
        nic = ""
        b_oui = a[0 : 24]
        b_nic = a[24 : 48]
        cutted = cut(b_oui, 8)
        for x in range(0, len(cutted)):
            oui += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
        cutted = cut(nic, 8)
        for x in range(0, len(cutted)):
            nic += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
        datas = [bool(int(a[7])), bool(int(a[6])), oui, nic, "", a]
        cutted = cut(a, 8)
        for x in range(0, len(cutted)):
            datas[4] += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
            if x != len(temp)-1:
                datas[4] += ":"
        return tuple(datas)

    def _get_address_from_mac64_address(self, mac64address):
        if mac64address.version == 64:
            datas = [mac64address.unicast, mac64address.globally_unique, None, None, "", ""]
            address = ""
            binary = ""
            splittedwith2 = split(address, [":"])
            splittedwithone = split(address, ["-"])
            splitted = None
            if len(splittedwith2) >= len(splittedwithone):
                splitted = split(address, [":"])
            if len(splittedwith2) < len(splittedwithone):
                splitted = split(address, ["-"])
            for x in range(0, 8):
                if x != 3 and x != 4:
                    address += splitted[x]
                    if x != 7:
                        address += ":"
            datas[4] = address
            splitted = split(address, ":")
            for x in range(0, len(splitted)):
                v = get_basenumber_from_int(get_int_from_basenumber(splitted[x], 16), 2)
                if len(v) < 8:
                    for y in range(0, 8-len(v)):
                        v = "0" + v
                binary += v
            oui = ""
            nic = ""
            b_oui = binary[0 : 24]
            b_nic = binary[24 : 48]
            cutted = cut(b_oui, 8)
            for x in range(0, len(cutted)):
                oui += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
            cutted = cut(b_nic, 8)
            for x in range(0, len(cutted)):
                nic += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
            datas[5] = binary
            datas[2] = oui
            datas[3] = nic
            self._check_string_address(datas[4])
            return tuple(datas)
        if mac64address.version == 48:
            return mac64address
        msg = "Invalid version {0} for address".format(mac48address.version)
        raise MacAddressValueError(msg)

class Mac48Address(_Mac48Base):
    _address = None
    _binary_address = None
    _oui = None
    _nic = None
    _globally = None
    _unicast = None
    _reversed = None

    @property
    def address(self):
        return self._address

    @property
    def unicast(self):
        return self._unicast

    @property
    def organization_unique_identifier(self):
        return self._oui

    @property
    def nic(self):
        return self._nic

    @property
    def globally_unique(self):
        return self._globally

    @property
    def reversed(self):
        return self._reversed

    def __init__(self, address):
        _is_string_address = True
        _is_binary_address = False
        _is_integer_address = False
        _skip = False
        if isinstance(address, Mac48Address):
            self._address = address._address
            self.globally_unique = address._globally
            self.organization_unique_identifier = address._oui
            self.nic = address._nic
            self._binary_address = address._binary_address
            self._reversed = address._reversed
            _skip = True
        if isinstance(address, Mac64Address):
            datas = self._get_address_from_mac64_address(address)
            self._address = datas[4]
            self._binary_address = datas[5]
            self._globally = datas[1]
            self._unicast = datas[0]
            self._oui = datas[2]
            self._nic = datas[3]
        if not isinstance(address, Mac48Address) and not isinstance(address, Mac64Address):
            try:
                self._check_string_address(address)
            except:
                _is_string_address = False
                _is_binary_address = True
                
            if not _is_string_address and _is_binary_address:
                try:
                    self._check_binary_address(address)
                except:
                    _is_binary_address = False
                    _is_integer_address = True
                    
            if not _is_string_address and not _is_binary_address and _is_integer_address:
                try:
                    self._check_int_adress(address)
                except:
                    _is_integer_address = False
                    
            if _is_string_address:
                datas = self._get_address_from_string(address)
                self._address = datas[4]
                self._binary_address = datas[5]
                self._globally = datas[1]
                self._unicast = datas[0]
                self._oui = datas[2]
                self._nic = datas[3]
                
            if _is_binary_address:
                datas = self._get_address_from_binary(address)
                self._address = datas[4]
                self._binary_address = datas[5]
                self._globally = datas[1]
                self._unicast = datas[0]
                self._oui = datas[2]
                self._nic = datas[3]
                
            if _is_integer_address:
                datas = self._get_address_from_int(address)
                self._address = datas[4]
                self._binary_address = datas[5]
                self._globally = datas[1]
                self._unicast = datas[0]
                self._oui = datas[2]
                self._nic = datas[3]
                
            if not _is_binary_address and not _is_integer_address and not _is_string_address:
                msg = "Unable to cast address {0} in a mac 48 address".format(address)
                raise MacAddressValueError(msg)

        if _is_binary_address or _is_integer_address or _is_string_address and not _skip:
            self._reversed = ""
            cutted = cut(self._binary_address, 8)
            for x in cutted:
                self._reversed += reverse(x)

class _Mac64Base(_MacBase):
    @property
    def version():
        return 64

    def _get_address_from_int(self, address):
        self._check_int_adress(address)
        a = get_basenumber_from_int(address, 2)
        if len(a) < MAC64:
            for x in range(0, MAC64-len(a)):
                a = "0" + a
        oui = ""
        nic = ""
        b_oui = a[0 : 36]
        b_nic = a[36 : 60]
        cutted = cut(b_oui, 8)
        for x in range(0, len(cutted)):
            oui += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
        cutted = cut(b_nic, 8)
        for x in range(0, len(cutted)):
            nic += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
        datas = [bool(int(a[7])), bool(int(a[6])), oui, nic, "", a]
        cutted = cut(a, 8)
        for x in range(0, len(cutted)):
            datas[4] += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
            if x != len(cutted)-1:
                datas[4] += ":"
        return tuple(datas)
        
    def _get_address_from_string(self, address):
        self._check_string_address(address)
        splittedwith2 = split(address, [":"])
        splittedwithone = split(address, ["-"])
        splitted = None
        if len(splittedwith2) >= len(splittedwithone):
            splitted = split(address, [":"])
        if len(splittedwith2) < len(splittedwithone):
            splitted = split(address, ["-"])
        v = ""
        for spl in splitted:
            a = str(get_basenumber_from_int(get_int_from_basenumber(spl, 16), 2))
            for x in range(0, 8-len(a)):
                a = "0" + a
            v += a
        oui = ""
        nic = ""
        b_oui = v[0 : 36]
        b_nic = v[36 : 60]
        cutted = cut(b_oui, 8)
        for x in range(0, len(cutted)):
            oui += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
        cutted = cut(b_nic, 8)
        for x in range(0, len(cutted)):
            nic += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
        datas = [bool(int(v[7])), bool(int(v[6])), oui, nic, address, v]
        return tuple(datas)

    def _get_address_from_binary(self, address):
        self._check_binary_address(address)
        a = str(address)
        if len(address) < MAC48:
            for b in range(0, MAC48-len(address)):
                a = "0" + a
        oui = ""
        nic = ""
        b_oui = a[0 : 36]
        b_nic = a[36 : 60]
        cutted = cut(b_oui, 8)
        for x in range(0, len(cutted)):
            oui += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
        cutted = cut(b_nic, 8)
        for x in range(0, len(cutted)):
            nic += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
        datas = [bool(int(a[7])), bool(int(a[6])), oui, nic, "", a]
        cutted = cut(a, 8)
        for x in range(0, len(cutted)):
            datas[4] += get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16)
            if x != len(temp)-1:
                datas[4] += ":"
        return tuple(datas)

    def _get_address_from_mac48_address(self, mac48address):
        if mac48address.version == 48:
            datas = [mac48address.unicast, mac48address.globally_unique, None, None, "", ""]
            address = ""
            binary = ""
            splittedwith2 = split(address, [":"])
            splittedwithone = split(address, ["-"])
            splitted = None
            if len(splittedwith2) >= len(splittedwithone):
                splitted = split(address, [":"])
            if len(splittedwith2) < len(splittedwithone):
                splitted = split(address, ["-"])
            for x in range(0, 8):
                skip = False
                if x == 3:
                    address += "FF:"
                if x == 4:
                    address += "FE:"
                if x > 4:
                    address += splitted[x-2]
                    if x != 7:
                        address += ":"
                if x < 3:
                    address += splitted[x] + ":"
            datas[4] = address
            splitted = split(address, [":"])
            for x in range(0, len(splitted)):
                v = get_basenumber_from_int(get_int_from_basenumber(splitted[x], 16), 2)
                if len(v) < 8:
                    for y in range(0, 8-len(v)):
                        v = "0" + v
                binary += v
            datas[5] = binary
            oui = ""
            nic = ""
            b_oui = binary[0 : 36]
            b_nic = binary[36 : 60]
            cutted = cut(b_oui, 8)
            for x in range(0, len(cutted)):
                oui += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
            cutted = cut(b_nic, 8)
            for x in range(0, len(cutted)):
                nic += str(get_basenumber_from_int(get_int_from_basenumber(cutted[x], 2), 16))
            datas[2] = oui
            datas[3] = nic
            self._check_string_address(datas[4])
            return tuple(datas)
        if mac48address.version == 64:
            return mac48address
        msg = "Invalid version {0} for address".format(mac48address.version)
        raise MacAddressValueError(msg)

class Mac64Address:
    _address = None
    _binary_address = None
    _oui = None
    _nic = None
    _globally = None
    _unicast = None
    _reversed = None
    @property
    def address(self):
        return self._address
    @property
    def unicast(self):
        return self._unicast
    @property
    def organization_unique_identifier(self):
        return self._oui
    @property
    def nic(self):
        return self._nic
    @property
    def globally_unique(self):
        return self._globally
    @property
    def reversed(self):
        return self._reversed
    def __init__(self, address):
        _is_string_address = True
        _is_binary_address = False
        _is_integer_address = False
        _skip = False
        if isinstance(address, Mac48Address):
            datas = self._get_address_from_mac48_address(address)
            self._address = datas[4]
            self._binary_address = datas[5]
            self._globally = datas[1]
            self._unicast = datas[0]
            self._oui = datas[2]
            self._nic = datas[3]
        if isinstance(address, Mac64Address):
            self._address = address._address
            self.globally_unique = address._globally
            self.organization_unique_identifier = address._oui
            self.nic = address._nic
            self._binary_address = address._binary_address
            self._reversed = address._reversed
            _skip = True
        if not isinstance(address, Mac48Address) and not isinstance(address, Mac64Address):
            try:
                self._check_string_address(address)
            except:
                _is_string_address = False
                _is_binary_address = True
                
            if not _is_string_address and _is_binary_address:
                try:
                    self._check_binary_address(address)
                except:
                    _is_binary_address = False
                    _is_integer_address = True
                    
            if not _is_string_address and not _is_binary_address and _is_integer_address:
                try:
                    self._check_int_adress(address)
                except:
                    _is_integer_address = False
                    
            if _is_string_address:
                datas = self._get_address_from_string(address)
                self._address = datas[4]
                self._binary_address = datas[5]
                self._globally = datas[1]
                self._unicast = datas[0]
                self._oui = datas[2]
                self._nic = datas[3]
                
            if _is_binary_address:
                datas = self._get_address_from_binary(address)
                self._address = datas[4]
                self._binary_address = datas[5]
                self._globally = datas[1]
                self._unicast = datas[0]
                self._oui = datas[2]
                self._nic = datas[3]
                
            if _is_integer_address:
                datas = self._get_address_from_int(address)
                self._address = datas[4]
                self._binary_address = datas[5]
                self._globally = datas[1]
                self._unicast = datas[0]
                self._oui = datas[2]
                self._nic = datas[3]
                
            if not _is_binary_address and not _is_integer_address and not _is_string_address:
                msg = "Unable to cast address {0} in a mac 64 address".format(address)
                raise MacAddressValueError(msg)

        if _is_binary_address or _is_integer_address or _is_string_address and not _skip:
            self._reversed = ""
            cutted = cut(self._binary_address, 8)
            for x in range(0, len(cutted)):
                self._reversed += reverse(cutted[x])


broadcast = Mac48Address("FF:FF:FF:FF:FF:FF")
cisco_discovery_protocol = Mac48Address("01:00:0C:CC:CC:CC")
spaning_tree_protocol = Mac48Address("01:80:C2:00:00:00")
