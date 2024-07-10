#   demo_create_entry.py
#
#   Tests and demonstrates working with the FieldWorks lexicon.
#
#   Platforms: Python .NET and IronPython
#
#   Copyright Craig Farrow, 2008 - 2022
#

import sys

from flexlibs import FLExInitialize, FLExCleanup
from flexlibs import FLExProject, FP_ProjectError

from SIL.LCModel import (
    ILexEntryFactory,
    )
    
#============ Configurables ===============

# Project to use
TEST_PROJECT = "__flexlibs_testing"

# Enable writing tests
WriteTests = True
      
#--------------------------------------------------------------------
def createLexicalEntry(project):
    
    try:
        entry = project.project.ServiceLocator.GetInstance(ILexEntryFactory).Create()
    except Exception as e:
        print(f"Failed to create entry: {e}")
        return
    print(f"Entry: {repr(entry)}")


#--------------------------------------------------------------------


if __name__ == "__main__":

    FLExInitialize()
    
    project = FLExProject()

    try:
        project.OpenProject(projectName = TEST_PROJECT,
                            writeEnabled = WriteTests)
    except FP_ProjectError as e:
        print("OpenProject failed!")
        print(e.message)
        FLExCleanup()
        sys.exit(1)

    print("Opened project %s." % project.ProjectName())

    createLexicalEntry(project)
    
    # Clean-up
    project.CloseProject()
    
    FLExCleanup()
    
    
