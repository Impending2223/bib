import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from y1961 import W, MP, add, cite, var, chk

OPS = [
 add('cal.1963-02-10.vietnam-hanoi', 'Feb. 10', '1963-02-10',
     "The Politburo's statement: the fraternal parties asked to stop attacking one another in the press and on the radio, and to meet to settle their differences.",
     f"{W}, III, 98.",
     [], also=['soviet-union', 'china']),
 add('cal.1963-05-14.vietnam-hanoi-2', 'May 14', '1963-05-14',
     "The National Liberation Front's statement on the shooting of unarmed demonstrators at Huế May 8: a crime against the people and the Buddhists, exposing the Diệm government's claim to respect freedom of belief.",
     f"{W}, III, 311.",
     [], also=['vietnam']),
 add('cal.1963-08.vietnam-hanoi', 'Aug.', '1963-08',
     "The Central Military Commission and the Defense Ministry hand transport by sea to the South to the navy.",
     f"{W}, III, 206 (in October the General Staff meets the Naval Department and Group 759 to carry it out). {MP}",
     ['vis:only:drv'], also=['vietnam']),
 add('cal.1963-10.vietnam-hanoi-4', 'Oct.', '1963-10',
     "The Politburo and the Central Military Commission set up the Region's Military Party Committee and Military Command: Nguyễn Văn Linh, COSVN's secretary, secretary of the committee; Lt. Gen. Trần Văn Trà, deputy chief of the General Staff, sent south as commander.",
     f"{W}, III, 243, 343. {MP} Names: Nguyễn Văn Linh, Trần Văn Trà.",
     ['vis:only:drv', 'name:tran-van-tra'], also=['vietnam']),
 cite('cal.1963-01-02.vietnam', f"{W}, III, 215–36 (a company each of the 261st, Region 8's main-force battalion, and the 514th, Mỹ Tho's, with the village guerrillas; withdrawn at 10 p.m., the night of Jan. 2)", 'A'),
 var('cal.1963-01-02.vietnam', 'B', '450 killed and wounded, 11 American advisers and technicians among them; five helicopters down, three M113s destroyed, a boat sunk; its own losses 18 dead and 39 wounded, through Sheehan', 'III, 235–36'),
 cite('cal.1963-12.vietnam', f"{W}, III, 98, 323, 337 (the ninth plenum, early December: the world situation and the South)", 'A'),
]
