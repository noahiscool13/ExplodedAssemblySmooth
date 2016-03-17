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


# Container python folder 'ExplodedAssembly'
class ExplodedAssemblyFolder:
    def __init__(self, obj):
        obj.addProperty('App::PropertyPythonObject', 'InitialPlacements').InitialPlacements = {}
        obj.addProperty('App::PropertyInteger', 'AnimationStep').AnimationStep = 0
        obj.addProperty('App::PropertyInteger', 'CurrentTrajectory').CurrentTrajectory = 0
        obj.addProperty('App::PropertyBool', 'ResetAnimation').ResetAnimation = False
        obj.addProperty('App::PropertyBool', 'InAnimation').InAnimation = False
        obj.addProperty('App::PropertyBool', 'RemoveAllTrajectories').RemoveAllTrajectories = False
        obj.Proxy = self

    def execute(self, fp):
        if fp.ResetAnimation:
            resetPlacement()
            fp.ResetAnimation = False

        if fp.RemoveAllTrajectories:
            fp.RemoveAllTrajectories = False
            for obj in fp.Group:
                FreeCAD.ActiveDocument.removeObject(obj.Name)

            # reset initial placement dict
            fp.InitialPlacements = {}


class ExplodedAssemblyFolderViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/WorkbenchIcon.svg'


def checkDocumentStructure():
    # checks the existence of the folder 'ExplodedAssembly' and creates it if not
    try:
        folder = FreeCAD.ActiveDocument.ExplodedAssembly

    except:
        folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'ExplodedAssembly')
        ExplodedAssemblyFolder(folder)
        ExplodedAssemblyFolderViewProvider(folder.ViewObject)


# Bolt group trajectory ########################################################
class BoltGroupObject:
    def __init__(self, obj):
        obj.addProperty('App::PropertyPythonObject', 'names').names = []
        obj.addProperty('App::PropertyPythonObject', 'dir_vectors').dir_vectors = []
        obj.addProperty('App::PropertyPythonObject', 'rot_vectors').rot_vectors = []
        obj.addProperty('App::PropertyPythonObject', 'rot_centers').rot_centers = []
        #
        obj.addProperty('App::PropertyFloat', 'Distance').Distance = 20.0
        obj.addProperty('App::PropertyFloat', 'Revolutions').Revolutions = 0.0
        obj.addProperty('App::PropertyFloat', 'AnimationStepTime').AnimationStepTime = 0.0
        obj.addProperty('App::PropertyInteger', 'AnimationSteps').AnimationSteps = 20
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        resetPlacement()
        goToEnd()
        FreeCAD.ActiveDocument.ExplodedAssembly.CurrentTrajectory = -1

class BoltGroupObjectViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/BoltGroup.svg'


def createBoltDisassemble():
    # add object to the Document and initialize it
    SDObj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython','BoltGroup')
    BoltGroupObject(SDObj)
    BoltGroupObjectViewProvider(SDObj.ViewObject)
    # retrieve selection
    selection = FreeCAD.Gui.Selection.getSelectionEx()
    # try to find the face wich its normal gives the disassemble direction
    dir_vector = FreeCAD.Vector(0, 0, 1)
    for sel_obj in selection:
        for subObject in sel_obj.SubObjects:
            try:
                dir_vector = subObject.normalAt(0, 0)
                break

            except:
                pass

    for sel_obj in selection:
        for subObject in sel_obj.SubObjects:
            try:
                if str(subObject.Curve)[0:6] == 'Circle':
                    # append object name
                    SDObj.names.append(sel_obj.Object.Name)
                    # append unmount direction
                    JSON_dir_vector = (dir_vector[0], dir_vector[1], dir_vector[2])
                    SDObj.dir_vectors.append(JSON_dir_vector)
                    # apend rotation axis
                    JSON_rot_axis = (dir_vector[0], dir_vector[1], dir_vector[2])
                    SDObj.rot_vectors.append(JSON_rot_axis)
                    # append rotation center
                    rot_center = subObject.Curve.Center
                    JSON_rot_center = (rot_center[0], rot_center[1], rot_center[2])
                    SDObj.rot_centers.append(JSON_rot_center)
                    # append initial values for distance, revs, steps
                    SDObj.distance.append(10.0)
                    SDObj.revolutions.append(0)
                    SDObj.animation_steps.append(20.0)

            except:
                pass

    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly
    # add initial placement if this is the first movement of the parts
    for name in SDObj.names:
        try:
            plm = EAFolder.InitialPlacements[name]

        except:
            an_object = FreeCAD.ActiveDocument.getObject(name)
            # prepare object placement for JSON serialization
            # store base placement as vector
            plm = an_object.Placement
            base = (plm.Base[0], plm.Base[1], plm.Base[2])
            # store rotation as a quaternion
            rot = plm.Rotation.Q
            placement = (base, rot)
            EAFolder.InitialPlacements[name] = placement

    # place inside ExplodedAssembly folder and update document
    EAFolder.addObject(SDObj)
    updateTrajectoryLines()
    FreeCAD.ActiveDocument.recompute()


# simple group trajectory ########################################################
class SimpleGroupObject:
    def __init__(self, obj):
        obj.addProperty('App::PropertyPythonObject', 'names').names = []
        obj.addProperty('App::PropertyPythonObject', 'dir_vectors').dir_vectors = []
        obj.addProperty('App::PropertyPythonObject', 'rot_vectors').rot_vectors = []
        obj.addProperty('App::PropertyPythonObject', 'rot_centers').rot_centers = []
        #
        obj.addProperty('App::PropertyFloat', 'Distance').Distance = 20.0
        obj.addProperty('App::PropertyFloat', 'Revolutions').Revolutions = 0.0
        obj.addProperty('App::PropertyFloat', 'AnimationStepTime').AnimationStepTime = 0.0
        obj.addProperty('App::PropertyInteger', 'AnimationSteps').AnimationSteps = 20
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        resetPlacement()
        goToEnd()
        FreeCAD.ActiveDocument.ExplodedAssembly.CurrentTrajectory = -1


class SimpleGroupObjectViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/SimpleGroup.svg'


def createSimpleDisassemble():
    # add object to the Document and initialize it
    SDObj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'SimpleGroup')
    SimpleGroupObject(SDObj)
    SimpleGroupObjectViewProvider(SDObj.ViewObject)
    # retrieve selection
    selection = FreeCAD.Gui.Selection.getSelectionEx()
    # the last face of the last object selected determines the disassemble dir vector
    dir_vector = selection[-1].SubObjects[-1].normalAt(0, 0)
    # the rotation center is the center of mass of the last face selected
    rot_center = selection[-1].SubObjects[-1].CenterOfMass
    # create trajectory data
    for sel_obj in selection:
        # append object name
        SDObj.names.append(sel_obj.Object.Name)
        # append unmount direction
        JSON_dir_vector = (dir_vector[0], dir_vector[1], dir_vector[2])
        SDObj.dir_vectors.append(JSON_dir_vector)
        # apend rotation axis
        JSON_rot_axis = (dir_vector[0], dir_vector[1], dir_vector[2])
        SDObj.rot_vectors.append(JSON_rot_axis)
        # append rotation center
        JSON_rot_center = (rot_center[0], rot_center[1], rot_center[2])
        SDObj.rot_centers.append(JSON_rot_center)

    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly
    # add initial placement if this is the first move of the parts
    for name in SDObj.names:
        try:
            plm = EAFolder.InitialPlacements[name]

        except:
            an_object = FreeCAD.ActiveDocument.getObject(name)
            # prepare object placement for JSON serialization
            # store base placement as vector
            plm = an_object.Placement
            base = (plm.Base[0], plm.Base[1], plm.Base[2])
            # store rotation as a quaternion
            rot = plm.Rotation.Q
            placement = (base, rot)
            EAFolder.InitialPlacements[name] = placement

    # place inside ExplodedAssembly folder and update document
    EAFolder.addObject(SDObj)
    updateTrajectoryLines()
    FreeCAD.ActiveDocument.recompute()


def resetPlacement():
    # restore the placement of all objects
    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly
    # set everything to its initial position
    for traj in EAFolder.Group:
        for name in traj.names:
            obj = FreeCAD.ActiveDocument.getObject(name)
            # create placement from initial placement list
            plm = EAFolder.InitialPlacements[name]
            base = FreeCAD.Vector(plm[0][0], plm[0][1], plm[0][2])
            rot = FreeCAD.Rotation(plm[1][0], plm[1][1], plm[1][2], plm[1][3])
            obj.Placement = FreeCAD.Placement(base, rot)



def runAnimation(start=0, end=0, mode='complete', direction='forward'):
    # runs the animation from a start step number to the end step number
    # mode: 'complete', 'toPoint'
    # 'complete' means forward from start to end and backwars if already in end
    # 'forward' means disassemble from start to end
    # 'backward' means assemble from start to end
    # 'toPoint' means go to an especific end point without animation
    # toggle 'InAnimation variable' to disable other icons temporally
    FreeCAD.ActiveDocument.ExplodedAssembly.InAnimation = True
    # # complete mode
    # start animation
    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly.Group
    if mode == 'complete':
        number_of_trajectories = len(EAFolder)

    elif mode == 'toPoint':
        number_of_trajectories = len(EAFolder) - start - end

    traj_iterator = xrange(number_of_trajectories)
    if direction == 'backward':
        traj_iterator = xrange(number_of_trajectories-1, -1, -1)

    animation_paused = False
    for r in traj_iterator:
        # break animation loop if not InAnimation (this is where pause animation takes place):
        EA = FreeCAD.ActiveDocument.ExplodedAssembly
        if not(EA.InAnimation):
            animation_paused = True
            break

        if direction == 'forward':
            traj = EAFolder[r+start]
            # set current stop point
            EA.CurrentTrajectory = r+start

        elif direction == 'backward':
            traj = EAFolder[r]
            # set current stop point
            EA.CurrentTrajectory = r-1

        # highligh current trajectory
        FreeCAD.Gui.Selection.addSelection(traj)
        # buffer objects
        objects = []
        for name in traj.names:
            objects.append(FreeCAD.ActiveDocument.getObject(name))

        inc_D = traj.Distance / float(traj.AnimationSteps)
        inc_R = traj.Revolutions / float(traj.AnimationSteps)
        if direction == 'backward':
            inc_D = inc_D*-1.0
            inc_R = inc_R*-1.0

        for i in xrange(traj.AnimationSteps):
            if i == 0:
                dir_vectors = []
                rot_vectors = []
                rot_centers = []
                for s in xrange(len(objects)):
                    dir_vectors.append(FreeCAD.Vector(tuple(traj.dir_vectors[s])))
                    rot_vectors.append(FreeCAD.Vector(tuple(traj.rot_vectors[s])))
                    rot_centers.append(FreeCAD.Vector(tuple(traj.rot_centers[s])))

            for n in xrange(len(objects)):
                obj = objects[n]
                obj_base = dir_vectors[n]*inc_D
                obj_rot = FreeCAD.Rotation(rot_vectors[n], inc_R*360.0)
                obj_rot_center = rot_centers[n]
                incremental_placement = FreeCAD.Placement(obj_base, obj_rot, obj_rot_center)
                obj.Placement = incremental_placement.multiply(obj.Placement)

            FreeCAD.Gui.updateGui()
            time.sleep(traj.AnimationStepTime)

        # clear selection
        FreeCAD.Gui.Selection.clearSelection()

    # set pointer to current trajectory index
    EA = FreeCAD.ActiveDocument.ExplodedAssembly
    # toggle InAnimation to activate icons deactivated before
    EA.InAnimation = False
    # set CurrentTrajectory number
    if not(animation_paused):
        if direction == 'forward' and end == 0:
            EA.CurrentTrajectory = -1

        if direction == 'backward' and start == 0:
            EA.CurrentTrajectory = 0



def goToEnd():
    # start animation
    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly.Group
    for traj in EAFolder:
        objects = []
        for name in traj.names:
            objects.append(FreeCAD.ActiveDocument.getObject(name))

        inc_D = traj.Distance / float(1)
        inc_R = traj.Revolutions / float(1)
        for i in xrange(1):
            if i == 0:
                dir_vectors = []
                rot_vectors = []
                rot_centers = []
                for s in xrange(len(objects)):
                    dir_vectors.append(FreeCAD.Vector(tuple(traj.dir_vectors[s])))
                    rot_vectors.append(FreeCAD.Vector(tuple(traj.rot_vectors[s])))
                    rot_centers.append(FreeCAD.Vector(tuple(traj.rot_centers[s])))

            for n in xrange(len(objects)):
                obj = objects[n]
                obj_base = dir_vectors[n]*inc_D
                obj_rot = FreeCAD.Rotation(rot_vectors[n], inc_R*360)
                obj_rot_center = rot_centers[n]
                incremental_placement = FreeCAD.Placement(obj_base, obj_rot, obj_rot_center)
                obj.Placement = incremental_placement.multiply(obj.Placement)


    FreeCAD.Gui.updateGui()


def goToSelectedTrajectory():
    # retrieve selection
    traj_name = FreeCAD.Gui.Selection.getSelectionEx()[0].Object.Name
    # start animation
    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly.Group
    for r in xrange(len(EAFolder)):
        traj = EAFolder[r]
        objects = []
        update_gui = False
        for name in traj.names:
            objects.append(FreeCAD.ActiveDocument.getObject(name))

        if traj_name == traj.Name:
            inc_D = traj.Distance / float(traj.AnimationSteps)
            inc_R = traj.Revolutions / float(traj.AnimationSteps)
            animation_range = traj.AnimationSteps
            update_gui = True

        else:
            inc_D = traj.Distance / float(1)
            inc_R = traj.Revolutions / float(1)
            animation_range = 1

        for i in xrange(animation_range):
            if i == 0:
                dir_vectors = []
                rot_vectors = []
                rot_centers = []
                for s in xrange(len(objects)):
                    dir_vectors.append(FreeCAD.Vector(tuple(traj.dir_vectors[s])))
                    rot_vectors.append(FreeCAD.Vector(tuple(traj.rot_vectors[s])))
                    rot_centers.append(FreeCAD.Vector(tuple(traj.rot_centers[s])))

            for n in xrange(len(objects)):
                obj = objects[n]
                obj_base = dir_vectors[n]*inc_D
                obj_rot = FreeCAD.Rotation(rot_vectors[n], inc_R*360)
                obj_rot_center = rot_centers[n]
                incremental_placement = FreeCAD.Placement(obj_base, obj_rot, obj_rot_center)
                obj.Placement = incremental_placement.multiply(obj.Placement)

            if update_gui:
                FreeCAD.Gui.updateGui()

        if traj_name == traj.Name:
            # exit once selected trajectory has been reached
            break

    # set current trajectory cursor to current trajectory
    FreeCAD.ActiveDocument.ExplodedAssembly.CurrentTrajectory = r

def placeBeforeSelectedTrajectory():
    # select the trajectoreis you want to reallocate and finally,
    # the trajectory before wich you want to place them
    sel_traj = FreeCAD.Gui.Selection.getSelectionEx()
    # retrieve EA folder
    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly
    # create an auxiliary folder to re organizate exploded assembly
    aux_folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroup','ea_aux')
    before_traj = sel_traj[-1].Object
    for traj in EAFolder.Group:
        if traj.Name == before_traj.Name:
            for sel in sel_traj:
                aux_folder.addObject(sel.Object)

        elif traj.Name != before_traj.Name:
            add_traj = True
            for sel in sel_traj:
                if traj.Name == sel.Object.Name:
                    add_traj = False
                    break

            if add_traj:
                aux_folder.addObject(traj)

    # save the attributes of EAFolder'
    EAF_InitialPlacements = EAFolder.InitialPlacements
    EAF_CurrentTrajectory = EAFolder.CurrentTrajectory
    EAF_ResetAnimation = EAFolder.ResetAnimation
    EAF_InAnimation = EAFolder.InAnimation
    EAF_RemoveAllTrajectories = EAFolder.RemoveAllTrajectories
    FreeCAD.ActiveDocument.removeObject(EAFolder.Name)
    # create the EAFolder
    EAFolder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'ExplodedAssembly')
    ExplodedAssemblyFolder(EAFolder)
    ExplodedAssemblyFolderViewProvider(EAFolder.ViewObject)
    # restore its content
    for traj in aux_folder.Group:
        EAFolder.addObject(traj)

    EAFolder.InitialPlacements = EAF_InitialPlacements
    EAFolder.CurrentTrajectory = EAF_CurrentTrajectory
    EAFolder.ResetAnimation = EAF_ResetAnimation
    EAFolder.InAnimation = EAF_InAnimation
    EAFolder.RemoveAllTrajectories = EAF_RemoveAllTrajectories
    # remove auxiliary folder
    FreeCAD.ActiveDocument.removeObject(aux_folder.Name)
    # recompute document
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.Gui.updateGui()


def updateTrajectoryLines():
    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly.Group
    # remove all the previous trajectory lines
    for traj in EAFolder:
        for lines in traj.Group:
            FreeCAD.ActiveDocument.removeObject(lines.Name)

    # re-draw all trajectories
    for traj in EAFolder:
        lines_compound = []
        objects = []
        for name in traj.names:
            objects.append(FreeCAD.ActiveDocument.getObject(name))

        inc_D = traj.Distance
        dir_vectors = []
        rot_centers = []
        for s in xrange(len(objects)):
            dir_vectors.append(FreeCAD.Vector(tuple(traj.dir_vectors[s])))
            rot_centers.append(FreeCAD.Vector(tuple(traj.rot_centers[s])))

        for n in xrange(len(objects)):
            pa = rot_centers[n]# objects[n].Placement.Base
            pb = rot_centers[n] + dir_vectors[n]*inc_D
            lines_compound.append(Part.makeLine(pa, pb))

        l_obj = FreeCAD.ActiveDocument.addObject('Part::Feature','trajectory_line')
        l_obj.Shape = Part.makeCompound(lines_compound)
        l_obj.ViewObject.DrawStyle = "Dashed"
        l_obj.ViewObject.LineWidth = 1.0
        traj.addObject(l_obj)

    FreeCAD.Gui.updateGui()



def visibilityTrajectoryLines(show):
    # show or hide trajectory lines
    EAFolder = FreeCAD.ActiveDocument.ExplodedAssembly.Group
    for traj in EAFolder:
        for lines in traj.Group:
            lines.ViewObject.Visibility = show
