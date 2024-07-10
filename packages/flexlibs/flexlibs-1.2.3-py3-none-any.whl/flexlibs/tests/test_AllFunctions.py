from builtins import str

import unittest

from flexlibs import FLExInitialize, FLExCleanup
from flexlibs import FLExProject, AllProjectNames, FP_FileLockedError

# --- Constants ---

TEST_PROJECT = r"__flexlibs_testing"

#----------------------------------------------------------- 

class TestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        FLExInitialize()
        self.fp = self._openProject(self)

    @classmethod
    def tearDownClass(self):
        self.fp.CloseProject()
        FLExCleanup()

    def _openProject(self):
        fp = FLExProject()
        try:
            fp.OpenProject(TEST_PROJECT,
                           writeEnabled = True)
        except FP_FileLockedError:
            self.fail("The test project is open in another application. Please close it and try again.")

        except Exception as e:
            self.fail("Exception opening project %s:\n%s" % 
                      (TEST_PROJECT, e.message))
        return fp

    def test_WritingSystems(self):
        allWS = self.fp.GetWritingSystems()
        self.assertIsInstance(allWS, list)
        self.assertNotEqual(len(allWS), 0)
        self.assertIsInstance(allWS[0], tuple)
        self.assertEqual(len(allWS[0]), 4)
        
        self.assertIsInstance(self.fp.WSUIName(allWS[0][1]), str)
        self.assertIsInstance(self.fp.WSHandle(allWS[0][1]), int)
        self.assertIsInstance(self.fp.GetDefaultVernacularWS(), tuple)
        self.assertIsInstance(self.fp.GetDefaultAnalysisWS(), tuple)
        
    def test_Lists(self):
        self.assertIsInstance(self.fp.GetPartsOfSpeech(), list)
        self.assertIsInstance(self.fp.GetAllSemanticDomains(), list)
        
     
    
if __name__ == "__main__":
    unittest.main()
