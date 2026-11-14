import re,sys
t=open(sys.argv[1]).read()
# flatten each page into one line of text, keep page marker
pages=re.split(r'^@@ ',t,flags=re.M)
kw=re.compile(r'(Bộ Chính trị|Ban Chấp hành Trung ương|Hội nghị Trung ương|Hội nghị lần thứ|Ban Bí thư|Quân ủy Trung ương|Quân uỷ Trung ương|Trung ương Cục|Bộ Tổng Tư lệnh|Bộ Tổng tư lệnh|Bộ Tổng Tham mưu|Bộ Quốc phòng|Hồ Chí Minh|Chủ tịch|Lê Duẩn|Võ Nguyên Giáp|Văn Tiến Dũng|Nguyễn Chí Thanh|Phạm Văn Đồng|Quốc hội|Hội đồng Chính phủ|Chính phủ|Mặt trận|Quân giải phóng|Bộ Tư lệnh|nghị quyết|Nghị quyết|chỉ thị|Chỉ thị|mệnh lệnh|lời kêu gọi|Lời kêu gọi|điện)')
dt=re.compile(r'(ngày\s+\d{1,2}(?:\s*(?:đến|và|-|,)\s*\d{1,2})*\s*-\s*\d{1,2}\s*-\s*19\d\d|\d{1,2}\s*-\s*\d{1,2}\s*-\s*19\d\d|tháng\s+\d{1,2}\s*-\s*19\d\d)')
for pg in pages:
    if not pg.strip(): continue
    head,_,body=pg.partition('\n')
    flat=re.sub(r'-\n(?=\S)','',body); flat=re.sub(r'\s*\n\s*',' ',flat)
    sents=re.split(r'(?<=[.;!?])\s+(?=[A-ZĐÂĂÊÔƠƯÁÀẢÃẠ"(])',flat)
    for s in sents:
        if dt.search(s) and kw.search(s) and re.search(r'ngày\s+\d',s):
            print(head.split()[0], s[:420])
