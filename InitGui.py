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
        self.tools = ['CreateBoltGroup',
                      'CreateSimpleGroup',
                      'GoToStart',
                      'PlayBackward',
                      'PlayForward',
                      'GoToEnd',
                      'ToggleTrajectoryVisibility']

        self.tools1 = ['AlignToEdge',
                       'PointToPoint',
                       'PlaceConcentric']

        self.appendToolbar('ExplodedAssembly', self.tools)
        self.appendToolbar('ExplodedAssembly', self.tools1)
        self.appendMenu('ExplodedAssembly', self.tools)
        self.appendMenu('ExplodedAssembly', self.tools1)

    def Activated(self):
        import ExplodedAssembly as ea
        ea.checkDocumentStructure()
        FreeCAD.Console.PrintMessage('Exploded Assembly workbench loaded\n')


FreeCADGui.addWorkbench(ExplodedAssembly)
