# -*- coding: utf-8 -*-
# FreeCAD Exploded Assembly Animation Workbench
# (c) 2016 Javier Martínez García

#***************************************************************************
#*   (c) Javier Martínez García 2016                                       *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU General Public License (GPL)            *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This macro is distributed in the hope that it will be useful,         *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************/

import os
import FreeCAD
import FreeCADGui
import ExplodedAssembly as ea
__dir__ = os.path.dirname(__file__)

# TODO CHANGE NAME: SIMPLE DISASSEMBLE GROUP, WIRE DISASSEMBLE GROUP


class CreateBoltGroup:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/BoltGroup.svg',
                'MenuText': 'Create Bolt Group',
                'ToolTip': 'Create a special exploded group for screws, nuts, bolts... \n Select circular edges of the shape you want to animate, then\n select one face (arbitrary shape) wich has as normal vector\nin the direction in wich you want to move the selected shapes'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        ea.checkDocumentStructure()
        ea.createBoltDisassemble()


class CreateSimpleGroup:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/SimpleGroup.svg',
                'MenuText': 'Create Simple Group',
                'ToolTip': 'Select the objects you want to explode and\nfinally the face which its normal is the trajectory director vector'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        ea.checkDocumentStructure()
        ea.createSimpleDisassemble()

class CreateWireGroup:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/WireTrajectory.svg',
                'MenuText': 'Create Route',
                'ToolTip': 'Select first one or more shapes and last the wire or sketch that represents the trajectory'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        pass


class PlaceBeforeSelectedTrajectory:
    # execute this function with caution
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/PlaceBeforeTrajectory.svg',
                'MenuText': 'PlaceBefore',
                'ToolTip': 'Select the trajectories you want to reallocate (in order) and finally\nthe trajectory before which you want to place them'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        # check selection before running (rearrange objects is dangerous, use with caution)
        try:
            sel = FreeCAD.Gui.Selection.getSelectionEx()
            a = sel[0].Object.Distance
            a = sel[1].Object.Distance
            #  selection are trajectories, proceed
            ea.placeBeforeSelectedTrajectory()
            ea.resetPlacement()
            FreeCAD.Gui.Selection.clearSelection()
            FreeCAD.Gui.Selection.addSelection(sel[0].Object)
            ea.goToSelectedTrajectory()

        except:
            FreeCAD.Console.PrintError('\n Select exploded assembly trajectory objects only')


class PlayForward:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/PlayForward.svg',
                'MenuText': 'Create Route',
                'ToolTip': 'Run the assembly animation'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        EA = FreeCAD.ActiveDocument.ExplodedAssembly
        if EA.CurrentTrajectory <= 0:
            # if exploded state = 0 or -1, reset and run
            ea.resetPlacement()
            ea.runAnimation()

        else:
            # if animation has been paused in the middle:
            cr_traj = EA.Group[EA.CurrentTrajectory]
            ea.runAnimation(start=EA.CurrentTrajectory+1, mode='toPoint')


class PlayBackward:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/PlayBackward.svg',
                'MenuText': 'Create Route',
                'ToolTip': 'Run the assembly animation backwards'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        EA = FreeCAD.ActiveDocument.ExplodedAssembly
        if EA.CurrentTrajectory <= 0:
            # if exploded state = 0 or -1, reset and run
            ea.resetPlacement()
            ea.goToEnd()
            ea.runAnimation(direction='backward')

        else:
            # if animation has been paused in the middle:
            ea.runAnimation(end=-EA.CurrentTrajectory - 1 + len(EA.Group),
                            mode='toPoint',
                            direction='backward')


class StopAnimation:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/Pause.svg',
                'MenuText': 'StopAnimation',
                'ToolTip': 'Stops the animation at the current trajectory'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return False

            else:
                return True

        else:
            return False

    def Activated(self):
        FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation = False
        # FreeCAD.Gui.updateGui()


class GoToStart:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/GoToStart.svg',
                'MenuText': 'Assemble',
                'ToolTip': 'Go to the assembled position of the parts'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument.ExplodedAssembly:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        ea.resetPlacement()
        FreeCAD.ActiveDocument.ExplodedAssembly.CurrentTrajectory = 0


class GoToEnd:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/GoToEnd.svg',
                'MenuText': 'Disassemble',
                'ToolTip': 'Expand all trajectories'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument.ExplodedAssembly:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        ea.resetPlacement()
        ea.goToEnd()
        FreeCAD.ActiveDocument.ExplodedAssembly.CurrentTrajectory = -1


class GoToSelectedTrajectory:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/ExplodeToSelection.svg',
                'MenuText': 'ExplodeToSelection',
                'ToolTip': 'Expand up to the selected trajectory'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument.ExplodedAssembly:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        try:
            ea.resetPlacement()
            ea.goToSelectedTrajectory()

        except:
            FreeCAD.Console.PrintError('Error: Select one exploded animation trajectory')


class ToggleTrajectoryVisibility:
    def __init__(self):
        self.visibility = True

    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/TrajectoryLineVisibility.svg',
                'MenuText': 'Trajectory Visibility',
                'ToolTip': 'Toggle trajectory visibility'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument.ExplodedAssembly:
            return True

        else:
            return False

    def Activated(self):
        self.visibility = not(self.visibility)
        ea.visibilityTrajectoryLines(self.visibility)



# Assembly tools ###############################################################
class AlignToEdge:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/AlignToEdge.svg',
                'MenuText': 'Align to edge',
                'ToolTip': 'Auxiliary tool to align shapes.\nPick one edge of the object you want to align and\nthen the edge of the object used as reference'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        sel = FreeCAD.Gui.Selection.getSelectionEx()
        objA = sel[0].Object
        edgeA = sel[0].SubObjects[0]
        edgeB = sel[1].SubObjects[0]
        # transform object A placement
        # edge vector
        va = (edgeA.Curve.EndPoint - edgeA.Curve.StartPoint).normalize()
        vb = (edgeB.Curve.EndPoint - edgeB.Curve.StartPoint).normalize()
        # rot centre
        centre = edgeA.Curve.StartPoint
        # new placement
        new_plm = FreeCAD.Placement(FreeCAD.Vector(0,0,0), FreeCAD.Rotation(va, vb), centre)
        # apply placement
        objA.Placement = new_plm.multiply(objA.Placement)


class PointToPoint:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/SharePoint.svg',
                'MenuText': 'Point to point',
                'ToolTip': 'Auxiliary tool to move point to point.\nSelect one point from the shape you want to move \n and then the point from other shape where you want to place it'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        sel = FreeCAD.Gui.Selection.getSelectionEx()
        objA = sel[0].Object
        PA = sel[0].SubObjects[0]
        PB = sel[1].SubObjects[0]
        v = PB.Point - PA.Point
        objA.Placement.Base.x += v.x
        objA.Placement.Base.y += v.y
        objA.Placement.Base.z += v.z


class PlaceConcentric:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/ShareCenter.svg',
                'MenuText': 'Place concentrically',
                'ToolTip': 'Auxiliary tool to place two shapes concentrically\nPlace the first circular edge selected concentric to \nthe second circular edge selected'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation):
                return True

        else:
            return False

    def Activated(self):
        sel = FreeCAD.Gui.Selection.getSelectionEx()
        objA = sel[0].Object
        CentreA = sel[0].SubObjects[0].Curve.Center
        CentreB = sel[1].SubObjects[0].Curve.Center
        v = CentreB - CentreA
        objA.Placement.Base.x += v.x
        objA.Placement.Base.y += v.y
        objA.Placement.Base.z += v.z


if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('CreateBoltGroup', CreateBoltGroup())
    FreeCAD.Gui.addCommand('CreateSimpleGroup', CreateSimpleGroup())
    FreeCAD.Gui.addCommand('CreateWireGroup', CreateWireGroup())
    FreeCAD.Gui.addCommand('PlaceBeforeSelectedTrajectory', PlaceBeforeSelectedTrajectory())
    FreeCAD.Gui.addCommand('GoToStart', GoToStart())
    FreeCAD.Gui.addCommand('PlayBackward', PlayBackward())
    FreeCAD.Gui.addCommand('StopAnimation', StopAnimation())
    FreeCAD.Gui.addCommand('PlayForward', PlayForward())
    FreeCAD.Gui.addCommand('GoToEnd', GoToEnd())
    FreeCAD.Gui.addCommand('GoToSelectedTrajectory',GoToSelectedTrajectory())
    FreeCAD.Gui.addCommand('ToggleTrajectoryVisibility', ToggleTrajectoryVisibility())
    FreeCAD.Gui.addCommand('AlignToEdge', AlignToEdge())
    FreeCAD.Gui.addCommand('PointToPoint', PointToPoint())
    FreeCAD.Gui.addCommand('PlaceConcentric', PlaceConcentric())
