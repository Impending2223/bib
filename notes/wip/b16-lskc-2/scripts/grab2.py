import re,sys
t=open(sys.argv[1]).read()
pages=re.split(r'^@@ ',t,flags=re.M)
kw=re.compile(r'(Bộ Chính trị|Ban Chấp hành Trung ương|Hội nghị Trung ương|Ban Bí thư|Quân [ủu]y Trung ương|Trung ương Cục|Bộ Tổng [Tt]ư lệnh|Bộ Tổng [Tt]ham mưu|Tổng cục|Bộ Quốc phòng|Chủ tịch Hồ|Hồ Chủ tịch|Bác Hồ|Lê Duẩn|Võ Nguyên Giáp|Văn Tiến Dũng|Nguyễn Chí Thanh|Phạm Văn Đồng|Quốc hội|Hội đồng Chính phủ|Chính phủ|Bộ Tư lệnh|[Nn]ghị quyết|[Cc]hỉ thị|[Mm]ệnh lệnh|[Ll]ời kêu gọi|[Bb]ức điện|[Đđ]iện số|Trung ương Đảng|Trung ương)')
dt=re.compile(r'(\d{1,2}\s*-\s*\d{1,2}\s*-\s*19\d\d|tháng\s+\d{1,2}\s*-\s*19\d\d|ngày\s+\d{1,2}\b)')
for pg in pages:
    if not pg.strip(): continue
    head,_,body=pg.partition('\n')
    flat=re.sub(r'(?<=\w)-\n(?=\w)','',body); flat=re.sub(r'\s*\n\s*',' ',flat)
    sents=re.split(r'(?<=[.;!?])\s+(?=[A-ZĐÂĂÊÔƠƯÁÀẢÃẠ"(\d])',flat)
    for s in sents:
        if dt.search(s) and kw.search(s):
            print(head.split()[0], s[:500])
