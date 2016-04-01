# -*- coding: utf-8 -*-
# Exploded Assembly Animation workbench for FreeCAD
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
#*   This program is distributed in the hope that it will be useful,       *
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

from __future__ import division
import os
import time
import FreeCAD
import Part
from pivy import coin



"""
class AnimationCamera:
    def __init__(self, obj):
        obj.addProperty('App::PropertyBool', 'Enable')
        obj.addProperty('App::PropertyString', 'RunFrom', 'Interval')
        obj.addProperty('App::PropertyString', 'RunTo', 'Interval')
        # edge trajectory
        obj.addProperty('App::PropertyBool', 'EdgeTrajectory', 'Follow Edge')
        obj.addProperty('App::PropertyString','ShapeName', 'Follow Edge')
        obj.addProperty('App::PropertyFloat', 'EdgeNumber', 'Follow Edge')
        # Manual trajectory
        obj.addProperty('App::PropertyBool', 'ManualTrajectory', 'Manual trajectory')
        obj.addProperty('App::PropertyVector', 'InitialCameraBase', 'Manual trajectory')
        obj.addProperty('App::PropertyVector', 'InitialCameraLookPoint', 'Manual trajectory')
        obj.addProperty('App::PropertyVector', 'FinalCameraBase', 'Manual trajectory')
        obj.addProperty('App::PropertyVector', 'FinalCameraLookPoint', 'Manual trajectory')
        obj.addProperty('App::PropertyStringList', 'TransitionMode', 'Manual trajectory').TransitionMode = 'Frame', 'Smooth'
        # Attached trajectory
        obj.addPropertyd

"""
class ManualAnimationCamera:
    def __init__(self, obj):
        obj.addProperty('App::PropertyBool', 'Enable', 'Enable Camera')
        obj.addProperty('App::PropertyString', 'RunFrom', 'Interval')
        obj.addProperty('App::PropertyString', 'RunTo', 'Interval')
        obj.addProperty('App::PropertyVector', 'InitialCameraBase', 'Camera Position')
        obj.addProperty('App::PropertyVector', 'FinalCameraBase', 'Camera Position')
        obj.addProperty('App::PropertyVector', 'InitialCameraLookPoint', 'Camera Position')
        obj.addProperty('App::PropertyVector', 'FinalCameraLookPoint', 'Camera Position')
        obj.addProperty('App::PropertyEnumeration', 'Transition', 'Camera Transition').Transition = ['Sudden', 'Linear']


class ManualAnimationCameraViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/AnimationCameraManual.svg'


def createManualCamera():
    # retrieve selection
    initial_obj = FreeCAD.Gui.Selection.getSelectionEx()[0].Object.Name
    final_obj = FreeCAD.Gui.Selection.getSelectionEx()[1].Object.Name
    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly
    MCObj = FreeCAD.ActiveDocument.addObject('App::FeaturePython', 'ManualCamera')
    ManualAnimationCamera(MCObj)
    ManualAnimationCameraViewProvider(MCObj.ViewObject)
    EAFolder.addObject(MCObj)
    # add selection to camera from-to
    MCObj.RunFrom = initial_obj
    MCObj.RunTo = final_obj
    # organize inside folder
    FreeCAD.Gui.Selection.clearSelection()
    FreeCAD.Gui.Selection.addSelection(MCObj)
    FreeCAD.Gui.Selection.addSelection(EAFolder.Group[0])
    from ExplodedAssembly import placeBeforeSelectedTrajectory
    placeBeforeSelectedTrajectory()
    FreeCAD.Console.PrintMessage('\nManual camera created\n')

"""from FreeCAD import Base
cam = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()
trajectory = Gui.Selection.getSelectionEx()[0].Object.Shape.Edges
for edge in trajectory:
  startPoint = edge.valueAt( 0.0 )
  endPoint = edge.valueAt( edge.Length )
  dirVector = ( endPoint - startPoint ).normalize()
  currentPoint = startPoint
  while (currentPoint - startPoint).Length < edge.Length:
    currentPoint = currentPoint + dirVector
    cam.position.setValue(currentPoint + Base.Vector( 0,0, 10) )
    cam.pointAt( coin.SbVec3f( endPoint[0], endPoint[1], endPoint[2]+10) , coin.SbVec3f( 0, 0, 1 ) )
    Gui.updateGui()
    time.sleep(0.005)
"""
