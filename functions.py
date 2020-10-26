_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "W", "X", "Y", "Z"]

_cache = []
_temp = []

class BaseValueError(ValueError):
    pass

class CharacterError(ValueError):
    pass

class OpeningFileError(ValueError):
    pass

def get_int_from_basenumber(number="", base=10):
    value = 0
    if base < 2 or base > len(_chars):
        msg = "Base for {0} is unusable".format(base)
        raise BaseValueError(msg)
    num = len(number)-1
    for x in range(0, len(number)):
        if _chars.index(number[x].upper()) >= base:
            msg = "Found invalid character for base {0}".format(base)
            raise CharacterError(msg)
        value += _chars.index(number[x])*(base**(num-x))
    return value

def get_basenumber_from_int(number=0, base=10):
    value = int(number)
    base_value = ""
    if base < 2 or base > len(_chars):
        msg = "Base for {0} is unusable".format(base)
        raise BaseValueError(msg)
    exponent = 0
    while base**exponent-1 < value:
        exponent += 1
    num = exponent-1
    for x in range(0, exponent):
        skip = False
        value_at = base**(num-x)
        for y in range(0, base):
            if value >= (base-1-y)*(value_at) and not skip:
                skip = True
                value -= (base-1-y)*(value_at)
                base_value += _chars[base-1-y]
                break
    return base_value

def isValidBase(base=0):
    if base < 2 and base < len(_chars):
        return False
    return True

def parse(text='', separators=[], brackets={}):
	if text == "":
		return []
	elif separators == []:
		return [text]
	elif brackets == {}:
		return split(text, separators)
	else:
		separated = []
		temp = ""
		opened_brackets = []
		skip = False
		skip_for = 0
		for indx in range(0, len(text)):
			if not skip:
				for bracket in brackets:
					if opened_brackets != [] and bracket == opened_brackets[len(opened_brackets)-1]:
						if text[indx:indx+len(brackets[bracket])] == brackets[bracket]:
							del opened_brackets[len(opened_brackets)-1]
					else:
						if bracket == text[indx:indx+len(bracket)]:
							opened_brackets.append(bracket)
				if opened_brackets == []:
					did = False
					for separator in separators:
						if separator == text[indx:indx+len(separator)]:
							skip = True
							skip_for = indx+len(separator)-1
							did = True
					if not did:
						temp += text[indx]
					if did and temp != "":
						separated.append(temp)
						temp = ''
				if opened_brackets != []:
					temp += text[indx]
			if skip and skip_for == indx:
				skip = False
			if temp != "" and indx == len(text)-1:
				separated.append(temp)
		return separated
	return None

def split(string="", separators=[]):
    separated_string = []
    buff = ""
    skipfor = 0
    skip = False
    if string != "" and separators != [] and separators != None:
        for value in range(0, len(string)):
            if skip:
                if value == skipfor:
                    skip = False
                    skipfor = 0

            wrong = False
            for x in range(0, len(separators)):
                if string[value] == separators[x][0] and not skip:
                    if string[value : value + len(separators[x])] == separators[x]:
                        wrong = True
                        if skipfor < value+len(separators[x])-1:
                            skipfor = value + len(separators[x]) 

            if not wrong and not skip:
                buff += string[value]

            if wrong and not skip:
                if buff != "":
                    separated_string.append(buff)
                    buff = ""

            if value == len(string)-1 and buff != "" and not skip:
                separated_string.append(buff)
                buff = ""
        return separated_string
    return string

def cut(string="", step=0):
    step = int(step)
    counter = 0
    buff = ""
    cutted_string = []
    rcounter = 0
    for char in string:
        skip = False
        if counter != int(step):
            buff += char
            if rcounter == len(string)-1:
                cutted_string.append(buff)
                buff = ""
                counter = 0
                skip = True
        if counter == step-1:
            cutted_string.append(buff)
            buff = ""
            counter = 0
            skip = True
        if not skip:
            counter += 1
        rcounter += 1
    return cutted_string

def contains(text='', contained='', brackets={}):
	if text == '':
		return False
	else:
		opened_brackets = []
		for indx in range(0, len(text)):
			for bracket in brackets:
				if opened_brackets != [] and bracket == opened_brackets[len(opened_brackets)-1] and text[indx:indx+len(brackets[bracket])] == brackets[bracket]:
					del opened_brackets[len(opened_brackets)-1]
				else:
					if text[indx:indx+len(bracket)] == bracket:
						opened_brackets.append(bracket)
			if opened_brackets == [] and text[indx:indx+len(contained)] == contained:
				return True	
		return False
	return False

def sub(string="", sub_string=""):
    returned_string = string
    if len(string) >= len(sub_string):
        if returned_string[len(string)-len(sub_string) : len(string)] == sub_string:
            del returned_string[len(string)-len(sub_string) : len(string)]
    return returned_string

def endswith(string="", end_string=""):
    if string[len(string)-len(end_string) : len(string)] == end_string:
        return True
    return False

def startswith(string="", start_string=""):
    if string[0 : len(start_string)] == start_string:
        return True
    return False

def onlycontains(string="", chars=[]):
    if string != "" and chars != []:
        for x in range(0, len(string)):
            for y in range(0, len(chars)):
                if x+len(chars[y])+1 <= len(string):
                    if not string[x : x+len(chars[y])] in chars:
                        return False
        return True
    return False

def reverse(entry):
	if isinstance(entry, list):
		if entry == []:
			return []
		else:
			for x in range(0, len(entry)):
				if x == len(entry)%2+(len(entry)-len(entry)%2)/2:
					break
				else:
					temp = entry[x]
					entry[x] = entry[len(entry)-1-x]
					entry[len(entry)-1-x] = temp
			return entry
	if isinstance(entry, str):
		returned_string = ""
		if entry != "":
			     		for x in range(0, len(entry)):
			     			returned_string += entry[len(entry)-1-x]
		return returned_string
	return None

def replace(_dict={}, root=[], value="0"):
    if not isinstance(_dict, dict):
    	raise ValuError("Invalid object")
    if _dict != {} and root != []:
        changed_dict = None
        counter = 0
        threshold = len(root)-1
        for root_at in range(0, len(root)):
            _temp_dict = _dict
            for y in range(0, len(root)):
                if y == threshold:
                    if y == len(root)-1:
                        _temp_dict[root[threshold]] = value
                    if root[y] != len(root)-1:
                        changed_dict = _temp_dict
                        threshold -= 1
                if y != threshold:
                    _temp_dict = _temp_dict[root[y]]
        return changed_dict
    if _dict == {} or root == []:
        return _dict

#could be faster using str for big numbers
def is_pair(value):
			if not isinstance(value, int):
				raise ValueError("Invalid entry")
			return not bool(value%2)
			
def is_impair(value):
			if not isinstance(value, int):
				raise ValueError("Invalid entry")
			return bool(value%2)
			
def sort(lst=[]):
    if not isinstance(lst, list):
        raise ValueError("The given value isn't a list")
    if lst == []:
        return []
    temp = lst[0]
    while(temp != None):
        temp = None
        for x in range(0, len(lst)):
            if x > 0 and lst[x-1] > lst[x]:
                temp = lst[x-1]
                lst[x-1] = lst[x]
                lst[x] = temp
    return lst
	
def gcd(a, b):
	if not isinstance(a, int) or not isinstance(b, int) or a < b:
		raise ValueError("Invalid entry")
	while(a%b != 0):
		b = a%b
	return b

def is_prime(a):
    _temp = []
    if not isinstance(a, int):
        raise ValueError("Invalid entry")
    if is_pair(a):
        if a == 2:
            _cache.append(a)
            return True
        return False
    if not is_pair(a):
        n = a-2
        if _cache != []:
            for x in range(0, len(_cache)):
                if _cache[x] < a and a%_cache[x] == 0:
                    return False
                if _cache[x] > a:
                    break
                if _cache[x] == a:
                    return True
                _temp.append(_cache[x])
        while(n != 1):
            n -= 2
            if not n in _temp and gcd(a, n) != 1:
                return False
        _cache.append(a)
        return True
    return False

def clear_cache():
    _cache = []

def decompose_in_prime_factors(a):
	if not isinstance(a, int):
		raise ValueError("Invalid given entry, should be int")
	if is_prime(a):
		return (a, 1)
	else:
		factors = []
		while(not is_prime(int(a))):
			b = 2
			while(b < a):
				if  is_prime(b) and a%b == 0:
					a/=b
					factors.append(b)
					b = 0
				b+=1
		factors.append(int(a))
		factors.append(1)
		return factors
	return None

class ListError(ValueError):
	pass

def make_stats(lst):
	if not isinstance(lst, list) and not isinstance(lst, tuple):
		raise ListError("Given input isn't a list")
	if isinstance(lst, list) or isinstance(lst, tuple):
		if lst == [] or lst == ():
			raise ListError("Empty list or tuple")
		if lst != [] and lst != ():
			for x in range(0, len(lst)):
				if not isinstance(lst[x], int) and not isinstance(lst[x], float):
					if isinstance(lst[x], str):
						try:
							a = int(lst[x])
						except:
							raise ListError("Invalid conversion from str to int")
					if not isinstance(lst[x], str):
						raise ListError("Unable to deal with something else than numbers")
			datas = []
			a = 0
			c = len(lst)
			for x in range(0, len(lst)):
				a += float(lst[x])
			datas.append(a/c)
			lst = sort(list(lst))
			print(lst)
			datas.append(lst[len(lst)-1]-int(lst[0]))
			if isPair(len(lst)):
				datas.append((lst[int(len(lst)/2-1)]+lst[int(len(lst)/2)])/2)
				if isPair(int(len(lst)/2)):
					datas.append((lst[int(len(lst)/2-(len(lst)/2-(len(lst)/2)%2)/2)-1]+lst[int(len(lst)/2-(len(lst)/2-(len(lst)/2)%2)/2)])/2)
					datas.append((lst[int(len(lst)/2-(len(lst)/2-(len(lst)/2)%2)/2-1+len(lst)/2)]+lst[int(len(lst)/2-(len(lst)/2-(len(lst)/2)%2)/2+len(lst)/2)])/2)
				if isImpair(int(len(lst)/2)):
					datas.append(lst[int(len(lst)/2-(len(lst)/2-(len(lst)/2)%2)/2)-1])
					datas.append(lst[int(len(lst)/2-(len(lst)/2-(len(lst)/2)%2)/2)+int(len(lst)/2)-1])
			if isImpair(len(lst)):
				datas.append(int(lst[int(((len(lst)-1)/2+1)-1)]))
				datas.append(int(lst[int((len(lst)-len(lst)%4)/4)]))
			return datas
		return None
	return None
	
def read_csv(input="", separators=[",", ", ", "\n", "\r"]):
	if not isinstance(input, str):
		raise ValueError("Invalid input")
	return split(input, separators)
	
def write_csv(input=[], separators=[","]):
	if not isinstance(input, list) and not isinstance(input, tuple):
		raise ValueError("Invalid input")
	if len(separators) != 1:
		raise ValueError("Wrong separators list")
	r = ""
	for x in range(0, len(input)):
		r += str(input[x])
		if x != len(input)-1:
			r += ","
	return r
	
def are_brackets_closed(text='', brackets={}):
	if text == '':
		return True
	elif brackets == {}:
		return True
	else:
		opened_brackets = []
		for indx in range(0, len(text)):
			for bracket in brackets:
				if opened_brackets != [] and bracket == opened_brackets[len(opened_brackets)-1] and text[indx:indx+len(brackets[bracket])] == brackets[bracket]:
					del opened_brackets[len(opened_brackets)-1]
				else:
					if text[indx:indx+len(bracket)] == bracket:
						opened_brackets.append(bracket)
		return opened_brackets == []
		
def comparison(a, b):
	a = bytes(a)
	b = bytes(b)
	if len(a) != len(b):
		raise RuntimeError('Can\'t compare two objects of different length')
	c = 0
	for indx in range(0, len(a)):
		if a[indx] == b[indx]:
			c += 1
	return c/len(a)
