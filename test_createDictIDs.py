from arXivExtracter.createDictIDs import extractIds
from xml.dom import minidom
import unittest

xml = """<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
<responseDate>2015-03-26T22:02:38Z</responseDate>
<request verb="ListRecords" resumptionToken="788421|42001">http://export.arxiv.org/oai2</request>
<ListRecords>
<record>
<header>
 <identifier>oai:arXiv.org:0712.4079</identifier>
 <datestamp>2007-12-27</datestamp>
 <setSpec>physics:cond-mat</setSpec>
</header>
<metadata>
 <arXiv xmlns="http://arxiv.org/OAI/arXiv/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://arxiv.org/OAI/arXiv/ http://arxiv.org/OAI/arXiv.xsd">
 <id>0712.4079</id><created>2007-12-25</created><authors><author><keyname>Doria</keyname><forenames>Mauro M.</forenames></author><author><keyname>Romaguera</keyname><forenames>Antonio R. de C.</forenames></author><author><keyname>Peeters</keyname><forenames>F. M.</forenames></author></authors><title>Effect of the boundary condition on the vortex patterns in mesoscopic
  three-dimensional superconductors - disk and sphere</title><categories>cond-mat.supr-con cond-mat.mes-hall cond-mat.mtrl-sci</categories><comments>7 pages, 4 figures (low resolution)</comments><journal-ref>Phys. Rev. B 75, 064505 (2007) (7 pages)</journal-ref><doi>10.1103/PhysRevB.75.064505</doi><abstract>  The vortex state of mesoscopic three-dimensional superconductors is
determined using a minimization procedure of the Ginzburg-Landau free energy.
We obtain the vortex pattern for a mesoscopic superconducting sphere and find
that vortex lines are naturally bent and are closest to each other at the
equatorial plane. For a superconducting disk with finite height, and under an
applied magnetic field perpendicular to its major surface, we find that our
method gives results consistent with previous calculations. The matching
fields, the magnetization and $H_{c3}$, are obtained for models that differ
according to their boundary properties. A change of the Ginzburg-Landau
parameters near the surface can substantially enhance $H_{c3}$ as shown here.
</abstract></arXiv>
</metadata>
</record>
<record>
<header>
 <identifier>oai:arXiv.org:0712.4080</identifier>
 <datestamp>2009-11-13</datestamp>
 <setSpec>physics:cond-mat</setSpec>
</header>
<metadata>
 <arXiv xmlns="http://arxiv.org/OAI/arXiv/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://arxiv.org/OAI/arXiv/ http://arxiv.org/OAI/arXiv.xsd">
 <id>0712.4080</id><created>2007-12-25</created><authors><author><keyname>Inarrea</keyname><forenames>J.</forenames></author><author><keyname>Lopez-Monis</keyname><forenames>C.</forenames></author><author><keyname>MacDonald</keyname><forenames>A. H.</forenames></author><author><keyname>Platero</keyname><forenames>G.</forenames></author></authors><title>Hysteretic behavior in weakly coupled double-dot transport in the spin
  blockade regime</title><categories>cond-mat.mes-hall</categories><comments>3 pages and 4 figures. Accepted in APL</comments><journal-ref>Applied Physics Letters, 91, 252112, (2007)</journal-ref><doi>10.1063/1.2828029</doi><abstract>  Double quantum dot systems in the spin blockade regime exhibit leakage
currents that have been attributed to the Hyperfine interaction. We model
weakly coupled double-dot transport using a rate equation approach which
accounts for Hyperfine flip-flop transitions. The rate equations allow us to
obtain self-consistently the time evolution for electronic charge occupations
and for the nuclei polarizations in each dot. We analyze the current in the
spin blockade region as a function of magnetic field and observe hysteretic
behavior for fields corresponding to the crossing between triplet and singlet
states.
</abstract></arXiv>
</metadata>
</record>
<resumptionToken cursor="42000" completeListSize="1024354">788421|43001</resumptionToken>
</ListRecords>
</OAI-PMH>
"""

class TestXmlExtracter(unittest.TestCase):
    def setUp(self):
        self.xmldoc = minidom.parseString(xml)
        self.identifiers = {}
        self.subIds = {}
        self.identifiers, self.subIds = extractIds(self.identifiers, self.subIds, self.xmldoc)

    def testId(self):
        self.assertEqual(self.identifiers['0712.4079'], 'physics~cond-mat', 'incorrect ID')

    def testSubId(self):
        self.assertEqual(self.subIds['0712.4080'], 'cond-mat-mes-hall', 'incorrect subID')

    def testIdFail(self):
        self.assertNotEqual(self.identifiers['0712.4079'], 'cs', 'incorrect ID')

    def testIdKeyError(self):
        with self.assertRaises(KeyError):
            self.identifiers['0712.4021']
        

if __name__ == "__main__":
    unittest.main()
