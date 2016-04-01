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

__title__="Exploded Assembly Workbench for FreeCAD"
__author__ = "Javier Martínez García"
__url__ = "http://linuxforanengineer.blogspot.com"

import FreeCAD
import FreeCADGui

class ExplodedAssembly(Workbench):
    import EAInit# this is needed to load the workbench icon
    # __dir__ = os.path.dirname( __file__ ) # __file__ is not working
    Icon = EAInit.__dir__ + '/icons/WorkbenchIcon.svg'
    MenuText = 'Exploded Assembly'
    ToolTip = 'Assemble parts and create exploded drawings and animations'

    def GetClassName(self):
        return 'Gui::PythonWorkbench'

    def Initialize(self):
        import EAInit
        self.CreationTools = ['CreateBoltGroup',
                              'CreateSimpleGroup',
                              'ModifyIndividualObjectTrajectory',
                              'PlaceBeforeSelectedTrajectory',
                              'ToggleTrajectoryVisibility']

        self.CameraAnimation = ['CreateManualCamera',
                                'CreateEdgeCamera',
                                'CreateFollowCamera']

        self.AnimationControlTools = ['GoToStart',
                                      'PlayBackward',
                                      'StopAnimation',
                                      'PlayForward',
                                      'GoToEnd',
                                      'GoToSelectedTrajectory']

        self.AuxiliaryAssemblyTools = ['AlignToEdge',
                                       'Rotate15',
                                       'PointToPoint',
                                       'PlaceConcentric']

        self.Menu_tools = ['CreateBoltGroup',
                              'CreateSimpleGroup',
                              'ModifyIndividualObjectTrajectory',
                              'PlaceBeforeSelectedTrajectory',
                              'GoToSelectedTrajectory',
                              'GoToStart',
                              'PlayBackward',
                              'StopAnimation',
                              'PlayForward',
                              'GoToEnd',
                              'ToggleTrajectoryVisibility',
                              'AlignToEdge',
                              'Rotate15',
                              'PointToPoint',
                              'PlaceConcentric',
                              'LoadExampleFile']

        self.appendToolbar('ExplodedAssemblyCreationTools', self.CreationTools)
        #self.appendToolbar('ExplodedAssemblyCameraTools', self.CameraAnimation)
        self.appendToolbar('ExplodedAssemblyAnimationControlTools', self.AnimationControlTools)
        self.appendToolbar('ExplodedAssemblyAuxiliarAssemblyTools', self.AuxiliaryAssemblyTools)
        self.appendMenu('ExplodedAssembly', self.Menu_tools)

    def Activated(self):
        import ExplodedAssembly as ea
        if not(FreeCAD.ActiveDocument):
            FreeCAD.newDocument()

        ea.checkDocumentStructure()
        FreeCAD.Console.PrintMessage('Exploded Assembly workbench loaded\n')


FreeCADGui.addWorkbench(ExplodedAssembly)
