import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts2'))
import dsl
from dsl import *
VH = 'vietnam-hanoi'; OP = ['vietnam-operations']
NP('hoa-nhat', 'Hòa Nhật'); NP('ho-coc', 'Hồ Cóc')
A('1962-0715-hoanhat', '1962-07-15', VH, 'Biên Hòa. The people of Tân Hiệp and Tân Hòa communes, Châu Thành, penned in the Hòa Nhật strategic hamlet, break out: the night of July 15 guerrillas outside fire on the blockhouse at the gate and 200 families go through the fence before dawn; the night of July 16 again, with the people calling the soldiers by loudspeaker to stand still or surrender; the morning of July 17, 107 more families leave. The hamlet is leveled.', 'III, 193', to='1962-07-17', place='hoa-nhat', band_='night', also=OP + ['vietnam'])
A('1962-01-hococ', '1962-01', VH, 'The people of Phước Hải bring a boat out to Hồ Cóc, in the freed area, and hand it to the Region at the end of January; they get Saigon permits for the six crew to pass the sea checks. It is one of the boats for the trips to the North.', 'III, 150', when='Jan., late', place='ho-coc', vis=True, also=OP + ['vietnam'], check='the day.')
