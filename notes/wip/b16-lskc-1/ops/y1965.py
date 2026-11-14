import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from y1961 import W, MP, add, cite, var, chk

OPS = [
 add('cal.1965-04-27.vietnam-hanoi', 'Apr. 27', '1965-04-27',
     "The Central Military Commission and the High Command, after the eleventh plenum, direct the fronts in the South: the main forces' fighting stepped up, campaigns on several fronts at once with risings of the masses, to hasten the Saigon army's and government's collapse and be ready to beat a \"local war\" should the Americans widen it.",
     f"{W}, III, 416–17. {MP} See [[cal.1965-03-28.vietnam]].",
     ['vis:only:drv'], also=['vietnam']),
 add('cal.1965-07-22.vietnam-hanoi', 'July 22', '1965-07-22',
     "The Đồng Xoài campaign, opened May 10–11 at Phước Long, ends. By the Region's count four battalions and 24 companies put out of action, 4,459 men, 73 American advisers among them; 1,652 weapons taken, 60 military vehicles and 34 aircraft destroyed. In Phước Long province 56,000 of 67,000 people won from the strategic hamlets.",
     f"{W}, III, 416–36. See [[cal.1965-05-11.vietnam-operations]], [[cal.1965-06-09.vietnam-operations]].",
     [], also=['vietnam-operations']),
 cite('cal.1965-02-07.vietnam', f"{W}, III, 397–98 (the night of Feb. 6–7, sappers against the Cù Hanh airfield and Camp Holloway; the Second Regiment, Region 5's, against Dương Liễu, Bình Định)", 'A'),
 var('cal.1965-02-07.vietnam', 'A', 'eight Americans killed, nearly 100 wounded, 20 aircraft destroyed or damaged, after thirty minutes', 'III, 398'),
 cite('cal.1965-02-07.vietnam', f"{W}, III, 403–04 (Flaming Dart I against Vĩnh Linh and Đồng Hới, Feb. 7; the Air Defense–Air Force on alert from the early morning)", 'C'),
 cite('cal.1965-02-16.vietnam-operations', f"{W}, III, 210–11 (ship 143, 100 tons, Lê Văn Thêm master, Phạm Văn Bảng political officer, out Feb. 1, in at Vũng Rô the night of Feb. 15)", 'A'),
 var('cal.1965-02-16.vietnam-operations', 'A', 'most of the cargo carried into the caves before dawn; the ship, unable to leave, spotted at noon, bombed, scuttled by its crew; fighting on the shore Feb. 17 and 19', 'III, 210–11'),
 cite('cal.1965-03-28.vietnam', f"{W}, III, 413–14 (the eleventh plenum, Mar. 25–27, 1965; its resolution, archive no. TW 816)", 'A'),
 cite('cal.1965-04-03.vietnam', f"{W}, III, 410–11 (Apr. 3, two flights of MiG-17s of the 921st Air Regiment, under Phạm Ngọc Lan and Trần Hanh, with the 234th Air Defense Regiment and the militia at Hàm Rồng)", 'A, B'),
 var('cal.1965-04-03.vietnam', 'B', 'Apr. 3, two F-8s shot down by the MiGs, the Vietnamese air force\'s first fight, and an F-4 at Đò Lèn; more shot down Apr. 4 at Hàm Rồng, the Ghép ferry and Hoàng Mai', 'III, 410–11'),
 cite('cal.1965-05-11.vietnam-operations', f"{W}, III, 417–19 (the Đồng Xoài campaign's first phase, Lê Trọng Tấn commanding, Trần Độ political commissar, Hoàng Cầm deputy: the night of May 10–11 the First Battalion of the First Regiment (Q761) and Battalion 840 against the town, the Second Regiment toward Phước Bình)", 'A'),
 var('cal.1965-05-11.vietnam-operations', 'B', 'the town left May 12; the Rangers airlifted to Hiếu Phong, toward Phước Bình, gone before the Second Regiment came', 'III, 419'),
 cite('cal.1965-05-29.vietnam-operations', f"{W}, III, 423–27 (Region 5's Ba Gia campaign, Chu Huy Mân commanding, from the night of May 28; a Saigon First Battalion destroyed May 29 at Phước Lộc; May 30 the Third Marine Battalion mostly destroyed, the Second of the 51st mauled)", 'A'),
 cite('cal.1965-06-09.vietnam-operations', f"{W}, III, 419–22 (the campaign's second phase: the night of June 9 the approach, by 4 a.m. June 10 most of the post taken; the battalions landed by air beaten June 10–11; the post wholly taken; the Second Regiment named the Đồng Xoài Regiment)", 'A, B'),
]
