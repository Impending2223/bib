import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts2'))
import dsl
from dsl import *
VH = 'vietnam-hanoi'; OP = ['vietnam-operations']
NP('bau-gia', 'Bàu Giá')
A('1960-01-baugia', '1960-01', VH, 'Bàu Giá, Tây Ninh. The military board of the Eastern Nam Bộ interprovince committee meets in the first days of January to carry out the Regional Committee\'s directive. Two plans: take one or two district seats and four or five strongpoints, or attack Tua Hai, the base of the Saigon 32d Regiment. It proposes Tua Hai; the Regional Committee approves.', 'II, 316', when='Jan., early', place='bau-gia', vis=True, also=OP, check='the day; the meeting is not dated more closely than "the first days of the year".')
A('1960-02-quangngai', '1960-02', VH, 'Quảng Ngãi. A conference of the province in February sums up the Trà Bồng rising and the struggle of 1954–60; Võ Chí Công, secretary of the Interzone V committee, speaks.', 'II, 296 n.1', when='Feb.', names=['Võ Chí Công'], place='quang-ngai-province', vis=True, check='the day; the speech is quoted from the Party History Board of Quảng Ngãi, an archive not read.')
