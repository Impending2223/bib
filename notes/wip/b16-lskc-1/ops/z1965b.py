import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts2'))
import dsl
from dsl import *
RV = ['polity:rvn']
def AR(*a, **k):
    k.setdefault('tags', []); k['tags'] = list(k['tags']) + ['polity:rvn']
    A(*a, **k)
# The Buddhist crisis, as the history gives it (thread vietnam; not the DRV's acts)
A('1963-0506-tudam', '1963-05-06', 'vietnam', 'Huế. 1 p.m., May 6. The province chief of Thừa Thiên, also mayor of Huế, comes to the Từ Đàm pagoda with a "request" from Ngô Đình Cẩn that the organizers of the Buddha\'s birthday observance keep it quiet. That night the Buddhist leaders of the South meet at Từ Đàm and agree on a plan.', 'III, 305–06', names=['Ngô Đình Cẩn'], place='hue', time='13:00', tz='Asia/Ho_Chi_Minh', tags=['polity:rvn', 'ok:fields-time'], check='the history\'s account; the American record of the days not matched.')
A('1963-0507-flags', '1963-05-07', 'vietnam', 'Huế. Police and secret agents begin tearing down Buddhist flags, May 7, throw them in the street, and threaten with prison all believers and monks who protest.', 'III, 307', place='hue', tags=['polity:rvn'])
A('1963-0510-tinhkhiet', '1963-05-10', 'vietnam', 'Huế. The monks\' and believers\' declaration, read by the Venerable Thích Tịnh Khiết at the mass meeting at the Từ Đàm pagoda, May 10.', 'III, 309 n.1', place='hue', tags=['polity:rvn'], check='the document (National Archives Center II, SC.04, HS.8352) not read.')
A('1963-0603-hue-students', '1963-06-03', 'vietnam', 'Huế. Five hundred students go to the office of the Saigon representative, June 3, to protest.', 'III, 312', place='hue', tags=['polity:rvn'])
A('1963-0816-hue-strike', '1963-08-16', 'vietnam', 'Huế. A general strike, Aug. 16: markets, schools, offices and plants all shut against the curfew, martial law and the blockade of the pagodas.', 'III, 312', place='hue', tags=['polity:rvn'])
A('1963-0821-deans', '1963-08-21', 'vietnam', 'Saigon. Many deans and professors of the universities resign, Aug. 21, after the raids on the pagodas.', 'III, 313', place='saigon', tags=['polity:rvn'])
A('1963-0822-studentcommittee', '1963-08-22', 'vietnam', 'Saigon. The "Committee to Lead Students and Pupils" formed, Aug. 22.', 'III, 313', place='saigon', tags=['polity:rvn'])
A('1963-0824-studentrally', '1963-08-24', 'vietnam', 'Saigon. Some 1,200 students of the Polytechnic, 700 of the School of Pharmacy and over 1,200 of the Law School leave exams and classes, Aug. 24, and rally against the Diệm government. Aug. 25 several thousand students and pupils hold a large rally at the Bến Thành market.', 'III, 313', to='1963-08-25', place='saigon', tags=['polity:rvn'])
# cites to the calendar's American and Saigon entries
C('cal.1961-04-29.vietnam', 'III, 13 (Apr. 29, the NSC meets and sets the policy, measures and steps)', 'A')
C('cal.1961-10-18.vietnam', 'III, 18 (Oct. 18, Taylor and Rostow, two members of the NSC, lead a mission of military and civil experts to the South)', 'A')
C('cal.1961-11-03.vietnam', 'III, 19–22 (Nov. 3, the Taylor mission\'s report, its proposals: administrative advisers; the intelligence net; a survey of the provinces; more arms and training for the Civil Guard and Self-Defense Corps; control of the coasts and rivers; MAAG reorganized and enlarged; a task force of 6,000 to 8,000)', 'A')
C('cal.1961-11-22.vietnam', 'III, 22 (NSAM 111, Nov. 22, 1961; the history gives Nov. 16 for the President\'s approval of Taylor\'s plan at III, 167)', 'A')
C('cal.1962-02-08.vietnam', 'III, 23 (Feb. 8, 1962, MAAG becomes MACV under Gen. Paul Harkins, who replaces McGarr)', 'A')
C('cal.1963-05-08.vietnam', 'III, 305–09 (the Buddha\'s birthday at Huế; the night of May 8 a crowd of thousands of monks, nuns and believers at the radio station)', 'A')
C('cal.1963-06-11.vietnam', 'III, 310 (Thích Quảng Đức, in Saigon, June 11)', 'A')
C('cal.1963-06-16.vietnam', 'III, 312 (the morning of June 16, about 700,000 people go to the Xá Lợi pagoda, where Thích Quảng Đức\'s body lies)', 'A')
V('cal.1963-06-16.vietnam', 'A', 'the morning of June 16, some 700,000 people and Buddhists into the streets toward Xá Lợi', 'III, 312')
C('cal.1963-08-21.vietnam', 'III, 313 (the night of Aug. 20–21, Diệm\'s field police and Nhu\'s special forces attack almost every pagoda together)', 'A')
C('cal.1963-11-01.vietnam', 'III, 316–19 (Nov. 1, "All Saints", the officials and soldiers off the morning; the command decides to act at 1 p.m.; Capt. Hùng Minh\'s 4th Marine Battalion takes the national police headquarters; Nov. 2, 5 a.m., armor and marines on Gia Long Palace; 6:30 a.m. Dương Văn Minh announces on Saigon radio the end of the Diệm–Nhu government; 11 p.m. Nov. 2 the prisoners released)', 'A')
C('cal.1963-11-26.vietnam', 'III, 329 (NSAM 273, Nov. 26, 1963; the aim of ending the war and winning by the end of 1965)', 'A')
C('cal.1963-12-21.vietnam', 'III, 330 (McNamara\'s report "Situation in Vietnam", Dec. 21, 1963)', 'A')
C('cal.1964-01-30.vietnam', 'III, 327 (Jan. 30, 1964, Gen. Nguyễn Khánh overthrows the Dương Văn Minh government)', 'A')
C('cal.1964-03-16.vietnam', 'III, 332 (McNamara and Taylor in Saigon Mar. 8–12; the report of Mar. 16; approved Mar. 17 as NSAM 288)', 'A')
C('cal.1964-08-07.vietnam', 'III, 366 (Aug. 7, Congress passes the Tonkin Gulf resolution by an overwhelming majority)', 'A')
C('cal.1965-01-27.vietnam-2', 'III, 394 (the memorandum of Jan. 27, 1965 from McNamara and Bundy: the policy "could lead only to a disastrous defeat")', 'A')
