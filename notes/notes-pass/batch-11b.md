# Batch 11b: not done, no source could be fetched

On Nov. 26, 2026 (about 23:15 UTC) every Drive download for the works these entries cite (Dikötter, Chang, Chen Jian's Zhou Enlai, the Chen Yun, Zhu De, Peng Zhen, Peng Dehuai and Deng Xiaoping nianpu, Yang Shangkun's diary II, Mao's Jianguo yilai wengao XVI, the Jianguo yilai zhongyao wenxian, Yang Jisheng's Mubei) came back from curl as the page 'Google Drive - Quota exceeded', on both drive.usercontent.google.com and drive.google.com/uc, with a range request and without, and again after a minute. The connector's `read_file_content` returned an empty text for the Chen Yun nianpu (a scan), and `download_file_content` refuses files over 10 MB (all of these are 17 to 182 MB). No page was read, so under R4 no words were added, no `names` or `ok:note-substance` tag was written, and no patch was made. Each entry stays as it is and goes back to the queue; the 22 entries and their pages to read:

- `cal.1961-05-02.china-leadership`: not read, no source fetched; to do: words: we beg for your pardon; figures: 1 percent, 2 percent.
- `cal.1961-05-09.china-leadership`: not read, no source fetched; to do: persons: Mao Zedong; words:  两道烟 and Shaanxi's ; figures: 50 percent.
- `cal.1961-05-30.china-leadership`: not read, no source fetched; to do: words: the King of Hell keeping a wine shop; figures: 13.7 billion, 26.3 billion.
- `cal.1961-05-31.china-leadership`: not read, no source fetched; to do: words: Mobilize the urban population to go to t; figures: 30 billion, 25 million, 3 billion, 9 billion.
- `cal.1961-06-16.china-leadership-2`: not read, no source fetched; to do: persons: Chen Yun; words: came on 18 June 1961; figures: 129 million.
- `cal.1961-07-07.china`: not read, no source fetched; to do: persons: Wang Bingnan, Kennedy; words: The Signs of Chinese Communist Friendlin.
- `cal.1961-10-20.china-leadership`: not read, no source fetched; to do: persons: Khrushchev, Zhu De; words: we will not attack unless attacked; if a.
- `cal.1961-10.china-leadership-2`: not read, no source fetched; to do: words: well water not to trespass on river wate; figures: 50 billion, 20 million, 4 billion.
- `cal.1961-12-16.china-leadership-3`: not read, no source fetched; to do: persons: Peng Zhen; words: Mao on the general line and the struggle; figures: 7,000.
- `cal.1962-01-11.china-leadership`: not read, no source fetched; to do: persons: Lin Biao, Peng Dehuai; words: the Seven Thousand Cadres Conference.
- `cal.1962-02-08.china-leadership-3`: not read, no source fetched; to do: words: only three parts of what they think; figures: 90 percent, 6.9 billion, 5.4 billion, 3.8 billion.
- `cal.1962-02-21.china-leadership-3`: not read, no source fetched; to do: persons: Liu Shaoqi; words: I firmly support you; figures: 3 billion.
- `cal.1962-02-28.china-leadership-3`: not read, no source fetched; to do: persons: Li Fuchun, Peng Zhen; words: Seventy Articles on industry.
- `cal.1962-04-23.china-leadership`: not read, no source fetched; to do: persons: Ma Mingfang, Zhou Enlai, Zhu De; figures: 2 billion.
- `cal.1962-05-07.china-leadership`: not read, no source fetched; to do: persons: Chen Yun; words: extraordinary measures for an extraordin; figures: 20 million.
- `cal.1962-05-11.china-leadership`: not read, no source fetched; to do: persons: Liu Shaoqi, Deng Xiaoping; figures: 10 million, 20 million, 700 million, 10.7 million.
- `cal.1962-05-24.china-leadership-3`: not read, no source fetched; to do: persons: Li Fuchun, Tian Jiaying, Lin Ke; figures: 130 billion.
- `cal.1962-06-20.china-leadership-3`: not read, no source fetched; to do: persons: Luo Ruiqing, Chen Yi; words: counterattack on the mainland.
- `cal.1962-07-07.china-leadership-3`: not read, no source fetched; to do: persons: Deng Zihui, Tian Jiaying; words: dividing the fields to go it alone.
- `cal.1962-08-02.china-leadership-2`: not read, no source fetched; to do: words: print for the comrades; figures: 81 percent, 80 percent.
- `cal.1962-08-11.china-leadership`: not read, no source fetched; to do: persons: Peng Zhen; words: autumn from a leaf; figures: 200,000.
- `cal.1962-08-18.china-leadership`: not read, no source fetched; to do: persons: Peng Zhen, Yang Shangkun; words: tit-for-tat struggles against the Indian.
