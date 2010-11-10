# -*- coding: utf-8 -*-
import hdtv.cmdline
from hdtv.errvalue import ErrValue
import hdtv.ui
import csv
import os
    
class _Element(object):
    """
    Store info about elements
    """
    
    __slots__ = ("ID", "z", "symbol", "name", "m")

    def __init__(self, Z, Symbol, Name = None, M = None):
        
        self.z = Z
        self.symbol = Symbol    # Symbol of element (e.g. H)
        self.name = Name        # Full name of element (e.g. Hydrogen)
        self.m = M              # Atomic weight, This is normalizes over nuclides of element and abundancies
        self.ID = self.symbol
        
    def _get_Z(self):
        return self.z
    
    Z = property(_get_Z)
    
    def _get_M(self):
        return self.m
    M = property(_get_M)
    
    def __str__(self):
        text = str()
        text += "Name:          " + str(self.name) + "\n"
        text += "Z:             " + str(self.z) + " \n"
        text += "Symbol:        " + self.symbol + " \n"
        text += "atomic Mass:   " + str(self.m) + " u \n"
        return text

class _Elements(list):
    """
    Read and hold complete elements list
    """
    
    def __init__(self, csvfile = os.path.join(hdtv.datadir, "elements.dat")):

        super(_Elements, self).__init__()

        tmp = list()
        
        try:
            datfile = open(csvfile, "rb")
            reader = csv.reader(datfile)
            reader.next() # Skip header
            
            for line in reader:
                Z = int(line[0])
                Symbol = line[1].strip()
                Name = line[2].strip()
                try:
                    Mass = ErrValue(line[3].strip())
                except ValueError:
                    Mass = None
                element = _Element(Z, Symbol, Name, Mass)
                tmp.append(element)
        except csv.Error, e:
            hdtv.ui.error('file %s, line %d: %s' % (csvfile, reader.line_num, e))
        finally:
            datfile.close()
            
        # Now store elements finally
        maxZ = max(tmp, key = lambda x: x.z) # Get highest Z
        for i in range(maxZ.z):
            self.append(None)

        for e in tmp:
            self[e.z] = e

    def __call__(self, Z = None, symbol = None, name = None):
        
        if symbol:
            for z in self:
                try:
                    if z.symbol.lower() == symbol.lower():
                        return z
                except AttributeError:
                    pass      
            raise ValueError # If we reach this point there is no element with this symbol
        if name:
            for z in self:
                try:
                    if z.name.lower() == name.lower():
                        return z
                except AttributeError:
                    pass
            raise ValueError # If we reach this point there is no element with this name
                
        if Z:
            return self[Z]
        
        return self
    
    def __setitem__(self, index, value):
        if index == 0:
            return None
        
        if index > 0:
            index = index - 1
        
        return super(_Elements, self).__setitem__(index, value)
        
    def __getitem__(self, index):
        if index == 0:
            return None
        
        if index > 0:
            index = index - 1
        
        return super(_Elements, self).__getitem__(index)
    


class _Nuclide(_Element):
    
    __slots__ = ("ID", "element", "a", "m", "sigma", "abundance")

    def __init__(self, element, A, abundance = None, sigma = None, M = None):
        
        self.element = element
        super(_Nuclide, self).__init__(element.z, element.symbol, element.name, M = None) # M is different for nuclides and elements
        self.a = A
        self.m = M
        self.sigma = sigma
        self.abundance = abundance
        self.ID = str(self.a) + "-" + str(self.symbol)    
    
    
    def _get_symbol(self):
        return self.element.symbol
    
    def _set_symbol(self, symbol):
        self.element.symbol = symbol
    
    symbol = property(_get_symbol, _set_symbol)#    def _Z(self):
    
    def __str__(self):
        text = str()
        text += "ID:            " + self.ID + "\n"
        text += "Z:             " + str(self.z) + " \n"
        text += "A:             " + str(self.a) + "\n"
        text += "atomic Mass:   " + str(self.m) + " u\n"
        try:
            abundance = str(self.abundance * 100.0) + " %"
        except TypeError:   # Unstable nuclide -> no abundance
            abundance = "---"
        text += "Abundance:     " + abundance + " \n"
        if self.sigma.value is None:
            sigma = "???"
        else:
            sigma = str(self.sigma) + " b"
        text += "Sigma_0:       " + sigma + "\n"
        return text


class _Nuclides(object):
    
    def __init__(self, csvfile = os.path.join(hdtv.datadir, "nuclides.dat")):
        
        self._storage = dict()
        try:
            datfile = open(csvfile, "rb")
            reader = csv.reader(datfile)
            reader.next() # Skip header
            
            for line in reader:
                Z = int(line[0].strip())
                element = Elements(Z)
                A = int(line[1].strip())
                if line[2].strip():
                    abd = ErrValue(line[2].strip()) / 100.0
                else:
                    abd = ErrValue(None, None)
                if line[3].strip():
                    M = ErrValue(line[3].strip())
                else:
                    M = ErrValue(None, None)
                if line[4].strip():
                    sigma = ErrValue(line[4].strip())
                else:
                    sigma = ErrValue(None, None)
                
                if not Z in self._storage:
                    self._storage[Z] = dict()
                self._storage[Z][A] = _Nuclide(element, A, abundance = abd, sigma = sigma, M = M)
        except csv.Error, e:
            hdtv.ui.error('file %s, line %d: %s' % (csvfile, reader.line_num, e))      
        finally:
            datfile.close()

    def __call__(self, Z = None, A = None, symbol = None, name = None):
        '''
        Return a list of nuclides with given properties (Z, A, symbol, name)
        
        e.g.: Nuclides(A=197, symbol="Au") returns [Au-197]
              Nuclides(symbol="Au") or Nuclides(name="gold") or Nuclides(Z=79) return list of all gold nuclides
        '''
        
        ret = list()
        
        if Z is not None: # Z is given, so it is faster if we start with nuclides of this Z
            if A is not None: # Nuclide uniquely defined
                ret.append(self._storage[Z][A])
            else:   # All nuclides with given Z
                for n in self._storage[Z].itervalues():
                    ret.append(n)
        
        if len(ret) == 0: # Z was not given, so we have to cycle through all nuclides
            for n in self._storage.itervalues():
                for e in n.itervalues():
                    ret.append(e)
        
        tmp = list()
        
        # Select by A
        if A is not None:
            for n in ret:
                if n.a == A:
                    tmp.append(n)
        
            ret = tmp
            tmp = list()
            
        
        # Select by symbol
        if symbol is not None:
            for n in ret:
                if n.symbol.lower() == symbol.lower():
                    tmp.append(n)
                    
            ret = tmp
            tmp = list()
            
        # Select by name
        if name is not None:
            for n in ret:
                if n.name.lower() == name.lower():
                    tmp.append(n)
        
            ret = tmp
        
        return ret 


class Gamma(object):
    """Class for storing information about gammas"""
    
    __slots__ = ("ID", "nuclide", "energy", "sigma", "intensity")
     
    def __init__(self, nuclide, energy, sigma, intensity):
        self.ID = str(nuclide.ID) + "@" + str(energy.value.__int__())
        self.nuclide = nuclide
        self.energy = energy
        self.sigma = sigma
        self.intensity = intensity

    def __str__(self):
        text = str()
        text += "ID:        " + str(self.ID) + "\n"
        text += "Energy:    " + str(self.energy) + " keV\n"
        if not self.sigma is None:
            text += "Sigma:     " + str(self.sigma) + " b\n"
        if not self.intensity is None:
            text += "Intensity: " + str(self.intensity * 100.0) + " %\n"
        return text
    
    def _Z(self):
        return self.nuclide.z
    
    z = property(_Z)
    
    def _A(self):
        return self.nuclide.a
    
    a = property(_A)
    
    def _symbol(self):
        return self.nuclide.symbol
    
    symbol = property(_symbol)
        
    def __cmp__(self, other):
        
        ret = cmp(self.energy, other.energy)
        
        if ret == 0 and other.ID != None:
            if self.ID == other.ID:
                return ret
            else: # Gammas are from different isotope
                return cmp(self.ID, other.ID)
        else:
            return ret

# TODO: this should be an abstract baseclass!         
class GammaLib(list):
    """
    Class for storing a gamma library
    
    The real libs should be derived from this
    """
    
    __slots__ = ("nuclide", "energy", "sigma", "intensity", "E_fuzziness")

    def __init__(self, fuzziness = 1.0):
        list.__init__(self)
        self.fuzziness = fuzziness  # Fuzzyness for energy identification
        self.opened = False
    
    def find(self, fuzziness = None, sort_key=None, sort_reverse=False, **args):   
        """
        Find in gamma lib
        
        Does a fuzzy compare for floats. All strings are compared lowercase.
        
        Valid key args are:
        
         * sort_key: key to sort
         * sort_reverse: sort_reverse
         * "key: value" : key value pairs to find
        """
        if not self.opened:
            self.open()
        
        if fuzziness is None:
            fuzziness = self.fuzziness

        # convert keys to lowercase
        fields_lower = dict()
        args_lower = dict()
        for (key, conv) in self.fParamConv.items():
            fields_lower[key.lower()] = conv
            
        for (key, value) in args.items():
            try:
                conv = fields_lower[key.lower()] # if this raises a KeyError it was an invalid argument
            except KeyError:
                hdtv.ui.error("Invalid key " + str(key))
                raise KeyError
            if value is None:
                continue
            args_lower[key.lower()] = conv(value)

        # Prepare find args
        fargs = dict()

        for (key, conv) in fields_lower.items():
            try:
                fargs[key] = conv(args_lower[key]) # Convert as described in fParamConv dict
            except KeyError:
                pass       

        
        # Do the search
        results = self[:]
        
        if fuzziness is None:
            fuzziness = self.fuzziness
                
        if len(fargs) == 0:
            return []

        for (key, value) in fargs.items():
            if not value is None:
                if isinstance(value, int): 
                    results = filter(lambda x: getattr(x, key) == value, results)
                elif isinstance(value, str): # Do lowercase cmp for strings
                    value_l = value.lower()
                    results = filter(lambda x: getattr(x, key).lower() == value_l, results)
                else: # Do fuzzy compare
                    results = filter(lambda x: (abs(getattr(x, key) - value) <= fuzziness), results)    

        # Sort
        try:
            if not sort_key is None:
                results.sort(key = lambda x: getattr(x, sort_key), reverse = sort_reverse)
        except AttributeError:
            hdtv.ui.warn("Could not sort by \'" + str(sort_key) + "\': No such key")    
            raise AttributeError
        
        return results


Elements = _Elements()
Nuclides = _Nuclides()
