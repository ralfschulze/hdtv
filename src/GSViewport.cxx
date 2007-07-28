/*
 * gSpec - a viewer for gamma spectra
 *  Copyright (C) 2006  Norbert Braun <n.braun@ikp.uni-koeln.de>
 *
 * This file is part of gSpec.
 *
 * gSpec is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * gSpec is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with gSpec; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
 * 
 */

#include "GSViewport.h"
#include <Riostream.h>

GSViewport::GSViewport(const TGWindow *p, UInt_t w, UInt_t h)
  : TGFrame(p, w, h)
{
  SetBackgroundColor(GetBlackPixel());
  fXVisibleRegion = 100.0;
  fYVisibleRegion = 100.0;
  fYMinVisibleRegion = 20.0;
  fOffset = 0.0;
  fMinEnergy = 0;
  fMaxEnergy = 5000;
  fNbins = 0;
  fSpec = NULL;
  fDispSpec = NULL;
  fYAutoScale = true;
  fNeedClear = false;
  fDragging = false;
  fLeftBorder = 60;
  fRightBorder = 3;
  fTopBorder = 4;
  fBottomBorder = 30;

  AddInput(kPointerMotionMask | kEnterWindowMask | kLeaveWindowMask
		   | kButtonPressMask | kButtonReleaseMask);

  GCValues_t gval;
  gval.fMask = kGCForeground | kGCFunction;
  gval.fFunction = kGXxor;
  gval.fForeground = GetWhitePixel();
  fCursorGC = gClient->GetGCPool()->GetGC(&gval, true);
  fCursorVisible = false;
  fSpecPainter = new GSSpecPainter();
  fSpecPainter->SetDrawable(GetId());
  fSpecPainter->SetAxisGC(GetHilightGC().GetGC());
  fSpecPainter->SetClearGC(GetBlackGC().GetGC());
  fSpecPainter->SetLogScale(false);
  fSpecPainter->SetXVisibleRegion(fXVisibleRegion);
  fSpecPainter->SetYVisibleRegion(fYVisibleRegion);
}

GSViewport::~GSViewport() {
  cout << "viewport destructor" << endl;
  fClient->GetGCPool()->FreeGC(fCursorGC);   //?
  if(fDispSpec)
	delete fDispSpec;
}

void GSViewport::SetLogScale(Bool_t l)
{
  fSpecPainter->SetLogScale(l);
  Update(true);
}

void GSViewport::ShiftOffset(int dO)
{
  Bool_t cv = fCursorVisible;
  UInt_t x, y, w, h;
  double az;

  x = fLeftBorder + 2;
  y = fTopBorder + 2;
  w = fWidth - fLeftBorder - fRightBorder - 4;
  h = fHeight - fTopBorder - fBottomBorder - 4;

  if(!fSpec) return;
  
  // TODO: debug code, remove
  if(dO == 0) {
	cout << "WARNING: Pointless call to ShiftOffset()." << endl;
	return;
  }

  if(cv) DrawCursor();

  if(dO < -((Int_t) w) || dO > ((Int_t) w)) { // entire area needs updating
	gVirtualX->FillRectangle(GetId(), GetBlackGC()(), x, y, w+1, h+1);
	DrawRegion(x, x+w);
  } else if(dO < 0) {   // move right (note that dO ist negative)
	gVirtualX->CopyArea(GetId(), GetId(), GetWhiteGC()(), x, y,
						w + dO + 1, h + 1, x - dO, y);
	// Note that the area filled by FillRectangle() will not include
	// the border drawn by DrawRectangle() on the right and the bottom
	gVirtualX->FillRectangle(GetId(), GetBlackGC()(), x, y, -dO, h+1);
	DrawRegion(x, x-dO);
  } else { // if(dO > 0) : move left (we caught dO == 0 above)
	gVirtualX->CopyArea(GetId(), GetId(), GetWhiteGC()(), x + dO, y,
						w - dO + 1, h + 1, x, y);
	gVirtualX->FillRectangle(GetId(), GetBlackGC()(), x+w-dO+1, y, dO, h+1);
	DrawRegion(x+w-dO+1, x+w);
  }

  // Redrawing the entire scale is not terribly efficent, but
  // for now I am lazy...
  fSpecPainter->ClearXScale();
  fSpecPainter->DrawXScale(x, x+w);

  if(cv) DrawCursor();
}

void GSViewport::SetViewMode(EViewMode vm)
{
  if(vm != fSpecPainter->GetViewMode()) {
	fSpecPainter->SetViewMode(vm);
	fNeedClear = true;
	gClient->NeedRedraw(this);
  }
}

void GSViewport::LoadSpectrum(GSSpectrum *spec)
{
  fSpec = spec;
  fDispSpec = new GSDisplaySpec(fSpec);

  fNbins = fSpec->GetNbinsX();
}

void GSViewport::XZoomAroundCursor(double f)
{
  fOffset += fSpecPainter->dXtodE(fCursorX - fSpecPainter->GetBaseX()) * (1.0 - 1.0/f);
  fXVisibleRegion /= f;

  Update(false);
}

void GSViewport::ToBegin(void)
{
  SetOffset(fSpec->GetMinEnergy());
}

void GSViewport::ShowAll(void)
{
  fOffset = fSpec->GetMinEnergy();
  fXVisibleRegion = fSpec->GetMaxEnergy() - fSpec->GetMinEnergy();
  Update(false);
}

/* GSViewport::Update

   This function brings the viewport up-to-date after a change in any
   relevant parameters. It tries to do so with minimal effort,
   i.e. not by redrawing unconditionally.
*/
void GSViewport::Update(bool redraw)
{
  double az;
  double dO, dOPix;

  //cout << "Update() called" << endl;

  // Remember not to compare floating point values
  // for equality directly (rouding error problems)
  if(TMath::Abs(fXVisibleRegion - fSpecPainter->GetXVisibleRegion()) > 1e-7) {
	redraw = true;
	fSpecPainter->SetXVisibleRegion(fXVisibleRegion);
	UpdateScrollbarRange();
  }

  dO = fOffset - fSpecPainter->GetOffset();
  if(TMath::Abs(dO) > 1e-5) {
	fSpecPainter->SetOffset(fOffset);
  }

  if(fYAutoScale)
	fYVisibleRegion = TMath::Max(fYMinVisibleRegion, fSpecPainter->GetYAutoZoom(fDispSpec));

  if(TMath::Abs(fYVisibleRegion - fSpecPainter->GetYVisibleRegion()) > 1e-7) {
	redraw = true;
	fSpecPainter->SetYVisibleRegion(fYVisibleRegion);
  }

  // We can only use ShiftOffset if the shift is an integer number
  // of pixels, otherwise we will have to do a full redraw
  dOPix = fSpecPainter->dEtodX(dO);
  if(TMath::Abs(TMath::Ceil(dOPix - 0.5) - dOPix) > 1e-7) {
	redraw = true;
  }
  
  if(redraw) {
	//cout << "redraw" << endl;
	fNeedClear = true;
	gClient->NeedRedraw(this);
  } else if(TMath::Abs(dOPix) > 0.5) {
	ShiftOffset((int) TMath::Ceil(dOPix - 0.5));
  }

  UpdateScrollbarRange();
}

void GSViewport::DrawRegion(UInt_t x1, UInt_t x2)
{
  fSpecPainter->DrawSpectrum(fDispSpec, x1, x2);
}

void GSViewport::UpdateScrollbarRange(void)
{
  if(fScrollbar) {
	UInt_t as, rs, pos;
	double minE, maxE;

	as = fSpecPainter->GetWidth();

	minE = fSpec ? fSpec->GetMinEnergy() : 0.0;
	minE = TMath::Min(minE, fSpecPainter->GetOffset());
	
	maxE = fSpec ? fSpec->GetMaxEnergy() : 0.0;
	maxE = TMath::Max(maxE, fSpecPainter->GetOffset() + fXVisibleRegion);

	rs = (UInt_t) TMath::Ceil(fSpecPainter->dEtodX(maxE - minE));

	pos = (UInt_t) TMath::Ceil(fSpecPainter->dEtodX(fSpecPainter->GetOffset() - minE) - 0.5);

	fScrollbar->SetRange(rs, as);
	fScrollbar->SetPosition(pos);
  }
}

void GSViewport::SetOffset(double offset)
{
  fOffset = offset;
  Update();
}

void GSViewport::HandleScrollbar(Long_t parm)
{
  // Callback for scrollbar motion

  // Capture nonsense input (TODO: still required?)
  if(parm < 0)
  	parm = 0;

  if(fOffset < fSpec->GetMinEnergy())
	fOffset += fSpecPainter->dXtodE(parm);
  else
	fOffset = fSpec->GetMinEnergy() + fSpecPainter->dXtodE(parm);

  Update();
}


Bool_t GSViewport::HandleMotion(Event_t *ev)
{
  bool cv = fCursorVisible;
  if(cv) DrawCursor();
  if(fDragging) {
	SetOffset(fOffset + fSpecPainter->dXtodE((int) fCursorX - ev->fX));
  }
  fCursorX = ev->fX;
  fCursorY = ev->fY;
  if(cv) DrawCursor();
}

Bool_t GSViewport::HandleButton(Event_t *ev)
{
  if(ev->fType == kButtonPress)
	fDragging = true;
  else
	fDragging = false;
}

Bool_t GSViewport::HandleCrossing(Event_t *ev)
{
  if(ev->fType == kEnterNotify) {
	if(fCursorVisible) DrawCursor();
	fCursorX = ev->fX;
	fCursorY = ev->fY;
	DrawCursor();
  } else if(ev->fType == kLeaveNotify) {
	if(fCursorVisible) DrawCursor();
  }
}

void GSViewport::DrawCursor(void)
{
  gVirtualX->DrawLine(GetId(), fCursorGC->GetGC(), 1, fCursorY, fWidth, fCursorY);
  gVirtualX->DrawLine(GetId(), fCursorGC->GetGC(), fCursorX, 1, fCursorX, fHeight);
  fCursorVisible = !fCursorVisible;
}

void GSViewport::Layout(void)
{ 
  fSpecPainter->SetBasePoint(fLeftBorder + 2, fHeight - fBottomBorder - 2);
  fSpecPainter->SetSize(fWidth - fLeftBorder - fRightBorder - 4,
						fHeight - fTopBorder - fBottomBorder - 4);
}

/* GSViewport::DoRedraw

   Redraws the Viewport completely.  If fNeedClear is set, it is
   cleared first, otherwise it is just redrawn. This is a callback for
   the windowing system. It should not be called directly, but via 
   gClient->NeedRedraw() .
*/
void GSViewport::DoRedraw(void)
{
  Bool_t cv;
  UInt_t x, y, w, h;

  x = fLeftBorder;
  y = fTopBorder;
  w = fWidth - fLeftBorder - fRightBorder;
  h = fHeight - fTopBorder - fBottomBorder;

  //cout << "DoRedraw()" << endl;

  fSpecPainter->SetXVisibleRegion(fXVisibleRegion);
  fSpecPainter->SetYVisibleRegion(fYVisibleRegion);
  fSpecPainter->SetOffset(fOffset);

  cv = fCursorVisible;
  if(cv) DrawCursor();

  if(fNeedClear) {
	// Note that the area filled by FillRectangle() will not include
	// the border drawn by DrawRectangle() on the right and the bottom
	gVirtualX->FillRectangle(GetId(), GetBlackGC()(), 0, 0, fWidth, fHeight);
	fNeedClear = false;
  }

  gVirtualX->DrawRectangle(GetId(), GetHilightGC()(), x, y, w, h);

  if(fSpec) {
	DrawRegion(x+2, x+w-2);
	fSpecPainter->DrawXScale(x+2, x+w-2);
	fSpecPainter->DrawYScale();
  }

  if(cv) DrawCursor();
}
