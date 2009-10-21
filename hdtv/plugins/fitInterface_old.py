# -*- coding: utf-8 -*-

# HDTV - A ROOT-based spectrum analysis software
#  Copyright (C) 2006-2009  The HDTV development team (see file AUTHORS)
#
# This file is part of HDTV.
#
# HDTV is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# HDTV is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with HDTV; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
import ROOT
import hdtv.cmdline
import hdtv.cmdhelper
import hdtv.options
import hdtv.util
import hdtv.ui
import weakref

from hdtv.marker import MarkerCollection
from hdtv.fitter import Fitter
from hdtv.fit import Fit
# TODO: Remove or fix FitPanel
#from hdtv.fitpanel import FitPanel

import sys

class FitInterface:
    """
    User interface for fitting 1-d spectra
    """
    # TODO: remove show_panel(?)
    def __init__(self, window, spectra, show_panel=False):
#        hdtv.ui.msg("Loaded user interface for fitting of 1-d spectra")

#        self.window = window
#        self.spectra = spectra

#        self.defaultFitter = Fitter(peakModel = "theuerkauf", bgdeg = 1)
#        self._workFit = None # Fit we are currently working on

#        # tv commands
#        self.tv = TvFitInterface(self)

#        # Register configuration variables for fit interface
#        opt = hdtv.options.Option(default = 20.0)
#        hdtv.options.RegisterOption("fit.quickfit.region", opt) # default region width for quickfit
#        opt = hdtv.options.Option(default = False, parse = hdtv.options.ParseBool)
#        hdtv.options.RegisterOption("__debug__.fit.show_inipar", opt)
        

        # fit panel
        #self.fitPanel = FitPanel()
        #self.fitPanel.fFitHandler = self.Fit
        #self.fitPanel.fClearHandler = self.ClearFit
        #self.fitPanel.fResetHandler = self.ResetParameters
        #self.fitPanel.fDecompHandler = lambda(stat): self.SetDecomp(stat)
        #if show_panel:
        #    self.fitPanel.Show()

#        # Register hotkeys
#        self.window.AddHotkey(ROOT.kKey_Q, self.Quickfit)
#        self.window.AddHotkey(ROOT.kKey_b, lambda: self._PutMarker("bg"))
#        self.window.AddHotkey([ROOT.kKey_Minus, ROOT.kKey_b],
#                                lambda: self._DeleteMarker("bg"))
#        self.window.AddHotkey(ROOT.kKey_r, lambda: self._PutMarker("region"))
#        self.window.AddHotkey([ROOT.kKey_Minus, ROOT.kKey_r],
#                                lambda: self._DeleteMarker("region"))
#        self.window.AddHotkey(ROOT.kKey_p, lambda: self._PutMarker("peak"))
#        self.window.AddHotkey([ROOT.kKey_Minus, ROOT.kKey_p],
#                                lambda: self._DeleteMarker("peak"))
#        self.window.AddHotkey(ROOT.kKey_B, lambda: self.Fit(peaks = False))
#        self.window.AddHotkey([ROOT.kKey_Minus, ROOT.kKey_B], self.ClearBackground)
#        self.window.AddHotkey(ROOT.kKey_F, lambda: self.Fit(peaks = True))
#        self.window.AddHotkey([ROOT.kKey_Plus, ROOT.kKey_F], self.StoreFit)
#        self.window.AddHotkey([ROOT.kKey_Minus, ROOT.kKey_F], self.ClearFit)
##       self.window.AddHotkey(ROOT.kKey_I, self.Integrate)
#        self.window.AddHotkey(ROOT.kKey_D, lambda: self.SetDecomp(True))
#        self.window.AddHotkey([ROOT.kKey_Minus, ROOT.kKey_D],
#                                lambda: self.SetDecomp(False))
#        self.window.AddHotkey([ROOT.kKey_f, ROOT.kKey_s],
#                        lambda: self.window.EnterEditMode(prompt = "Show Fit: ",
#                                           handler = self._HotkeyShow))
#        self.window.AddHotkey([ROOT.kKey_f, ROOT.kKey_a],
#                        lambda: self.window.EnterEditMode(prompt = "Activate Fit: ",
#                                           handler = self._HotkeyActivate))
#        self.window.AddHotkey([ROOT.kKey_f, ROOT.kKey_p], self._HotkeyShowPrev)
#        self.window.AddHotkey([ROOT.kKey_f, ROOT.kKey_n], self._HotkeyShowNext)
        
#    @property    
#    def workFit(self):
#        """
#        Returns always a current working fit.
#        
#        A new fit is created if necessary.
#        """

#        if not self.spectra.activeID is None:
#            spec = self.spectra[self.spectra.activeID]
#            if spec.fits.activeID is None:
#                if self._workFit in spec.fits.values():
#                    # If self._workFit is stored in spec.fits.values
#                    # it is still some old remainder, else it would be active 
#                    self._workFit = None
#                try: 
#                    # check if self._workfit is a invalid weak-reference
#                    if self._workFit is not None and self._workFit.active:
#                        pass
#                except ReferenceError:
#                    # Reference is gone -> Set to None
#                    self._workFit = None 
#            else :
#                # Use weakrefs here because self._workfit may block the destruction of fit
#                self._workFit = weakref.proxy(spec.fits[spec.fits.activeID])

#        # create new workFit if there is for whatever reason none
#        if self._workFit is None:
#            self._workFit = Fit(self.defaultFitter.Copy())
#            self._workFit.Draw(self.window.viewport)
#        
#        return self._workFit
#        
#        
#        if self.spectra.activeID is None and self._workFit: # No active spectrum
#            self._workFit = Fit(self.defaultFitter.Copy())
#            self._workFit.Draw(self.window.viewport)
#        else:
#            spec = self.spectra[self.spectra.activeID]
#            if spec.fits.activeID is None:
#                try: # Just check if self._workfit is a invalid weak-reference
#                    if self._workFit is not None and self._workFit.active:
#                        pass
#                except ReferenceError:
#                    self._workFit = None # Reference is gone -> Set to None
#                # No active fit so we have work on the temporary work fit or 
#                # create a new fit. If self._workFit is stored in spec.fits.values
#                # it is still some old remainder, else it would be active 
#                if self._workFit is None or self._workFit in spec.fits.values():
#                    self._workFit = Fit(self.defaultFitter.Copy())
#                    self._workFit.Draw(self.window.viewport)
#            else:
#                # Use weakrefs here because self._workfit may block the destruction of fit
#                self._workFit = weakref.proxy(spec.fits[spec.fits.activeID])

#        return self._workFit

     
#    def Quickfit(self):
#        self.ClearFit()
#        fit = self.workFit
#        pos = self.window.viewport.GetCursorX()
#        region_width = hdtv.options.Get("fit.quickfit.region")
#        fit.PutRegionMarker(pos - region_width / 2.)
#        fit.PutRegionMarker(pos + region_width / 2.)
#        fit.PutPeakMarker(pos)
#        self.Fit()
#        
    
#    def _HotkeyShowPrev(self):
#        """
#        ShowPrev wrapper for use with a Hotkey (internal use)
#        """
#        if self.spectra.activeID == None:
#            self.window.viewport.SetStatusText("No active spectrum")
#            return
#        
#        if not self.ShowFits([self.spectra[self.spectra.activeID].fits.prevID], self.spectra.activeID):
#                        self.window.viewport.SetStatusText("No fits available")

#            
#    def _HotkeyShowNext(self):
#        """
#        ShowNext wrapper for use with a Hotkey (internal use)
#        """
#        if self.spectra.activeID == None:
#            self.window.viewport.SetStatusText("No active spectrum")
#            return
#        if not self.ShowFits([self.spectra[self.spectra.activeID].fits.nextID], self.spectra.activeID):
#            self.window.viewport.SetStatusText("No fits available")
#            
#            
#    def _HotkeyShow(self, args):
#        """
#        Show wrapper for use with a Hotkey (internal use)
#        """
#        if self.spectra.activeID == None:
#            self.window.viewport.SetStatusText("No active spectrum")
#            return
#        try:
#            ids = hdtv.cmdhelper.ParseFitIds(args, self.spectra[self.spectra.activeID].fits)
#            if len(ids) == 0:
#                self.spectra[self.spectra.activeID].fits.HideAll()
#            else:
#                if not self.ShowFits(ids, self.spectra.activeID):
#                    self.window.viewport.SetStatusText("No fits available for active spectrum")
#        except ValueError:
#            self.window.viewport.SetStatusText("Invalid fit identifier: %s" % args)

#    def _HotkeyActivate(self, arg):
#        """
#        ActivateObject wrapper for use with a Hotkey (internal use)
#        """
#        if self.spectra.activeID == None:
#            self.window.viewport.SetStatusText("No active spectrum")
#            return
#        try:
#            ID = int(arg)
#            self.ActivateFit(ID)
#        except ValueError:
#            self.window.viewport.SetStatusText("Invalid fit identifier: %s" % arg)
#        except KeyError:
#            self.window.viewport.SetStatusText("No such id: %d" % ID)

#    def _PutMarker(self, mtype):
#        """
#        Put marker of type region, peak or bg to the current position of cursor 
#        (internal use)
#        """
#        fit = self.workFit
#        pos = self.window.viewport.GetCursorX()
#        getattr(fit, "Put%sMarker" % mtype.title())(pos)


#    def _DeleteMarker(self, mtype):
#        """
#        Delete the marker of type region, peak or bg, that is nearest to cursor 
#        (internal use)
#        """
#        fit = self.workFit
#        pos = self.window.viewport.GetCursorX()
#        markers = getattr(fit, "%sMarkers" % mtype.lower())
#        markers.RemoveNearest(pos)   

#    def Fit(self, specID=None, fitID=None, peaks = True):
#        """
#        Fit the peak
#        
#        If there are background markers, a background fit is included.
#        """
#        
#        if specID is None:
#            specID = self.spectra.activeID
#            
#        if specID is None:
#            hdtv.ui.error("There is no active spectrum")
#            return 
#        
#        #if self.fitPanel:
#        #    self.fitPanel.Show()
#        
#        spec = self.spectra[specID]
#        if fitID is None:
#            fit = self.workFit
#        else:
#            try:
#                fit = spec.fits[fitID]
#            except KeyError:
#                hdtv.ui.warn("No fit %d in spectrum %d" %(fitID, specID))
#                return

#        if not peaks and len(fit.bgMarkers) > 0:
#            # pure background fit
#            fit.FitBgFunc(spec)
#        if peaks:
#            # full fit
#            fit.FitPeakFunc(spec)

#        fit.Draw(self.window.viewport)

#        # update fitPanel
#        #self.UpdateFitPanel()


    def FitReset(self, specID=None, fitID=None, resetFitter=True):
        """
        Reset fit to unfitted default fitter
        """
        if specID is None:
            specID = self.spectra.activeID
            
        if specID is None:
            hdtv.ui.error("There is no active spectrum")
            return 

        spec = self.spectra[specID]
        if fitID is None:
            fit = self.workFit
        else:
            try:
                fit = spec.fits[fitID]
            except KeyError:
                hdtv.ui.warn("No fit %d in spectrum %d" %(fitID, specID))
                return

        fit.Reset()
        if resetFitter:
            fit.fitter = self.defaultFitter.Copy()
            fit.fitter.parent=fit
        
        
#    def ActivateFit(self, ID):
#        """
#        Activate one fit
#        """
#        spec = self.spectra[self.spectra.activeID]

#        # Active objects should always be visible
#        assert self.spectra.activeID in self.spectra.visible, "Active spectrum not visible"

#        # activate another fit
#        spec.fits.ActivateObject(ID)

#        # Delete old working fit
#        self._workFit = None
#    
#        if ID is not None:
#            if not spec.fits.isInVisibleRegion(ID):
#                spec.fits.FocusObject(ID)

#        # update fitPanel
#        #self.UpdateFitPanel()


#    def ShowFits(self, ids, specID, adjustViewport=False):
#        """ 
#        Show and focus fits if necessary
#        """
#        if ids[0] is None or len(ids) == 0:
#            return False
#        spec = self.spectra[specID]
#        spec.fits.ShowObjects(ids)
#         # Check if we have to refocus the viewport
#        if adjustViewport:
#            refocus = False
#            if specID == self.spectra.activeID:   
#                for i in ids:
#                    if not spec.fits.isInVisibleRegion(i):
#                        refocus = True
#                if refocus:
#                    spec.fits.FocusObjects(ids)
#        return True
#        

#    def PrintFits(self, ids, specIDs, onlyVisible=False, sortBy="", reverseSort=False):
#        """
#        Print fit properties
#        """
#        sids = hdtv.cmdhelper.ParseIds(specIDs, self.spectra)

#        if len(sids) == 0:
#            hdtv.ui.warn("No active spectrum, no action taken.")
#            return

#        hdtv.ui.debug("FitList: working on" + str(sids), level=4)
#        
#        for sid in sids:
#            
#            try:
#                spec = self.spectra[sid]
#            except KeyError:
#                hdtv.ui.error("No spectrum " + str(sid))
#                continue

#            fids = hdtv.cmdhelper.ParseIds(ids, spec.fits)

#            if len(fids) == 0:
#                hdtv.ui.warn("No active fit for spectrum %d" % sid)
#                continue
#            
#            result_header = "Fits in Spectrum " + str(sid) + " (" + str(spec) + ")" + "\n"
#            count_fits = 0
#            count_peaks = 0
#            
#             # Get sort key
#            if sortBy != "":
#                key = sortBy
#            else:
#                key = hdtv.options.Get("fit.list.sort_key")
#            
#            # Build table
#            params = ["id", "stat"]
#            key = key.lower()
#    
#            objects = list()
#            
#            if len(spec.fits) == 0:
#                hdtv.ui.newline()
#                hdtv.ui.msg("Spectrum " + str(sid) + " (" + str(spec) + "): No fits")                
#                hdtv.ui.newline()
#                continue
#            
#            # Get fits
#            for ID in fids:
#                
#                try:
#                    obj = spec.fits[ID]
#                except KeyError:
#                    hdtv.ui.warn("No fit %s in spec %s" %(ID, sid))
#                    continue
#                
#                if onlyVisible: # Don't print on visible fits
#                    if not ID in spec.fits.visible:
#                        continue
#                    
#                count_fits += 1
#                
#                # Get peaks
#                for peak in obj.peaks:
#                    
#                    thispeak = dict()
#                    thispeak["id"] = str(ID) + "." + str(obj.peaks.index(peak))
#                    
#                    thispeak["stat"] = str()
#                    if ID == spec.fits.activeID:
#                        thispeak["stat"] += "A"
#                    
#                    if ID in spec.fits.visible:
#                        thispeak["stat"] += "V"
#                    
#                    count_peaks += 1

#                    for p in obj.fitter.peakModel.fOrderedParamKeys:
#            
#                        if p == "pos": # Store channel additionally to position
#                            thispeak["channel"] = getattr(peak, "pos")
#                            if "channel" not in params:
#                                params.append("channel")
#                        
#                        p_cal = p + "_cal" # Use calibrated values if available
#                        if hasattr(peak, p_cal):
#                            thispeak[p] = getattr(peak, p_cal)
#                    
#                        if p not in params:
#                            params.append(p)

#                    # Calculate normalized volume if efficiency calibration is present
#                    if spec.fEffCal is not None:
#                        volume = thispeak["vol"]
#                        par_index = params.index("vol") + 1
#                        energy = thispeak["pos"]
#                        norm_volume = volume / spec.fEffCal(energy)
#                        thispeak["vol/eff"] = norm_volume
#                        if "vol/eff" not in params:
#                            params.insert(par_index, "vol/eff")
#                        
#                    objects.append(thispeak)
#            
#            result_footer = "\n" + str(count_peaks) + " peaks in " + str(count_fits) + " fits."
#            
#            try:
#                table = hdtv.util.Table(objects, params, sortBy=key, reverseSort=reverseSort,
#                                        extra_header = result_header, extra_footer = result_footer)
#                hdtv.ui.msg(str(table))
#            except KeyError:
#                
#                hdtv.ui.error("Spectrum " + str(sid) + ": No such attribute: " + str(key))
#                hdtv.ui.error("Spectrum " + str(sid) + ": Valid attributes are: " + str(params))
#                continue
    
#    def FocusFits(self, ids):
#        """
#        Focus fits
#        """
#        spec = self.spectra[self.spectra.activeID]
#        spec.fits.FocusObjects(ids)
#        if self.spectra.activeID in self.spectra.visible and spec.fits.activeID:
#            spec.fits[spec.fits.activeID].Show()
            

#    def StoreFit(self):
#        """
#        Store this fit or delete it, if it is invalid 
#        """
#        # get active spectrum
#        if self.spectra.activeID==None:
#            hdtv.ui.error("There is no active spectrum")
#            return
#        spec = self.spectra[self.spectra.activeID]
#        if self.workFit in spec.fits.values(): 
#            # FIXME: this is not working as expected because of weakref.proxy
#            hdtv.ui.warn("Fit already stored")
#        elif self.workFit is not None:
#            ID = spec.AddFit(self.workFit)
#        else:
#            hdtv.ui.warn("No fit to store")
#            
#        # Reset work fit
#        self._workFit = None 

#        # deactivate all objects
#        spec.fits.ActivateObject(None)


#    def ClearFit(self):
#        """
#        Clear all fit markers and the pending fit, if there is one
#        """
#        if not self.spectra.activeID is None:
#            spec = self.spectra[self.spectra.activeID]
#            if not spec.fits.activeID is None:
#                # FIXME: here we want to clear all markers and the functions
#                # to get an empty fit, instead of removing the whole fit,
#                # because then we would loose the ID
#                spec.fits.ActivateObject(None)# just deactivate the fit for now!
#                #spec.fits.RemoveObjects(spec.fits.activeID)

#        # Reset work fit
#        self._workFit = None
#        # update fitPanel
#        #self.UpdateFitPanel()

#    
#    def ClearBackground(self):
#        """
#        Clear Background markers and refresh fit without background
#        """
#        fit = self.workFit
#        # remove background markers
#        while len(fit.bgMarkers) > 0:
#            fit.bgMarkers.pop()
#           
#        # redo Fit without Background
#        fit.Refresh()
#        # update fitPanel
#        #self.UpdateFitPanel()
#        
#    def CopyFits(self, fitIDs, fromSpecID, toSpecIDs, refit=False):
#        """
#        Copy fits to other spectra which are defined by the parameter ids
#        
#        If "refit" is True the copied fits will automatically be fitted
#        """
#        
#        if isinstance(fitIDs, int):
#            fitIDs = [fitIDs]
#        
#        self.window.viewport.LockUpdate()
#        # get active fit to make the copies
##        fit = self.workFit
#        try:
#            fromSpec = self.spectra[fromSpecID] 
#        except KeyError:
#            hdtv.ui.error("No spectrum with ID %d" % fromSpecID)
#            return False
#            
#        for fitID in fitIDs:
#            self.spectra.ShowObjects(toSpecIDs + [fromSpecID])
#            for specID in toSpecIDs:
#                
#                # Get target spectrum
#                try:
#                    toSpec = self.spectra[specID]
#                except KeyError:
#                    hdtv.ui.warn("No target spectrum %d" % specID)
#                    continue
#                
#                # Get fit to copy
#                try:
#                    fit = fromSpec.fits[fitID].Copy(cal=toSpec.cal, color=None)
#                except KeyError:
#                    hdtv.ui.warn("No fit with ID %d in spectrum %d" %(fitID, fromSpecID))
#                    continue 
#            
#                
#                # Add fit to target spectrum
#                newFitID = toSpec.AddFit(fit)
#                hdtv.ui.msg("Copied fit #%d.%d to #%d.%d" %(fromSpecID, fitID, specID, newFitID))
#                if refit:
#                    self.Fit(specID = specID, fitID = newFitID, peaks=True)

#        self.window.viewport.UnlockUpdate()    


#    def SetDecomp(self, stat = True):
#        """
#        Show peak decomposition
#        """
#        fit = self.workFit
#        fit.SetDecomp(stat)
#        #if self.fitPanel:
#        #    self.fitPanel.SetDecomp(stat)
#        

#    def ShowFitStatus(self, default = False, ids = []):
#        if default:
#            ids.extend("d")
#        else:
#            ids.extend("a")
#        statstr = str()
#        for ID in ids:
#            if ID == "a":
#                fitter = self.workFit.fitter
#                statstr += "active fitter: \n"
#            elif ID == "d":
#                fitter = self.defaultFitter
#                statstr += "default fitter: \n"
#            else:
#                fitter = self.spectra[self.spectra.activeID].fits[ID].fitter
#                statstr += "fitter status of fit id %d: \n" % ID
#            statstr += "Background model: polynomial, deg=%d\n" % fitter.bgdeg
#            statstr += "Peak model: %s\n" % fitter.peakModel.name
#            statstr += "\n"
#            statstr += fitter.OptionsStr()
#            statstr += "\n\n"
#        hdtv.ui.msg(statstr)


#    def SetParameter(self, parname, status, default = False, ids = []):
#        """
#        Sets status of fit parameter
#        If not specified otherwise only the active fiter will be changed,
#        if default=True, also the default fitter will be changed,
#        if a list of fits is given, we try to set the parameter status also 
#        for these fits. Be aware that failures for the fits from the list will
#        be silently ignored.
#        """
#        # default fit
#        if default:
#            try:
#                self.defaultFitter.SetParameter(parname, status)
#            except ValueError, msg:
#                hdtv.ui.error("while editing default Fit: \n\t%s" % msg)
#        # active fit
#        fit = self.workFit
#        try:
#            fit.fitter.SetParameter(parname, status)
#            fit.Refresh()
#        except ValueError, msg:
#            hdtv.ui.error("while editing active Fit: \n\t%s" % msg)
#        # fit list
#        for ID in ids:
#            try:
#                fit = self.spectra[self.spectra.activeID].fits[ID]
#                fit.fitter.SetParameter(parname, status)
#                fit.Refresh()
#            except ValueError:
#                pass
#        # Update fitPanel
#        #self.UpdateFitPanel()
 

#    def ResetParameters(self, default = False, ids = []):
#        if default:
#            self.defaultFitter.ResetParamStatus()
#        # active Fit
#        fit = self.workFit
#        fit.fitter.ResetParamStatus()
#        fit.Refresh()
#        # fit list
#        for ID in ids:
#            fit = self.spectra[self.spectra.activeID].fits[ID]
#            fit.fitter.ResetParamStatus()
#            fit.Refresh()
#        # Update fitPanel
#        #self.UpdateFitPanel()


#    def SetPeakModel(self, peakmodel, default = False, ids = []):
#        """
#        Set the peak model (function used for fitting peaks)
#        """
#        # default
#        if default:
#            self.defaultFitter.SetPeakModel(peakmodel)
#        # active fit
#        fit = self.workFit
#        fit.fitter.SetPeakModel(peakmodel)
#        fit.Refresh()
#        for ID in ids:
#            fit = self.spectra[self.spectra.activeID].fits[ID]
#            fit.fitter.SetPeakModel(peakmodel)
#            fit.Refresh()
#        # Update fit panel
#        #self.UpdateFitPanel()
            
# TODO: Remove or fix
#    def UpdateFitPanel(self):
#        
#        if not self.fitPanel:
#            return
#        fit = self.workFit
#        # options
#        text = str()
#        text += "Background model: polynomial, deg=%d\n" % fit.fitter.bgdeg
#        text += "Peak model: %s\n" % fit.fitter.peakModel.name
#        text += "\n"
#        text += fit.fitter.peakModel.OptionsStr()
#        self.fitPanel.SetOptions(text)
#        # data
#        text = str()
#        if fit.fitter.bgFitter:
#            deg = fit.fitter.bgFitter.GetDegree()
#            chisquare = fit.fitter.bgFitter.GetChisquare()
#            text += "Background (seperate fit): degree = %d   chi^2 = %.2f\n" % (deg, chisquare)
#            for i in range(0, deg + 1):
#                value = hdtv.util.ErrValue(fit.fitter.bgFitter.GetCoeff(i),
#                                           fit.fitter.bgFitter.GetCoeffError(i))
#                text += "bg[%d]: %s   " % (i, value.fmt())
#            text += "\n\n"
#        i = 0
#        if fit.fitter.peakFitter:
#            text += "Peak fit: chi^2 = %.2f\n" % fit.fitter.peakFitter.GetChisquare()
#            for peak in fit.peaks:
#                text += "Peak %d:\n%s\n" % (i, str(peak))
#                i += 1
#        self.fitPanel.SetData(text)
#        

class TvFitInterface:
    """
    TV style interface for fitting
    """
    def __init__(self, fitInterface):
        self.fitIf = fitInterface
        self.spectra = self.fitIf.spectra     
        
        # Register configuration variables for fit list
#        opt = hdtv.options.Option(default = "ID")
#        hdtv.options.RegisterOption("fit.list.sort_key", opt) 
#        
#        prog = "fit fit"
#        description = "(re)fit a fit"
#        usage = "%prog [OPTIONS] <fit-ids>"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-s", "--spectrum", action = "store", default = "active",
#                            help = "Spectra to work on")
#        parser.add_option("-b", "--background", action = "store_true", default = False,
#                            help = "fit only the background")
#        hdtv.cmdline.AddCommand(prog, self.DoFit, level=0, parser = parser)
#        # the "fit fit" command is registered with level=0, 
#        # this allows "fit fit" to be abbreviated as "fit", register all other 
#        # commands starting with spectrum with default or higher priority
#        
#        prog = "fit marker set"
#        description = "set a marker to position"
#        description +="(possible types are background, region, peak)"
#        usage = "%prog type position"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        hdtv.cmdline.AddCommand(prog, self.FitMarkerSet, nargs=2,
#                                parser = parser, completer=self.MarkerCompleter)
#        
#        prog = "fit marker delete"
#        description = "delete the marker of the given type that is nearest to position."
#        description += "(possible types are background, region, peak)"
#        usage = "%prog type position"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        hdtv.cmdline.AddCommand(prog, self.FitMarkerDelete, nargs=2,
#                                parser = parser, completer=self.MarkerCompleter)
#        
#        prog = "fit store"
#        description = "store the active work fit to fitlist"
#        usage = "%prog"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        hdtv.cmdline.AddCommand(prog, self.FitStore, nargs=0, parser = parser)
#        
#        prog = "fit clear"
#        description = "clear the active work fit"
#        usage = "%prog"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        hdtv.cmdline.AddCommand(prog, self.FitClear, nargs=0, parser = parser)
        
#        prog = "fit list"
#        description = "show a list of all fits belonging to the active spectrum"
#        usage = "%prog"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-l", "--long", action = "store_true", default = False,
#                        help = "show more details")
#        hdtv.cmdline.AddCommand(prog, self.FitList, nargs = 0, parser = parser)
        
#        prog = "fit show"
#        description = "display fits"
#        usage = "%prog none|all|<ids>"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-s", "--spectrum", action = "store", default = "active",
#                        help = "select spectra to work on")
#        parser.add_option("-v", "--adjust-viewport", action = "store_true", default = False,
#                        help = "adjust viewport to include all fits")
#        # TODO: add option to show the fit, that is closest to a certain value
#        hdtv.cmdline.AddCommand(prog, self.FitShow, minargs = 1, parser = parser)
#        
#        prog = "fit hide"
#        description = "hide fits"
#        usage = "%prog all|<ids>"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-s", "--spectrum", action = "store", default = "active",
#                        help = "select spectra to work on")
#        # TODO: add option to show the fit, that is closest to a certain value
#        hdtv.cmdline.AddCommand(prog, self.FitHide, parser = parser)
#        
        
#        prog = "fit focus"
#        description = "focus on fit with id"
#        usage = "fit focus [<id>]"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        hdtv.cmdline.AddCommand(prog, self.FitFocus, minargs = 0, parser = parser)
        
#        prog = "fit print"
#        description = "print fit results"
#        usage = "%prog all|<ids>"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-v", "--visible", action = "store_true", default = False,
#                        help = "only list visible fit")
#        parser.add_option("-k", "--key-sort", action = "store", default = "",
#                        help = "sort by key")
#        parser.add_option("-r", "--reverse-sort", action = "store_true", default = False,
#                        help = "reverse the sort")
#        parser.add_option("-s", "--spectrum", action = "store", default = "active",
#                        help = "select spectra to work on")       
#        hdtv.cmdline.AddCommand(prog, self.FitPrint, level=2, parser = parser)
        
#        prog = "fit delete"
#        description = "delete fits"
#        usage = "%prog all|<ids>"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-s", "--spectrum", action = "store", default = "active",
#                        help = "spectrum ids to work on")
#        hdtv.cmdline.AddCommand(prog, self.FitDelete, minargs = 1, parser = parser)
#        
#        prog = "fit activate"
#        description = "activate fit for further work"
#        usage = "%prog <id>"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        # TODO: add option to re-activate newest fit
#        # TODO: add option to activate the fit, that is closest to a certain value
#        hdtv.cmdline.AddCommand(prog, self.FitActivate, nargs = 1, parser = parser)
#        
#        prog = "fit copy"
#        description = "Copy fit parameter and marker to another spectrum"
#        usage = "%prog -s <targetSpecs> <fit-ids>"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage=usage)
#        parser.add_option("-s", "--spectrum", action = "store", default = "all", help = "Target spectra")
#        parser.add_option("-f", "--refit", action = "store_true", default = False, help = "Perform fit on new spectrum")
#        hdtv.cmdline.AddCommand(prog, self.FitCopy, parser = parser)
        
#        prog = "fit parameter"
#        description = "show status of fit parameter, reset or set parameter"
#        usage = "%prog [OPTIONS] status | reset | parname <valuePeak1>, <valuePeak2>, ..."
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-d", "--default", action = "store_true", default = False,
#                            help = "act on default fitter")
#        parser.add_option("-f", "--fit", action = "store", default = None,
#                            help = "change parameter of selected fit and refit")
#        hdtv.cmdline.AddCommand(prog, self.FitParam, completer = self.ParamCompleter,
#                                parser = parser, minargs = 1)
#                                
#                                
#        prog = "fit reset"
#        description = "reset fit functions of a fit"
#        usage = "%prog [OPTIONS] <fit-ids>"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-s", "--spectrum", action = "store", default = "active",
#                            help = "Spectra to work on")
#        parser.add_option("-k", "--keep-fitter", action = "store_true", default = False,
#                            help = "Keep fitter parameters")
#        hdtv.cmdline.AddCommand(prog, self.ResetFit, parser = parser)
#        
#        prog = "fit function peak activate"
#        description = "selects which peak model to use"
#        usage = "%prog [OPTIONS] name"
#        parser = hdtv.cmdline.HDTVOptionParser(prog = prog, description = description, usage = usage)
#        parser.add_option("-d", "--default", action = "store_true", default = False,
#                            help = "change default fitter")
#        parser.add_option("-f", "--fit", action = "store", default = None,
#                            help = "change selected fits and refit")
#        hdtv.cmdline.AddCommand(prog, self.FitSetPeakModel,
#                                completer = self.PeakModelCompleter,
#                                parser = parser, minargs = 1)

#    def FitList(self, args, options):
#        """
#        Print a list of all fits belonging a spectrum
#        """
#        hdtv.ui.error("\"fit list\" command is currently reworked. Functionality has been merged with \"fit print\"")
#        hdtv.ui.error("Please use \"fit print all\" for equivalent functionality")
#        return
    
#    def FitDelete(self, args, options):
#        """ 
#        Delete fits
#        """
#        sids = hdtv.cmdhelper.ParseIds(options.spec, self.spectra)
#          
#        if len(sids)>0:
#            for s in sids:
#                spec = self.spectra[s]
#                ids = hdtv.cmdhelper.ParseIds(args, spec.fits)
#                spec.fits.RemoveObjects(ids)
#        else:
#            hdtv.ui.warn("Nothing to do (No spectra chosen or active)")
#            return

#    def FitHide(self, args, options):
#        """
#        Hide Fits
#        """
#        # FitHide is the same as FitShow, except that the spectrum selection is inverted
#        self.FitShow(args, options, inverse=True)
#    
#    def FitShow(self, args, options, inverse=False):
#        """
#        Show Fits
#        
#        inverse = True inverses the fit selection i.e. FitShow becomes FitHide
#        """
#        sids = hdtv.cmdhelper.ParseIds(options.spec, self.spectra)

#        for sid in sids:
#            try:
#                spec = self.spectra[sid]
#            except KeyError:
#                hdtv.msg.error("No spectrum " + str(sid))
#                continue

#            fitIDs = hdtv.cmdhelper.ParseIds(args, spec.fits)
#     
#            if len(fitIDs) > 0:
#                if inverse:
#                    spec.fits.HideObjects(fitIDs)
#                else:
#                    self.fitIf.ShowFits(fitIDs, specID = sid, adjustViewport=options.adjust_viewport)
#            else:
#                spec.fits.HideAll()


#    def FitPrint(self, args, options):
#        """
#        Print fit results
#        """
#        self.fitIf.PrintFits(args, options.spec, onlyVisible=options.visible, 
#                             sortBy=options.key_sort, reverseSort=options.reverse_sort)


#    def FitActivate(self, args, options):
#        """
#        Activate one fit
#        """
#        
#        if self.spectra.activeID==None:
#            hdtv.ui.error("There is no active spectrum")
#            return
#        
#        spec = self.spectra[self.spectra.activeID]

#        if len(spec.fits) == 0:
#            hdtv.ui.error("There are no fits for this spectrum")
#            return

#        ID = hdtv.cmdhelper.ParseIds(args, spec.fits)
#       
#        if len(ID) == 1:
#            hdtv.ui.msg("Activating fit %s" %ID[0])
#            self.fitIf.ActivateFit(ID[0])
#        elif len(ID) == 0:
#            hdtv.ui.msg("Deactivating fit")
#            self.fitIf.ActivateFit(None)
#        else:
#            hdtv.ui.error("Can only activate one fit")

#    def FitFocus(self, args, options):
#        """
#        Focus a fit. If no fit is given focus the active fit
#        """
#        if self.spectra.activeID==None:
#            hdtv.ui.error("There is no active spectrum")
#            return False
#        
#        assert self.spectra.activeID in self.spectra.visible, "Active objects should always be visible"
#                
#        if len(args) == 0:
#            args = ["active"]
#        ids = hdtv.cmdhelper.ParseIds(args, self.spectra[self.spectra.activeID].fits)
#        
#        if len(ids) > 0:
#            self.fitIf.FocusFits(ids)
#        else:
#            hdtv.ui.error("Nothing to focus")

#    def FitCopy(self, args, options):
#        """
#        Copy fit parameter and marker to other spectra and optionally fit on new spectrum
#        """
#        if self.spectra.activeID is None:
#            hdtv.ui.error("No active spectrum")
#            return
#        
#        specIDs = hdtv.cmdhelper.ParseIds(options.spec, self.spectra)
#        
#        # Remove active spectrum from target specIDs
#        try:
#            specIDs.remove(self.spectra.activeID)
#        except ValueError:
#            pass

#        if len(specIDs) == 0:
#            hdtv.ui.error("No target spectra")
#            
#        if len(args) == 0:
#            args = ["active"]
#            
#        ids = hdtv.cmdhelper.ParseIds(args, self.spectra[self.spectra.activeID].fits)
#       
#        self.fitIf.CopyFits(ids, self.spectra.activeID, specIDs, refit=options.refit)

#    def FitSetPeakModel(self, args, options):
#        """
#        Defines peak model to use for fitting
#        """
#        name = args[0].lower()
#        # complete the model name if needed
#        models = self.PeakModelCompleter(name)
#        # check for unambiguity
#        if len(models)>1:
#            hdtv.ui.error("Peak model name '%s' is ambiguous" %name)
#        if len(models)==0:
#            hdtv.ui.error("Invalid peak model '%s'" %name)
#        else:
#            name = models[0]
#            name = name.strip()
#            ids = list()
#            if options.fit:
#                if self.spectra.activeID is None:
#                    hdtv.ui.warn("No active spectrum, no action taken.")
#                    return
#                spec = self.spectra[self.spectra.activeID]
#                ids = hdtv.cmdhelper.ParseFitIds(options.fit, spec.fits)
#            self.fitIf.SetPeakModel(name, options.default, ids)

#    def PeakModelCompleter(self, text, args=None):
#        """
#        Creates a completer for all possible peak models
#        """
#        return hdtv.cmdhelper.GetCompleteOptions(text, hdtv.peakmodels.PeakModels.iterkeys())

#    def FitParam(self, args, options):
#        # first argument is parameter name
#        param = args.pop(0)
#        # complete the parameter name if needed
#        parameter = self.ParamCompleter(param)
#        # check for unambiguity
#        if len(parameter)>1:
#            hdtv.ui.error("Parameter name %s is ambiguous" %param)
#            return
#        if len(parameter)==0:
#            hdtv.ui.error("Parameter name %s is not valid" %param)
#            return
#        param = parameter[0]
#        param = param.strip()
#        ids =list()
#        if options.fit:
#            if self.spectra.activeID is None:
#                hdtv.ui.warn("No active spectrum, no action taken.")
#                return
#            spec = self.spectra[self.spectra.activeID]
#            ids = hdtv.cmdhelper.ParseFitIds(options.fit, spec.fits)
#        if param=="status":
#            self.fitIf.ShowFitStatus(options.default, ids)
#        elif param == "reset":
#            self.fitIf.ResetParameters(options.default, ids)
#        else:
#            try:
#                self.fitIf.SetParameter(param, " ".join(args), options.default, ids)
#            except ValueError, msg:
#                hdtv.ui.error(msg)
#        
#    def ParamCompleter(self, text, args=None):
#        """
#        Creates a completer for all possible parameter names 
#        or valid states for a parameter (args[0]: parameter name).
#        If the different peak models are used for active fitter and default fitter,
#        options for both peak models are presented to the user.
#        """
#        if not args:
#            params = set(["status", "reset"])
#            defaultParams = set(self.fitIf.defaultFitter.params)
#            activeParams  = set(self.fitIf.workFit.fitter.params)
#            # create a list of all possible parameter names
#            params = params.union(defaultParams).union(activeParams)
#            return hdtv.cmdhelper.GetCompleteOptions(text, params)
#        else:
#            param = args[0]
#            states = set()
#            # valid states for param in default fitter
#            defaultPM = self.fitIf.defaultFitter.peakModel
#            try:
#                defaultStates = set(defaultPM.fValidParStatus[param])
#                if len(defaultStates)>1:
#                    states.update(defaultStates)
#            except KeyError:
#                # param is not a parameter of the peak model of the default fitter
#                pass
#            # valid states for param in active fitter
#            activePM = self.fitIf.workFit.fitter.peakModel
#            try:
#                activeStates = activePM.fValidParStatus[param]
#                if len(activeStates)>1:
#                    states.update(activeStates)
#            except KeyError:
#                # param is not a parameter of the peak model of active fitter
#                pass
#            # remove <type: float> option
#            states.discard(float)
#            return hdtv.cmdhelper.GetCompleteOptions(text, states)
        
#    def FitMarkerSet(self, args, options):
#        """
#        Set Marker from command line
#        """
#        # first argument is marker type name
#        mtype = args[0]
#        # complete markertype if needed
#        mtype = self.MarkerCompleter(mtype)
#        if len(mtype)==0:
#            hdtv.ui.error("Markertpye %s is not valid" %args[0])
#            return
#        # parse position
#        try:
#            pos = float(args[1])
#        except ValueError:
#            hdtv.ui.error("Invalid position argument")
#            return
#        # replace "background" with "bg" which is internally used
#        if mtype[0].strip()=="background": mtype[0]="bg"
#        fit = self.fitIf.workFit
#        getattr(fit, "Put%sMarker" % mtype[0].strip().title())(pos)
#        
#    def FitMarkerDelete(self, args, options):
#        """
#        Set Marker from command line
#        """
#        # first argument is marker type name
#        mtype = args[0]
#        # complete markertype if needed
#        mtype = self.MarkerCompleter(mtype)
#        if len(mtype)==0:
#            hdtv.ui.error("Markertpye %s is not valid" %args[0])
#            return
#        # parse position
#        try:
#            pos = float(args[1])
#        except ValueError:
#            hdtv.ui.error("Invalid position argument")
#            return
#        # replace "background" with "bg" which is internally used
#        if mtype[0].strip()=="background": mtype[0]="bg"
#        fit = self.fitIf.workFit
#        markers = getattr(fit, "%sMarkers" % mtype[0].strip().lower())
#        markers.RemoveNearest(pos)  
#        
#    def MarkerCompleter(self, text, args=None):
#        """
#        Completer for marker names
#        """
#        mtypes = ["background","region", "peak"]
#        return hdtv.cmdhelper.GetCompleteOptions(text, mtypes)

#    def FitStore(self, args, options):
#        """
#        Stores work fit
#        """
#        self.fitIf.StoreFit()
#        
#    def FitClear(self, args, options):
#        """
#        Clears work fit
#        """
#        self.fitIf.ClearFit()
        
#    def DoFit(self, args, options):
#        """
#        Perform a fit
#        """
#        specIDs = hdtv.cmdhelper.ParseIds(options.spec, self.spectra)
#        
#        if len(specIDs) == 0:
#            hdtv.ui.warn("No spectrum to work on")
#            return
#        
#        if options.background:
#            doPeaks = False
#        else:
#            doPeaks = True

#        for specID in specIDs:
#            
#            fitIDs = hdtv.cmdhelper.ParseIds(args, self.spectra[specID].fits)
#            
#            if len(fitIDs) == 0:
#                if specID==self.spectra.activeID and self.fitIf._workFit:
#                    self.fitIf.Fit(peaks=doPeaks) 
#                else:
#                    hdtv.ui.warn("No fit for spectrum %s to work on." %specID)
#            for fitID in fitIDs:    
#                self.fitIf.Fit(specID=specID, fitID=fitID, peaks=doPeaks) 
    
    def ResetFit(self, args, options):
        """
        Reset fitter of a fit to unfitted default.
        """
        specIDs = hdtv.cmdhelper.ParseIds(options.spec, self.spectra)
        
        if len(specIDs) == 0:
            hdtv.ui.error("No spectrum to work on")
            return
        
        for specID in specIDs:
            
            fitIDs = hdtv.cmdhelper.ParseIds(args, self.spectra[specID].fits)
            
            if len(fitIDs) == 0:
                hdtv.ui.warn("No fit for spectrum %d to work on", specID)
                continue
            
            for fitID in fitIDs:    
                self.fitIf.FitReset(specID=specID, fitID=fitID, resetFitter=not options.keep_fitter) 

# plugin initialisation
import __main__
if not hasattr(__main__, "window"):
    import hdtv.window
    __main__.window = hdtv.window.Window()
if not hasattr(__main__, "spectra"):
    import hdtv.drawable
    __main__.spectra = hdtv.drawable.DrawableCompound(__main__.window.viewport)
__main__.f = FitInterface(__main__.window, __main__.spectra, show_panel = False)


