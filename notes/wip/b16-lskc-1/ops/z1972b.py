import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts2'))
import dsl
from dsl import *
VH = 'vietnam-hanoi'; OP = ['vietnam-operations']
NP('phu-long-bt', 'Phú Long'); NP('bsar', 'B\'Sar'); NP('lam-dong', 'Lâm Đồng province')
A('1965-0517-phulong', '1965-05-17', VH, 'Bình Thuận. May 17 Region 6\'s troops, dressed as civilians in two three-wheeled taxis, open fire by surprise on the guards of a bridge and take the Saigon office at Phú Long. The Phan Thiết subsector sends Civil Guard Companies 441 and 887 with five M113s; seven times they cross the river and are thrown back.', 'III, 434–35', place='phu-long-bt', also=OP)
A('1965-0522-phulong2', '1965-05-22', VH, 'Bình Thuận. May 22 Saigon sends a marine battalion and a Ranger battalion to counterattack at Phú Long; after four hours Region 6\'s troops break their assaults, 150 killed or wounded.', 'III, 435', place='phu-long-bt', also=OP)
A('1965-0627-bsar', '1965-06-27', VH, 'Lâm Đồng. June 27 the province\'s troops destroy the B\'Sar strongpoint, which commands a wide area south of the Blao pass, and bring down the bridges at Đậm Mrế and Đạc Oai; the people along Routes 20 and 14 bis rise and Saigon pulls back to Bảo Lộc and Di Linh.', 'III, 434', place='bsar', also=OP)
A('1963-0201-hochi', '1963-02-01', VH, 'Hồ Chí Minh\'s article in *Nhân Dân*, under the pen name TL, Feb. 1, on the defeat of the Americans\' newest tactics and arms by the people\'s spirit; the history cites it for the Ấp Bắc battle.', 'III, 239 n.1', place='hanoi', names=['Hồ Chí Minh'], also=['vietnam'], check='the article itself not read; its subject is the history\'s.')
