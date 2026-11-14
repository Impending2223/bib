# Văn kiện Đảng toàn tập (w.van-kien-dang-toan): book check

## 1960–61 (batch 12, the DRV's records; vols. 21 and 22)

Reader: batch 12, share "b12-vkd-a", Nov. 12, 2026 (a restart of a reader stopped by an interruption; its downloads, its table of contents and the series card were taken over and checked). Patch: `inbox/2026-11-12-b12-drv-1960-61.yaml` (patch name `2026-11-12-b12-drv-1960-61`), 165 ops: 153 new entries, 11 edits of entries the calendar held, 1 cite. No witnesses file, no by-work edges.

### The card

`w.van-kien-dang-toan`, in `works/v.yaml` (made by the first reader, uncommitted; mended here, that card alone): *Văn kiện Đảng toàn tập* [Complete Party Documents], 54 vols. (Chính trị quốc gia, 1998–2007), the publisher added, the note cut to two fragments. Cited like the Presidium's volumes (`[[w.prezidium-tsk-kpss-1954]], I, 419`): the volume in Roman, then the book's page, `[[w.van-kien-dang-toan]], XXI, 288–305`; the src rows `w.van-kien-dang-toan XXI, 288–305`. The document's own heading, in Vietnamese and in italics, opens each new note, with its signer where the page prints one. "Made public: 2002." on every record kept in the Party archive ("Lưu tại Kho Lưu trữ Trung ương Đảng"), not on the communiqués or the Congress's public documents.

### The copies

- Vol. 21 (1960): Drive `1JStHLzzzKuM3VJtButpRYQ6cwuo7ZqLf`, 580 PDF pages, A4 landscape, PDF 1.4 (iTextSharp). Colophon (XXI, 1150): CTQG-2002, "In xong và nộp lưu chiểu tháng 10 năm 2002", 6,000 copies. Book pp. V, 1–1150; contents at 1139–50; appendix (the regional committees' resolutions) 1059–1137.
- Vol. 22 (1961): Drive `1b5CamzHVz1DkcpWmxk6livk5ad-zgGlz`, 412 PDF pages, letter, PDF 1.4. Colophon (XXII, 818): CTQG-2002, printed November 2002. Book pp. V–VI, 1–818; contents at 809–17; appendix 631–807.
- Both downloaded by the first reader into the scratchpad (`books/b12-vkd-a/v21`, `v22`); deleted when done.

### The encoding and the converter

Text layers in the TCVN3 (ABC) font encoding (fonts VnCenturySchoolbook, VnCenturySchoolbookH, embedded, WinAnsi). `tools/vn/vkd2txt.py` (pdftotext -layout, then iconv from TCVN5712-1) converts it cleanly; the first reader's `split.py` applies the same conversion (the same FIX table and iconv) to each half of a two-up page, by `pdftotext -x -W`, so that each book page comes out alone; its output was used for reading and page numbers. Headings in the capitals font come out lower-case with capital marks ("NGHị QUYếT"); read as capitals. Quotation marks inside the text sometimes come out as "Ỏ ... Õ" and a dash as "Ọ" (TCVN3's own code points for the curly marks): read as quotation marks and a dash. No OCR needed.

### Two-up, and the offset

Both volumes print two book pages to a PDF page (left and right halves). Every cite gives the book's page, read from the running heads and folios in the text layer, not computed. For the record: vol. 21, book page = 2 × PDF page − 7 (left half; − 6 the right) from PDF 4 (p. 1) to PDF 391; from PDF 392 (p. 775, the statute) − 9 (two unnumbered book pages before the statute). Vol. 22, 2 × PDF page − 7 throughout. Checked against the folios at XXI, 1, 3–6, 393–94, 593–94, 891–92, 1111–12, 1131–32; XXII, 1, 807–18. Page images not rendered: the folios of the text layer stand for them (the merger may want to look at a page or two, e.g. XXI, 293 and XXII, 158).

### The rules used

The brief (notes/briefs/batch12-foreign.md): one entry a document of the Politburo, the Secretariat, the Central Committee and its plenums, the Congress, the directives to the South; a session that the record names (the Politburo of Apr. 21–22, 1960, of Sept. 8, 1961; the Secretariat of Sept. 27, 1960, of Mar. 22, July 3 and Nov. 6, 1961) entered on the session's day, its record cited there. The reader's card for the test; R1 for the span (Jan. 6, 1960: the documents of Jan. 4 and 5, 1960 passed over as before it); R18 for what is passed over (commemorations, provincial matters). Names: everyone `c` names; `name:` tags only for those with name entries (`lists/vn/III.H.yaml`, `vn.who.*`, and the kja names).

### Doubtful, for the merger

- Same-day entries: 24 new ids share their day and thread with another entry (22 days among the new entries, Mar. 7, 1960 with three; Apr. 15 and July 1960 and Oct. 31, 1961 beside entries the calendar held), each a separate document (patch-check warns "one event?" and "a duplicate of"): at the merge, `./bib resolve ID --take keep` for each. None is the same document twice.
- cal.1961-02-25 (`cal.1961-02-25.vietnam-hanoi`): the Politburo's resolution no. 12-NQ/TW on the spring rectification campaign, dated Feb. 25, 1961, entered apart from cal.1961-02-25.vietnam (the Politburo's sessions of Jan. 31 and Feb. 25 on the military tasks, by *Victory in Vietnam*). The resolution names no session; whether it came from the same session the volume does not say.
- The Third Congress (Sept. 5–10, 1960) stays one entry, cal.1960-09-05.vietnam, cited for its resolution, the opening and closing addresses and the elections; the political report (Lê Duẩn, Sept. 5), the report on the statute (Lê Đức Thọ, Sept. 6) and the five-year plan report (Nguyễn Duy Trinh, Sept. 7) were not read through and not entered as days of their own: a later reader may.
- cal.1960-05-04.vietnam-hanoi: the Interzone V resolution, dated May 4, 1960, quotes word for word as the Center's line the Center's cable of May 21, 1960 (XXI, 1110 against 333): a Check.
- cal.1961-01-24.vietnam-hanoi: the instruction raises armed struggle "song song" (parallel) with political, military struggle the chief form in the mountains (XXII, 157–58), against the entry's "political struggle still central": a Check.
- The third plenum: its communiqué has it meet Dec. 28, 1960–Jan. 6, 1961; its two resolutions, Dec. 30–Jan. 5 and Jan. 5–7 (a Check on `cal.1960-12-30.vietnam-hanoi`).
- "Miền Tây" (`cal.1961-07-25.vietnam-hanoi`): the regulation of July 25, 1961 on cadres sent to "the West" at "the friendly party's" request is entered in its own words; the place is not named.
- `cal.1961-07-19.vietnam-hanoi`: the Politburo's resolution of July 19, 1961, on credit and money, known only from the Secretariat's directive of Nov. 9 (XXII, 508), not printed in the volume.

### Persons named with no name entry (named in `c` and "Names:", not tagged)

Nguyễn Văn Trân, Nguyễn Lương Bằng, Song Hào, Hoàng Văn Hoan, Phạm Hùng, Tố Hữu, Lê Văn Lương, Lê Thanh Nghị, Chu Văn Tấn, Hoàng Anh, Trần Quốc Hoàn, Nguyễn Văn Thao, Huỳnh Tấn Phát, Cung ("Dr. Cung"), Trần Lương, Võ Chí Công, Trần Văn Quang, Nguyễn Đôn, Trần Danh Tuyên, Hoàng Quốc Việt, Phạm Huy Thông, Vũ Quang, Lê Bình, Nguyễn Văn Trọng. Signers named only in the notes: Nguyễn Duy Trinh, Lê Văn Lương, Nguyễn Khai, Phạm Chung.

### The documents, one by one

Every document in the two tables of contents, in the volume's order, with its first page and the ruling. Ids are the new entries' (claimed in `inbox/new-entries.tsv`).

| Page | Document (the contents' heading) | Ruling |
|---|---|---|
| XXI, 1 | Nghị quyết của Bộ Chính trị số 98-NQ/TW, ngày 4-11960 (họp ngày 12-9-1959) về quy hoạch cải tạo và mở rộng thành phố Hà Nội | passed over: before the span (Jan. 4, 1960) |
| XXI, 14 | Chỉ thị của Ban Bí thư số 178-CT/TW, ngày 4-1-1960 về việc tăng cường chỉ đạo công tác phát triển Đảng lớp "6-1" | passed over: before the span (Jan. 4, 1960) |
| XXI, 20 | Thư của Ban Chấp hành Trung ương Đảng ngày 4-11960 gửi các đồng chí đảng bộ miền Nam nhân dịp tết Nguyên đán 1960 | passed over: before the span (Jan. 4, 1960); a New Year letter to the South |
| XXI, 25 | Chỉ thị của Ban Bí thư số 179-CT/TW, ngày 5-1-1960 về công tác chuẩn bị điều tra dân số | passed over: before the span (Jan. 5, 1960) |
| XXI, 29 | Bài nói của Chủ tịch Hồ Chí Minh tại lễ kỷ niệm 30 năm ngày thành lập Đảng | passed over: before the span (spoken the evening of Jan. 5, 1960); a commemoration |
| XXI, 34 | Chỉ thị của Ban Bí thư số 181-CT/TW, ngày 13-1-1960 về công tác thể dục thể thao | entered: cal.1960-01-13.vietnam-hanoi |
| XXI, 39 | Thông tri của Ban Bí thư số 305-TT/TW, ngày 19-1-1960 về việc tăng cường lãnh đạo, quyết tâm hoàn thành tốt công tác trung tâm ở nông thôn h | entered: cal.1960-01-19.vietnam-hanoi |
| XXI, 43 | Nghị quyết của Bộ Chính trị số 100-NQ/TW, ngày 20-11960 về việc một số nhân sĩ trí thức cao cấp trong Chính phủ xin gia nhập Đảng ta 43 | entered: cal.1960-01-20.vietnam-hanoi |
| XXI, 45 | Thông tri của Ban Bí thư số 307-TT/TW, ngày 21-1-1960 về việc tổ chức học tập Nghị quyết Hội nghị Trung ương lần thứ XIV, XV, XVI cho cán bộ | entered: cal.1960-01-21.vietnam-hanoi-2 |
| XXI, 49 | Thông tri của Ban Bí thư số 309-TT/TW, ngày 21-1-1960 về việc chấn chỉnh bộ máy tổ chức của phụ nữ ở các xã | entered: cal.1960-01-21.vietnam-hanoi |
| XXI, 52 | Thông tri của Ban Bí thư số 310-TT/TW, ngày 23-1-1960 bổ sung một số điểm cụ thể về chính sách hợp tác hóa nông nghiệp | entered: cal.1960-01-23.vietnam-hanoi |
| XXI, 63 | Chỉ thị của Ban Bí thư số 183-CT/TW, ngày 5-2-1960 về việc tăng cường công tác điều tra thống kê | entered: cal.1960-02-05.vietnam-hanoi |
| XXI, 67 | Chỉ thị của Ban Bí thư số 184-CT/TW, ngày 6-2-1960 về việc áp dụng chế độ hợp đồng kinh tế giữa các xí nghiệp quốc doanh và các cơ quan Nhà  | entered: cal.1960-02-06.vietnam-hanoi |
| XXI, 70 | Chỉ thị của Ban Bí thư số 185-CT/TW, ngày 9-2-1960 về việc lãnh đạo bầu cử đại biểu Quốc hội | entered: cal.1960-02-09.vietnam-hanoi |
| XXI, 74 | Thông tri của Ban Bí thư số 314-TT/TW, ngày 9-2-1960 bổ sung một số điểm về hoàn thành cải cách dân chủ trong cuộc vận động hợp tác hóa nông | entered: cal.1960-02-09.vietnam-hanoi-2 |
| XXI, 106 | Chỉ thị của Ban Bí thư số 186-CT/TW, ngày 17-2-1960 về mấy công tác lớn phải làm để đẩy mạnh công tác đấu tranh chống bọn phản cách mạng | entered: cal.1960-02-17.vietnam-hanoi |
| XXI, 131 | Nghị quyết của Ban Bí thư số 103-NQ/TW, ngày 19-2-1960 về vấn đề thanh toán các khoản nợ của các xí nghiệp tư doanh khi thực hiện công tư hợ | entered: cal.1960-02-19.vietnam-hanoi |
| XXI, 136 | Chỉ thị của Ban Bí thư số 187-CT/TW, ngày 20-2-1960 tăng cường sự lãnh đạo của các cấp uỷ Đảng đối với công tác công an và cơ quan công an | entered: cal.1960-02-20.vietnam-hanoi |
| XXI, 140 | Nghị quyết của Ban Bí thư số 104-NQ/TW, ngày 24-21960 kiện toàn Ban Công tác nông thôn các cấp | entered: cal.1960-02-24.vietnam-hanoi |
| XXI, 145 | Nghị quyết của Ban Bí thư số 105-NQ/TW, ngày 25-21960 về việc thành lập Vụ Nghiên cứu Xã hội | entered: cal.1960-02-25.vietnam-hanoi |
| XXI, 147 | Nghị quyết của Ban Bí thư số 111-NQ/TW, ngày 26-21960 về việc giải quyết vấn đề vàng bạc đối với tư sản trong công tư hợp doanh | entered: cal.1960-02-26.vietnam-hanoi |
| XXI, 150 | Chỉ thị của Ban Bí thư số 189-CT/TW, ngày 26-2-1960 về việc các thành phố, khu, tỉnh, tham gia xây dựng dự thảo chỉ thị về kế hoạch 5 năm lầ | entered: cal.1960-02-26.vietnam-hanoi-2 |
| XXI, 154 | Chỉ thị của Ban Bí thư số 190-CT/TW, ngày 29-2-1960 về việc thành lập Ban Vận động hợp tác xã thủ công nghiệp các cấp | entered: cal.1960-02-29.vietnam-hanoi |
| XXI, 158 | Chỉ thị của Ban Bí thư số 191-CT/TW, ngày 3-3-1960 về việc xây dựng và phát triển công nghiệp địa phương | entered: cal.1960-03-03.vietnam-hanoi |
| XXI, 172 | Chỉ thị của Ban Bí thư số 192-CT/TW, ngày 7-3-1960 về chính sách đối với đảng viên, cán bộ, nhân viên Nhà nước và nhân sĩ, trí thức, tư sản  | entered: cal.1960-03-07.vietnam-hanoi |
| XXI, 175 | Thông tri của Ban Bí thư số 317-TT/TW, ngày 7-3-1960 về việc tăng cường lãnh đạo, tiếp tục mở rộng phong trào cải tạo công thương nghiệp tư  | entered: cal.1960-03-07.vietnam-hanoi-2 |
| XXI, 178 | Thông tri của Ban Bí thư số 318-TT/TW, ngày 7-3-1960 về công tác tuyên truyền vận động quán triệt Luật Hôn nhân và gia đình | entered: cal.1960-03-07.vietnam-hanoi-3 |
| XXI, 181 | Thông tri của Ban Bí thư số 319-TT/TW, ngày 8-3-1960 về việc đẩy mạnh hơn nữa công tác chuẩn bị bầu cử đại biểu Quốc hội | entered: cal.1960-03-08.vietnam-hanoi |
| XXI, 184 | Thông tri của Ban Bí thư số 320-TT/TW, ngày 8-3-1960 về tăng cường công tác đối với đảng viên dự bị | entered: cal.1960-03-08.vietnam-hanoi-2 |
| XXI, 190 | Thông tri của Ban Bí thư số 321-TT/TW, ngày 11-3-1960 về việc tiếp tục đẩy công tác củng cố hợp tác xã lên một bước nữa | entered: cal.1960-03-11.vietnam-hanoi |
| XXI, 193 | Chỉ thị của Ban Bí thư số 193-CT/TW, ngày 14-3-1960 về mấy ngày kỷ niệm trong năm 1960 | passed over: commemorations (Lenin, Hồ Chí Minh at 70, the DRV at 15) |
| XXI, 198 | Chỉ thị của Ban Bí thư số 195-CT/TW, ngày 15-3-1960 về việc đẩy mạnh phong trào hợp tác hóa và phát triển sản xuất thủ công nghiệp năm 1960 | entered: cal.1960-03-15.vietnam-hanoi |
| XXI, 201 | Chỉ thị của Ban Bí thư số 196-CT/TW, ngày 17-3-1960 về việc tổ chức nghiên cứu chính sách mua bán lương thực thích hợp với tình hình mới | entered: cal.1960-03-17.vietnam-hanoi |
| XXI, 205 | Chỉ thị của Ban Bí thư số 198-CT/TW, ngày 17-3-1960 về việc tiến hành Đại hội các cấp | entered: cal.1960-03-17.vietnam-hanoi-2 |
| XXI, 214 | Nghị quyết của Ban Bí thư số 107-NQ/TW, ngày 19-31960 về việc thành lập Ban Vận động hợp tác xã thủ công nghiệp Trung ương | entered: cal.1960-03-19.vietnam-hanoi |
| XXI, 216 | Chỉ thị của Ban Bí thư số 197-CT/TW, ngày 19-3-1960 về công tác thiếu niên, nhi đồng | entered: cal.1960-03-19.vietnam-hanoi-2 |
| XXI, 226 | Chỉ thị của Ban Bí thư số 199-CT/TW, ngày 24-3-1960 về việc lập dự án kế hoạch động viên và kết hợp giữa kinh tế và quốc phòng | entered: cal.1960-03-24.vietnam-hanoi |
| XXI, 230 | Chỉ thị của Ban Bí thư số 200-CT/TW, ngày 30-3-1960 về việc cải tạo những người có nhiều nhà cho thuê và quản lý toàn bộ nhà cửa cho thuê ở  | entered: cal.1960-03-30.vietnam-hanoi |
| XXI, 233 | Chỉ thị của Ban Bí thư số 201-CT/TW, ngày 30-3-1960 về việc tăng cường lãnh đạo phát triển và củng cố hợp tác xã vay mượn trong năm 1960 | entered: cal.1960-03-30.vietnam-hanoi-2 |
| XXI, 240 | Nghị quyết của Ban Bí thư số 109-NQ/TW, ngày 31-3-1960 về việc thành lập Đảng uỷ Công an nhân dân vũ trang | entered: cal.1960-03-31.vietnam-hanoi |
| XXI, 242 | Nghị quyết của Ban Bí thư số 110-NQ/TW, ngày 31-31960 về tổ chức bộ phận chuyên trách việc hoàn thành cải cách dân chủ trong cuộc vận động h | entered: cal.1960-03-31.vietnam-hanoi-2 |
| XXI, 245 | Chỉ thị của Ban Bí thư số 202-CT/TW, ngày 4-4-1960 về việc tích cực lãnh đạo công tác chăn nuôi | entered: cal.1960-04-04.vietnam-hanoi |
| XXI, 254 | Thông tri của Ban Bí thư số 324-TT/TW, ngày 4-4-1960 về việc tăng cường lãnh đạo và thực hiện tốt nhiệm vụ công tác thuỷ lợi năm 1960 | entered: cal.1960-04-04.vietnam-hanoi-2 |
| XXI, 258 | Chỉ thị của Ban Bí thư số 203-CT/TW, ngày 7-4-1960 về nhiệm vụ phát triển giáo dục bổ túc văn hóa và phổ thông năm học 1960-1961 | entered: cal.1960-04-07.vietnam-hanoi |
| XXI, 264 | Thông tri của Ban Bí thư số 327-TT/TW, ngày 13-4-1960 về việc tăng cường tổ chức và cán bộ đối với toà án nhân dân các cấp | entered: cal.1960-04-13.vietnam-hanoi |
| XXI, 268 | Chỉ thị của Ban Bí thư số 204-CT/TW, ngày 15-4-1960 về công tác hợp tác hóa nông nghiệp trong năm 1960 và trong đợt Xuân - Hạ | entered: cal.1960-04-15.vietnam-hanoi-2 |
| XXI, 276 | Nghị quyết của Bộ Chính trị số 113-NQ/TW, ngày 22-41960 về công tác học tập lý luận của cán bộ | entered: cal.1960-04-22.vietnam-hanoi |
| XXI, 280 | Chỉ thị của Ban Bí thư số 205-CT/TW, ngày 25-4-1960 về việc tiến hành công tác thu thuế nông nghiệp, thu nợ và mua thóc vụ chiêm 1960 280 | entered: cal.1960-04-25.vietnam-hanoi |
| XXI, 288 | Điện mật của Trung ương Đảng số 160, ngày 28-4-1960 gửi Xứ uỷ Nam Bộ, đồng gửi Liên khu uỷ V để nghiên cứu | cited: cal.1960-04-28.vietnam-hanoi |
| XXI, 306 | Điện của Trung ương Đảng số 34, ngày 30-4-1960 gửi Xứ uỷ Nam Bộ, Khu uỷ V | entered: cal.1960-04-30.vietnam-hanoi |
| XXI, 309 | Nghị quyết của Ban Bí thư số 114-NQ/TW, ngày 13-51960 về việc xây dựng ba công trình thuỷ điện Làng Hít, Thác Bà, Quảng Cư | entered: cal.1960-05-13.vietnam-hanoi |
| XXI, 311 | Nghị quyết của Bộ Chính trị số 115-NQ/TW, ngày 20-51960 về cải tiến chế độ tiền lương và tăng lương năm 1960 | entered: cal.1960-05-20.vietnam-hanoi |
| XXI, 326 | Thông tri của Ban Bí thư số 331-TT/TW, ngày 20-5-1960 về việc quy định Đại hội đảng bộ các cấp thảo luận Đề cương Báo cáo Chính trị của Trun | entered: cal.1960-05-20.vietnam-hanoi-2 |
| XXI, 328 | Chỉ thị của Ban Bí thư số 206-CT/TW, ngày 21-5-1960 về việc tiến hành Đại hội đại biểu khu, thành, tỉnh | entered: cal.1960-05-21.vietnam-hanoi |
| XXI, 332 | Điện của Trung ương ngày 21-5-1960 gửi X.U.N.B và L.K.U. V | entered: cal.1960-05-21.vietnam-hanoi-2 |
| XXI, 337 | Chỉ thị của Ban Bí thư số 207-CT/TW, ngày 27-5-1960 về việc dời dân và những cơ sở kinh tế, chính trị ở trong khu vực hồ chứa của Nhà máy th | entered: cal.1960-05-27.vietnam-hanoi |
| XXI, 340 | Thông tri của Ban Bí thư số 332-TT/TW, ngày 28-5-1960 về việc thi hành Nghị quyết của Hội nghị Bộ Chính trị về cải tiến chế độ tiền lương và | entered: cal.1960-05-28.vietnam-hanoi |
| XXI, 344 | Chỉ thị của Ban Bí thư số 208-CT/TW, ngày 2-6-1960 về công tác phòng và chống lụt bão năm 1960 | entered: cal.1960-06-02.vietnam-hanoi |
| XXI, 349 | Chỉ thị của Ban Bí thư số 211-CT/TW, ngày 9-6-1960 về việc tăng cường công tác y tế | entered: cal.1960-06-09.vietnam-hanoi |
| XXI, 358 | Chỉ thị của Bộ Chính trị số 212-CT/TW, ngày 16-6-1960 về việc tiến hành hợp tác hóa nghề cá ở miền biển 358 | entered: cal.1960-06-16.vietnam-hanoi |
| XXI, 376 | Chỉ thị của Ban Bí thư số 213-CT/TW, ngày 22-6-1960 về chủ trương đối với một số vấn đề cụ thể trong công tác cải tạo công thương nghiệp tư  | entered: cal.1960-06-22.vietnam-hanoi |
| XXI, 383 | Thông tri của Ban Bí thư số 336-TT/TW, ngày 22-6-1960 về việc ban hành các bảng lương cho cán bộ, công nhân, viên chức công tác ở các cơ qua | entered: cal.1960-06-22.vietnam-hanoi-2 |
| XXI, 387 | Chỉ thị của Ban Bí thư số 214-CT/TW ngày 27-6-1960 về vấn đề mở một đợt đấu tranh chính trị rộng lớn chống Mỹ - Diệm nhân dịp 20-7 | entered: cal.1960-06-27.vietnam-hanoi |
| XXI, 392 | Chỉ thị của Ban Bí thư số 215-CT/TW, ngày 30-6-1960 về việc tăng cường lực lượng lãnh đạo của Đảng nhằm giải quyết tốt vấn đề lương thực | entered: cal.1960-06-30.vietnam-hanoi |
| XXI, 395 | Nghị quyết của Bộ Chính trị số 119-NQ/TW, ngày 4-71960 về bản báo cáo "Phương hướng, nhiệm vụ và các con số kiểm tra chủ yếu làm căn cứ cho  | entered: cal.1960-06-27.vietnam-hanoi-2 |
| XXI, 398 | Chỉ thị của Ban Bí thư số 217-CT/TW, ngày 9-7-1960 về công tác đối với Phật giáo | entered: cal.1960-07-09.vietnam-hanoi |
| XXI, 402 | Thông tri của Ban Bí thư số 338-TT/TW, ngày 20-7-1960 về việc tăng cường lãnh đạo hơn nữa đối với công tác tiền lương và việc vận động gửi t | entered: cal.1960-07-20.vietnam-hanoi |
| XXI, 406 | Thông tri của Ban Bí thư số 339-TT/TW, ngày 28-7-1960 giải thích và bổ sung thêm một số điểm về chính sách cụ thể xây dựng hợp tác xã nông n | entered: cal.1960-07-28.vietnam-hanoi |
| XXI, 421 | Chỉ thị của Ban Bí thư số 218-CT/TW, ngày 29-7-1960 bổ sung về việc tổ chức đợt kỷ niệm 15 năm nước Việt Nam Dân chủ Cộng hoà | passed over: commemoration (the DRV at 15) |
| XXI, 425 | Chỉ thị của Ban Bí thư số 219-CT/TW, ngày 12-8-1960 về những biện pháp cấp bách để giải quyết khó khăn về lương thực hiện nay | entered: cal.1960-08-12.vietnam-hanoi |
| XXI, 431 | Chỉ thị của Ban Bí thư số 220-CT/TW, ngày 15-8-1960 về việc tích cực thi hành Chỉ thị số 186 đẩy mạnh cuộc đấu tranh chống bọn phản cách mạn | entered: cal.1960-08-15.vietnam-hanoi |
| XXI, 439 | Thông cáo của Hội nghị lần thứ 18 Ban Chấp hành Trung ương Đảng Lao động Việt Nam ngày 15-8-1960 về Hội nghị Bucarét | entered: cal.1960-08-15.vietnam-hanoi-2 |
| XXI, 442 | Thông cáo của Hội nghị lần thứ 18 Ban Chấp hành Trung ương Đảng Lao dộng Việt Nam ngày 15-8-1960 về việc triệu tập Đại hội Đảng | cited: the second communiqué, cal.1960-08-15.vietnam-hanoi-2 |
| XXI, 443 | Nghị quyết của Bộ Chính trị số 122-NQ/TW, ngày 16-81960 về việc thống nhất chế độ tiền lương của công nhân, viên chức lưu dung vào chế độ ti | entered: cal.1960-08-16.vietnam-hanoi |
| XXI, 446 | Chỉ thị của Ban Bí thư số 221-CT/TW ngày 18-8-1960 về việc căn bản hoàn thành hợp tác hóa nông nghiệp và đẩy mạnh sản xuất nông nghiệp trong | entered: cal.1960-08-18.vietnam-hanoi |
| XXI, 460 | Nghị quyết của Bộ Chính trị số 124-NQ/TW ngày 30-81960 (họp tháng 4-1960) về vấn đề đẩy mạnh việc cải tạo và phát triển thủ công nghiệp theo | entered: cal.1960-08-30.vietnam-hanoi |
| XXI, 475 | Chỉ thị của Ban Bí thư số 222-CT/TW ngày 5-9-1960 về việc tiến hành một đợt tuyên truyền cổ động rộng rãi để giới thiệu những Nghị quyết của | entered: cal.1960-09-05.vietnam-hanoi |
| XXI, 481 | Diễn văn khai mạc Đại hội đại biểu toàn quốc lần thứ III do Chủ tịch Hồ Chí Minh đọc, ngày 5-9-1960 | cited: cal.1960-09-05.vietnam |
| XXI, 491 | Báo cáo của Ban thẩm tra bầu cử đọc tại đại hội toàn quốc lần thứ III tháng 9 năm 1960 | the Third Congress (cal.1960-09-05.vietnam): the election commissions report; not read through, not entered apart |
| XXI, 495 | Báo cáo Chính trị của Ban Chấp hành Trung ương Đảng tại Đại hội đại biểu toàn quốc lần thứ III do đồng chí Lê Duẩn trình bày, ngày 5-9-1960  | the Third Congress (cal.1960-09-05.vietnam): the political report, Lê Duẩn, Sept. 5; not read through, not entered apart |
| XXI, 657 | Báo cáo về việc sửa đổi Điều lệ Đảng của Ban Chấp hành Trung ương Đảng Lao động Việt Nam ở Đại hội đại biểu toàn quốc lần thứ III do đồng ch | the Third Congress (cal.1960-09-05.vietnam): the report on the statute, Lê Đức Thọ, Sept. 6; not read through, not entered apart |
| XXI, 775 | Điều lệ Đảng (do Đại hội đại biểu toàn quốc lần thứ III của Đảng thông qua) | the Third Congress (cal.1960-09-05.vietnam): the statute; not read through, not entered apart |
| XXI, 815 | Nhiệm vụ và phương hướng của kế hoạch 5 năm lần thứ nhất phát triển kinh tế quốc dân (1961-1965). Báo cáo bổ sung tại Đại hội đại biểu toàn  | the Third Congress (cal.1960-09-05.vietnam): the five-year plan report, Nguyễn Duy Trinh, Sept. 7; not read through, not entered apart |
| XXI, 904 | Nghị quyết của Đại hội đại biểu toàn quốc lần thứ III của Đảng Lao động Việt Nam, ngày 10-9-1960 về ngày thành lập Đảng | the Third Congress (cal.1960-09-05.vietnam): the resolution on the Partys founding day (Feb. 3), Sept. 10; not read through, not entered apart |
| XXI, 905 | Danh sách các đồng chí trúng cử Ban Chấp hành Trung ương khóa III (trích Báo cáo kết quả cuộc bầu cử Ban Chấp hành Trung ương tại Đại hội đạ | cited: cal.1960-09-05.vietnam |
| XXI, 913 | Nghị quyết của Đại hội đại biểu toàn quốc lần thứ III của Đảng Lao động Việt Nam về nhiệm vụ và đường lối của Đảng trong giai đoạn mới ngày  | cited: cal.1960-09-05.vietnam |
| XXI, 946 | Lời kêu gọi của Đại hội đại biểu toàn quốc lần thứ III của Đảng Lao động Việt Nam | the Third Congress (cal.1960-09-05.vietnam): the Congresss appeal; not read through, not entered apart |
| XXI, 950 | Diễn văn bế mạc Đại hội đại biểu toàn quốc lần thứ III do Chủ tịch Hồ Chí Minh đọc, ngày 10-9-1960 | cited: cal.1960-09-05.vietnam |
| XXI, 953 | Chỉ thị của Ban Bí thư số 01-CT/TW, ngày 6-10-1960 về việc tiến hành hội nghị ở các cấp, các ngành để thảo luận các nghị quyết của Đại hội đ | entered: cal.1960-10-06.vietnam-hanoi |
| XXI, 957 | Nghị quyết của Ban Bí thư số 01-NQ/TW, ngày 11-10-1960 về việc nghiên cứu quy định nhiệm vụ, quyền hạn cụ thể giữa cấp khu và cấp tỉnh trong | passed over: a provincial matter (the Việt Bắc zone and its provinces) |
| XXI, 960 | Thông báo số 02-TB/TH, ngày 11-10-1960 về Hội nghị Ban Bí thư | entered: cal.1960-09-27.vietnam-hanoi |
| XXI, 964 | Chỉ thị của Ban Bí thư số 02-CT/TW, ngày 12-10-1960 về tăng cường công tác thông tấn xã | entered: cal.1960-10-12.vietnam-hanoi |
| XXI, 968 | Thông tri của Ban Bí thư số 05-TT/TW, ngày 13-10-1960 về việc tăng cường lãnh đạo cuộc vận động hợp tác hóa nông nghiệp kết hợp hoàn thành c | entered: cal.1960-10-13.vietnam-hanoi |
| XXI, 983 | Nghị quyết của Ban Bí thư số 02-NQ/TW, ngày 17-101960 về Nhà xuất bản Sự thật | cited: with the session of Sept. 27, cal.1960-09-27.vietnam-hanoi |
| XXI, 985 | Chỉ thị của Ban Bí thư số 03-CT/TW, ngày 18-10-1960 về lãnh đạo tốt việc phân chia hoa lợi năm 1960 trong các hợp tác xã sản xuất nông nghiệ | entered: cal.1960-10-18.vietnam-hanoi |
| XXI, 995 | Chỉ thị của Ban Bí thư số 04-CT/TW ngày 3-11-1960, ra sức phấn đấu để giải quyết thắng lợi vấn đề lương thực | entered: cal.1960-11-03.vietnam-hanoi |
| XXI, 1001 | Thông tri của Ban Bí thư số 09-TT/TW, ngày 7-11-1960 về việc tổng kết cuộc vận động hợp tác hóa nông nghiệp kết hợp hoàn thành cải cách dân  | entered: cal.1960-11-07.vietnam-hanoi |
| XXI, 1004 | Đề cương hướng dẫn nội dung tổng kết cuộc vận động hợp tác hóa nông nghiệp kết hợp hoàn thành cải cách dân chủ ở miền núi | cited: with the circular, cal.1960-11-07.vietnam-hanoi |
| XXI, 1009 | Thông tri của Ban Bí thư số 10-TT/TW ngày 10-11-1960 về việc tuyên truyền thực hiện Luật Hôn nhân và gia đình, chuẩn bị đợt tuyên truyền vận | entered: cal.1960-11-10.vietnam-hanoi |
| XXI, 1012 | Điện của Bộ Chính trị, số 17-NB, ngày 11-11-1960 gửi Xứ uỷ Nam Bộ và Liên khu uỷ V | entered: cal.1960-11-11.vietnam-hanoi |
| XXI, 1017 | Điện của Bộ Chính trị số 20-NB, ngày 12-11-1960, gửi Xứ uỷ Nam Bộ và Liên khu uỷ V 1017 | entered: cal.1960-11-12.vietnam-hanoi |
| XXI, 1023 | Điện của Ban Bí thư số 34/NB, ngày 16-11-1960 gửi Xứ uỷ Nam Bộ | entered: cal.1960-11-16.vietnam-hanoi |
| XXI, 1025 | Điện của Ban Bí thư số 35/NB, ngày 20-11-1960, gửi Xứ uỷ Nam Bộ và Liên khu uỷ V | entered: cal.1960-11-20.vietnam-hanoi |
| XXI, 1029 | Điện của Ban Bí thư số 40/NB, ngày 24-11-1960, gửi Xứ uỷ Nam Bộ | entered: cal.1960-11-24.vietnam-hanoi |
| XXI, 1030 | Chỉ thị của Ban Bí thư số 06-CT/TW, ngày 29-11-1960 về việc mở một đợt tuyên truyền rộng rãi chống Mỹ - Diệm nhân cuộc đảo chính xảy ra ở Sà | entered: cal.1960-11-29.vietnam-hanoi |
| XXI, 1035 | Bài nói của đồng chí Hồ Chí Minh thay mặt đoàn đại biểu Đảng Lao động Việt Nam trong cuộc Hội nghị đại biểu các Đảng Cộng sản và Đảng Công n | cited: cal.1960-11.vietnam-hanoi |
| XXI, 1047 | Điện của Ban Bí thư số 49/NB, ngày 3-12-1960, gửi Xứ uỷ Nam Bộ | entered: cal.1960-12-03.vietnam-hanoi |
| XXI, 1049 | Thông tri của Ban Bí thư số 13-TT/TW, ngày 12-12-1960, về việc tăng cường lãnh đạo công tác kiểm sát | entered: cal.1960-12-12.vietnam-hanoi |
| XXI, 1053 | Chỉ thị của Ban Bí thư số 07-CT/TW, ngày 17-12-1960 về đợt tuyên truyền vận động thi hành Luật Hôn nhân và gia đình vào tháng 1-1961 | entered: cal.1960-12-17.vietnam-hanoi |
| XXI, 1059 | Nghị quyết Hội nghị Xứ uỷ Nam Bộ lần thứ V (tháng 7-1960) | cited: cal.1960-07.vietnam-hanoi |
| XXI, 1095 | Nghị quyết Hội nghị Liên khu uỷ V (mở rộng) ngày 4-5-1960 | cited: cal.1960-05-04.vietnam-hanoi |
| XXI, 1128 | Nghị quyết của Khu uỷ Việt Bắc số 49/VP-KU ngày 69-1960 về kế hoạch củng cố và phát triển Đảng trong cuộc vận động hợp tác hóa nông nghiệp k | passed over: a provincial matter (the Việt Bắc zone committee) |
| XXII, 1 | CT 08-CT/TW, 3-1-1961, công tác văn hoá trong quần chúng | entered: cal.1961-01-03.vietnam-hanoi |
| XXII, 13 | HNTƯ 3 (30-12-1960 to 5-1-1961), nghị quyết kế hoạch nhà nước 1961 | entered: cal.1960-12-30.vietnam-hanoi |
| XXII, 52 | Lê Duẩn report on the Moscow conference, to the 3rd plenum | entered: cal.1961-01-05.vietnam-hanoi |
| XXII, 104 | HNTƯ 3 resolution (5-7 Jan. 1961) on the Moscow conference | cited: with the report, cal.1961-01-05.vietnam-hanoi |
| XXII, 115 | HNTƯ 3 resolution 06-NQ/TW, 23-1-1961, phân công | entered: cal.1961-01-23.vietnam-hanoi |
| XXII, 118 | Thông cáo of the CC on the 3rd plenum | cited: the communiqué: a Check on cal.1960-12-30.vietnam-hanoi |
| XXII, 123 | BBT NQ 29-NQ/TW, 11-1-1961, Đảng đoàn phụ nữ TƯ | entered: cal.1961-01-11.vietnam-hanoi |
| XXII, 125 | BBT TT 14-TT/TW, 13-1-1961, army farm party committees to local | entered: cal.1961-01-13.vietnam-hanoi |
| XXII, 127 | BBT TT 15-TT/TW, 13-1-1961, chỉ tiêu kinh tế kỹ thuật | entered: cal.1961-01-13.vietnam-hanoi-2 |
| XXII, 130 | BBT CT 9-CT/TW, 14-1-1961, tuyên truyền kế hoạch 1961 | entered: cal.1961-01-14.vietnam-hanoi |
| XXII, 138 | BBT TT 17-TT/TW, 16-1-1961, liên hiệp HTX thủ công | entered: cal.1961-01-16.vietnam-hanoi |
| XXII, 140 | BBT NQ 5-NQ/TW, 19-1-1961, báo chí 1961 | entered: cal.1961-01-19.vietnam-hanoi |
| XXII, 149 | BCT CT 24-1-1961, cách mạng miền Nam | cited: cal.1961-01-24.vietnam-hanoi |
| XXII, 170 | BBT NQ 7-NQ/TW, 26-1-1961, thi đua yêu nước | entered: cal.1961-01-26.vietnam-hanoi |
| XXII, 180 | BBT CT 10-CT/TW, 27-1-1961, cán bộ HTX nông nghiệp | entered: cal.1961-01-27.vietnam-hanoi |
| XXII, 184 | BCT NQ 11-NQ/TW, 8-2-1961, quản lý xí nghiệp | entered: cal.1961-02-08.vietnam-hanoi |
| XXII, 196 | BBT CT 12-CT/TW, 18-2-1961, xí nghiệp công tư hợp doanh | entered: cal.1961-02-18.vietnam-hanoi |
| XXII, 205 | BCT NQ 12-NQ/TW, 25-2-1961, chỉnh huấn mùa xuân 1961 | entered: cal.1961-02-25.vietnam-hanoi |
| XXII, 215 | BCT NQ 13-NQ/TW, 27-2-1961, hợp tác hoá 1961 | entered: cal.1961-02-27.vietnam-hanoi |
| XXII, 234 | BBT CT 13-CT/TW, 1-3-1961, chống phản cách mạng | entered: cal.1961-03-01.vietnam-hanoi |
| XXII, 242 | BBT CT 14-CT/TW, 10-3-1961, dân quân tự vệ | entered: cal.1961-03-10.vietnam-hanoi |
| XXII, 248 | BBT CT 15-CT/TW, 10-3-1961, lâm nghiệp | entered: cal.1961-03-10.vietnam-hanoi-2 |
| XXII, 254 | BBT CT 16-CT/TW, 13-3-1961, Đảng trong công an vũ trang | entered: cal.1961-03-13.vietnam-hanoi |
| XXII, 263 | TƯ điện mật 28/ĐM, 14-3-1961, Trung ương Cục miền Nam | cited: cal.1961-03-14.vietnam-hanoi |
| XXII, 266 | BBT TT 20-TT/TW, 15-3-1961, công tác mặt trận | entered: cal.1961-03-15.vietnam-hanoi |
| XXII, 269 | BBT TT 21-TT/TW, 18-3-1961, Đại hội MTTQ lần hai | entered: cal.1961-03-18.vietnam-hanoi |
| XXII, 271 | BBT NQ 15-NQ/TW, 24-3-1961, Khu uỷ Hồng Quảng | passed over: a provincial matter (the Hồng Quảng zone committee; the Secretariat of Jan. 7, 1961) |
| XXII, 276 | BBT NQ 16-NQ/TW, 31-3-1961, tổ chức Đảng ở ngoài nước | entered: cal.1961-03-31.vietnam-hanoi |
| XXII, 282 | BBT TT 22-TT/TW, 31-3-1961, chương I Điều lệ | entered: cal.1961-03-31.vietnam-hanoi-2 |
| XXII, 291 | BBT TT 23-TT/TW, 5-4-1961, phổ biến Điều lệ | entered: cal.1961-04-05.vietnam-hanoi |
| XXII, 294 | BBT TT 24-TT/TW, 6-4-1961, bầu cử HĐND huyện xã | entered: cal.1961-04-06.vietnam-hanoi |
| XXII, 297 | BBT TT 25-TT/TW, 6-4-1961, bầu thẩm phán | entered: cal.1961-04-06.vietnam-hanoi-2 |
| XXII, 300 | BBT CT 17-CT/TW, 11-4-1961, lương thực | entered: cal.1961-04-11.vietnam-hanoi |
| XXII, 305 | BBT NQ 389-NQNS/TW, 14-4-1961, Đảng đoàn Tổng Công đoàn | entered: cal.1961-04-14.vietnam-hanoi |
| XXII, 306 | BBT TT 27-TT/TW, 14-4-1961, bầu BCH huyện | entered: cal.1961-04-14.vietnam-hanoi-2 |
| XXII, 308 | BBT CT 18-CT/TW, 28-4-1961, thuỷ lợi đê điều | entered: cal.1961-04-28.vietnam-hanoi |
| XXII, 313 | BCT NQ 18-NQ/TW, 8-5-1961, chính sách lương thực | entered: cal.1961-05-08.vietnam-hanoi |
| XXII, 323 | BBT CT 19-CT/TW, 11-5-1961, chống Mỹ đưa quân vào miền Nam | entered: cal.1961-05-11.vietnam-hanoi |
| XXII, 327 | BBT NQ 19-NQ/TW, 1-6-1961, Liên chi | entered: cal.1961-06-01.vietnam-hanoi |
| XXII, 332 | BBT NQ 20-NQ/TW, 1-6-1961, Ban Thống nhất | entered: cal.1961-03-22.vietnam-hanoi |
| XXII, 337 | BBT CT 20-CT/TW, 26-6-1961, biệt kích gián điệp | entered: cal.1961-06-26.vietnam-hanoi |
| XXII, 345 | HNTƯ 4 NQ 22-NQ/TW, 30-6-1961, lãnh đạo của Trung ương | entered: cal.1961-06-30.vietnam-hanoi |
| XXII, 365 | BBT CT 21-CT/TW, 4-7-1961, đấu tranh 20-7 | cited: cal.1961-07-04.vietnam-hanoi |
| XXII, 371 | BBT NQ 21-NQ/TW, 5-7-1961, thủ công nghiệp | entered: cal.1961-07-05.vietnam-hanoi |
| XXII, 389 | BBT CT 23-CT/TW, 7-7-1961, lương thực vụ chiêm | entered: cal.1961-07-07.vietnam-hanoi |
| XXII, 395 | BBT CT 24-CT/TW, 12-7-1961, giảng viên lý luận | entered: cal.1961-07-12.vietnam-hanoi |
| XXII, 399 | BBT CT 25-CT/TW, 24-7-1961, hợp lý hoá sản xuất | entered: cal.1961-07-24.vietnam-hanoi |
| XXII, 404 | BBT QĐ 24-QĐ/TW, 25-7-1961, chế độ cán bộ miền Tây | entered: cal.1961-07-25.vietnam-hanoi |
| XXII, 410 | Hồ Chí Minh at the 5th plenum | cited: cal.1961-07.vietnam-hanoi-3 |
| XXII, 413 | HNTƯ 5 NQ 26-NQ/TW, 7-1961, nông nghiệp | cited: cal.1961-07.vietnam-hanoi-3 |
| XXII, 459 | Thông báo on the 5th plenum | cited: cal.1961-07.vietnam-hanoi-3 |
| XXII, 461 | BBT điện mật 168, 10-8-1961, to XUNB on the first COSVN conference | entered: cal.1961-08-10.vietnam-hanoi |
| XXII, 464 | BBT TT 35-TT/TW, 16-8-1961, kỷ niệm CM tháng Tám | passed over: commemoration (the August Revolution, Sept. 2) |
| XXII, 469 | BBT TT 36-TT/TW, 21-8-1961, thảo luận NQ HNTƯ 5 | entered: cal.1961-08-21.vietnam-hanoi |
| XXII, 472 | BBT CT 26-CT/TW, 15-9-1961, giúp đỡ cách mạng miền Nam | entered: cal.1961-09-15.vietnam-hanoi |
| XXII, 475 | TB 10-TB/VPTW, 20-9-1961, Politburo of 8-9-1961 on cooperativization in the mountains | entered: cal.1961-09-08.vietnam-hanoi |
| XXII, 480 | BBT CT 27-CT/TW, 4-10-1961, tập trung cải tạo | entered: cal.1961-10-04.vietnam-hanoi |
| XXII, 484 | BBT TT 45-TT/TW, 31-10-1961, chống can thiệp Mỹ | cited: cal.1961-10-31.vietnam-hanoi |
| XXII, 490 | BBT CT 28-CT/TW, 31-10-1961, kỷ niệm CM tháng Mười | passed over: commemoration (the October Revolution) |
| XXII, 496 | BBT CT 29-CT/TW, 31-10-1961, lương thực vụ mùa | entered: cal.1961-10-31.vietnam-hanoi-2 |
| XXII, 503 | BBT NQ 27-NQ/TW, 3-11-1961, Khu tự trị Việt Bắc | passed over: a provincial matter (the Việt Bắc autonomous zones powers) |
| XXII, 507 | BBT NQ 28-NQ/TW, 3-11-1961, giải thể Đảng bộ trường phổ thông Hà Nội | passed over: a local matter (the Hanoi schools Party committee dissolved) |
| XXII, 508 | BBT CT 30-CT/TW, 9-11-1961, tiền tệ tín dụng | entered: cal.1961-11-09.vietnam-hanoi; and cal.1961-07-19.vietnam-hanoi (the Politburo's resolution of July 19, 1961, it cites) |
| XXII, 512 | BBT CT 31-CT/TW, 9-11-1961, tài chính mậu dịch ngân hàng | entered: cal.1961-11-09.vietnam-hanoi-2 |
| XXII, 530 | BCT NQ 30-NQ/TW, 13-11-1961, tổ chức đảng trong quân đội | entered: cal.1961-11-13.vietnam-hanoi |
| XXII, 536 | BBT CT 32-CT/TW, 13-11-1961, bảo vệ trị an | entered: cal.1961-11-13.vietnam-hanoi-2 |
| XXII, 540 | TB HN BBT 13-TB/HN, 17-11-1961, Đại hội liên hiệp Thanh niên | entered: cal.1961-11-06.vietnam-hanoi |
| XXII, 543 | BBT CT 33-CT/TW, 22-11-1961, hợp nhất HTX | entered: cal.1961-11-22.vietnam-hanoi |
| XXII, 550 | TB HN BBT 14-TB/TW, 24-11-1961, đãi ngộ cán bộ xã | entered: cal.1961-07-03.vietnam-hanoi |
| XXII, 555 | BCT NQ 31-NQ/TW, 24-11-1961, Hải Phòng | entered: cal.1961-11-24.vietnam-hanoi |
| XXII, 561 | BBT điện 525, 25-11-1961, to COSVN on reporting the enemy | entered: cal.1961-11-25.vietnam-hanoi |
| XXII, 568 | Lê Duẩn report on CPSU 22nd Congress to 6th plenum | entered: cal.1961-11-30.vietnam-hanoi |
| XXII, 603 | HNTƯ 6 kết luận (30-11 to 2-12-1961) | cited: with the report, cal.1961-11-30.vietnam-hanoi |
| XXII, 605 | Thông cáo on the 6th plenum | cited: with the report, cal.1961-11-30.vietnam-hanoi |
| XXII, 609 | BBT CT 34-CT/TW, 11-12-1961, lương thực | entered: cal.1961-12-11.vietnam-hanoi |
| XXII, 616 | BBT CT 35-CT/TW, 22-12-1961, chống Mỹ đưa vũ khí | entered: cal.1961-12-22.vietnam-hanoi |
| XXII, 621 | BCT NQ 32-NQ/TW, 28-12-1961, Vinh | entered: cal.1961-12-28.vietnam-hanoi |
| XXII, 628 | BBT CT 36-CT/TW, 31-12-1961, đông xuân | entered: cal.1961-12-31.vietnam-hanoi |
| XXII, 633 | TƯC CT 16-6-1961, dân vận mặt trận | entered: cal.1961-06-16.vietnam-hanoi |
| XXII, 641 | TƯC CT 4-8-1961, chống gián điệp | entered: cal.1961-08-04.vietnam-hanoi |
| XXII, 653 | TƯC CT số 4, 27-11-1961, đổi tên Đảng | cited: cal.1961-11-27.vietnam-hanoi |
| XXII, 656 | NQ Hội nghị R lần thứ I (mở rộng) | cited: cal.1961-10.vietnam |
| XXII, 731 | Khu uỷ V NQ 62, 2-1961, binh vận | entered: cal.1961-02.vietnam-hanoi |
| XXII, 754 | Khu uỷ Việt Bắc 02-NQ/VB, 3-4-1961, chỉnh huấn | passed over: a provincial matter (the Việt Bắc zone committee) |
| XXII, 759 | Khu uỷ Tây Bắc 11-NQ/TB, 14-11-1961, nông lâm nghiệp | passed over: a provincial matter (the Tây Bắc zone committee) |

Read: every document's opening and close, and the operative sections (the numbered heads) of each; the cables to the South, the plenums' resolutions, the Politburo's instruction of Jan. 24, 1961, COSVN's instruction no. 4 and the cables of November 1960 in full. Counts: vol. 21, 112 documents (107 in the span): 85 entered (87 entries: the Politburo's session of Apr. 21–22 and the eighteenth plenum entered beside the documents that record them), 11 cited (on entries the calendar held, or with the new entry they belong to), 7 of the Congress's documents not read through, 9 passed over; vol. 22, 85 documents: 65 entered (66 entries, with the Politburo's resolution of July 19 that the Secretariat cites), 13 cited, 7 passed over.

### Where batch 12 stopped

Both volumes done, to the last page of each table of contents (XXI, 1128; XXII, 759). Not done: the Third Congress's long reports as days of their own (above); the regional committees of Việt Bắc and Tây Bắc (passed over); no witnesses file (the volume is the record itself). Stopped cleanly, the patch checked to 0 errors (85 warnings, all of the kinds above).


## 1962–64 (batch 12, the DRV's records; vols. 23, 24 and 25)

Reader: batch 12, share "b12-vkd-b", Nov. 12, 2026 (a restart of a reader stopped by an interruption; its downloads and converted text taken over). Patch: `inbox/2026-11-12-b12-drv-1962-64.yaml` (patch name `2026-11-12-b12-drv-1962-64`), 166 ops: 147 new entries (claimed in `inbox/new-entries.tsv`), 16 edits of entries the calendar held (each the plain "To check: ... *Văn kiện Đảng toàn tập*, 2N:..." item taken out and the card cited in the run of works read, with its src row), 2 cites, 1 check. No witnesses file, no by-work edges. `./bib patch-check`: 0 errors, 64 warnings (same-day "one event?" and "a duplicate of" at the merge for separate documents of one day, and "sets only n, src" for the edits, which also take text out).

### The form

As the 1960–61 section: `[[w.van-kien-dang-toan]], XXV, 11–25`, the src rows `w.van-kien-dang-toan XXV, 11–25`; each new note opens with the document's own heading in italics (the "về ..." title from the volume) and its signer. Made public: XXIII, 2002 (title page "Hà Nội - 2002", colophon "In xong và nộp lưu chiểu tháng 12 năm 2002"); XXIV, 2003 (title page "Hà Nội - 2003", introduction January 2003); XXV, 2003 (title page "Hà Nội - 2002", but its introduction dated January 2003: 2003 used). Not on the communiqués, the public speeches or the NLF congress.

### The copies

- Vol. 23 (1962): Drive `1upRXoizdfxWBY_emRkOTegqlS_VYLPPy`, 506 PDF pages, letter, two-up, PDF 1.4 (iTextSharp 5.1.1). Book pp. V–VI, 1–976; contents at 977–89 (its page numbers run off from the text's in places: e.g. Lê Duẩn's letter of July 18 listed at 700, printed at 705; the text's folios used); appendix 851–976. The contents list a Secretariat circular no. 62-TT/TW of Jan. 30, 1962 (cadres in the countryside at Tết) that the copy does not print.
- Vol. 24 (1963): Drive `172mXcdm2w51tR83qCTMmZoAxsWC8KF7M`, 485 PDF pages, letter, two-up, PDF 1.4 (Ghostscript 8.15). Book pp. 1–910 and an appendix. **The copy wants book pp. 777–862** (PDF 388R, p. 776, is followed by PDF 389L, p. 863): what stands there was not read; by the intervening pages, the Ninth Plenum's papers after the communiqué (Lê Duẩn's speech to the plenum, printed in *Học Tập*, February 1964, is likely among them). The appendix's folios print only "V"/"VI": its pages here counted on from 910 (the first appendix page 912). No contents and no colophon in the copy.
- Vol. 25 (1964): Drive `1OgpxUm0O5polcWekBlzIqDJP7fO5AcHF`, 399 PDF pages, letter, two-up, PDF 1.4 (Ghostscript 8.15). Book pp. 1–793; appendix 699–793. No contents and no colophon in the copy; the introduction counts 48 documents, 45 and 3 in the appendix.
- Downloaded by the first reader into the scratchpad (`books/b12-vkd-b/`); converted with `tools/vn/vkd2txt.py` and split by half-page; deleted when done.

### Pages

Every cite gives the book's page from the running heads and folios of the text layer (not computed). Asselin's pinpoints into these volumes differ from the copy's in places (XXV, 74-CT/TW at 43–59 by Asselin, 42–49 here; the Ninth Plenum's resolutions at XXIV, 716–800 and 811–62 by Asselin, 691–767 and 863–908 here): another printing, or a slip; the copy's pages are cited, the To check items of Asselin's pinpoints taken out.

### The rules used

The brief and the 1960–61 reader's rulings: an entry a document of the Politburo, the Secretariat, the Central Committee and its plenums, and the directives to the South; a meeting that a notice records (the Secretariat's "Thông báo ... về cuộc họp") entered on the meeting's day, the notice cited there; two documents of one body on one day in one entry where they read as one session (the Politburo of Jan. 20, 1962 and of Apr. 26, 1962; the Secretariat's party groups of Sept. 5, 1963; the Politburo of Jan. 9, 1964), else each its own. Passed over (R18): commemorations, provincial and local matters. COSVN's and the interzones' resolutions (the appendices) entered under `vietnam-hanoi`; the NLF's first congress under `vietnam`, `also: vietnam-hanoi`. Visibility: `polity:drv` on every entry, with `polity:us`, `ussr`, `prc`, `rvn`, `dprk`, `th` where `c` names the country outright.

### Doubtful, for the merger

- Same-day entries: separate documents (patch-check warns "one event?"/"a duplicate of"): at the merge `./bib resolve ID --take keep`. Beside entries the calendar held: cal.1964-08-07.vietnam-hanoi-2 (Hồ Chí Minh's speech to the air-defense and naval units, beside the Politburo's instruction no. 81), cal.1964-12-26.vietnam-hanoi-2 (the Politburo's commissions for the Fourth Congress, beside the tenth plenum), cal.1964-12.vietnam-hanoi-2 (Hồ Chí Minh at the army's twentieth anniversary, beside the Cambodian foreign minister), cal.1963-07.vietnam-hanoi-2 (COSVN on the hamlets, beside *Học Tập* no. 7), cal.1963-10.vietnam-hanoi-3 (Interzone VI, beside *Nhân Dân* and Nguyễn Chí Thanh).
- The Ninth Plenum's days: the volume's editors have it sit Nov. 22–Dec. 7, 1963 (XXIV, 5); Asselin has it still sitting Dec. 25 (a Check on cal.1963-12.vietnam and on cal.1963-12-25.vietnam-hanoi).
- The eighth plenum: the editors have it sit Mar. 26–Apr. 8, 1963 (XXIV, 481 n.), the communiqué dated April; the entry, cal.1963-03-26.vietnam-hanoi, is "Mar. 26–27" (by the reports): a Check.
- The seventh plenum, Mar. 26–Apr. 16, 1962 (the communiqué; the contents say to Apr. 14): one entry, on its last day and Hồ Chí Minh's speech, cal.1962-04-16.vietnam-hanoi.
- cal.1963-03-08.vietnam-hanoi: the Politburo's resolution no. 74 cites its session of Mar. 8, no. 77 its meeting of Mar. 9: one entry "Mar. 8–9", a Check whether one session.
- cal.1962-05-05.vietnam-hanoi: COSVN's minutes of its conference of Apr. 20–May 5, 1962 and its resolution on military tasks of May 1962, in one entry; whether the second is that conference's, a Check.
- cal.1963-11-27.vietnam-hanoi: the Secretariat's rules for the cadres sent to "miền Tây" at "Bạn"'s request, entered in their words, `also: laos`; the place not named (as cal.1961-07-25.vietnam-hanoi).
- cal.1962-12-06.vietnam: the volume prints the Politburo's resolution of Dec. 6–10, 1962 in part ("Phần này không trích vào đây", XXIII, 838): the passages on the Center's leadership and the North's part are left out; the entry's unit B (units sent south, the trail) not borne.
- cal.1964-12-26.vietnam-hanoi: the report to the tenth plenum (XXV, 293–511) names no speaker; Lê Duẩn's speech (514) says Phạm Hùng reported the Politburo's view of the amendments.
- Hoàng Văn Thái, secretary of the sports committee's party group (cal.1963-08-19.vietnam-hanoi): named, not tagged; whether he is the general of `vn.who.hoang-van-thai` the page does not say.
- The x. witnesses for these documents (`x.1964-01-17.nghi-quyet-92-nq-tw` and the like, `read: false`, `open: not held`) are now read in this print: not changed here (no witnesses file).

### Persons named with no name entry (named in `c` and "Names:", not tagged)

Đặng Tính, Hoàng Quốc Việt, Kim Chang-bong, Nguyễn Duy Trinh, Nguyễn Lương Bằng, Hoàng Văn Hoan, Phạm Văn Bạch, Chu Văn Tấn, Nguyễn Văn Hưởng, Tôn Quang Phiệt, Trần Quốc Hoàn, Nguyễn Văn Vịnh, Nguyễn Khang, Lê Trọng Nghĩa, Nguyễn Văn Trân, Lê Văn Lương, Tố Hữu, Hoàng Anh, Phạm Hùng, Nguyễn Khai, Hoàng Văn Thái (above), Nguyễn Văn Quạn, Ngô Luân, Hà Huy Giáp, Cù Huy Cận, Nguyễn Đức Quỳ, Võ Hồng Cương, Đặng Khánh Côn, Phạm Hồng, Nguyễn Đình Thi, Hoài Thanh, Nông Quốc Chấn, Bảo Định Giang, Đỗ Nhuận, Stalin. Signers named only in the notes: Lê Thanh Nghị, Phạm Chung, Minh Châu.

### The documents, one by one

Every document of the three volumes, in the volume's order, with its first page and the ruling (vol. 24's pp. 777–862 wanting). Read: each document's opening and close and its operative sections; the Ninth Plenum's resolution on the South, the Politburo's resolutions on the South of February and December 1962, Lê Duẩn's letter of July 18, 1962, the letter to the CPSU, the Secretariat's circular on international relations of Aug. 27, 1963, and the Politburo's instruction no. 81 of Aug. 7, 1964 at length; the plenums' long reports and resolutions on the economy, and the appendices, by their headings and operative sections.


#### Vol. XXV (1964)

| Page | Document (the volume's heading) | Ruling |
|---|---|---|
| XXV, 1 | Thông tri Của Ban Bí thư Số 133-TT/TW, ngày 8 tháng 1 năm 1964 | entered: cal.1964-01-08.vietnam-hanoi |
| XXV, 7 | nghị quyết của Bộ Chính trị Số 90-NQ/TW, ngày 9 tháng 1 năm 1964 | entered: cal.1964-01-09.vietnam-hanoi |
| XXV, 9 | Quyết định của Bộ Chính trị Số 91-NQ/TW, ngày 9 tháng 1 năm 1964 | entered with cal.1964-01-09.vietnam-hanoi (the same day) |
| XXV, 11 | Nghị quyết của Bộ Chính trị Số 92-NQ/TW, ngày 17 tháng 1 năm 1964 | cited on cal.1964-01-17.vietnam-hanoi (edit) |
| XXV, 26 | Nghị quyết của Ban Bí thư Số 93-NQNS/TW, ngày 17 tháng 1 năm 1964 | passed over: a local matter (the Sầm Sơn town committee) |
| XXV, 27 | Chỉ thị của Ban Bí thư Số 73-CT/TW, ngày 24 tháng 1 năm 1964 | cited on cal.1964-01-24.vietnam-hanoi (edit) |
| XXV, 42 | Chỉ thị của bộ chính trị Số 74-CT/TW, ngày 27 tháng 1 năm 1964 | cited on cal.1964-01-27.vietnam-hanoi (edit) |
| XXV, 50 | Thông báo của Bộ Chính trị Số 50-TB/TW, ngày 1 tháng 2 năm 1964 | entered: cal.1964-02-01.vietnam-hanoi |
| XXV, 52 | Nghị quyết của Bộ Chính trị Số 95-NQ/TW, ngày 4 tháng 2 năm 1964 | cited on cal.1964-02-04.vietnam-hanoi (edit) |
| XXV, 70 | Chỉ thị của Ban Bí thư Số 75-CT/TW, ngày 3 tháng 3 năm 1964 | cited on cal.1964-03-03.vietnam-hanoi (edit) |
| XXV, 73 | Chỉ thị của Bộ Chính trị Số 76-CT/TW, ngày 5 tháng 3 năm 1964 | entered: cal.1964-03-05.vietnam-hanoi |
| XXV, 80 | Thông tri của Ban Bí thư Số 137-TT/TW, ngày 6 tháng 3 năm 1964 | entered: cal.1964-03-06.vietnam-hanoi |
| XXV, 87 | Thông tri của Ban Bí thư Số 138-TT/TW, ngày 14 tháng 3 năm 1964 | entered: cal.1964-03-14.vietnam-hanoi |
| XXV, 90 | Báo cáo của Chủ tịch Hồ Chí Minh tại Hội nghị Chính trị đặc biệt, 27–28-3-1964 | cited on cal.1964-03-27.vietnam (cite) |
| XXV, 109 | Nghị quyết của Ban Bí thư Số 98-NQ/TW, ngày 31 tháng 3 năm 1964 | passed over: a local matter (the Nam Định textile combine's Party organization) |
| XXV, 112 | Thông tri của Ban Bí thư Số 140-TT/TW, ngày 4 tháng 4 năm 1964 | entered: cal.1964-04-04.vietnam-hanoi |
| XXV, 116 | Chỉ thị của Ban Bí thư Số 77-CT/TW, ngày 18 tháng 4 năm 1964 | cited on cal.1964-04-18.vietnam-hanoi (edit) |
| XXV, 127 | Chỉ thị của Ban Bí thư Số 78-CT/TW, ngày 23 tháng 4 năm 1964 | passed over: commemorations (three anniversaries, May 1964) |
| XXV, 133 | Nghị quyết của Ban Bí thư Số 969-NQNS/TW, ngày 8 tháng 5 năm 1964 | entered: cal.1964-05-08.vietnam-hanoi |
| XXV, 135 | Nghị quyết của Ban Bí thư Số 99-NQ/TW, ngày 13 tháng 5 năm 1964 | entered: cal.1964-05-13.vietnam-hanoi |
| XXV, 137 | Nghị quyết của Bộ Chính trị Số 100-NQ/TW, ngày 15 tháng 5 năm 1964 | entered: cal.1964-05-15.vietnam-hanoi |
| XXV, 139 | Thông tri của Ban Bí thư Số 141-TT/TW, ngày 25 tháng 5 năm 1964 | entered: cal.1964-05-25.vietnam-hanoi |
| XXV, 149 | Chỉ thị của Ban Bí thư Số 79-CT/TW, ngày 3 tháng 6 năm 1964 | entered: cal.1964-06-03.vietnam-hanoi |
| XXV, 154 | Nghị quyết của Ban Bí thư Số 983-NQNS/TW, ngày 23 tháng 6 năm 1964 | entered: cal.1964-06-23.vietnam-hanoi |
| XXV, 156 | Thông tri của Ban Bí thư Số 142-TT/TW, ngày 24 tháng 6 năm 1964 | entered: cal.1964-06-24.vietnam-hanoi |
| XXV, 160 | Chỉ thị của Ban Bí thư Số 80-CT/TW, ngày 10 tháng 7 năm 1964 | entered: cal.1964-07-10.vietnam-hanoi |
| XXV, 168 | Nghị quyết của Ban Bí thư Số 103-NQ/TW, ngày 23 tháng 7 năm 1964 | entered: cal.1964-07-23.vietnam-hanoi |
| XXV, 184 | Chỉ thị của Bộ Chính trị Số 81-CT/TW, ngày 7 tháng 8 năm 1964 | cited on cal.1964-08-07.vietnam-hanoi (edit) |
| XXV, 201 | Bài nói của Chủ tịch Hồ Chí Minh tuyên dương các đơn vị phòng không và hải quân, 7-8-1964 | entered: cal.1964-08-07.vietnam-hanoi-2 |
| XXV, 203 | Chỉ thị của Ban Bí thư Số 82-CT/TW, ngày 15 tháng 8 năm 1964 | passed over: commemoration (the August Revolution, Sept. 2) |
| XXV, 209 | Chỉ thị của Ban Bí thư Số 83-CT/TW, ngày 21 tháng 8 năm 1964 | entered: cal.1964-08-21.vietnam-hanoi |
| XXV, 213 | Chỉ thị của Ban Bí thư Số 84-CT/TW, ngày 3 tháng 9 năm 1964 | entered: cal.1964-09-03.vietnam-hanoi |
| XXV, 223 | Thông tri của Ban Bí thư Số 147-TT/TW, ngày 12 tháng 9 năm 1964 | passed over: commemoration (the PRC at 15) |
| XXV, 227 | Thông tri của Ban Bí thư Số 148-TT/TW, ngày 12 tháng 9 năm 1964 | passed over: commemoration (the GDR at 15) |
| XXV, 230 | Nghị quyết của bộ chính trị Số 105-NQ/TW, ngày 17 tháng 9 năm 1964 | entered: cal.1964-09-17.vietnam-hanoi |
| XXV, 266 | Thông tri của Ban Bí thư Số 150-TT/TW, ngày 25 tháng 9 năm 1964 | entered: cal.1964-09-25.vietnam-hanoi |
| XXV, 270 | Chỉ thị của Ban Bí thư Số 86-CT/TW, ngày 7 tháng 10 năm 1964 | entered: cal.1964-10-07.vietnam-hanoi |
| XXV, 273 | Thông tri của Ban Bí thư Số 152-TT/TW, ngày 26 tháng 10 năm 1964 | entered: cal.1964-10-26.vietnam-hanoi |
| XXV, 276 | Thông tri của Ban Bí thư Số 153-TT/TW, ngày 26 tháng 11 năm 1964 | entered: cal.1964-11-26.vietnam-hanoi |
| XXV, 279 | Đề cương hướng dẫn Một số vấn đề cần chú ý trong việc kiểm tra, đánh giá, tổng kết cuộc | entered with cal.1964-11-26.vietnam-hanoi (its outline) |
| XXV, 285 | Chỉ thị Của Ban Bí thư Số 87-CT/TW, ngày 11 tháng 12 năm 1964 | passed over: commemorations (Dec. 19, 20 and 22) |
| XXV, 288 | Bài nói của Chủ tịch Hồ Chí Minh, chiêu đãi mừng Quân đội 20 tuổi, 12-1964 | entered: cal.1964-12.vietnam-hanoi-2 |
| XXV, 290 | Nghị quyết của Bộ Chính trị Số 107-NQ/TW, ngày 26 tháng 12 năm 1964 | entered: cal.1964-12-26.vietnam-hanoi-2 |
| XXV, 293 | Báo cáo tại Hội nghị TƯ lần thứ 10, thương nghiệp và giá cả, 12-1964 | cited on cal.1964-12-26.vietnam-hanoi (edit) |
| XXV, 514 | Bài nói của Lê Duẩn tại Hội nghị TƯ lần thứ 10, 26-12-1964 | cited on cal.1964-12-26.vietnam-hanoi (edit) |
| XXV, 583 | NQ Hội nghị TƯ lần thứ 10, 12-1964 | cited on cal.1964-12-26.vietnam-hanoi (edit) |
| XXV, 682 | Thông cáo Hội nghị TƯ lần thứ 10 | cited on cal.1964-12-26.vietnam-hanoi (edit) |
| XXV, 701 | NQ Hội nghị TƯ Cục lần thứ hai 2/NQ, 3-1964 (phụ lục) | entered: cal.1964-03.vietnam-hanoi |
| XXV, 780 | NQ Ban Thường vụ Khu uỷ Việt Bắc 97-NQ/KU, 28-10-1964 (phụ lục) | passed over: a provincial matter (the Việt Bắc zone committee) |
| XXV, 785 | CT Ban thường vụ khu uỷ Tây Bắc 61-CT/TB, 10-3-1964 (phụ lục) | passed over: a provincial matter (the Tây Bắc zone committee) |

#### Vol. XXIV (1963)

| Page | Document (the volume's heading) | Ruling |
|---|---|---|
| XXIV, 8 | Nghị quyết của bộ chính trị Số 65-NQ/TW, ngày 2 tháng 1 năm 1963 | entered: cal.1963-01-02.vietnam-hanoi |
| XXIV, 12 | Nghị quyết của Bộ Chính trị Số 66-NQ/TW, ngày 5 tháng 1 năm 1963 | entered: cal.1963-01-05.vietnam-hanoi |
| XXIV, 33 | Nghị quyết của Ban Bí thư Số 688-NQ/TW, ngày 7 tháng 1 năm 1963 | passed over: a provincial matter (Bắc Ninh and Bắc Giang committees merged into Hà Bắc) |
| XXIV, 35 | Nghị quyết của Ban Bí thư Số 689-NQ/TW, ngày 7 tháng 1 năm 1963 | passed over: a provincial matter (two provincial Party organizations merged) |
| XXIV, 37 | Thông tri của Ban Bí thư Số 107-TT/TW, ngày 9 tháng 1 năm 1963 | entered: cal.1963-01-09.vietnam-hanoi |
| XXIV, 40 | Nghị quyết của Bộ Chính trị Số 67-NQ/TW, ngày 12 tháng 1 năm 1963 | entered: cal.1963-01-12.vietnam-hanoi |
| XXIV, 50 | Thông báo của Ban Bí thư Số 42-TB/TW, ngày 15 tháng 1 năm 1963 | entered: cal.1963-01-02.vietnam-hanoi-2 |
| XXIV, 58 | Chỉ thị của Ban Bí thư Số 57-CT/TW, ngày 16 tháng 1 năm 1963 | entered: cal.1963-01-16.vietnam-hanoi |
| XXIV, 65 | Thông báo của Ban Bí thư Số 43-TB/TW, ngày 16 tháng 1 năm 1963 | passed over: a provincial matter (Phú Thọ) |
| XXIV, 73 | Điện của Ban Bí thư Gửi trung ương cục miền nam | cited on cal.1963-01-24.vietnam-hanoi (edit) |
| XXIV, 75 | Chỉ thị của Ban Bí thư Số 58-CT/TW, ngày 31 tháng 1 năm 1963 | entered: cal.1963-01-31.vietnam-hanoi |
| XXIV, 81 | Nghị quyết của Bộ Chính trị Số 68-NQ/TW, ngày 1 tháng 2 năm 1963 | entered: cal.1963-02-01.vietnam-hanoi |
| XXIV, 87 | Nghị quyết của Ban Bí thư Số 69-NQ/TW, ngày 11 tháng 2 năm 1963 | entered: cal.1963-02-11.vietnam-hanoi |
| XXIV, 98 | Chỉ thị của ban bí thư Số 59-CT/TW, ngày 16 tháng 2 năm 1963 | entered: cal.1963-02-16.vietnam-hanoi |
| XXIV, 101 | Nghị quyết của Bộ Chính trị Số 70-NQ/TW, ngày 19 tháng 2 năm 1963 | entered: cal.1963-02-19.vietnam-hanoi |
| XXIV, 118 | Nghị quyết của Bộ chính trị Số 71-NQ/TW, ngày 23 tháng 2 năm 1963 | entered: cal.1963-02-23.vietnam-hanoi |
| XXIV, 156 | Chỉ thị của Ban Bí thư Số 60-CT/TW, ngày 25 tháng 2 năm 1963 | cited on cal.1963-02-25.vietnam-hanoi (edit) |
| XXIV, 170 | Thông báo của Ban Bí thư Số 46-TB/TW, ngày 27 tháng 2 năm 1963 | entered: cal.1963-02-11.vietnam-hanoi-2 |
| XXIV, 174 | Thông tri của Ban Bí thư Số 112-TT/TW, ngày 28 tháng 2 năm 1963 | cited on cal.1963-02-28.vietnam-hanoi (edit) |
| XXIV, 178 | Nghị quyết của Bộ Chính trị Số 72-NQ/TW, ngày 2 tháng 3 năm 1963 | entered: cal.1963-03-02.vietnam-hanoi |
| XXIV, 180 | Nghị quyết của Bộ Chính trị Số 73-NQ/TW, ngày 7 tháng 3 năm 1963 | entered: cal.1963-03-07.vietnam-hanoi |
| XXIV, 190 | Nghị quyết của Bộ Chính trị Số 74-NQ/TW, ngày 14 tháng 3 năm 1963 | entered: cal.1963-03-08.vietnam-hanoi |
| XXIV, 195 | Chỉ thị của Ban Bí thư Số 61-CT/TW, ngày 29 tháng 3 năm 1963 | entered: cal.1963-03-29.vietnam-hanoi |
| XXIV, 204 | Báo cáo tại Hội nghị TƯ lần thứ tám, 26-3-1963 | cited on cal.1963-03-26.vietnam-hanoi (edit) |
| XXIV, 278 | Báo cáo tại Hội nghị TƯ lần thứ tám, 27-3-1963, kế hoạch 5 năm | cited on cal.1963-03-26.vietnam-hanoi (edit) |
| XXIV, 423 | NQ Hội nghị TƯ lần thứ tám 78-NQ/TW, 4-1963 | cited on cal.1963-03-26.vietnam-hanoi (edit) |
| XXIV, 481 | Thông cáo Hội nghị TƯ lần thứ tám, 4-1963 | cited on cal.1963-03-26.vietnam-hanoi (edit) |
| XXIV, 484 | Chỉ thị của Ban Bí thư Số 62-CT/TW, ngày 1 tháng 4 năm 1963 | entered: cal.1963-04-01.vietnam-hanoi |
| XXIV, 492 | Nghị quyết của ban bí thư Số 75-NQ/TW, ngày 15 tháng 4 năm 1963 | entered: cal.1963-04-15.vietnam-hanoi |
| XXIV, 506 | Thông tri của Ban Bí thư Số 115-TT/TW, ngày 15 tháng 4 năm 1963 | entered: cal.1963-04-15.vietnam-hanoi-2 |
| XXIV, 509 | Nghị quyết của Ban Bí thư Số 76-NQ/TW, ngày 16 tháng 4 năm 1963 | entered: cal.1963-04-16.vietnam-hanoi |
| XXIV, 527 | Nghị quyết của Bộ chính trị Số 77-NQ/TW, ngày 18 tháng 4 năm 1963 | entered with cal.1963-03-08.vietnam-hanoi (the Politburo of Mar. 9) |
| XXIV, 530 | Thông báo của Ban Bí thư Số 47-TB/TW, ngày 22 tháng 4 năm 1963 | entered: cal.1963-04-22.vietnam-hanoi |
| XXIV, 534 | Thông tri của Ban Bí thư Số 116-TT/TW, ngày 23 tháng 4 năm 1963 | passed over: commemoration (May Day) |
| XXIV, 540 | Nghị quyết của Bộ Chính trị Số 79-NQ/TW, ngày 30 tháng 4 năm 1963 | entered: cal.1963-04-30.vietnam-hanoi |
| XXIV, 543 | Thông tri của Ban Bí thư Số 118-TT/TW, ngày 14 tháng 5 năm 1963 | entered: cal.1963-05-14.vietnam-hanoi |
| XXIV, 549 | Nghị quyết của Bộ Chính trị Số 80-NQ/TW, ngày 21 tháng 5 năm 1963 | entered: cal.1963-05-21.vietnam-hanoi |
| XXIV, 553 | Thông báo của Ban Bí thư Số 48-TB/TW, ngày 22 tháng 5 năm 1963 | passed over: a provincial matter (Thái Bình) |
| XXIV, 557 | Thông tri của Ban Bí thư Số 120-TT/TW, ngày 1 tháng 6 năm 1963 | entered: cal.1963-06-01.vietnam-hanoi |
| XXIV, 560 | Chỉ thị của Ban Bí thư Số 63-CT/TW, ngày 5 tháng 6 năm 1963 | cited on cal.1963-06-05.vietnam-hanoi (edit) |
| XXIV, 566 | Thông tri của Ban Bí thư Số 123-TT/TW, ngày 22 tháng 6 năm 1963 | entered: cal.1963-06-22.vietnam-hanoi |
| XXIV, 569 | Chỉ thị của Ban Bí thư Số 64-CT/TW, ngày 4 tháng 7 năm 1963 | entered: cal.1963-07-04.vietnam-hanoi |
| XXIV, 580 | Chỉ thị của Ban Bí thư Số 65-CT/TW, ngày 8 tháng 7 năm 1963 | entered: cal.1963-07-08.vietnam-hanoi-2 |
| XXIV, 584 | Thông tri của Ban Bí thư Số 124-TT/TW, ngày 8 tháng 7 năm 1963 | entered: cal.1963-07-08.vietnam-hanoi |
| XXIV, 588 | Nghị quyết của bộ chính trị Số 85-NQ/TW, ngày 24 tháng 7 năm 1963 | entered: cal.1963-07-24.vietnam-hanoi |
| XXIV, 603 | Bài nói của Chủ tịch Hồ Chí Minh Tại Hội nghị phổ biến | entered: cal.1963-07-27.vietnam-hanoi |
| XXIV, 609 | Nghị quyết của Ban Bí thư Số 809-NQNS/TW, ngày 19 tháng 8 năm 1963 | entered: cal.1963-08-19.vietnam-hanoi |
| XXIV, 610 | Thông tri của Ban Bí thư Số 128-TT/TW, ngày 27 tháng 8 năm 1963 | entered: cal.1963-08-27.vietnam-hanoi |
| XXIV, 612 | Nghị quyết của Ban Bí thư Số 822-NQNS/TW, ngày 30 tháng 8 năm 1963 | entered: cal.1963-08-30.vietnam-hanoi |
| XXIV, 613 | Nghị quyết của Ban Bí thư Số 824-NQNS/TW, ngày 5 tháng 9 năm 1963 | entered: cal.1963-09-05.vietnam-hanoi |
| XXIV, 614 | Nghị quyết của Ban Bí thư Số 839-NQNS/TW, ngày 5 tháng 9 năm 1963 | entered with cal.1963-09-05.vietnam-hanoi (the same day) |
| XXIV, 616 | Chỉ thị của Ban Bí thư Số 66-CT/TW, ngày 11 tháng 9 năm 1963 | entered: cal.1963-09-11.vietnam-hanoi |
| XXIV, 626 | Chỉ thị của Ban Bí thư Số 67-CT/TW, ngày 20 tháng 9 năm 1963 | entered: cal.1963-09-20.vietnam-hanoi |
| XXIV, 628 | Nghị quyết của Ban Bí thư Số 85-NQ/TW, ngày 18 tháng 11 năm 1963 | passed over: a provincial matter (Hồng Quảng and Hải Ninh merged into Quảng Ninh) |
| XXIV, 630 | Chỉ thị của Ban Bí thư Số 68-CT/TW, ngày 19 tháng 11 năm 1963 | entered: cal.1963-11-19.vietnam-hanoi |
| XXIV, 642 | Quy định của Ban bí thư Số 86-NQ/TW, ngày 27 tháng 11 năm 1963 | entered: cal.1963-11-27.vietnam-hanoi |
| XXIV, 650 | Chỉ thị của Ban Bí thư Số 69-CT/TW, ngày 29 tháng 11 năm 1963 | entered: cal.1963-11-29.vietnam-hanoi |
| XXIV, 655 | Nghị quyết của Bộ Chính trị Số 87-NQ/TW, ngày 13 tháng 12 năm 1963 | entered: cal.1963-12-13.vietnam-hanoi |
| XXIV, 657 | Chỉ thị của Ban Bí thư Số 70-CT/TW, ngày 14 tháng 12 năm 1963 | entered: cal.1963-12-14.vietnam-hanoi |
| XXIV, 667 | Nghị quyết của Bộ Chính trị Số 88-NQ/TW, ngày 16 tháng 12 năm 1963 | entered: cal.1963-12-16.vietnam-hanoi |
| XXIV, 669 | Nghị quyết của Ban Bí thư Số 89-NQ/TW, ngày 18 tháng 12 năm 1963 | entered: cal.1963-12-18.vietnam-hanoi |
| XXIV, 673 | Chỉ thị của Ban Bí thư Số 71-CT/TW, ngày 24 tháng 12 năm 1963 | entered: cal.1963-12-24.vietnam-hanoi |
| XXIV, 678 | Chỉ thị của Ban Bí thư Số 72-CT/TW, ngày 30 tháng 12 năm 1963 | entered: cal.1963-12-30.vietnam-hanoi |
| XXIV, 691 | NQ Hội nghị TƯ lần thứ chín về tình hình thế giới và nhiệm vụ quốc tế, 12-1963 | cited on cal.1963-12.vietnam (edit) |
| XXIV, 768 | Thông cáo Hội nghị TƯ lần thứ chín, 12-1963 | cited on cal.1963-12.vietnam (edit) |
| XXIV, 863 | NQ Hội nghị TƯ lần thứ chín, Ra sức phấn đấu ... ở miền Nam, 12-1963 | cited on cal.1963-12.vietnam (edit) |
| XXIV, 912 | NQ TƯ Cục miền Nam, 7-1963, chống phá ấp chiến lược (phụ lục) | entered: cal.1963-07.vietnam-hanoi-2 |
| XXIV, 940 | NQ Hội nghị Khu uỷ Khu V mở rộng lần thứ III, 15–31-7-1963 (phụ lục) | entered: cal.1963-07-31.vietnam-hanoi |
| XXIV, 994 | NQ số 128, Khu uỷ Khu VI, đến 10-1963 (phụ lục) | entered: cal.1963-10.vietnam-hanoi-3 |

#### Vol. XXIII (1962)

| Page | Document (the volume's heading) | Ruling |
|---|---|---|
| XXIII, 1 | Nghị quyết của Bộ Chính trị Số 33-NQ/TW, ngày 5 tháng 1 năm 1962 Về chính sách bảo hiểm xã hội đối với | entered: cal.1962-01-05.vietnam-hanoi |
| XXIII, 15 | Chỉ thị của Ban Bí thư Số 38-CT/TW, ngày 10 tháng 1 năm 1962 Về việc tăng cường công tác kiểm tra | entered: cal.1962-01-10.vietnam-hanoi-2 |
| XXIII, 20 | Thư BCH TƯ gửi BCH TƯ Đảng Cộng sản Liên Xô, 10-1-1962 | entered: cal.1962-01-10.vietnam-hanoi |
| XXIII, 24 | Nghị quyết của Ban bí thư Số 35-NQ/TW, ngày 11 tháng 1 năm 1962 Về việc sửa đổi chế độ trợ cấp đối với cá | entered: cal.1962-01-11.vietnam-hanoi |
| XXIII, 31 | Nghị quyết của Ban Bí thư Số 36-NQ/TW, ngày 16 tháng 1 năm 1962 Về việc thống nhất Trường Nguyễn ái Quốc | entered: cal.1962-01-16.vietnam-hanoi |
| XXIII, 33 | Nghị quyết của Bộ chính trị Số 39-NQ/TW, ngày 20 tháng 1 năm 1962 Về việc tăng cường đấu tranh chống các  | entered: cal.1962-01-20.vietnam-hanoi |
| XXIII, 56 | NQ BCT 40-NQ/TW, 20-1-1962, củng cố lực lượng công an | entered with cal.1962-01-20.vietnam-hanoi (the Politburo, the same day) |
| XXIII, 60 | Nghị quyết của Ban Bí thư Số 38-NQ/TW, ngày 20 tháng 1 năm 1962 Thành lập Tiểu ban giúp Ban Tuyên giáo Tr | entered: cal.1962-01-20.vietnam-hanoi-2 |
| XXIII, 63 | NQ BCT 41-NQ/TW, 24-1-1962, Ban Nghiên cứu Lịch sử Đảng | entered: cal.1962-01-24.vietnam-hanoi |
| XXIII, 70 | Thông tri của Ban Bí thư Số 59-TT/TW, ngày 24 tháng 1 năm 1962 Về việc đẩy mạnh tổ chức nghiên cứu và | entered: cal.1962-01-24.vietnam-hanoi-2 |
| XXIII, 74 | Thông tri của Ban Bí thư Số 60-TT/TW, ngày 30 tháng 1 năm 1962 Về việc lãnh đạo bầu cử hội đồng nhân dân  | entered: cal.1962-01-30.vietnam-hanoi |
| XXIII, 79 | Thông tri của ban bí thư Số 61-TT/TW, ngày 30 tháng 1 năm 1962 Về quyết định họp ngày 27-1-1962 | entered: cal.1962-01-27.vietnam-hanoi |
| XXIII, 84 | Nghị quyết của Bộ Chính trị Số 43-NQ/TW, ngày 1 tháng 2 năm 1962 Về phương hướng và nhiệm vụ kế hoạch năm | entered: cal.1962-02-01.vietnam-hanoi |
| XXIII, 115 | NQ BCT 44-NQ/TW, 10-2-1962, quy hoạch thành phố Nam Định | entered: cal.1962-02-10.vietnam-hanoi |
| XXIII, 121 | Nghị quyết của Ban Bí thư Số 45-NQ/TW, ngày 16 tháng 2 năm 1962 Về việc thành lập Ban phụ trách chuẩn bị  | entered: cal.1962-02-16.vietnam-hanoi |
| XXIII, 123 | NQ BCT 46-NQ/TW, 19-2-1962, phong trào thi đua yêu nước | entered: cal.1962-02-19.vietnam-hanoi |
| XXIII, 136 | Thông tri của Ban bí thư số 64-TT/TW, ngày 20 tháng 2 năm 1962 Về việc quản lý chặt chẽ chi tiêu trong Đả | entered: cal.1962-02-20.vietnam-hanoi |
| XXIII, 140 | Thông tri của Ban Bí thư Số 67-TT/TW, ngày 24 tháng 2 năm 1962 Về việc chuyển giao tổ chức cơ sở đảng ở | entered: cal.1962-02-24.vietnam-hanoi |
| XXIII, 143 | Nghị quyết của Bộ chính trị Họp ngày 26 - 27 tháng 2 năm 1962 Về công tác cách mạng miền Nam | cited on cal.1962-02-26.vietnam-hanoi (edit) |
| XXIII, 165 | Nghị quyết của ban bí thư Số 47-NQ/TW, ngày 27 tháng 2 năm 1962 Về việc chuyển lớp A1 thành trường | entered: cal.1962-02-27.vietnam-hanoi |
| XXIII, 168 | Nghị quyết của ban bí thư Số 48-NQ/TW, ngày 27 tháng 2 năm 1962 Về phương hướng công tác báo chí năm 1962 | entered: cal.1962-02-27.vietnam-hanoi-2 |
| XXIII, 176 | Chỉ thị của Ban Bí thư Số 38-CT/TW, ngày 28 tháng 2 năm 1962 Về tăng cường công tác thể dục thể thao quốc | entered: cal.1962-02-28.vietnam-hanoi |
| XXIII, 181 | NQ BCT 50-NQ/TW, 14-3-1962, tình hình thế giới và nhiệm vụ quốc tế | entered: cal.1962-03-14.vietnam-hanoi |
| XXIII, 201 | Chỉ thị của ban bí thư Số 39-CT/TW, ngày 17 tháng 3 năm 1962 Về việc tuyên truyền và giáo dục nhân dịp | entered: cal.1962-03-17.vietnam-hanoi |
| XXIII, 208 | Chỉ thị của ban bí thư Số 40-CT/TW, ngày 23 tháng 3 năm 1962 Về việc mở cuộc vận động "bảo mật phòng gian | entered: cal.1962-03-23.vietnam-hanoi |
| XXIII, 348 | NQ Hội nghị TƯ lần thứ bảy, về công nghiệp | entered with cal.1962-04-16.vietnam-hanoi |
| XXIII, 388 | Bài nói của Chủ tịch Hồ Chí Minh tại Hội nghị TƯ lần thứ bảy, 16-4-1962 | entered with cal.1962-04-16.vietnam-hanoi |
| XXIII, 393 | Thông cáo Hội nghị TƯ lần thứ bảy (26-3 đến 16-4-1962) | entered with cal.1962-04-16.vietnam-hanoi |
| XXIII, 396 | Thông tri của Ban Bí thư Số 69-TT/TW, ngày 2 tháng 4 năm 1962 Về việc thi hành Nghị quyết số 39 của Bộ Ch | entered: cal.1962-04-02.vietnam-hanoi |
| XXIII, 400 | Chỉ thị của Bộ Chính trị Số 41-CT/TW, ngày 7 tháng 4 năm 1962 Về việc cải tiến tạp chí lý luận của Đảng | entered: cal.1962-04-07.vietnam-hanoi |
| XXIII, 405 | Chỉ thị của Ban Bí thư Số 42-CT/TW, ngày 21 tháng 4 năm 1962 Về nhiệm vụ công tác quân sự địa phương | entered: cal.1962-04-21.vietnam-hanoi |
| XXIII, 411 | Thông tri của Ban Bí Thư Số 71-TT/TW, ngày 23 tháng 4 năm 1962 Về việc tổ chức ngày Quốc tế lao động 1-5 | passed over: commemoration (May Day) |
| XXIII, 417 | Chỉ thị của Ban Bí thư Số 43-CT/TW, ngày 25 tháng 4 năm 1962 Về công tác bảo vệ bà mẹ và trẻ em | entered: cal.1962-04-25.vietnam-hanoi |
| XXIII, 423 | NQ BCT 51-NQ/TW, 26-4-1962, cuộc vận động chống tham ô, lãng phí, quan liêu | entered: cal.1962-04-26.vietnam-hanoi |
| XXIII, 436 | NQ BCT 52-NQ/TW, 26-4-1962, giáo dục lý luận và chính trị | entered with cal.1962-04-26.vietnam-hanoi (the Politburo, the same day) |
| XXIII, 457 | Tạo một chuyển biến mạnh mẽ về công tác tư tưởng (Lê Duẩn, 4-1962) | entered: cal.1962-04.vietnam-hanoi |
| XXIII, 504 | Thông tri của Ban Bí thư Số 72-TT/TW, ngày 4 tháng 5 năm 1962 Về việc lập dự án kế hoạch 5 năm lần thứ nh | entered: cal.1962-05-04.vietnam-hanoi |
| XXIII, 507 | Nghị quyết của Bộ Chính trị Số 53-NQ/TW, ngày 9 tháng 5 năm 1962 Về công tác mặt trận dân tộc thống nhất | entered: cal.1962-05-09.vietnam-hanoi |
| XXIII, 521 | CT BCT 45-CT/TW, 10-5-1962, tuyên truyền đối ngoại | entered: cal.1962-05-10.vietnam-hanoi |
| XXIII, 535 | Chỉ thị của Ban Bí thư Số 44-CT/TW, ngày 11 tháng 5 năm 1962 Về nhiệm vụ công tác tuyên giáo trong năm 19 | entered: cal.1962-05-11.vietnam-hanoi |
| XXIII, 554 | Thông báo của ban bí thư Số 18-TB/HN, ngày 18 tháng 5 năm 1962 Về cuộc họp Ban Bí thư bàn phương hướng | passed over: a provincial matter (Nghệ An) |
| XXIII, 566 | Thông báo của ban bí thư Số 19-TB/HN, ngày 19 tháng 5 năm 1962 Về cuộc họp Ban Bí thư bàn phương hướng ph | passed over: a provincial matter (Phú Thọ) |
| XXIII, 573 | Thông báo của ban bí thư Số 21-TB/HN, ngày 29 tháng 5 năm 1962 Về Hội nghị Bộ Chính trị bàn công tác lươn | entered: cal.1962-03-30.vietnam-hanoi |
| XXIII, 580 | Thông báo của ban bí thư Số 22-TB/HN, ngày 31 tháng 5 năm 1962 Về phiên họp của Ban Bí thư với Khu uỷ | passed over: a provincial matter (the Hồng Quảng zone) |
| XXIII, 583 | Chỉ thị của Ban Bí thư Số 46-CT/TW, ngày 1 tháng 6 năm 1962 Phát động một tháng đấu tranh chống đế quốc | entered: cal.1962-06-01.vietnam-hanoi |
| XXIII, 590 | Thông báo của ban bí thư Số 24-TB/TW, ngày 1 tháng 6 năm 1962 Về cuộc họp Ban Bí thư bàn phát triển | passed over: a provincial matter (Thái Bình) |
| XXIII, 602 | Thông tri của Ban Bí thư Số 79-TT/TW, ngày 5 tháng 6 năm 1962 Về biên chế cán bộ của Đoàn Thanh niên | entered: cal.1962-06-05.vietnam-hanoi |
| XXIII, 604 | CT BCT 47-CT/TW, 6-6-1962, tuyên truyền quốc tế ở trong nước | entered: cal.1962-06-06.vietnam-hanoi |
| XXIII, 616 | Thông báo của ban bí thư Số 25-TB/HN, ngày 16 tháng 6 năm 1962 Về cuộc họp Ban Bí thư bàn phương hướng | passed over: a provincial matter (Hải Dương) |
| XXIII, 627 | Thông báo của ban bí thư Số 26-TB/HN, ngày 21 tháng 6 năm 1962 Về Hội nghị Ban bí thư bàn việc tăng cường | entered: cal.1962-04-30.vietnam-hanoi |
| XXIII, 633 | Thông báo của ban bí thư Số 27-TB/HN, ngày 22 tháng 6 năm 1962 Về cuộc họp Ban Bí thư bàn phương hướng | passed over: a provincial matter (Nam Định) |
| XXIII, 647 | Thông báo của ban bí thư Số 28-TB/HN, ngày 3 tháng 7 năm 1962 Về cuộc họp Ban Bí thư bàn phương hướng | passed over: a provincial matter (Hà Đông) |
| XXIII, 662 | Chỉ thị của Ban bí thư Số 50-CT/TW, ngày 4 tháng 7 năm 1962 Về việc tăng cường công tác kiểm tra việc chấ | entered: cal.1962-07-04.vietnam-hanoi |
| XXIII, 669 | NQ BBT 55-NQ/TW, 5-7-1962, Ban chỉ đạo TƯ cuộc vận động | entered: cal.1962-07-05.vietnam-hanoi |
| XXIII, 672 | Thông báo của ban bí thư Số 29-TB/HN, ngày 9 tháng 7 năm 1962 Về Hội nghị Ban Bí thư bàn vấn đề tổ chức | entered: cal.1962-07-09.vietnam-hanoi |
| XXIII, 678 | Thông báo của ban bí thư Số 30-TB/HN, ngày 9 tháng 7 năm 1962 Về Hội nghị Ban Bí thư ngày 25-6-1962 | entered: cal.1962-06-25.vietnam-hanoi |
| XXIII, 685 | NQ BCT 56-NQ/TW, 10-7-1962, khu gang thép Thái Nguyên | entered: cal.1962-06-01.vietnam-hanoi-2 |
| XXIII, 692 | Chỉ thị của Ban bí thư Số 51-CT/TW, ngày 10 tháng 7 năm 1962 Tích cực củng cố các trường nội trú học sinh | entered: cal.1962-07-10.vietnam-hanoi |
| XXIII, 698 | Thông tri của Ban bí thư Số 83-TT/TW, ngày 10 tháng 7 năm 1962 Về việc thi hành Nghị quyết Hội nghị | entered: cal.1962-07-10.vietnam-hanoi-2 |
| XXIII, 700 | Chỉ thị của Ban bí thư Số 52-CT/TW, ngày 13 tháng 7 năm 1962 Về việc tăng cường lãnh đạo | entered: cal.1962-07-13.vietnam-hanoi |
| XXIII, 705 | Thư của đồng chí Lê Duẩn Bí thư thứ nhất Đảng Lao động Việt Nam Gửi Trung ương cục miền Nam | cited on cal.1962-07-18.vietnam (edit) |
| XXIII, 727 | Thông tri của Ban Bí thư Số 86-TT/TW, ngày 7 tháng 8 năm 1962 Về việc phổ biến và tổ chức thực hiện Nghị  | entered: cal.1962-08-07.vietnam-hanoi |
| XXIII, 730 | Thông tri của Ban Bí thư Số 89-TT/TW, ngày 15 tháng 9 năm 1962 Về vấn đề tăng cường công tác dân tộc | entered: cal.1962-06-23.vietnam-hanoi |
| XXIII, 735 | Thông tri của Ban Bí thư Số 91-TT/TW, ngày 18 tháng 9 năm 1962 Về việc thành lập ban nghiên cứu lịch sử Đ | entered: cal.1962-09-18.vietnam-hanoi |
| XXIII, 738 | Thông tri của Ban Bí thư Số 93-TT/TW, ngày 24 tháng 9 năm 1962 Về Tháng ủng hộ nhân dân Angiêri và nhân d | entered: cal.1962-09-24.vietnam-hanoi |
| XXIII, 741 | Chỉ thị của Ban Bí thư Số 53-CT/TW, ngày 27 tháng 9 năm 1962 Về ổn định tình hình sinh hoạt và đẩy mạnh | entered: cal.1962-09-27.vietnam-hanoi-2 |
| XXIII, 746 | Nghị quyết của Ban Bí thư Số 58-NQ/TW, ngày 27 tháng 9 năm 1962 Về việc thành lập Ban công tác quốc tế nh | entered: cal.1962-09-27.vietnam-hanoi |
| XXIII, 748 | CT BBT 54-CT/TW, 1-10-1962, công tác xuất bản | entered: cal.1962-10-01.vietnam-hanoi |
| XXIII, 754 | Thông tri của Ban Bí thư Số 95-TT/TW, ngày 17 tháng 10 năm 1962 Về việc tổ chức kỷ niệm lần thứ 45 | passed over: commemoration (the October Revolution) |
| XXIII, 757 | Thông báo của ban bí thư Số 36-TB/HN, ngày 17 tháng 10 năm 1962 Về cuộc họp Ban Bí thư với các ban và đản | entered: cal.1962-10-11.vietnam-hanoi |
| XXIII, 763 | Chỉ thị của Ban bí thư Số 55-CT/TW, ngày 22 tháng 10 năm 1962 Về việc giáo dục chính trị cơ bản cho đảng  | entered: cal.1962-10-22.vietnam-hanoi |
| XXIII, 769 | Chỉ thị của Ban bí thư Số 56-CT/TW, ngày 22 tháng 10 năm 1962 Về phương hướng và biện pháp đẩy mạnh chăn  | entered: cal.1962-10-22.vietnam-hanoi-2 |
| XXIII, 783 | Thông báo của Ban bí thư Số 37-TB/HN, ngày 22 tháng 10 năm 1962 Về Hội nghị Bộ Chính trị bàn về | entered: cal.1962-09-08.vietnam-hanoi |
| XXIII, 787 | Thông tri của Ban Bí thư Số 99-TT/TW, ngày 13 tháng 11 năm 1962 Về tiến hành kiểm tra việc quản lý sản xu | entered: cal.1962-11-13.vietnam-hanoi |
| XXIII, 791 | Nghị quyết của Ban Bí thư Số 60-NQ/TW, ngày 17 tháng 11 năm 1962 Về việc cải tiến tổ chức Ban Cơ yếu Trun | entered: cal.1962-11-17.vietnam-hanoi |
| XXIII, 795 | Nghị quyết của Bộ chính trị Số 61-NQ/TW, ngày 29 tháng 11 năm 1962 Về chế độ đóng đảng phí mới | entered: cal.1962-11-29.vietnam-hanoi |
| XXIII, 802 | Thông tri của Ban bí thư Số 101-TT/TW, ngày 6 tháng 12 năm 1962 Về kỷ niệm ngày toàn quốc kháng chiến | passed over: commemoration (Dec. 19 and 22) |
| XXIII, 806 | Nghị quyết của Ban Bí thư Số 62-NQ/TW, ngày 8 tháng 12 năm 1962 Về việc chuyển giao đảng bộ các cơ quan c | entered: cal.1962-12-08.vietnam-hanoi |
| XXIII, 808 | Thông tri của Ban Bí thư Số 102-TT/TW, ngày 10 tháng 12 năm 1962 Về việc chuẩn bị Hội nghị khoa học kỹ th | entered: cal.1962-12-10.vietnam-hanoi |
| XXIII, 812 | NQ Hội nghị BCT 6–10-12-1962, cách mạng miền Nam | cited on cal.1962-12-06.vietnam (cite) |
| XXIII, 839 | Thông báo của ban bí thư Số 39-TB/HN, ngày 24 tháng 12 năm 1962 Về cuộc họp Ban Bí thư với các ban và đản | entered: cal.1962-12-13.vietnam-hanoi |
| XXIII, 844 | Thông tri của Ban Bí thư Số 105-TT/TW, ngày 27 tháng 12 năm 1962 Về cuộc vận động bảo mật phòng gian | entered: cal.1962-12-27.vietnam-hanoi |
| XXIII, 846 | Thông báo của ban bí thư Số 40-TBHN/TW, ngày 28 tháng 12 năm 1962 Về Hội nghị Ban Bí thư bàn đại hội các  | entered: cal.1962-12-18.vietnam-hanoi |
| XXIII, 851 | Biên bản hội nghị Anh Trọng, 20-4 đến 5-5-1962 (phụ lục) | entered: cal.1962-05-05.vietnam-hanoi |
| XXIII, 907 | NQ Hội nghị TƯ Cục miền Nam, 5-1962, nhiệm vụ quân sự (phụ lục) | entered with cal.1962-05-05.vietnam-hanoi (COSVN; Check: the same conference?) |
| XXIII, 916 | NQ Hội nghị thường vụ Khu uỷ 5, cuối năm 1962 (phụ lục) | entered: cal.1962-12.vietnam-hanoi |
| XXIII, 940 | NQ Đại hội đại biểu MTDTGP miền Nam lần thứ nhứt, 16-2 đến 3-3-1962 (phụ lục) | entered: cal.1962-03-03.vietnam-2 |
| XXIII, 957 | NQ Khu uỷ Việt Bắc 50-NQ/KU, 10-5-1962 (phụ lục) | passed over: a provincial matter (the Việt Bắc zone committee) |

### Where batch 12 stopped (1962–64)

All three volumes done, to the last page of each copy (XXIII, 976; XXIV, the appendix to its end; XXV, 793), in the order 1964, 1963, 1962. Not done: vol. XXIV, pp. 777–862, wanting in the copy; the plenums' long reports on the economy as days of their own; the regional committees of Việt Bắc and Tây Bắc (passed over); no witnesses file. Stopped cleanly, the patch checked to 0 errors.

### Audit (batch 12, 1960)

Auditor: batch 12, Nov. 12, 2026, the 1960 half of `inbox/2026-11-12-b12-drv-1960-61.yaml` (ops 1–88, the adds dated 1960, the third plenum's among them; the edits 154–157; the cite 165: 93 ops; the brief's "6 edits" are 4 on 1960 entries, 7 on 1961's). Corrected half: `inbox/2026-11-12-b12-drv-1960-audited.yaml`, its `patch:` left as the reader's, `2026-11-12-b12-drv-1960-61`, so that the ledger's claims hold (with the name `2026-11-12-b12-drv-1960-audited` patch-check gives 88 errors, "claimed by 2026-11-12-b12-drv-1960-61", and no other; the ledger not touched); 0 errors, 55 warnings (the same-day flags and the edits' "sets only n, src"). Copies: vol. 21 downloaded again (Drive `1JStHLzzzKuM3VJtButpRYQ6cwuo7ZqLf`, 580 PDF pages) and split by the first reader's `split.py`, the offsets confirmed (book = 2 × PDF − 7 to PDF 391, − 9 after); vol. 22, PDF 8–64, for the third plenum (XXII, 13–51, 104, 118–19); deleted when done. Read: every 1960 document's heading, date, issuer and signature, its operative sections, and each claim of `c` looked up in the text; the cables to the South, the Interzone V and Nam Bộ resolutions, the eighteenth plenum's communiqués and the Third Congress's resolution, election list and Hồ Chí Minh's addresses at the points cited. No duplicates of the calendar found (the Politburo's sessions, the eighteenth and third plenums, the cables of November and December 1960 are not held elsewhere; the coup of Nov. 11 and the Front's founding of Dec. 20 are other events). No add dropped. Rulings: 63 right; 30 fixed, 18 of them errors and 12 an operative decision or number left out. Errors: 10 (directive no. 156's subject misread as reform "completed"), 11 (the places to watch: the leading organs left out, "guarded first"), 18 (70 percent of the craftsmen, not of the trades), 19 ("to serve agriculture first", not the text; self-reliance, small scale), 21 ("Hanoi, Haiphong and Nam Định first"; the deadline, first half of 1960 or Sept. 2, left out), 35 (the section sits in the Rural Work Board, under Nhị Quý), 41 ("social insurance" not in the text), 49 ("no evidence whatever" not the cable's words), 51 (circular no. 336 cites no. 332 as of May 27: a Check), 55 (the obstinate capitalists "set aside": they are watched and investigated; the suicides), 56 (the pay scales decided at the Secretariat's meeting of May 29, not the Politburo's), 62 (new posts to promote cadres, not "added allowances"), 66 ("continuing" the cold war, not "renewing"; See back to the plenum), 87 (the law promulgated, not "in force", Jan. 13, 1960), 155 (Asselin's fault laid on the armed struggle against the resolution's own causes, XXI, 1099, 1104: a Check), 156 (Asselin's "disappointing" against the resolution's gains, XXI, 1059–63: a Check), 157 (base stale, 0ae5de63 for 88bc5e36, and its `n` would have undone the card `[[w.china-quarterly]]`; "cực kỳ quan trọng" is "extremely", not "most", important: a Check, the VKD row A, C), 165 (unit A carries Hanoi, which the pages do not print: units B). Omissions supplied: 9 (the vote early in May), 40 (46 percent in, 75 by the year's end), 46 (12.4 percent over 1959), 47 (Group 959 among the bodies under the Center), 57 (the campaign's days, June 30–July 20), 65 (the excesses: wrong arrests, three suicides), 71 (the signers), 76 (the Politburo's grain resolution behind the directive), 78 (the central board, Xuân Thủy at its head, `name:xuan-thuy`), 82 (the Front's committees where the posts are gone), 85 (the first groups of cadres sent in), 88 (the 1961 farm targets). Error rate: 18 of 93 (19 percent); with the omissions, 30 of 93 (32 percent). Not settled, for the merger: the Politburo's resolution no. 113-NQ/TW is dated Apr. 22, 1960, the second day of the Politburo's session of Apr. 21–22 (cal.1960-04-21.vietnam-hanoi), and names no session: kept apart, as the reader had it, though it may be a document of that session; resolution no. 124-NQ/TW of Aug. 30 (handicrafts) is "of the April session" and may be the same session; the Secretariat's meeting of May 29, 1960 (the pay scales, XXI, 383) has no entry of its own; "Dr. Cung" (XXI, 1023) left as the cable names him; Nguyễn Duy Trinh, who signs most of the year's documents, appears in the notes only, untagged (a name tag `name:nguyen-duy-trinh` is used in the calendar elsewhere, with no name entry found). Stopped cleanly at the end of the 1960 half, 6:35 p.m. Pacific.

### Audit (batch 12, 1961)

Auditor: batch 12, the 1961 half of `inbox/2026-11-12-b12-drv-1960-61.yaml` (ops 89–153 and 158–164: 65 adds, 7 edits), Nov. 12, 2026. Corrected ops in `inbox/2026-11-12-b12-drv-1961-audited.yaml` (patch name `2026-11-12-b12-drv-1960-61`, the reader's ids kept; 0 errors, 30 warnings, all same-day "one event?"/duplicate prompts and "sets only n, src" on the reader's edits). Vol. 22 downloaded afresh (412 PDF pages, two-up, book page = 2 × PDF − 7, confirmed at XXII, 1, 52, 149, 809), converted by the reader's `split.py`; every document read at its opening, operative heads and close, the Politburo's instruction of Jan. 24, the cables to the South, COSVN's directives and instruction no. 4, the plenums' documents and the notices of the Secretariat's sessions in full. Rulings: 47 right, 23 fixed, 2 dropped (35 percent). Dropped: `cal.1961-02-25.vietnam-hanoi` (resolution 12-NQ/TW: the Politburo's own act on the day the calendar already holds its session, `cal.1961-02-25.vietnam`; folded in there by an edit, base 4e0e481e, the resolution in `c` as "the same day", its cite saying it names no session) and `cal.1961-08-21.vietnam-hanoi` (circular 36-TT/TW: a covering circular sending the fifth plenum's resolution, with rules for its discussion; its "July 1961" now cited on `cal.1961-07.vietnam-hanoi-3`). The third plenum's Moscow sittings (`cal.1961-01-05.vietnam-hanoi`) kept apart from the state-plan sittings (`cal.1960-12-30.vietnam-hanoi`): the resolution's own days, Jan. 5–7, the session over a week in all; the communiqué cited, and "Check: the day" (it closes the plenum Jan. 6). The Politburo's resolution of July 19 (`cal.1961-07-19.vietnam-hanoi`) kept: a dated act of the Politburo, its day printed by the Secretariat's directive of Nov. 9 (XXII, 508); "To check: the resolution itself". The Checks the reader added: Jan. 24 a real disagreement (XXII, 158, "song song", against "political struggle still central"), kept, the cite's parenthetical now saying what 157, 162 and 169 bear and that the page has no "explosion" or "relative calmness"; Mar. 14 no disagreement with the entry, folded into its existing Check as the cable's word (the third plenum of January decided COSVN), the unit map `all` cut to `?` (the cable has no choosing or training of cadres). Fixed for fact: the cultural directive given a five-year plan it does not name (Jan. 3); ten slogans for eleven (Jan. 14); "war preventable" for a world war (Jan. 5); Võ Chí Công's move to Interzone V a permission, not an order (Aug. 10); the July 4 map `all` to `A, C` ("so-called" subversive activities, not "all"); the fifth plenum's "Made public: 2002" (Hồ Chí Minh's address was in his *Toàn tập*, vol. 10, 2000; the communiqué public then) and its parenthetical (the address names the rectification campaign); the sixth plenum's communiqué no secret; the Secretariat of Nov. 6 a morning sitting on commune cadres' pay (XXII, 551–54) left out, now in `cal.1961-11-06.vietnam-hanoi` with the afternoon's youth congress. Fixed for the act: nine entries whose `c` held only the document's survey and not what it decided or ordered (Feb., Interzone V's resolution 62, "Interzone V Executive Committee" the house form; May 8; May 11; Aug. 4, COSVN's standing committee; Oct. 31; Nov. 9, 31-CT/TW; Nov. 13, 30-NQ/TW; Dec. 11; Dec. 31). Also: a Check on COSVN's directive of June 16 (headed COSVN, it reports to the Xứ uỷ); the Armed Police's tasks (Mar. 13); cable 525's heading the editors' (XXII, 561). Not settled: the link from `cal.1961-11-13.vietnam-hanoi-2` back to `cal.1960-02-17.vietnam-hanoi` removed (the 1960 entry is in the other half; restore it at the merge if that entry stands); the ledger still claims the two dropped ids (inbox/new-entries.tsv not touched). PDF and texts deleted. Stopped cleanly with the half done.

Addendum (the 1961 audit): the 1960 half was merged while this audit ran, so the link from `cal.1961-11-13.vietnam-hanoi-2` back to `cal.1960-02-17.vietnam-hanoi` is restored in the audited patch (it resolves; patch-check 0 errors).

### Audit (batch 12, 1964)

Auditor: batch 12, Nov. 12, 2026, the 1964 third of `inbox/2026-11-12-b12-drv-1962-64.yaml` (ops 1–36: 27 adds, 8 edits, 1 cite; no 1964 check op). Corrected ops in `inbox/2026-11-12-b12-drv-1964-audited.yaml` (patch name `2026-11-12-b12-drv-1962-64`, the reader's ids kept, each op headed by its number and ruling; 0 errors, 14 warnings: the three same-day "one event?"/duplicate pairs and "sets only n, src" on the eight edits). Vol. XXV downloaded afresh (Drive `1OgpxUm0O5polcWekBlzIqDJP7fO5AcHF`, 399 PDF pages, two-up; title page "Hà Nội - 2002", introduction "Tháng 1 năm 2003", 48 documents) and split by half-page (`pdftotext -x -W`, then the converter's TCVN3 table), the book's pages read from the folios. Every document read blind first, at its heading, date, issuer, signer, operative sections and close; then each op against it and the tree. Rulings: 26 right, 10 fixed, 0 dropped; 10 of 36 (28 percent): 5 errors (op 1, "bán công bán nông" is half workers, half farmers, not "half in trade"; 11, "a large province" of a million; 33, the instruction does name *Nhân Dân*'s editorial and Chiến Sĩ's article of Apr. 9 and 11 (117): the VKD row `all`, not `A-B`, and the parenthetical's "not *Nhân Dân*" wrong; 34, the `?` row's parenthetical now says the page bears no "special war"; 35, the report runs 293–513, not –511, and the communiqué 682–98, not –97, the src row with it) and 5 omissions of what the document decides (2, Trần Độ secretary of Military Region III's provisional committee; 17, the check ordered of every office's views and acts in foreign affairs since 1960, in secret, by the end of April; 22, 80 to 90 percent of the senior and middle cadres ill; 24, the Politburo's board to sum up the economy under Nguyễn Duy Trinh, for the second plan and the Fourth Congress's report; 25, the 1965 targets for illiteracy). No duplicate of a held entry found (the 1964 `vietnam-hanoi` thread and every 1964 entry naming Hanoi, the Politburo, Hồ Chí Minh or Lê Duẩn searched): the three same-day adds are distinct events (`cal.1964-08-07.vietnam-hanoi-2`, Hồ Chí Minh's speech to the air-defense and naval units, beside the Politburo's instruction no. 81; `cal.1964-12-26.vietnam-hanoi-2`, the Politburo's resolution no. 107 on the Fourth Congress's commissions, beside the tenth plenum; `cal.1964-12.vietnam-hanoi-2`, Hồ Chí Minh at the army's twentieth anniversary, beside the Cambodian foreign minister): `--take keep` at the merge. "Made public: 2003" ruled right for XXV (the introduction is dated January 2003; no colophon in the copy); none on Hồ Chí Minh's speeches, printed in his *Toàn tập* (2000) and public at the time. Not settled, for the merger: the Checks on `cal.1964-01-17.vietnam-hanoi` (Asselin's "early in 1964") and `cal.1964-12-26.vietnam-hanoi` ("the plenum's days and its other business") record no disagreement (the resolution is dated Jan. 17; Lê Duẩn's speech of Dec. 26 closes the plenum, the communiqué says only December), but patch-check refuses an edit that drops a Check, so both stand as the reader kept them; the circular for Mar. 19 (`cal.1964-03-14.vietnam-hanoi`) kept, though a commemoration, for what it adds (McNamara's visit, rallies and resolutions to the Front), while the reader passed over the like instruction no. 87-CT/TW of Dec. 11 (XXV, 285–87: a week's propaganda on Aug. 5 and the Hanoi conference, a rally in Hanoi; 1963's no. 69-CT/TW for Dec. 20 was entered): enter both or neither; the tenth plenum's communiqué is printed from the Party archive (XXV, 698), so "Made public: the communiqué at the time" rests on its kind, not the page; instruction no. 80 (July 10) cites a Politburo instruction "phổ biến ngày 29 tháng 6 năm 1964" (XXV, 161) neither printed nor in the calendar, a lead; Hồ Chí Minh's December speech has no day (the anniversary is Dec. 22; his *Toàn tập*, XI, 349–50, to check); Hồ Chí Minh's report of Mar. 27–28 (the cite, op 36) is reprinted from his *Toàn tập*, XI, 220–35 (XXV, 108), the text the held note already names, no independent witness; the International Conference in Support of the Vietnamese People (Hanoi, from Nov. 25) has no entry. Persons with no name entry: add Trần Độ. PDF and texts deleted. Stopped cleanly with the third done.

### Audit (batch 12, 1963)

Auditor: Claude, Nov. 12, 2026, evening; vol. XXIV downloaded afresh (Drive `172mXcdm2w51tR83qCTMmZoAxsWC8KF7M`, 485 PDF pages, two-up), converted half-page by half-page with the TCVN3 table of `tools/vn/vkd2txt.py`, every 1963 document read in it (the folios as the reader gave them; the appendix's from 910, which is the "Phụ lục" title page; pp. 777–862 wanting, as the reader found), and the copy deleted. Corrected third: `inbox/2026-11-12-b12-drv-1963-audited.yaml` (patch name the reader's), 57 ops, `./bib patch-check` 0 errors; it stands for the reader's ops 37–93, which are not to be merged from the reader's file. Of the reader's 56 ops: 34 right, 21 fixed, 1 dropped (39 percent wanting). Dropped: cal.1963-02-11.vietnam-hanoi-2, the Secretariat's meeting of Feb. 11 (notice no. 46-TB/TW), the same session as its resolution no. 69-NQ/TW of that day, folded into cal.1963-02-11.vietnam-hanoi. Split: cal.1963-03-08.vietnam-hanoi, "Mar. 8–9", is two meetings (no. 74-NQ/TW, "phiên họp ngày 8-3-1963"; no. 77-NQ/TW, "Hội nghị Bộ Chính trị ngày 9 tháng 3"), the second now cal.1963-03-09.vietnam-hanoi (claimed in the ledger under the reader's patch name). Fixed besides: a wrong title (no. 85-NQ/TW of July 24 carried the Nov. 18 merger's), a title cut short (no. 42-TB/TW), the editors' title misplaced (the cable of Jan. 24), a signer wanting (no. 70-NQ/TW, Lê Duẩn); `c` given only the review and not the decision (nos. 67-NQ, 59-CT, 80-NQ, 47-TB, 120-TT); words not on the page ("two wheels of one cart", "carts", "the hamlets the urgent task", "three builds, three antis" laid to the Politburo's resolution); no. 68-CT/TW printed as a draft (641), not an opening; names left out (the special direction's assignments of Mar. 8; the party groups of Sept. 5); `polity:` tags with no country named (Aug. 27, COSVN's July resolution); a Check with no disagreement (Nov. 27, "miền Tây" as Laos, with its `also: [laos]`; the 1961 rules it replaces linked back); Hồ Chí Minh's speech of July 27 printed from his *Toàn tập* (1996), XI, 108–12, put behind To check. Rows: cal.1963-03-26 `A`, cal.1963-06-05 `A-B` (the page states those units whole); the other edits' `?` right. The plenums' days: each Check a real disagreement (the eighth, the entry's Mar. 26–27 by the reports against the editors' Mar. 26–Apr. 8 and the communiqué's April, reworded; the ninth, the editors' Nov. 22–Dec. 7 against Asselin's still sitting Dec. 25, on cal.1963-12.vietnam and cal.1963-12-25.vietnam-hanoi, right as written). Same-day entries beside held ones: cal.1963-07.vietnam-hanoi-2 (COSVN) and cal.1963-10.vietnam-hanoi-3 (Interzone VI) distinct from the *Học Tập* and *Nhân Dân* entries, kept. Hoàng Văn Thái (Aug. 19): untagged rightly, but taken out of "Names:", where the build would link him to the general's entry by name alone; whether he is the general, not settled. Passed over by the reader and left so: the provincial mergers (nos. 688, 689-NQ/TW, Jan. 7; no. 85-NQ/TW, Nov. 18), though they carry out Politburo decisions merging provinces (Hà Bắc, Haiphong–Kiến An, Quảng Ninh), for the owner to rule.

### Audit (batch 12, 1962)

Auditor: batch 12, Nov. 12, 2026, the 1962 third of `inbox/2026-11-12-b12-drv-1962-64.yaml` (ops 94–166: 70 adds, the edits 164 and 165, the cite 166; 73 ops). Corrected third: `inbox/2026-11-12-b12-drv-1962-audited.yaml`, its `patch:` the reader's, `2026-11-12-b12-drv-1962-64`, so the ledger's claims hold; 75 ops (the 73, and a `variant` and a `check` on cal.1962-12-06.vietnam); `./bib patch-check` 0 errors, 28 warnings (the same-day "one event?"/"a duplicate of" flags, and the edits' "sets only n, src"). Copy: vol. XXIII downloaded again (Drive `1upRXoizdfxWBY_emRkOTegqlS_VYLPPy`, 506 PDF pages, two-up, rotated), split by half-page and paged by the folios (book = 2 × PDF − 7 at the start); deleted when done. Read: every 1962 document's heading, date, issuer and signature and its operative sections, each claim of `c` looked up; the Feb. 26–27 and Dec. 6–10 resolutions, Lê Duẩn's letter of July 18, the letter to the CPSU, the COSVN minutes and the May military resolution, the Front's resolution and the Interzone V resolution at the points cited. Duplicates: none found; the letter of Jan. 10 is not cal.1961-12.vietnam-hanoi (Asselin's "soon after" letter to fraternal parties, undated), and the Front's congress, Thái Nguyên, Interzone V and the Politburo's sessions are held nowhere else. No add dropped. The doubtful cases: cal.1962-05-05.vietnam-hanoi kept as one event, the May military resolution with the conference (the same body in conference, the month the conference closed, the same course quoted from "Anh Tư"), the Check put as the day of the military resolution; the "Anh Tư" course is word for word the Politburo's resolution of February (XXIII, 146; COSVN 879, 909). cal.1962-12-06.vietnam: unit B not borne, as the reader said, and unit A not either: the resolution has the "special war" a year old ("Từ một năm nay", 812), not two; the cite now `?`, a variant on A and a Check (with the session's days, Dec. 6–10, against the entry's Dec. 6). Rulings: 46 right; 27 fixed, 12 of them errors and 15 an operative decision or number left out. Errors: 98 (the 1961 plan "fulfilled": the text has "important victories"), 105 (Hồ Chí Minh's "farming first" not his words, "extremely important"; the plenum's dates are the editors' heading of the communiqué, not the communiqué's text; the contents give Apr. 16, not Apr. 14 as the reader's notes say), 108 ("the title the editors'" not in the note; the speech printed from the party school's *Văn kiện lịch sử Đảng*, vol. XI; "without an outline"), 114 (the month not "in answer to the troops sent into Thailand"; the Indian and Canadian members of the Commission left out), 116 ("a deciding factor" for "the deciding factor"), 118 (the program to year's end misstated: the fifth and seventh plenums, two plenums to prepare, the world and the South), 125 ("the first link" for "a link of the first importance"), 133 (the Politburo, not the Secretariat, heard Lê Đức Thọ's report, on Party building in the Soviet Union; he heads the board), 149 (86-TT/TW ends at 728), 164 (unit A mapped: "to be explored" not in the resolution, which makes neutrality a demand, a step of transition: `?`), 165 (the parenthetical "not the imperialists' other reactions" wrong: XXIII, 708 has them, in Laos's lesson; rows now A at 708 and `?` at 711–12), 166 (above). Omissions supplied: 97 (the target cut from 360,000 tons to some 250,000), 103 (the levy on the cooperative, forced purchase, incentive prices 10–30 percent), 110 (the course and COSVN's October 1961 resolution), 111 (the Front's tasks, the Central Front Board), 115 (100,000 tons, to 200,000, Lưu Xá; the talks with China), 120 (the levy fixed at 18 percent), 127 (Đặng Thai Mai at the head), 130 (the councils' make-up), 132 (the courts' decisions), 138 (300,000 by the end of 1961), 143 (the exemption from the hiring freeze), 145 (Phạm Hùng at the head), 146 (consumer goods to commerce), 157 (the Cipher Board under the Central Military Commission), 162 (the provincial congresses put off to the plenum). Error rate: 12 of 73 (16 percent); with the omissions, 27 of 73 (37 percent). Not settled, for the merger: the most routine of the Secretariat's circulars kept as entries, as the reader ruled and the owner's rulings lean (135, geological teams' cells; 143, the Youth Union's staff; 149, spreading the seventh plenum's resolution; 159, the central offices' cells to Hanoi), for the owner to rule; cal.1962-07-09.vietnam-hanoi dated to the notice, the meeting's day unknown (the reader's Check kept); the Secretariat's meeting of Feb. 12 (16-TB/HN, XXIII, 217) is missing from the reader's table of documents though entered; instruction no. 38-CT/TW is the number the volume prints for both Jan. 10 and Feb. 28. Persons named in the corrected `c` with no name entry: Đặng Thai Mai, Phạm Hùng (and the reader's). Stopped cleanly at the end of the 1962 third, 6:55 p.m. Pacific.


## 1967 (batch 16, the DRV's records; vol. 28)

Reader: batch 16, reader 2, Nov. 14, 2026. Patch: `inbox/2026-11-14-b16-vkd-1967.yaml` (patch name `2026-11-14-b16-vkd-1967`), 50 ops: 44 new entries (claimed in the ledger), 3 cites, 1 variant, 2 checks on entries the calendar held. No witnesses file, no by-work edges. `./bib patch-check`: 0 errors, 19 warnings (the same-day "one event?" and "a duplicate of" flags below).

### The copy

Vol. 28 (1967): Drive `1ejGXi7iLKyJ7JrmbmhQ4e1gP_iIbmpDP`, 305 PDF pages, letter, rotated 90, two-up, PDF 1.4 (iTextSharp 5.1.1, made 2019). TCVN3 text layer; converted with the batch-12 conversion applied half-page by half-page (`pdftotext -x -W`, then the FIX table and iconv from TCVN5712-1), which gives each book page alone. Title page "Hà Nội - 2003"; introduction April 2003; colophon CTQG-2003, "In xong và nộp lưu chiểu tháng 6 năm 2003," 6,000 copies. Book pp. V–VI, 1–603: 53 documents in the main part (1–482), 2 in the appendix (483–596), contents 597–603. Book page = 2 × PDF page − 7 (left half; − 6 the right) throughout, from PDF 4 (p. 1) to PDF 305; checked against the folios at 1, 5, 9, 597–604, and the contents' page numbers, which all fall on the page where each document opens. "Made public: 2003." on every document (each "Lưu tại Kho Lưu trữ Trung ương Đảng"). PDF deleted when done.

### The rules used

The brief of batch 16 and the batch-12 rules: an entry a document of the Secretariat, the Politburo, the Central Committee and the Party's directives to the South; a meeting that a notice records entered on the meeting's days, the notice cited there; routine circulars kept; commemorations passed over; every entry `polity:drv` and `vis:only:drv` (all are Party records secret at the time; the Central Office and Region V are the DRV's by the owner's ruling of Nov. 11), `polity:us` where `c` names the Americans outright, `polity:rvn` on the Region V resolution. The Thirteenth Plenum was already held by the calendar (`cal.1967-01.vietnam`, "Jan."); its four documents and Hồ Chí Minh's letter are cited there and on `cal.1967-02-15.vietnam`, not entered again. The Politburo's cable of Jan. 23 is cited also on `cal.1967-01-28.vietnam` (Trinh to Burchett).

### Doubtful, for the merger

- The plenum's four documents (Văn Tiến Dũng's outline, 88–115; Nguyễn Duy Trinh's, 116–40; the Politburo's resolution no. 154-NQ/TW, 141–70; the plenum's no. 155-NQ/TW, 171–79) sit in one cite on the held entry `cal.1967-01.vietnam`, with a variant on its quoted aim ("spontaneous uprising," by Nguyen: the volume has "tổng khởi nghĩa," general uprising, and a decisive victory in "a relatively short time") and a Check on the days (the volume: Jan. 23–27, XXVIII, 88 n.; Trinh's outline's note: Jan. 23–26, 116 n.). Trinh's outline is dated Jan. 23 and Dũng's carries no day: either could be a day of its own, and the plenum's closing (Jan. 27) another; left to the merger. Resolution no. 154 is headed "(tháng 10 và 11 năm 1966)" (the Politburo's sessions then) and dated Jan. 27, 1967, the day the plenum approved it (141 n.).
- Politburo resolution no. 161-NQ/TW on labor: dated Jun. 30 in its heading and the contents; the Secretariat's circular no. 207-TT/TW (468) calls it "30-7-1967" (a slip, or a second date); the Government's no. 103 is Jul. 6. Signed for the Politburo by Lê Thanh Nghị.
- The notices of the Secretariat's meetings are numbered out of the meetings' order: no. 06-TB/TW (Oct. 20) for Oct. 6–7; no. 07-TB (Nov. 7) for Oct. 16; no. 08-TB (Nov. 11) for Oct. 9–10; no. 09-TB (Nov. 16) for Oct. 17. Each entered on its meeting's days; no. 02-TB/TW (Apr. 17) for Apr. 10–11 (the one with Lê Duẩn and Phạm Hùng present).
- Same-day entries, each a separate document (patch-check "one event?"/"a duplicate of"; at the merge `./bib resolve ID --take keep`): Jan. 10 (nos. 152, 153), Jan. 23 (the cable, no. 191-TT/TW), Apr. 17 (nos. 148, 149), May 26 (no. 159, no. 151), Jun. 24 (nos. 153, 154); and `cal.1967-06-15.vietnam-hanoi-2`, `cal.1967-07-05.vietnam-hanoi-3` beside entries the calendar held for those days (Võ Văn Sung's briefing in Paris, Nguyễn Chí Thanh's lunch and walk), unrelated.
- `cal.1967-01-23.vietnam-hanoi`, the Politburo's cable "Số 00," signed "Bác Hương" (the Politburo's code name, 87 n.), is the plan for the Foreign Minister's interview of Jan. 28; it names Salisbury and the briefing in Paris as the occasion and Johnson's message to Congress as a target. Its addressee is "Trung ương Cục - Khu V"; the "representative" it has receive the Americans is not named.
- Hồ Chí Minh's letter (180–83): the volume has him receiving Johnson's letter Feb. 10 and answering Feb. 15, and the editors' note says Johnson ordered the bombing resumed Feb. 14 (a Check on `cal.1967-02-15.vietnam`, whose c has Hồ's "reply, received, it says, Feb. 10").
- `cal.1967-04-13.vietnam-hanoi`: a Secretariat directive about the Việt Bắc Autonomous Region, entered as a central act (the team the Center forms), not a regional one; the merger may pass it over under R18.
- The appendix resolutions (`cal.1967-05.vietnam-hanoi`, `cal.1967-03.vietnam-hanoi`) are dated only by month. The Region V tally of 135,160 enemy out of action is given without a period (561); the COSVN resolution's forecast of the American forces (about 500,000 by the end of 1967, 600,000–700,000 in 1968) is at 498.
- Not read in full (opening, headings and close, operative paragraphs): the economic and organizational directives (nos. 143, 146, 148, 150–152, 155, 156, 167, 198, 200, 207, 210, the notices of Oct. 9–17), the body of Dũng's outline (100–104) and Trinh's (137–40), the later half of resolution no. 154 (157–68), the COSVN resolution (493–559, by its headings and the forecasts) and the Region V resolution (563–96, by its headings and the figures at 561, 580, 585). `c` for these says what the headings and operative paragraphs bear and no more.

### Persons named with no name entry (named in `c` and "Names:", not tagged)

Phạm Hùng, Lê Văn Lương, Tố Hữu, Hoàng Anh, Nguyễn Văn Trân (the Secretariat's members at the meetings of Apr. 10–11, Oct. 6–7, 9–10, 16, 17). Signers named only in the notes: Lê Thanh Nghị, Phạm Chung, Minh Châu (and Vũ Tuân, on no. 194-TT/TW, passed over). Tagged: Lê Duẩn (Apr. 10–11), Hồ Chí Minh and Johnson (Mar. 22).

### The documents, one by one

Every document of the volume in its order, with its first page and the ruling (Vietnamese headings abridged to the number, date and subject).

| Page | Document | Ruling |
|---|---|---|
| XXVIII, 1 | Chỉ thị 139-CT/TW, 7-1-1967, vận động quần chúng thực hiện kế hoạch nhà nước 1967 | entered: cal.1967-01-07.vietnam-hanoi |
| XXVIII, 9 | Nghị quyết 152-NQ/TW, 10-1-1967, tổ chức lãnh đạo công tác phụ vận | entered: cal.1967-01-10.vietnam-hanoi |
| XXVIII, 22 | Nghị quyết 153-NQ/TW, 10-1-1967, công tác cán bộ nữ | entered: cal.1967-01-10.vietnam-hanoi-2 |
| XXVIII, 49 | Chỉ thị 140-CT/TW, 11-1-1967, bảo vệ và bồi dưỡng sức khoẻ | entered: cal.1967-01-11.vietnam-hanoi |
| XXVIII, 59 | Chỉ thị 141-CT/TW, 19-1-1967, công tác tư tưởng | entered: cal.1967-01-19.vietnam-hanoi |
| XXVIII, 68 | Chỉ thị 142-CT/TW, 20-1-1967, lực lượng tự vệ | entered: cal.1967-01-20.vietnam-hanoi |
| XXVIII, 77 | Thông tri 190-TT/TW, 23-1-1967, kỷ niệm lần thứ 37 ngày thành lập Đảng | passed over: a commemoration |
| XXVIII, 79 | Thông tri 191-TT/TW, 23-1-1967, hợp tác xã mua bán xã | entered: cal.1967-01-23.vietnam-hanoi-2 |
| XXVIII, 84 | Điện mật của Bộ Chính trị số 00, 23-1-1967, đấu tranh ngoại giao | entered: cal.1967-01-23.vietnam-hanoi |
| XXVIII, 88 | Đề cương báo cáo tại Hội nghị Trung ương tháng 1-1967 (Văn Tiến Dũng), chỉ đạo chiến lược 1966 | cited on cal.1967-01.vietnam (the held entry of the plenum) |
| XXVIII, 116 | Đề cương báo cáo tại Hội nghị Trung ương 23-1-1967 (Nguyễn Duy Trinh), công tác ngoại giao | cited on cal.1967-01.vietnam |
| XXVIII, 141 | Nghị quyết của Bộ Chính trị 154-NQ/TW, 27-1-1967 (tháng 10 và 11-1966), quân sự và chính trị ở miền Nam | cited on cal.1967-01.vietnam |
| XXVIII, 171 | Nghị quyết Hội nghị lần thứ 13 155-NQ/TW, 27-1-1967, đấu tranh ngoại giao | cited on cal.1967-01.vietnam |
| XXVIII, 180 | Thư của Chủ tịch Hồ Chí Minh trả lời Tổng thống Mỹ Giônxơn (Feb. 15) | cited on cal.1967-02-15.vietnam |
| XXVIII, 184 | Nghị quyết 157-NQ/TW, 22-2-1967, khoa học và kỹ thuật | entered: cal.1967-02-22.vietnam-hanoi |
| XXVIII, 201 | Chỉ thị 143-CT/TW, 8-3-1967, bầu cử Hội đồng nhân dân và Uỷ ban hành chính | entered: cal.1967-03-08.vietnam-hanoi |
| XXVIII, 207 | Chỉ thị 144-CT/TW, 10-3-1967, một tháng phòng không nhân dân | entered: cal.1967-03-10.vietnam-hanoi |
| XXVIII, 213 | Chỉ thị 145-CT/TW, 13-3-1967, an ninh miền Bắc | entered: cal.1967-03-13.vietnam-hanoi |
| XXVIII, 231 | Nghị quyết của Bộ Chính trị 158-NQ/TW, 20-3-1967, kỷ niệm lần thứ 50 Cách mạng Tháng Mười | passed over: a commemoration (read at its opening only) |
| XXVIII, 240 | Thông tri 193-TT/TW, 22-3-1967, động viên chính trị sau thư của Hồ Chí Minh | entered: cal.1967-03-22.vietnam-hanoi |
| XXVIII, 243 | Điện khẩn số 20, 31-3-1967, vụ đông - xuân (Ban Bí thư và Thường vụ Hội đồng Chính phủ) | entered: cal.1967-03-31.vietnam-hanoi |
| XXVIII, 245 | Chỉ thị 146-CT/TW, 1-4-1967, Nghị quyết 136 và đại hội đảng bộ huyện | entered: cal.1967-04-01.vietnam-hanoi |
| XXVIII, 258 | Chỉ thị 147-CT/TW, 13-4-1967, điều tra Luật Hôn nhân và Gia đình ở Khu tự trị Việt Bắc | entered: cal.1967-04-13.vietnam-hanoi (a regional matter, but a Secretariat directive) |
| XXVIII, 261 | Chỉ thị 148-CT/TW, 17-4-1967, tài chính, thương nghiệp, giá cả | entered: cal.1967-04-17.vietnam-hanoi |
| XXVIII, 276 | Chỉ thị 149-CT/TW, 17-4-1967, công tác lương thực | entered: cal.1967-04-17.vietnam-hanoi-2 |
| XXVIII, 284 | Thông báo 02-TB/TW, 17-4-1967, cuộc họp của Ban Bí thư (10-11 tháng 4) | entered: cal.1967-04-10.vietnam-hanoi (the meeting's days) |
| XXVIII, 289 | Thông tri 194-TT/TW, 18-4-1967, kỷ niệm ngày Quốc tế Lao động 1-5 | passed over: a commemoration |
| XXVIII, 297 | Chỉ thị 150-CT/TW, 10-5-1967, quản lý kinh tế tài chính, tiết kiệm | entered: cal.1967-05-10.vietnam-hanoi |
| XXVIII, 305 | Nghị quyết liên tịch 159-NQ/TW, 26-5-1967, cân đối lao động | entered: cal.1967-05-26.vietnam-hanoi |
| XXVIII, 311 | Chỉ thị 151-CT/TW, 26-5-1967, tuyển sinh học nước ngoài | entered: cal.1967-05-26.vietnam-hanoi-2 |
| XXVIII, 319 | Chỉ thị 152-CT/TW, 29-5-1967, Trường Nguyễn Ái Quốc phân hiệu II | entered: cal.1967-05-29.vietnam-hanoi |
| XXVIII, 324 | Thông tri 195-TT/TW, 15-6-1967, động viên tuyển quân | entered: cal.1967-06-15.vietnam-hanoi-2 |
| XXVIII, 328 | Chỉ thị 153-CT/TW, 24-6-1967, báo công, lập công | entered: cal.1967-06-24.vietnam-hanoi |
| XXVIII, 337 | Chỉ thị 154-CT/TW, 24-6-1967, vụ mùa | entered: cal.1967-06-24.vietnam-hanoi-2 |
| XXVIII, 343 | Nghị quyết của Bộ Chính trị 161-NQ/TW, 30-6-1967, công tác lao động | entered: cal.1967-06-30.vietnam-hanoi |
| XXVIII, 369 | Thông tri 196-TT/TW, 1-7-1967, giáo dục cán bộ lãnh đạo sơ cấp | entered: cal.1967-07-01.vietnam-hanoi |
| XXVIII, 375 | Điện mật của Ban Bí thư số 113, 5-7-1967, công tác lương thực | entered: cal.1967-07-05.vietnam-hanoi-3 |
| XXVIII, 379 | Chỉ thị 155-CT/TW, 21-7-1967, chống hạn | entered: cal.1967-07-21.vietnam-hanoi |
| XXVIII, 382 | Thông tri 197-TT/TW, 7-8-1967, thi hành Chỉ thị 145 | entered: cal.1967-08-07.vietnam-hanoi |
| XXVIII, 387 | Thông tri 198-TT/TW, 14-8-1967, kế hoạch nhà nước 1968 và kế hoạch địa phương 1968-70 | entered: cal.1967-08-14.vietnam-hanoi |
| XXVIII, 392 | Thông tri 199-TT/TW, 17-8-1967, kỷ niệm Cách mạng Tháng Tám và Quốc khánh | passed over: a commemoration |
| XXVIII, 394 | Thông tri 200-TT/TW, 1-9-1967, sơ kết Chỉ thị 149 | entered: cal.1967-09-01.vietnam-hanoi |
| XXVIII, 398 | Nghị quyết 167-NQ/TW, 21-9-1967, vận động công nhân và công đoàn | entered: cal.1967-09-21.vietnam-hanoi |
| XXVIII, 427 | Thông báo 06-TB/TW, 20-10-1967, cuộc họp của Ban Bí thư (6-7 tháng 10), thí điểm dân chủ ở miền núi | entered: cal.1967-10-06.vietnam-hanoi (the meeting's days) |
| XXVIII, 433 | Thông tri 202-TT/TW, 21-10-1967, kỷ niệm lần thứ 50 Cách mạng Tháng Mười | passed over: a commemoration |
| XXVIII, 437 | Thông báo 07-TB, 7-11-1967, cuộc họp của Ban Bí thư (16-10), cải tiến quản lý hợp tác xã | entered: cal.1967-10-16.vietnam-hanoi |
| XXVIII, 440 | Thông báo 08-TB, 11-11-1967, cuộc họp của Ban Bí thư (9-10 tháng 10), quản lý và phân phối lương thực | entered: cal.1967-10-09.vietnam-hanoi |
| XXVIII, 448 | Thông tri 204-TT/TW, 15-11-1967, chế độ đối với cán bộ, chiến sĩ vào Nam và ở trong Nam ra | entered: cal.1967-11-15.vietnam-hanoi |
| XXVIII, 451 | Thông báo 09-TB, 16-11-1967, cuộc họp của Ban Bí thư (17-10), phân phối trong hợp tác xã | entered: cal.1967-10-17.vietnam-hanoi |
| XXVIII, 456 | Chỉ thị 156-CT/TW, 20-11-1967, sức khoẻ cán bộ, công nhân, viên chức | entered: cal.1967-11-20.vietnam-hanoi |
| XXVIII, 468 | Thông tri 207-TT/TW, 27-11-1967, phổ biến Nghị quyết 161 và 103 về công tác lao động | entered: cal.1967-11-27.vietnam-hanoi |
| XXVIII, 473 | Thông tri 209-TT/TW, 1-12-1967, ba ngày kỷ niệm trong tháng 12 (19-12, 20-12, 22-12) | passed over: a commemoration |
| XXVIII, 476 | Thông tri 210-TT/TW, 22-12-1967, Uỷ ban Kiểm tra của Đảng và thanh tra | entered: cal.1967-12-22.vietnam-hanoi |
| XXVIII, 485 | Nghị quyết Hội nghị lần thứ năm Trung ương Cục, tháng 5-1967 (phụ lục) | entered: cal.1967-05.vietnam-hanoi |
| XXVIII, 560 | Nghị quyết Hội nghị lần thứ sáu Khu uỷ V (mở rộng), tháng 3-1967 (phụ lục) | entered: cal.1967-03.vietnam-hanoi |

### Where batch 16 stopped (1967)

The volume done, to the last page of its contents (XXVIII, 603): 55 documents, 42 of the main part and 2 of the appendix entered (44), 5 (the plenum's four and Hồ's letter) cited on entries held, 6 commemorations passed over. Stopped cleanly, the patch checked to 0 errors. No witnesses file.

### Audit (batch 16, 1967)

Auditor: Claude (Opus), Nov. 14, 2026. Corrected patch: `inbox/2026-11-14-b16-vkd-1967-audited.yaml` (patch name the reader's, `2026-11-14-b16-vkd-1967`, so the ledger's claims hold; 53 ops; `./bib patch-check` 0 errors, 20 warnings: the reader's 19 same-day flags and "sets only n" on the Jan. 28 edit). Vol. XXVIII downloaded afresh (305 PDF pages, two-up, rotated; book = 2 × PDF − 7 left, − 6 right, confirmed at the folios), split half-page by half-page with the converter's TCVN3 table; colophon CTQG-2003, June 2003: "Made public: 2003." right. Read: every add's heading, number, date, issuer and signer (all right), and in every month the claims of `c` against the text; the cable of Jan. 23, the plenum's four documents and Hồ Chí Minh's letter in full. Adds: 30 upheld, 14 fixed, 0 dropped, none a double of a held entry (the 1967 `vietnam-hanoi`, `vietnam`, `vietnam-diplomacy`, `vietnam-operations`, `vietnam-tet` entries searched). Errors: 04-13 (the team reports to the Politburo, not the Secretariat, and is also the National Assembly Standing Committee's, 259); 06-30 (unemployment "basically" ended, 343); 02-22 ("over" 20,000); 01-23 (the DRV's representative; illusions fought abroad and at home); 07-05 (its title the editors', 375 n.); 1967-03 (the tally is for "the past year", 561, and "diệt" is destroyed); signers 04-10 and 10-06 ("T/l Ban Bí thư", the deputy head of the office); 01-19 `polity:us` off (`c` names no Americans). Decisions left out, supplied: 04-10 (pilots, then report), 05-10 (to carry out the Government's no. 59-CP of the same day, 298), 07-21, 08-07 (385–86), 12-22 (the control committees' staffs, 480). Rulings asked for: the Thirteenth Plenum is a day entry, `cal.1967-01.vietnam` edited to `when: Jan. 23–27`, `date: '1967-01-23'` (88 n.; the resolutions Jan. 27; Trinh's outline's note Jan. 23–26 kept in the Check), tagged `polity:drv`, `vis:only:drv`, "Made public: 2003."; its one cite split into four (one pinpoint, one parenthetical each). Nguyen's "spontaneous uprising ... in the shortest possible time" is not in the volume: no. 154 has "tổng công kích, tổng khởi nghĩa" (general offensive, general uprising, 147) and "thắng lợi quyết định trong thời gian tương đối ngắn" (146); no. 155 has the aim (174) and no uprising; "tự phát" appears nowhere in the volume. Resolution no. 161: June 30 right; circular no. 207's "30-7-1967" (468) a slip, the Government's no. 103 of July 6 "following" it (said in the Nov. 27 note). The notices: numbered in the order of issue (Oct. 20, Nov. 7, 11, 16), not of the meetings; each entered on its meeting's days, right. Việt Bắc (Apr. 13): kept, a central act (a Secretariat directive forming a central team, reporting to the Politburo). The Jan. 28 cite turned into a See (the cable plans the interview; it is no source for it); Hồ's letter (Feb. 15) is printed from his *Toàn tập* (2002), XII, 230–32 (183), not the archive: said in the cite, units `?`; the reader's Check there dropped (no disagreement). Persons with no name entry: as the reader listed (Phạm Hùng, Lê Văn Lương, Tố Hữu, Hoàng Anh, Nguyễn Văn Trân, Lê Thanh Nghị; none in `sources/frus-names`). PDF and texts deleted.

## 1965–66 (batch 16, the DRV's records; vols. 26 and 27)

Reader: batch 16, reader 1, Nov. 14, 2026 (a Saturday). Patch: `inbox/2026-11-14-b16-vkd-1965-66.yaml` (patch name `2026-11-14-b16-vkd-1965-66`), 117 ops: 105 new entries (vol. 26, 1965: 54; vol. 27, 1966: 51), 8 cites and 4 checks on the 6 entries the calendar held (the two plenums\' two cites each), no edits, no witnesses file, no by-work edges. Cited as in batch 12: `[[w.van-kien-dang-toan]], XXVI, 20–25`, the volume in Roman, then the book's page; the note opens with the document's own heading in italics and its signer; "Made public: 2003." on every record kept in the Party archive ("Lưu tại Kho Lưu trữ Trung ương Đảng"), none on Hồ Chí Minh's public appeal of July 20, 1965 or on the greetings to foreign congresses (those five: no ruling, a Check on whether *Nhân Dân* printed them).

### The copies

- Vol. 26 (1965): Drive `1ELuJ9pUFbg_Vt7LvMsSMor3JkZaI7p-t`, 358 PDF pages, letter, each page rotated 90°, PDF 1.4 (Ghostscript 8.15, from a Word file, "VK Dang TT - Tap 26"). Introduction dated May 2003 (66 documents of the main part and 3 of the appendix, by the editors' count). Book pp. 1–710 on the PDF; **the PDF ends mid-sentence at p. 710**, in the third appendix document (COSVN's standing committee, Aug. 5, 1965): no contents, no colophon, no end of the volume. The introduction's count of documents is met by the PDF's headings, so only the tail of that last document is missing, and perhaps further pages after it. Not downloaded again.
- Vol. 27 (1966): Drive `1XaKJVe_z29uptq9-cyTtAisR4CAFrbCc`, 228 PDF pages, same build. Introduction dated Apr. 2003 (57 documents, 50 main, 7 appendix). Book pp. 1–451; the text ends at the last page of the Zone V resolution ("Lưu tại Kho Lưu trữ Trung ương Đảng"); no contents, no colophon.
- Both fetched whole by curl into the scratch directory; deleted when done.

### The encoding, the two-up pages and the offset

TCVN3 (ABC) text layers as in vols. 21–25; `tools/vn/vkd2txt.py` converts a whole page cleanly. Both volumes print two book pages to a PDF page (left and right halves, the PDF page rotated 90°); `vkd2txt.py` runs the halves together line by line, so the reader split each page with `pdftotext -layout -x 0|396 -y 0 -W 396 -H 612`, then the same FIX table and iconv. Book page = 2 × PDF page − 6 (the left half), − 5 (the right), in both volumes from PDF 3 (p. 1 on the right half; PDF 4 is pp. 2–3). Every cite gives the book's page, read from the folios in the text layer (checked at XXVI, 1, 96, 301, 596, 709–10; XXVII, 1, 4, 95, 269, 352, 427, 450–51), not computed. The volumes' own sequence of documents is by date within the main part, the appendix after; the editors' headings supplied where the document had none are marked "Đầu đề do chúng tôi đặt" (B.T) and given "(the title the editors')" in the notes. Quotation marks come out "Ỏ ... Õ"; read as quotation marks.

### The rules used

The batch brief and batch 12's: one entry a document of the Politburo, the Secretariat, the Central Committee and its plenums, the Party's cables and directives to the South and the zones; the routine circulars kept (the owner's ruling of Nov. 12); commemorations passed over and listed (R18): the anniversary directives and circulars on the Party's founding, Hồ Chí Minh's birthday, July 20, Aug. 2–Sept. 2, May Day, Nguyễn Du, the Dec. 1966 anniversaries (10 documents). Kept: the circular for the Chinese Party's anniversary (cal.1966-06-22), as a Việt–Trung act. The three Politburo resolutions of Apr. 8, 1965 merging provinces are one entry; the Twelfth Plenum's documents are one entry each for the Politburo's report and Lê Duẩn's speech (dated Dec. 21, the first day of the plenum, with a Check: the volume gives the span only) and cites on the plenum's entry held (cal.1965-12-27.vietnam-2); likewise the Eleventh Plenum (cal.1965-03-28.vietnam). Visibility: `vis:only:drv` on every Party document, cable and circular; none on Hồ Chí Minh's appeal of July 20, 1965 and the five greetings to foreign congresses. A document's own heading in Vietnamese with full diacritics; names with diacritics in `c`.

### Doubtful, for the merger

- Same-day entries: 28 new ids, on 13 days, share a day and thread with another new entry (patch-check's "one event?" and "a duplicate of" warnings, 43 of them): each is a separate document, listed in the table; at the merge `./bib resolve ID --take keep` for each. The two Dec. 21, 1965 entries (the Politburo's report and Lê Duẩn's speech) are two documents of one plenum on a day the volume does not give.
- The Twelfth Plenum's dates: the volume has it meet Dec. 21–27, 1965 (XXVII, 35 n.; Introduction to vol. 26), the resolution and Hồ Chí Minh's closing speech Dec. 27; `cal.1965-12-27.vietnam-2` has it "open" Dec. 27 (a Check added). The Eleventh Plenum: Mar. 25–27 in the volume (the outline report, XXVI, 56, and the resolution, 96), Mar. 28 on `cal.1965-03-28.vietnam` (a Check added).
- Page cites in the secondary books against the volume's own pages: Asselin, 207 n.11, has the Secretariat's instruction no. 99-CT/TW at XXVI, 198–203 (the volume: 190–95); Nguyen, 76 n.121, the Eleventh Plenum's resolution at 102–18 (the volume: 96–110); Asselin, 206 nn.3–5, and Nguyen, 78 n.136 (Lê Duẩn's speech, 594–95: the end of it, 542–95) agree with the volume. The "To check" sentences of those held entries (the instruction in *Văn kiện Đảng toàn tập*, 26:...) stay; the cites added are what was read. The volume's page 3 does carry the sentence Asselin quotes on revisionism (88-CT/TW).
- cal.1965-03-03.vietnam-hanoi: the cable no. 09/ĐK says "these past days" (mấy hôm nay) and names no event; entered beside cal.1965-03-02.vietnam (Rolling Thunder) with a Check.
- COSVN's resolutions (the third conference's, Jan. 1965; the fourth's, Mar. 1966), the standing committee's of Mar. 6 and Aug. 5, 1965 and the Zone V committee's of Mar. 20, 1966 are the volumes' appendices and are entered as the DRV's acts under the owner's ruling of Nov. 11 (the NLF's acts are the DRV's); they were read in part only (the opening and the passages named in `c`); the fourth conference's resolution (XXVII, 352–426) and the Zone V resolution (427–51) are long and not read through.
- Read to the depth the entries show: the openings of every document and the passages `c` names; not read through: the Politburo's resolution no. 123-NQ/TW (XXVI, 267–303) beyond its first pages, the Politburo's report to the Twelfth Plenum (485–541) beyond the first part, Lê Duẩn's speech (542–95) beyond the passages on the troop numbers and the line, the Twelfth Plenum's resolution (596–625) beyond its situation and its line; the Eleventh Plenum's outline (56–95).
- Several `c` lines (the circulars on culture, the cooperatives campaign, the Red Cross, the savings drive, finance and trade) say only what each opening says; a reader after the details has the pages.
- The Hanoi bombing of Dec. 13, 1966 (the Politburo's cable no. 43) is entered beside cal.1966-12-13.vietnam-air-war, and the Politburo's cable of Apr. 22, 1966 on the cities' movement under thread `vietnam-hanoi` with `also: vietnam-struggle`; neither cable names the day's American event beyond the bombing of Hanoi and "the movement over a month old".
- Cable no. 18 and no. 33 (Jan. 24 and 28, 1966) and no. 2 (Jan. 5): the pause in the bombing seen from Hanoi's Secretariat; `also: vietnam-pause`.

### Persons named with no name entry

Named in `c`: none left untagged (Hồ Chí Minh, Lê Duẩn, Morse, Nguyễn Văn Thiệu, Nguyễn Cao Kỳ, Johnson, Paul VI are tagged). Signers named only in the notes, with no name entry: Tố Hữu, Phạm Hùng, Lê Văn Lương, Vũ Tuân, Phạm Chung, Hoàng Anh, Minh Châu (not tagged; Lê Đức Thọ, Trường Chinh and Lê Duẩn as signers are not tagged either, as in batch 12).

### The documents, one by one

Every document in the two volumes by its heading, in the volume's order, with its first page and the ruling; the volumes print no contents in these PDFs, the list is from the documents' own headings (66 + 3 and 50 + 7 by the editors' count; the table has 123 rows, for the three province mergers of Apr. 8, 1965 are one row and the slogans of July 20, 1965 go with their circular).

| Page | Document (the heading) | Ruling |
|---|---|---|
| XXVI, 1 | Chỉ thị của Bộ Chính trị số 88-CT/TW, ngày 2-1-1965 về cuộc vận động chỉnh huấn mùa xuân năm 1965 | cited on cal.1965-01-02.vietnam-hanoi |
| XXVI, 10 | Chỉ thị của Ban Bí thư số 89-CT/TW, ngày 12-1-1965 về việc kỷ niệm lần thứ 35 ngày thành lập Đảng ta | passed over: a commemoration |
| XXVI, 14 | Thông tri của Ban Bí thư số 155-TT/TW về việc lãnh đạo bầu cử hội đồng nhân dân và uỷ ban hành chính các cấp | entered: cal.1965-01-20.vietnam-hanoi |
| XXVI, 20 | Bài nói của Chủ tịch Hồ Chí Minh tại Hội nghị bồi dưỡng chỉnh huấn do Trung ương triệu tập | entered: cal.1965-01-22.vietnam-hanoi |
| XXVI, 26 | Nghị quyết của Ban Bí thư số 109-NQ/TW về việc chuyển một số công việc của Ban Thống nhất sang Ban Tổ chức Trung ương và Đảng đoàn Bộ Nội vụ | entered: cal.1965-02-13.vietnam-hanoi |
| XXVI, 28 | Chỉ thị của Ban Bí thư số 92-CT/TW về việc thi hành Nghị quyết Hội nghị lần thứ 10 của Trung ương về thương nghiệp và giá cả | entered: cal.1965-02-27.vietnam-hanoi |
| XXVI, 41 | Chỉ thị của Ban Bí thư số 90-CT/TW, ngày 1-3-1965 (cuộc vận động bảo vệ đảng) | cited on cal.1965-03-01.vietnam-hanoi |
| XXVI, 54 | Điện của Ban Bí thư số 09/ĐK về công tác phòng không, sơ tán và phổ biến tin tức (the title the editors') | entered: cal.1965-03-03.vietnam-hanoi |
| XXVI, 56 | Đề cương báo cáo tại Hội nghị Ban Chấp hành Trung ương lần thứ 11 (đặc biệt), họp 25–27-3-1965 | cited on cal.1965-03-28.vietnam |
| XXVI, 96 | Nghị quyết Hội nghị Trung ương lần thứ 11 (đặc biệt), 25, 26, 27-3-1965 | cited on cal.1965-03-28.vietnam |
| XXVI, 111 | Thông báo của Ban Bí thư số 56-TB/TW về những quy định của Bộ Chính trị về việc tổ chức lãnh đạo công tác tiếp tục cải tạo xã hội chủ nghĩa đối với công thương nghiệp tư bản tư doanh, thủ công nghiệp và thương nghiệp nhỏ | entered: cal.1965-04-01.vietnam-hanoi |
| XXVI, 118 | Chỉ thị của Ban Bí thư số 94-CT/TW về công tác tư tưởng trong tình hình trước mắt | entered: cal.1965-04-02.vietnam-hanoi |
| XXVI, 129 | Chỉ thị của Ban Bí thư số 95-CT/TW về việc điều động cán bộ phục vụ cho yêu cầu xây dựng quân đội trong tình hình và nhiệm vụ mới | entered: cal.1965-04-08.vietnam-hanoi |
| XXVI, 132 | Nghị quyết của Bộ Chính trị số 111-NQ/TW, 112-NQ/TW và 113-NQ/TW về việc hợp nhất hai tỉnh Nam Định và Hà Nam, Thái Nguyên và Bắc Cạn, Hà Đông và Sơn Tây | entered: cal.1965-04-08.vietnam-hanoi-2 |
| XXVI, 138 | Nghị quyết của Ban Bí thư số 115-NQ/TW về việc thành lập Cục Bưu điện đặc biệt | entered: cal.1965-04-17.vietnam-hanoi |
| XXVI, 140 | Thông tri của Ban Bí thư số 158-TT/TW, ngày 17-4-1965 về việc mừng thọ Hồ Chủ tịch 75 tuổi | passed over: a commemoration (Hồ Chí Minh's 75th birthday) |
| XXVI, 142 | Nghị quyết của Bộ Chính trị số 116-NQ/TW về việc phân công nhiệm vụ giữa Quân đội nhân dân và lực lượng Công an nhân dân vũ trang trong việc bảo vệ trị an ở miền Bắc và điều chỉnh tổ chức lực lượng Công an nhân dân vũ trang | entered: cal.1965-04-28.vietnam-hanoi |
| XXVI, 151 | Nghị quyết của Ban Bí thư số 117-NQ/TW về thành lập Đảng bộ Bộ Tư lệnh Thủ đô | entered: cal.1965-04-29.vietnam-hanoi |
| XXVI, 153 | Điện mật của Ban Bí thư (ngày 5 tháng 5 năm 1965) về bảo đảm giao thông vận tải (the title the editors') | entered: cal.1965-05-05.vietnam-hanoi |
| XXVI, 155 | Chỉ thị của Ban Bí thư số 96-CT/TW về việc tăng cường công tác bảo mật phòng gian | entered: cal.1965-05-07.vietnam-hanoi |
| XXVI, 162 | Quyết định của Ban Bí thư và Thường vụ Hội đồng Chính phủ số 119-NQ/TW về một số vấn đề trong công tác giao thông vận tải ở các tỉnh Khu IV | entered: cal.1965-05-07.vietnam-hanoi-2 |
| XXVI, 166 | Thông tri của Ban Bí thư số 160-TT/TW về việc tổ chức Hội nghị uỷ ban công đoàn quốc tế đoàn kết với lao động và nhân dân Việt Nam chống đế quốc Mỹ xâm lược | entered: cal.1965-05-07.vietnam-hanoi-3 |
| XXVI, 169 | Chỉ thị của Ban Bí thư số 97-CT/TW về việc đẩy mạnh công tác bổ túc văn hoá | entered: cal.1965-05-18.vietnam-hanoi |
| XXVI, 184 | Thông tri của Ban Bí thư số 161-TT/TW về việc sơ tán Hoa kiều ở các thành phố, thị trấn và các vùng trọng điểm | entered: cal.1965-05-18.vietnam-hanoi-2 |
| XXVI, 187 | Thông tri của Ban Bí thư số 162-TT/TW về việc chọn người đi học khoa học, kỹ thuật ở nước ngoài | entered: cal.1965-05-29.vietnam-hanoi |
| XXVI, 190 | Chỉ thị của Ban Bí thư số 99-CT/TW, ngày 8-6-1965 (công tác vận động phụ nữ) | cited on cal.1965-06-08.vietnam-hanoi |
| XXVI, 196 | Chỉ thị của Ban Bí thư số 100-CT/TW về việc chuyển hướng công tác tài chính thương nghiệp trong tình hình mới | entered: cal.1965-06-14.vietnam-hanoi |
| XXVI, 218 | Chỉ thị của Ban Bí thư số 101-CT/TW về việc tăng cường lãnh đạo công tác lương thực hiện nay | entered: cal.1965-06-29.vietnam-hanoi |
| XXVI, 222 | Điện mật của Ban Bí thư số 146/HT về việc giải quyết lương thực, đẩy mạnh sản xuất (the title the editors') | entered: cal.1965-06-29.vietnam-hanoi-2 |
| XXVI, 226 | Thông tri của Ban Bí thư số 163-TT/TW, ngày 1-7-1965 về kế hoạch tuyên truyền động viên đấu tranh trong dịp 20 tháng 7 (with the Khẩu hiệu ngày 20 tháng 7 năm 1965, 231–32) | passed over: a commemoration (the Geneva anniversary) |
| XXVI, 233 | Chỉ thị của Ban Bí thư số 102-CT/TW về việc tăng cường công tác giáo dục tư tưởng và chính trị đối với cán bộ giảng dạy và sinh viên, học sinh | entered: cal.1965-07-03.vietnam-hanoi |
| XXVI, 247 | Nghị quyết của Ban Bí thư số 122-NQ/TW về tăng cường lãnh đạo, đẩy mạnh cuộc vận động xây dựng chi bộ và đảng bộ cơ sở bốn tốt | entered: cal.1965-07-06.vietnam-hanoi |
| XXVI, 267 | Nghị quyết của Bộ Chính trị số 123-NQ/TW về việc chuyển hướng công tác tổ chức trong tình hình và nhiệm vụ mới | entered: cal.1965-07-07.vietnam-hanoi |
| XXVI, 304 | Nghị quyết của Bộ Chính trị số 125-NQ/TW về việc thành lập Ban sơ tán Trung ương | entered: cal.1965-07-16.vietnam-hanoi |
| XXVI, 306 | Lời kêu gọi của Chủ tịch Hồ Chí Minh nhân ngày 20 tháng 7 (the title the editors') | entered: cal.1965-07-20.vietnam-hanoi |
| XXVI, 312 | Chỉ thị của Ban Bí thư số 104-CT/TW về công tác văn hoá, văn nghệ trong tình hình mới | entered: cal.1965-07-28.vietnam-hanoi |
| XXVI, 318 | Chỉ thị của Ban Bí thư số 105-CT/TW về việc tăng cường lãnh đạo công tác vận động thanh niên trong tình hình mới | entered: cal.1965-07-29.vietnam-hanoi |
| XXVI, 329 | Thông tri của Ban Bí thư số 164-TT/TW về nhiệm vụ và quyền hạn của các Ban Nghiên cứu Lịch sử đảng địa phương miền Nam | entered: cal.1965-07-30.vietnam-hanoi |
| XXVI, 332 | Chỉ thị của Ban Bí thư số 106-CT/TW, ngày 17-8-1965 về việc kỷ niệm lần thứ 20 ngày Cách mạng Tháng Tám và Quốc khánh 2-9 | passed over: a commemoration |
| XXVI, 340 | Nghị quyết của Bộ Chính trị số 126-NQ/TW về việc kiện toàn một bước tổ chức lãnh đạo và chỉ đạo thực hiện của Trung ương Đảng và Chính phủ | entered: cal.1965-08-17.vietnam-hanoi |
| XXVI, 363 | Chỉ thị của Ban Bí thư số 107-CT/TW về việc tiếp tục một bước mới cuộc vận động cải tiến quản lý hợp tác xã, cải tiến kỹ thuật, phát triển sản xuất nông nghiệp ở các tỉnh vùng đồng bằng và trung du | entered: cal.1965-08-21.vietnam-hanoi |
| XXVI, 378 | Nghị quyết của Ban Bí thư số 127-NQ/TW về việc thành lập trường Đảng bồi dưỡng cán bộ sơ cấp của các tỉnh thuộc Khu IV cũ | entered: cal.1965-08-23.vietnam-hanoi |
| XXVI, 380 | Chỉ thị của Ban Bí thư số 108-CT/TW về cuộc vận động cải tiến quản lý hợp tác xã, cải tiến kỹ thuật, nhằm phát triển sản xuất nông nghiệp toàn diện, mạnh mẽ và vững chắc ở miền núi | entered: cal.1965-08-25.vietnam-hanoi |
| XXVI, 396 | Chỉ thị của Ban Bí thư số 109-CT/TW về việc tăng cường lãnh đạo công tác vận động gửi tiền tiết kiệm trong tình hình mới | entered: cal.1965-09-06.vietnam-hanoi |
| XXVI, 402 | Điện mật của Ban Bí thư số 224 về việc tăng cường lãnh đạo, chỉ đạo để đảm bảo tình hình trị an bờ biển (the title the editors') | entered: cal.1965-09-06.vietnam-hanoi-2 |
| XXVI, 404 | Chỉ thị của Ban Bí thư số 110-CT/TW về việc tăng cường lãnh đạo công tác chính trị, sản xuất và trị an quốc phòng trong Khu tự trị Tây Bắc | entered: cal.1965-09-07.vietnam-hanoi |
| XXVI, 414 | Thông tri của Ban Bí thư số 166-TT/TW về việc tổ chức nghiên cứu các vấn đề về phương hướng xây dựng, phát triển và quản lý công nghiệp, quản lý xí nghiệp | entered: cal.1965-09-14.vietnam-hanoi |
| XXVI, 417 | Chỉ thị của Ban Bí thư số 112-CT/TW, ngày 26-10-1965 về việc kỷ niệm Nguyễn Du | passed over: a commemoration (the poet's bicentenary) |
| XXVI, 422 | Điện mật của Ban Bí thư số 283 về yêu cầu tập trung chỉ đạo, đảm bảo giao thông vận tải (the title the editors') | entered: cal.1965-10-29.vietnam-hanoi |
| XXVI, 424 | Chỉ thị của Ban Bí thư số 113-CT/TW về nhiệm vụ của báo Nhân dân trước tình hình và nhiệm vụ mới của cách mạng | entered: cal.1965-11-15.vietnam-hanoi |
| XXVI, 433 | Thông tri của Ban Bí thư số 169-TT/TW về việc tăng cường lãnh đạo công tác hồng thập tự | entered: cal.1965-11-26.vietnam-hanoi |
| XXVI, 436 | Nghị quyết của Bộ Chính trị số 129-NQ/TW về việc tiếp tục thi hành chính sách ổn định nghĩa vụ lương thực, ổn định nghĩa vụ thuế nông nghiệp trong hai năm 1966–1967, tăng cường quản lý phân phối, quản lý thị trường lương thực | entered: cal.1965-12-02.vietnam-hanoi |
| XXVI, 448 | Chỉ thị của Ban Bí thư số 114-CT/TW về việc tăng cường lãnh đạo công tác văn hoá, văn nghệ ở miền núi trong giai đoạn chống Mỹ, cứu nước hiện nay | entered: cal.1965-12-06.vietnam-hanoi |
| XXVI, 458 | Chỉ thị của Ban Bí thư số 116-CT/TW về nâng cao chất lượng của tạp chí Học tập để phục vụ sự nghiệp chống Mỹ, cứu nước và tiếp tục xây dựng cơ sở vật chất và kỹ thuật của chủ nghĩa xã hội | entered: cal.1965-12-14.vietnam-hanoi |
| XXVI, 467 | Điện mật của Ban Bí thư số 312 về việc tăng cường phòng không, sơ tán (the title the editors') | entered: cal.1965-12-17.vietnam-hanoi |
| XXVI, 469 | Thông tri của Ban Bí thư số 171-TT/TW về phương hướng thu, chi ngân sách đảng năm 1966 | entered: cal.1965-12-18.vietnam-hanoi |
| XXVI, 477 | Chỉ thị của Ban Bí thư số 117-CT/TW về việc đẩy mạnh công tác tuyên truyền ủng hộ cách mạng Lào | entered: cal.1965-12-22.vietnam-hanoi |
| XXVI, 480 | Chỉ thị của Ban Bí thư số 118-CT/TW về việc tăng cường công tác thông tin và cổ động | entered: cal.1965-12-23.vietnam-hanoi |
| XXVI, 485 | Báo cáo của Bộ Chính trị tại Hội nghị lần thứ 12 Ban Chấp hành Trung ương: Phương hướng nhiệm vụ kế hoạch hai năm 1966–1967 | entered: cal.1965-12-21.vietnam-hanoi |
| XXVI, 542 | Bài nói của đồng chí Lê Duẩn, Bí thư thứ nhất Ban Chấp hành Trung ương Đảng, tại Hội nghị lần thứ 12 của Trung ương: Phấn khởi tiến lên, đem toàn lực của nhân dân hai miền đánh thắng đế quốc Mỹ và bè lũ tay sai | entered: cal.1965-12-21.vietnam-hanoi-2 |
| XXVI, 596 | Nghị quyết Hội nghị lần thứ 12 của Ban Chấp hành Trung ương, ngày 27-12-1965 | cited on cal.1965-12-27.vietnam-2 |
| XXVI, 626 | Lời phát biểu của Hồ Chủ tịch trong phiên họp bế mạc hội nghị lần thứ 12 của Trung ương, chiều 27-12-1965 | cited on cal.1965-12-27.vietnam-2 |
| XXVI, 634 | Nghị quyết của Bộ Chính trị số 131-NQ/TW về việc thành lập Ban Nghiên cứu Lý luận của Trung ương | entered: cal.1965-12-28.vietnam-hanoi |
| XXVI, 643 | Nghị quyết Hội nghị Trung ương Cục lần thứ ba, số 2/NQ, tháng 1 năm 1965, về tình hình cách mạng miền Nam năm 1964 và nhiệm vụ trước mắt của ta (the title the editors') | entered: cal.1965-01.vietnam-hanoi |
| XXVI, 667 | Nghị quyết của Thường vụ Trung ương Cục miền Nam ("Thường vụ Năm Trường," the editors' note) số 4/NQ về công tác phụ vận | entered: cal.1965-03-06.vietnam-hanoi |
| XXVI, 693 | Nghị quyết hội nghị Thường vụ Trung ương Cục số 6/NQ về một số vấn đề trong công tác nông thôn sắp tới | entered: cal.1965-08-05.vietnam-hanoi |
| XXVII, 1 | Điện mật của Ban Bí thư số 2 yêu cầu thực hiện một số điểm trong thời kỳ Mỹ tạm ngừng ném bom miền Bắc (the title the editors') | entered: cal.1966-01-05.vietnam-hanoi |
| XXVII, 4 | Bài nói của Chủ tịch Hồ Chí Minh tại hội nghị cán bộ cao cấp nghiên cứu nghị quyết hội nghị lần thứ 12 Ban Chấp hành Trung ương Đảng | entered: cal.1966-01-16.vietnam-hanoi |
| XXVII, 18 | Thông tri của Ban Bí thư số 173-TT/TW, ngày 20-1-1966 về việc kỷ niệm lần thứ 36 ngày thành lập Đảng (3-2) | passed over: a commemoration |
| XXVII, 21 | Thông tri của Ban Bí thư số 174-TT/TW về việc học tập Nghị quyết Hội nghị lần thứ 12 của Trung ương và kế hoạch hai năm của Nhà nước | entered: cal.1966-01-20.vietnam-hanoi |
| XXVII, 26 | Điện mật của Ban Bí thư số 18 gửi các Khu uỷ, Thành uỷ và Tỉnh uỷ yêu cầu thực hiện một số việc để đánh bại âm mưu của Mỹ ném bom bắn phá trở lại miền Bắc (the title the editors') | entered: cal.1966-01-24.vietnam-hanoi |
| XXVII, 29 | Chỉ thị của Ban Bí thư số 119-CT/TW về việc phân cấp quản lý tài chính của Đảng | entered: cal.1966-01-28.vietnam-hanoi |
| XXVII, 33 | Điện mật của Ban Bí thư số 33 gửi các Khu uỷ, Thành uỷ, Tỉnh uỷ về việc lập kế hoạch đề phòng đế quốc Mỹ oanh tạc trở lại miền Bắc (the title the editors') | entered: cal.1966-01-28.vietnam-hanoi-2 |
| XXVII, 35 | Nghị quyết Hội nghị lần thứ 12 Ban Chấp hành Trung ương số 135-NQ/TW về việc vận dụng và bổ sung một số điểm cụ thể về Điều lệ Đảng | entered: cal.1966-01-31.vietnam-hanoi |
| XXVII, 41 | Chỉ thị của Ban Bí thư số 120-CT/TW về công tác tư tưởng trong năm 1966 | entered: cal.1966-02-17.vietnam-hanoi |
| XXVII, 61 | Thông tri của Ban Bí thư số 175-TT/TW về việc tổ chức "Cuộc họp mặt những nhà khoa học và văn hoá thế giới ủng hộ nhân dân Việt Nam chống cuộc chiến tranh xâm lược của Mỹ" | entered: cal.1966-03-08.vietnam-hanoi |
| XXVII, 64 | Thông tri của Ban Bí thư số 176-TT/TW về một số vấn đề cần chú ý trong cuộc vận động "Cải tiến quản lý hợp tác xã, cải tiến kỹ thuật, phát triển sản xuất nông nghiệp" | entered: cal.1966-03-15.vietnam-hanoi |
| XXVII, 69 | Chỉ thị của Ban Bí thư số 121-CT/TW về việc ra sức nâng cao chất lượng và tăng cường công tác phát triển đảng song song với việc củng cố đảng | entered: cal.1966-04-07.vietnam-hanoi |
| XXVII, 86 | Chỉ thị của Ban Bí thư số 122-CT/TW về việc tăng cường lãnh đạo phong trào thi đua yêu nước trước tình hình và nhiệm vụ mới | entered: cal.1966-04-07.vietnam-hanoi-2 |
| XXVII, 95 | Bài nói của Chủ tịch Hồ Chí Minh tại hội nghị tổng kết ba năm xây dựng chi bộ và đảng bộ cơ sở "bốn tốt" | entered: cal.1966-04.vietnam-hanoi |
| XXVII, 101 | Nghị quyết của Ban Bí thư số 137-NQ/TW về kiện toàn tổ chức Ban Tài chính thương nghiệp các cấp | entered: cal.1966-04-12.vietnam-hanoi |
| XXVII, 111 | Chỉ thị của Ban Bí thư số 123-CT/TW về việc tăng cường lãnh đạo và củng cố phong trào hợp tác xã mua bán xã | entered: cal.1966-04-14.vietnam-hanoi |
| XXVII, 118 | Điện mật của Ban Bí thư số 36 gửi Thành uỷ Hà Nội, Hải Phòng, Thái Nguyên và các Tỉnh uỷ (the title the editors') | entered: cal.1966-04-14.vietnam-hanoi-2 |
| XXVII, 120 | Điện mật của Bộ Chính trị số 110 gửi Trung ương Cục, Khu V, Liên tỉnh 1, về phong trào đấu tranh của quần chúng ở đô thị miền Nam (the title the editors'; "Bác Hương," the editors' note: the Politburo) | entered: cal.1966-04-22.vietnam-hanoi |
| XXVII, 130 | Thông tri của Ban Bí thư số 178-TT/TW, ngày 23-4-1966 về kỷ niệm lần thứ 80 ngày Quốc tế Lao động 1-5 | passed over: a commemoration |
| XXVII, 136 | Chỉ thị của Ban Bí thư số 124-CT/TW về tăng cường lãnh đạo công tác tài chính thương nghiệp và giá cả năm 1966–1967 | entered: cal.1966-04-27.vietnam-hanoi |
| XXVII, 148 | Nghị quyết của Bộ Chính trị số 140-NQ/TW về việc nghiên cứu kế hoạch dài hạn | entered: cal.1966-04-29.vietnam-hanoi |
| XXVII, 151 | Chỉ thị của Ban Bí thư số 126-CT/TW về nhiệm vụ của các cơ quan, xí nghiệp, bệnh viện, trường học sơ tán về nông thôn và trách nhiệm của các cấp | entered: cal.1966-05-04.vietnam-hanoi |
| XXVII, 157 | Thông tri của Ban Bí thư số 180-TT/TW về việc chấp hành chính sách tôn giáo đối với đạo Phật | entered: cal.1966-05-16.vietnam-hanoi |
| XXVII, 161 | Thông tri của Ban Bí thư số 181-TT/TW về việc tăng cường công tác vận động đồng bào theo đạo Thiên chúa trước tình hình mới | entered: cal.1966-05-16.vietnam-hanoi-2 |
| XXVII, 167 | Chỉ thị của Ban Bí thư số 127-CT/TW về việc tăng cường lãnh đạo công tác dân quân, tự vệ và hậu bị trong tình hình mới | entered: cal.1966-05-17.vietnam-hanoi |
| XXVII, 175 | Nghị quyết của Ban Bí thư số 136-NQ/TW về việc kiện toàn sự lãnh đạo và chỉ đạo thực hiện của các Huyện uỷ | entered: cal.1966-05-20.vietnam-hanoi |
| XXVII, 197 | Chỉ thị của Ban Bí thư số 128-CT/TW về việc tăng cường công tác tuyên truyền đối ngoại | entered: cal.1966-06-06.vietnam-hanoi |
| XXVII, 204 | Chỉ thị của Ban Bí thư số 129-CT/TW về việc tăng cường giữ gìn bí mật công tác thông tin liên lạc vô tuyến điện của các cơ quan đảng và nhà nước | entered: cal.1966-06-06.vietnam-hanoi-2 |
| XXVII, 208 | Chỉ thị của Ban Bí thư số 130-CT/TW, ngày 22-6-1966 về đợt tuyên truyền vận động trong dịp 20 tháng 7 năm 1966 | passed over: a commemoration (the Geneva anniversary) |
| XXVII, 218 | Thông tri của Ban Bí thư số 182-TT/TW về tổ chức kỷ niệm lần thứ 45 ngày thành lập Đảng Cộng sản Trung Quốc | entered: cal.1966-06-22.vietnam-hanoi |
| XXVII, 222 | Nghị quyết của Bộ Chính trị số 142-NQ/TW về việc đào tạo và bồi dưỡng cán bộ khoa học, kỹ thuật và cán bộ quản lý kinh tế | entered: cal.1966-06-28.vietnam-hanoi |
| XXVII, 237 | Chỉ thị của Ban Bí thư số 131-CT/TW về việc củng cố hợp tác xã tín dụng để tăng cường công tác tín dụng và quản lý tiền tệ ở nông thôn | entered: cal.1966-06-28.vietnam-hanoi-2 |
| XXVII, 252 | Thông tri của Ban Bí thư số 183-TT/TW về tổ chức điều tra tội ác chiến tranh của đế quốc Mỹ ở Việt Nam | entered: cal.1966-06-28.vietnam-hanoi-3 |
| XXVII, 256 | Nghị quyết của Ban Bí thư số 143-NQ/TW về việc thành lập Đảng uỷ Giao thông vận tải trung ương | entered: cal.1966-06-30.vietnam-hanoi |
| XXVII, 263 | Chỉ thị của Ban Bí thư số 132-CT/TW về một số vấn đề về kiện toàn tổ chức và tăng cường sự lãnh đạo và chỉ đạo thực hiện của Đảng đối với công tác giao thông vận tải ở các cấp | entered: cal.1966-06-30.vietnam-hanoi-2 |
| XXVII, 269 | Lời kêu gọi của Chủ tịch Hồ Chí Minh ngày 17-7-1966 ("Không có gì quý hơn độc lập, tự do") | cited on cal.1966-07-16.vietnam |
| XXVII, 273 | Chỉ thị của Ban Bí thư số 133-CT/TW về việc mở một đợt vận động chính trị hưởng ứng Lời kêu gọi của Chủ tịch Hồ Chí Minh | entered: cal.1966-07-20.vietnam-hanoi |
| XXVII, 276 | Chỉ thị của Ban Bí thư số 134-CT/TW về tăng cường lãnh đạo giáo dục rèn luyện thanh niên và dân quân, tự vệ, chuẩn bị tốt lực lượng bổ sung cho quân đội | entered: cal.1966-08-12.vietnam-hanoi |
| XXVII, 284 | Điện mật của Ban Bí thư ngày 14 tháng 8 năm 1966 gửi các Khu uỷ, Thành uỷ, Tỉnh uỷ về việc thực hiện triệt để biện pháp phòng không nhân dân đối phó âm mưu ném bom, bắn phá miền Bắc của đế quốc Mỹ (the title the editors') | entered: cal.1966-08-14.vietnam-hanoi |
| XXVII, 287 | Chỉ thị của Ban Bí thư số 135-CT/TW, ngày 15-8-1966 về việc kỷ niệm lần thứ 21 Cách mạng Tháng Tám và Quốc khánh 2-9 | passed over: a commemoration |
| XXVII, 295 | Thông tri của Ban Bí thư số 184-TT/TW về việc giáo dục chính trị cơ bản cho đảng viên mới | entered: cal.1966-08-15.vietnam-hanoi |
| XXVII, 298 | Nghị quyết của Ban Bí thư Trung ương Đảng số 148-NQ/TW về việc thành lập Trường Nguyễn Ái Quốc phân hiệu IV | entered: cal.1966-08-27.vietnam-hanoi |
| XXVII, 300 | Điện mật của Ban Bí thư số 109 gửi các Khu uỷ, Thành uỷ, Tỉnh uỷ chỉ đạo thực hiện Chỉ thị 134-CT/TW (the title the editors') | entered: cal.1966-08-29.vietnam-hanoi |
| XXVII, 302 | Thông tri của Ban Bí thư số 185-TT/TW về việc tổ chức nghiên cứu phương hướng phát triển tiểu công nghiệp và thủ công nghiệp trong tình hình mới | entered: cal.1966-09-06.vietnam-hanoi |
| XXVII, 305 | Chỉ thị của Ban Bí thư số 136-CT/TW về việc bảo đảm trật tự giao thông và bảo vệ tài sản nhà nước trong quá trình vận chuyển | entered: cal.1966-09-12.vietnam-hanoi |
| XXVII, 308 | Thông tri của Ban Bí thư số 188-TT/TW về việc ngăn chặn bọn phản động lợi dụng đạo Thiên chúa tổ chức cầu nguyện hoà bình giả hiệu | entered: cal.1966-10-05.vietnam-hanoi |
| XXVII, 311 | Chỉ thị của Ban Bí thư số 137-CT/TW về việc tăng cường lãnh đạo cuộc vận động cải tiến quản lý hợp tác xã nông nghiệp, cải tiến kỹ thuật | entered: cal.1966-10-31.vietnam-hanoi |
| XXVII, 323 | Thông tri của Ban Bí thư số 189-TT/TW, ngày 30-11-1966 về việc tuyên truyền động viên nhân dịp ba ngày kỷ niệm trong tháng 12 năm 1966 | passed over: a commemoration (Dec. 19, 20 and 22) |
| XXVII, 326 | Điện mật của Bộ Chính trị số 43 gửi Trung ương Cục miền Nam (ngày 13 tháng 12 năm 1966) | entered: cal.1966-12-13.vietnam-hanoi |
| XXVII, 327 | Chỉ thị của Ban Bí thư số 138-CT/TW về việc tăng cường và tập trung hơn nữa sự lãnh đạo và chỉ đạo công tác giao thông vận tải trong tình hình hiện nay | entered: cal.1966-12-19.vietnam-hanoi |
| XXVII, 339 | Điện của Ban Chấp hành Trung ương Đảng Lao động Việt Nam ngày 18 tháng 1 năm 1966 gửi Ban Chấp hành Trung ương Đảng Cộng sản Ý | entered: cal.1966-01-18.vietnam-hanoi |
| XXVII, 341 | Điện mừng của Ban Chấp hành Trung ương Đảng Lao động Việt Nam ngày 7 tháng 5 năm 1966 gửi Đại hội lần thứ XIX Đảng Cộng sản Canađa | entered: cal.1966-05-07.vietnam-hanoi |
| XXVII, 343 | Thư của Ban Chấp hành Trung ương Đảng Lao động Việt Nam ngày 1 tháng 6 năm 1966 gửi Đại hội lần thứ XV Đảng Nhân dân cách mạng Mông Cổ | entered: cal.1966-06-01.vietnam-hanoi |
| XXVII, 345 | Điện mừng của Ban Chấp hành Trung ương Đảng Lao động Việt Nam ngày 17 tháng 6 năm 1966 gửi Đại hội lần thứ XVIII Đảng Cộng sản Mỹ | entered: cal.1966-06-17.vietnam-hanoi |
| XXVII, 348 | Điện của Ban Chấp hành Trung ương Đảng ngày 22 tháng 10 năm 1966 gửi Đại hội đại biểu toàn quốc lần thứ X của Đảng Cộng sản Nhật Bản | entered: cal.1966-10-22.vietnam-hanoi |
| XXVII, 352 | Nghị quyết hội nghị Trung ương Cục lần thứ tư, số 1, tháng 3 năm 1966: Đánh giá tình hình cách mạng miền Nam năm 1965, phương hướng, nhiệm vụ sắp tới và một số nhiệm vụ của cách mạng miền Nam | entered: cal.1966-03.vietnam-hanoi |
| XXVII, 427 | Nghị quyết của Khu uỷ V ngày 20 tháng 3 năm 1966 về công tác thành phố | entered: cal.1966-03-20.vietnam-hanoi |

### Where reader 1 stopped

Both volumes done to their last page in the PDFs (XXVI, 710, mid-document; XXVII, 451): 126 documents by the editors' count, 105 entered, 8 cited on 6 entries held, 10 commemorations passed over, the three province mergers one entry. No pages skipped; the PDFs deleted.


## 1968–69 (batch 16, the DRV's records; vols. 29 and 30)

Reader: batch 16, reader 3, Nov. 14, 2026 (a Saturday). Patch: `inbox/2026-11-14-b16-vkd-1968-69.yaml` (patch name `2026-11-14-b16-vkd-1968-69`), 129 ops: 117 new entries (claimed in the ledger; 69 from vol. 29, 48 from vol. 30, one of them dated May 1968), 6 cites, 2 variants and 4 checks on 6 entries the calendar held. No edits, no witnesses file, no by-work edges. `./bib patch-check`: 0 errors, 33 warnings (the same-day "one event?" and "a duplicate of" flags of the 11 pairs below).

### The copies

- Vol. 29 (1968): Drive `14do8ZYd_BKhWC0TvYyrq2QHVptd8cCJh`, 387 PDF pages, letter, rotated 90, two-up, PDF 1.4 (GPL Ghostscript 8.15, made Mar. 7, 2019). Title page "Hà Nội - 2004"; introduction February 2004 ("76 tài liệu Văn kiện chính và 6 tài liệu phụ lục"). No contents and no colophon in the copy; the last two of the six appendix documents (PDF 377–87) carry the running head "lời giới thiệu tập 29 ... VII" and no folios. Every one of the 82 documents is in the copy (counted against the introduction).
- Vol. 30 (1969): Drive `117SWi30FzokIhs7UzELXYyPlyYXCGMbj`, 267 PDF pages, letter, rotated 90, two-up, PDF 1.4 (Ghostscript 8.15). Title page "Hà Nội - 2004" (at PDF 136, before the testament as published); introduction June 2004 ("58 tài liệu ... 49 ... văn kiện chính, 9 ... phụ lục"). No contents, no colophon; the appendix (PDF 160–267) prints only "V"/"VI" for folios. I count 47 headings in the main part: the funeral papers attached to directive no. 172 (slogans, rules of mourning, flags and armbands, the two programs) are one row below.
- TCVN3 text layers, converted half-page by half-page (`pdftotext -x -W`, then the batch-12 FIX table and iconv from TCVN5712-1), each half one book page. Both PDFs deleted when done.

### The folios are not the book's pages (for the merger and the owner)

Every cite gives the folio the copy prints, as the brief asks; but in these two copies the folios are demonstrably not the printed book's pages:

- Vol. 29's folios run on, inside continuous text, from 223 to 387, 398 to 497, 616 to 733, 776 to 863, and between documents from 1026 to 1167 and 1212 to 1267; they repeat 40–41 and 152–161 (the Planning Commission's report ends at 161, PDF 85; four documents of Jan. 12–16 then run 153–61, PDF 86–90). The left halves above 999 print only three digits ("101", "116"): the fourth is read from the facing page.
- Fixed points from outside the copy: the editors' own note on the Politburo's cable of Oct. 20 to Region V puts the cable of Oct. 10 "ở trang 468" (copy folio 940); Nguyen, *Hanoi's War*, cites the cables of Oct. 10 and 20 as 29:468–74 and 484–87 (copy 940–48, 960–63); vol. 30's note on circular no. 236 cites no. 220 at 29:324 (copy 587). Counting the copy's halves in order (book page = 2 × PDF − 7 on the right) gives 338, 489 and 509 for those three: so the copy is not a facsimile of the print either, its halves running some 4 percent ahead.
- Vol. 30: the folios run 1–265 in step with the halves (book page = 2 × PDF − 5 on the right, − 6 on the left), then jump to 313 at the testament as published (PDF 136); the editors' note in the appendix (COSVN's ninth conference) places its own earlier note "ở trang 365", which falls at PDF 183R, half 361: the folios after 265 run some 45 ahead of the print, and those up to 265 may be true.
- Batch 12 reported vol. 24 "wanting" pp. 777–862 at the same jump, 776 to 863: very likely the same artifact, not missing pages (the text should be compared across PDF 388R/389L).
- What I did: cited the folios as printed, ranges split at a jump ("214–23, 387"; "615–16, 733–38"; "775–76, 863–913"), the appendix of vol. 30 cited as "appendix (the copy's pages unnumbered)", and a Check on the two held entries where Nguyen's pages differ. A re-paging of these cites, if wanted, needs a printed copy.

### The rules used

The batch-16 brief and batch 12's: one entry a document of the Politburo, the Secretariat, the Central Committee and its plenums, the cables and directives to the South and the zones, COSVN's and Region V's resolutions (the appendices); routine circulars kept; a meeting a notice records entered on the meeting's day or days (two sittings three weeks apart, Nov. 12 and Dec. 2, 1968, on the second); commemorations passed over (R18). The Fourteenth Plenum held (`cal.1968-01.vietnam-tet`): its three documents cited there, not entered again. The Fifteenth and Sixteenth Plenums not held: entered, the Sixteenth as one entry of its three documents (May 8–10, 1969, by the editors' note at XXX, 76). The Politburo's resolution no. 185 entered on its session's days, Oct. 10–13, 1968, its date Dec. 26 in `c`. Hồ Chí Minh's appeals of July 20 and Nov. 3, 1968 cited on the entries held. Visibility: `vis:only:drv` on every Party record kept in the archive, `vis:only:drv+ussr` on the letter of July 16 and the cable of Dec. 1, 1968 to the Soviet leaders, `vis:only:drv+dprk` on the letter to Kim Il Sung; no ruling on what was published at the time (the communiqué and call on Hồ's death, the eulogy). The greetings of 1969 to foreign congresses, by the owner's territorial ruling of Nov. 14 (relayed by the coordinator): to the Danish and British parties, out of power and on territory outside the five named, `vis:only:drv` and no `polity:` for the country; to the Romanian party, a ruling party, `vis:only:drv+romania`; each with a Check whether *Nhân Dân* printed it (published, the ruling falls). "Made public: 2004." on the archive records (both volumes "Hà Nội - 2004"); none on the published ones; "Made public: 1989, the day" on Hồ's death of Sept. 2. `polity:` tags where `c` names the country or its leader outright. The document's own heading in italics opens each note, with its signer.

### Doubtful, for the merger

- Same-day pairs, each a separate document (patch-check "one event?"/"a duplicate of"; at the merge `./bib resolve ID --take keep`): Jan. 16, 1968 (resolutions 173 and 174); Apr. 3 (the Secretariat's and the Politburo's cables); May 8 (the Politburo on a coalition government; the Secretariat's cable no. 117); Dec. 12 (circular no. 224; the Politburo's cable to Phạm Hùng); Jan. 6, 1969 (the Secretariat's morning and afternoon meetings, youth and women); Jan. 17 (circular no. 226; the meeting on the three Northwest provinces); Apr. 1969 (Region V's two resolutions); May 10 (Hồ's testament; directive no. 170); June 18 (circulars 237, 238); Sept. 4 (the public communiqué; the Politburo's secret directive no. 172); Oct. 24 (the Secretariat's cable no. 00; its meeting of Oct. 24–25 on the cities). Also beside entries the calendar held on other threads: `cal.1968-04-03.vietnam-hanoi-2` (beside `cal.1968-04-03.vietnam`, Hanoi's public statement), `cal.1968-04-08.vietnam-hanoi` (beside `cal.1968-04-08.vietnam`, the site), `cal.1968-10-20.vietnam-hanoi` (beside `cal.1968-10-20.vietnam-paris`: the same day's cable to COSVN is cited there; this is the separate cable no. 00/1968 to Region V and Trị–Thiên, which the editors say differs from that of Oct. 10 in date, addressee and content).
- `cal.1968-12.vietnam-hanoi`: the Secretariat's cable to COSVN dated "Tháng 12 năm 1968" reads as of the first weeks of Tết (the cities' risings, Huế, Route 9); a Check.
- `cal.1969-07.vietnam-hanoi`: COSVN's ninth conference, "early July" by its resolution, "August" by COSVN's resolution of Oct. 5; it extends to June 1970 the "Hồ Chí Minh class" recruiting drive "just past," which may put the text after September; a Check.
- `cal.1969-08-09.vietnam-hanoi`: the resolution's number prints "1733-NQ/TW" among nos. 187–194 of 1969; a Check.
- `cal.1969-09-02.vietnam-hanoi`: Hồ's death at 9:47 a.m. Sept. 2, from the editors' note (XXX, 228–29 n.) quoting the Politburo's notice no. 151-TB/TW of Aug. 19, 1989; the documents of the day all say Sept. 3. The merger may prefer to source the day elsewhere as well.
- `cal.1969-05-10.vietnam-hanoi`: the testament entered on the day Hồ dated its last part; the 1965 draft (May 15, 1965, witnessed by Lê Duẩn) is named in `c`, not entered (vol. 26's span). That the text published in 1969 leaves out the cremation and the ashes (and the farm-tax remission) I read in this volume's two printings (XXX, 260–64 against 313–20), not in a source that says so.
- `cal.1968-01.vietnam-tet` (held): the volume names the plenum's cities "X, Y, Z" (a variant on B); the held `c` and its title for the resolution are the Politburo's December resolution by *Victory in Vietnam*; a Check states what the volume prints.
- `cal.1968-10-10.vietnam-paris` (held): the volume bears unit A; on B a variant (the conditions are that the Americans discuss the conference with the Front and that Saigon change its policy); C, the longer interval, is not in the cable. `cal.1968-10-20.vietnam-paris`: A in part (not Thọ's report or the delegation's seeming in no hurry) and B. The "Made public: ... Check the year" in both: the year is 2004.
- `cal.1968-02.vietnam` (held, the Alliance at Ban Mê Thuột by MACV): a Check with the Politburo's cables of Jan. 21 and Feb. 8 (the Alliance ordered formed in Saigon, its manifesto broadcast Feb. 7).
- `cal.1969-01-17.vietnam-hanoi-2` (the Secretariat on Sơn La, Nghĩa Lộ and Lai Châu) and `cal.1968-07-04.vietnam-hanoi`, `cal.1968-01-12.vietnam-hanoi` (cables to Vĩnh Linh): central acts on localities, entered; the merger may pass them over under R18.
- The 1968 Hoàng Văn Thái of the forward General Department of Rear Services (`cal.1968-07-03.vietnam-hanoi`) is not tagged `name:hoang-van-thai`: whether he is the general of `vn.who.hoang-van-thai` the page does not say (as batch 12 found for 1963).
- Not read through (heading, opening, operative heads and close only): the Planning Commission's report (XXIX, 69–161), Lê Duẩn's speeches at the Fourteenth and Sixteenth Plenums, resolution no. 179 on grain, resolution no. 181 on the young, no. 185 on the economy, the long COSVN and Region V resolutions, the outline on diplomacy of May 1969 beyond its heads. `c` says what the headings and operative paragraphs bear and no more.

### Persons named with no name entry (named in `c` and "Names:", not tagged)

Phạm Hùng, Võ Chí Công, Trần Văn Quang, Lê Văn Lương, Tố Hữu, Hoàng Anh, Nguyễn Văn Trân, Nguyễn Côn, Lê Thanh Nghị, Trần Hữu Dực, Nguyễn Văn Kỉnh, Lê Toàn Thư, Phạm Hồng, Lê Văn Hảo, Trịnh Đình Thảo, Phan Trọng Tuệ, Lê Quang Hòa, Lê Văn Tri, Hoàng Văn Thái (above), Nguyễn Tường Lân, Hoàng Sâm, Nguyễn Quyết, Madeleine Riffaud, Joris Ivens, Kenji Miyamoto, Bình Phương, Nguyễn Thương, Đỗ Mười, Trần Danh Tuyên, Nguyễn Hữu Mai, Đinh Đức Thiện, Ngô Minh Loan, Nguyễn Thanh Bình, Trần Ngọc Liễng. Signers named only in the notes: Trần Xuân Bách, Phạm Chung, Minh Châu. Tagged: Lê Duẩn, Hồ Chí Minh, Lê Đức Thọ, Xuân Thủy, Nguyễn Duy Trinh, Trường Chinh, Phạm Văn Đồng, Tôn Đức Thắng, Trần Bửu Kiếm, Johnson, Nixon, Humphrey, Thiệu, Kỳ, Khiêm, Brezhnev, Kosygin, Kim Il Sung, Sihanouk, Burchett.

### The documents, one by one

Every document of the two volumes in the volume's order, with the copy's folio where it opens and the ruling (Vietnamese headings abridged to the number, date and subject; BCT the Politburo, BBT the Secretariat, BCH the Central Committee, TƯC COSVN).

| Page | Document | Ruling |
|---|---|---|
| XXIX, 1 | Bài phát biểu của đồng chí Lê Duẩn tại Hội nghị lần thứ 14, tháng 1-1968 | cited on cal.1968-01.vietnam-tet (held), with a variant and a Check |
| XXIX, 41 | Nghị quyết Hội nghị lần thứ 14, tháng 1-1968, tổng công kích và tổng khởi nghĩa | cited on cal.1968-01.vietnam-tet |
| XXIX, 69 | Báo cáo của Uỷ ban Kế hoạch nhà nước tại Hội nghị lần thứ 14 (kinh tế 1968) | cited on cal.1968-01.vietnam-tet |
| XXIX, 153 | Điện mật BBT số 06, 12-1-1968, gửi Đảng uỷ Vĩnh Linh | entered: cal.1968-01-12.vietnam-hanoi |
| XXIX, 156 | Điện mật BBT số 09, 15-1-1968, thăm hỏi dịp Tết | entered: cal.1968-01-15.vietnam-hanoi |
| XXIX, 158 | Nghị quyết BCT 173-NQ/TW, 16-1-1968, Ban công tác Quốc tế | entered: cal.1968-01-16.vietnam-hanoi |
| XXIX, 160 | Nghị quyết BBT 174-NQ/TW, 16-1-1968, giải thể Ban Quốc tế Nhân dân | entered: cal.1968-01-16.vietnam-hanoi-2 |
| XXIX, 162 | Điện mật BCT, 21-1-1968, gửi Bảy Cường, Năm Công, Bảy Tiến (Mặt trận thứ hai) | entered: cal.1968-01-21.vietnam-hanoi |
| XXIX, 165 | Thông tri 211-TT/TW, 27-1-1968, kỷ niệm thành lập Đảng | passed over: a commemoration |
| XXIX, 167 | Điện mật BBT số 23, 1-2-1968, tin chiến thắng | entered: cal.1968-02-01.vietnam-hanoi |
| XXIX, 169 | Điện mật BCT số 44, 8-2-1968, Tuyên ngôn của Liên minh | entered: cal.1968-02-08.vietnam-hanoi; a Check on cal.1968-02.vietnam (held) |
| XXIX, 173 | Điện mật BCT, 10-2-1968, thư quyết tâm gửi Bác Hồ | entered: cal.1968-02-10.vietnam-hanoi |
| XXIX, 174 | Chỉ thị 157-CT/TW, 21-2-1968, bầu cử HĐND khu, tỉnh, thành | entered: cal.1968-02-21.vietnam-hanoi |
| XXIX, 180 | Thông tri 212-TT/TW, 26-2-1968, quản lý kinh tế - tài chính | entered: cal.1968-02-26.vietnam-hanoi |
| XXIX, 183 | Nghị quyết BCT 175-NQ/TW, 1-3-1968, động viên chính trị toàn dân | entered: cal.1968-03-01.vietnam-hanoi |
| XXIX, 192 | Thông báo 05-TB/TW, 15-3-1968, BBT và Thường vụ HĐCP (29-2), phân cấp quản lý kinh tế | entered: cal.1968-02-29.vietnam-hanoi (the meeting's day) |
| XXIX, 194 | Thông tri 213-TT/TW, 18-3-1968, hướng dẫn thi hành Nghị quyết 175 | entered: cal.1968-03-18.vietnam-hanoi |
| XXIX, 198 | Điện BBT, 3-4-1968, về tuyên bố 31-3 của Giônxơn | entered: cal.1968-04-03.vietnam-hanoi |
| XXIX, 201 | Điện mật BCT, 3-4-1968, gửi Trung ương Cục | entered: cal.1968-04-03.vietnam-hanoi-2; cited on cal.1968-04-03.vietnam (held) |
| XXIX, 204 | Điện mật BBT số 73, 5-4-1968, sửa Chỉ thị 157 | entered: cal.1968-04-05.vietnam-hanoi |
| XXIX, 206 | Điện mật BCT, 8-4-1968, đấu tranh ngoại giao | entered: cal.1968-04-08.vietnam-hanoi |
| XXIX, 214 | Chỉ thị 158-CT/TW, 10-4-1968, tài chính, thương nghiệp, giá cả | entered: cal.1968-04-10.vietnam-hanoi (folios 214–23, 387) |
| XXIX, 388 | Thông báo 07-TB/TW, 10-4-1968, BBT và Thường vụ HĐCP (15-3), kế hoạch | entered: cal.1968-03-15.vietnam-hanoi |
| XXIX, 392 | Thông tri 214-TT/TW, 15-4-1968, kỷ niệm 1-5, khẩu hiệu | passed over: a commemoration |
| XXIX, 398 | Chỉ thị BCT 159-CT/TW, 27-4-1968, 150 năm ngày sinh Các Mác | passed over: a commemoration (folios 398, 497–502) |
| XXIX, 503 | Điện mật BCT, 8-5-1968, gửi Bảy Cường, Chính phủ liên hiệp | entered: cal.1968-05-08.vietnam-hanoi |
| XXIX, 505 | Điện mật BBT số 117, 8-5-1968, Pari | entered: cal.1968-05-08.vietnam-hanoi-2 |
| XXIX, 507 | Thông báo 09-TB/TW, 10-5-1968, BBT (14-3), Đoàn Thanh niên | entered: cal.1968-03-14.vietnam-hanoi |
| XXIX, 513 | Điện mật BBT số 126, 14-5-1968, gửi Khu uỷ Trị - Thiên, Liên minh Huế | entered: cal.1968-05-14.vietnam-hanoi |
| XXIX, 515 | Điện mật BCT số 253, 17-5-1968, gửi Khu uỷ Khu IX | entered: cal.1968-05-17.vietnam-hanoi |
| XXIX, 518 | Thông tri 217-TT/TW, 20-5-1968, học sinh sơ tán dịp hè | entered: cal.1968-05-20.vietnam-hanoi |
| XXIX, 522 | Thông báo 11-TB/TW, 25-5-1968, BBT (23-4), vận động làm chủ tập thể trong xí nghiệp | entered: cal.1968-04-23.vietnam-hanoi |
| XXIX, 526 | Chỉ thị 161-CT/TW, 29-5-1968, đạo Phật, Cao đài, Tin lành | entered: cal.1968-05-29.vietnam-hanoi |
| XXIX, 530 | Chỉ thị 162-CT/TW, 30-5-1968, công tác Mặt trận ở miền Bắc | entered: cal.1968-05-30.vietnam-hanoi |
| XXIX, 536 | Thông tri 218-TT/TW, 6-6-1968, giao thông vận tải Quân khu IV | entered: cal.1968-06-06.vietnam-hanoi |
| XXIX, 539 | Nghị quyết BBT 179-NQ/TW, 8-6-1968, quản lý, phân phối lương thực | entered: cal.1968-06-08.vietnam-hanoi |
| XXIX, 565 | Điện mật BBT số 155, 13-6-1968, Nghệ An, Hà Tĩnh, Quảng Bình, Vĩnh Linh | entered: cal.1968-06-13.vietnam-hanoi |
| XXIX, 567 | Thông tri 219-TT/TW, 3-7-1968, Ban chỉ đạo giao thông vận tải Quân khu IV | entered: cal.1968-07-03.vietnam-hanoi |
| XXIX, 570 | Điện mật BBT số 21, 4-7-1968, gửi anh Đồng, Vĩnh Linh | entered: cal.1968-07-04.vietnam-hanoi |
| XXIX, 571 | Lời kêu gọi của Chủ tịch Hồ Chí Minh nhân ngày 20-7 | cited on cal.1968-07-20.vietnam (held) |
| XXIX, 575 | Chỉ thị 163-CT/TW, 11-7-1968, học tập Lời kêu gọi 20-7 | entered: cal.1968-07-11.vietnam-hanoi |
| XXIX, 581 | Chỉ thị 164-CT/TW, 13-7-1968, tiết kiệm dài hạn chống Mỹ, cứu nước | entered: cal.1968-07-13.vietnam-hanoi |
| XXIX, 585 | Điện mật BBT số 193, 26-7-1968, Quảng Bình, Hà Tĩnh, Nghệ An | entered: cal.1968-07-26.vietnam-hanoi |
| XXIX, 587 | Thông tri 220-TT/TW, 2-8-1968, hệ thống chỉ huy thống nhất giao thông vận tải Khu IV | entered: cal.1968-08-02.vietnam-hanoi |
| XXIX, 599 | Chỉ thị 165-CT/TW, 6-8-1968, đại hội đại biểu Đảng bộ các tỉnh | entered: cal.1968-08-06.vietnam-hanoi |
| XXIX, 604 | Điện mật BBT, 11-8-1968, chống lụt | entered: cal.1968-08-11.vietnam-hanoi |
| XXIX, 605 | Thông tri 221-TT/TW, 16-8-1968, kỷ niệm Cách mạng Tháng Tám, khẩu hiệu | passed over: a commemoration |
| XXIX, 611 | Thông báo 13-TB/TW, 24-8-1968, BBT và Thường vụ HĐCP (20-8), lụt, bão | entered: cal.1968-08-20.vietnam-hanoi |
| XXIX, 615 | Thông báo 14-TB/TW, 26-8-1968, BBT và Thường vụ HĐCP (8-8), giáo dục phổ thông | entered: cal.1968-08-08.vietnam-hanoi (folios 615–16, 733–38) |
| XXIX, 739 | Báo cáo tại Hội nghị lần thứ 15, 29-8-1968, đấu tranh ngoại giao | entered: cal.1968-08-29.vietnam-hanoi |
| XXIX, 775 | Nghị quyết BCT, tháng 8-1968, tổng khởi nghĩa, tổng công kích | entered: cal.1968-08.vietnam-hanoi (folios 775–76, 863–913) |
| XXIX, 914 | Thông tri 222-TT/TW, 12-9-1968, quản lý thị trường | entered: cal.1968-09-12.vietnam-hanoi |
| XXIX, 917 | Nghị quyết BBT 181-NQ/TW, 25-9-1968, vận động thanh niên | entered: cal.1968-09-25.vietnam-hanoi |
| XXIX, 940 | Điện mật BCT số 320, 10-10-1968, gửi Trung ương Cục | cited on cal.1968-10-10.vietnam-paris (held), with a variant and a Check |
| XXIX, 949 | Điện mật BCT (số 323), 15-10-1968, gửi Trung ương Cục | entered: cal.1968-10-15.vietnam-hanoi |
| XXIX, 954 | Nghị quyết BCT 183-NQ/TW, 16-10-1968, Khu uỷ Trị - Thiên - Huế | entered: cal.1968-10-16.vietnam-hanoi |
| XXIX, 958 | Điện mật BBT số 291, 19-10-1968 | entered: cal.1968-10-19.vietnam-hanoi |
| XXIX, 960 | Điện mật BCT, 20-10-1968, gửi Trung ương Cục | cited on cal.1968-10-20.vietnam-paris (held), with a Check |
| XXIX, 964 | Điện mật BCT số 00/1968, 20-10-1968, gửi Khu uỷ V và Trị - Thiên | entered: cal.1968-10-20.vietnam-hanoi |
| XXIX, 970 | Thông báo 18-TB/TW, 23-10-1968, BBT, lâm nghiệp | entered: cal.1968-10-23.vietnam-hanoi |
| XXIX, 975 | Điện mật BBT số 302, 31-10-1968, sắp ngừng ném bom | entered: cal.1968-10-31.vietnam-hanoi |
| XXIX, 978 | Điện mật BBT số 305, 2-11-1968, giải thích tình hình sau ngừng ném bom | entered: cal.1968-11-02.vietnam-hanoi |
| XXIX, 981 | Lời kêu gọi của Chủ tịch Hồ Chí Minh, 3-11-1968 | cited on cal.1968-11-03.vietnam (held) |
| XXIX, 985 | Chỉ thị BCT, 9-11-1968, bổ sung Nghị quyết tháng 8-1968 | entered: cal.1968-11-09.vietnam-hanoi |
| XXIX, 999 | Chỉ thị 166-CT/TW, 21-11-1968, trị an, thị trường, nếp sống mới ở thành phố | entered: cal.1968-11-21.vietnam-hanoi |
| XXIX, 1006 | Chỉ thị 167-CT/TW, 28-11-1968, địch bắt người làm nghề trên biển | entered: cal.1968-11-28.vietnam-hanoi |
| XXIX, 1013 | Điện mật BCT, 1-12-1968, gửi Bộ Chính trị Đảng Cộng sản Liên Xô | entered: cal.1968-12-01.vietnam-hanoi |
| XXIX, 1015 | Điện mật BBT số 348, 4-12-1968 | entered: cal.1968-12-04.vietnam-hanoi |
| XXIX, 1017 | Thông tri 223-TT/TW, 6-12-1968, kỷ niệm 19-12, 20-12, 22-12 | passed over: a commemoration |
| XXIX, 1020 | Thông tri 224-TT/TW, 12-12-1968, ba khoán và quản lý ruộng đất | entered: cal.1968-12-12.vietnam-hanoi |
| XXIX, 1167 | Điện mật BCT, 12-12-1968, gửi Bảy Cường | entered: cal.1968-12-12.vietnam-hanoi-2 |
| XXIX, 1171 | Thông báo 21-TB/TW, 18-12-1968, BBT (18-11), công đoàn | entered: cal.1968-11-18.vietnam-hanoi |
| XXIX, 1179 | Thông báo 22-TB/TW, 19-12-1968, BBT và Thường vụ HĐCP (12-11, 2-12), lao động | entered: cal.1968-12-02.vietnam-hanoi |
| XXIX, 1186 | Nghị quyết BCT 185-NQ/TW, 26-12-1968 (kỳ họp 10-13/10), kinh tế 1969 | entered: cal.1968-10-10.vietnam-hanoi (the session's days) |
| XXIX, 1206 | Thông tri 225-TT/TW, 28-12-1968, phổ biến Nghị quyết 185 | entered: cal.1968-12-28.vietnam-hanoi |
| XXIX, 1210 | Điện mật BBT, tháng 12-1968, gửi Trung ương Cục, Khu uỷ V, Trị - Thiên | entered: cal.1968-12.vietnam-hanoi (a Check on the month) |
| XXIX, 1267 | Phụ lục: Nghị quyết Thường vụ TƯC và Quân uỷ Miền, 5-2-1968, khu trọng điểm | entered: cal.1968-02-04.vietnam-hanoi |
| XXIX, 1275 | Phụ lục: Nghị quyết Hội nghị TƯC (mở rộng) lần thứ sáu, 01/NQNT, tháng 3-1968 | entered: cal.1968-03.vietnam-hanoi |
| XXIX, 1314 | Phụ lục: Thư của BCT, 16-7-1968, gửi Bơrêgiơnhép và Côxưghin | entered: cal.1968-07-16.vietnam-hanoi |
| XXIX, 1321 | Phụ lục: Nghị quyết Hội nghị lần thứ tám TƯC, 07/NQNT, tháng 10-1968 | entered: cal.1968-10.vietnam-hanoi |
| XXIX, appendix | Phụ lục: Thư của BCH, 27-10-1968, gửi Kim Nhật Thành (unpaged, PDF 377) | entered: cal.1968-10-27.vietnam-hanoi |
| XXIX, appendix | Phụ lục: Nghị quyết của Khu uỷ V về công tác kinh tế tài chính 1968 (unpaged, PDF 378–87) | passed over: undated (no day or month printed); a lead |
| XXX, 1 | Chỉ thị 168-CT/TW, 13-1-1969, người tốt, việc tốt | entered: cal.1969-01-13.vietnam-hanoi |
| XXX, 5 | Thông tri 228-TT/TW, 27-1-1969, bổ sung Chỉ thị 168 | entered: cal.1969-01-27.vietnam-hanoi |
| XXX, 7 | Thông tri 226-TT/TW, 17-1-1969, bầu cử HĐND huyện, xã | entered: cal.1969-01-17.vietnam-hanoi |
| XXX, 11 | Thông tri 227-TT/TW, 22-1-1969, kỷ niệm thành lập Đảng | passed over: a commemoration |
| XXX, 13 | Thông báo 04-TB/TW, 4-2-1969, BBT (chiều 6-1), vận động phụ nữ | entered: cal.1969-01-06.vietnam-hanoi-2 |
| XXX, 19 | Điện BCT, 11-2-1969, gửi Bảy Cường, đấu tranh ở đô thị | entered: cal.1969-02-11.vietnam-hanoi |
| XXX, 21 | Chỉ thị 169-CT/TW, 14-2-1969, giáo dục 1968-1970 | entered: cal.1969-02-14.vietnam-hanoi |
| XXX, 34 | Thông tri 229-TT/TW, 6-3-1969, vận động phụ nữ 1969 | entered: cal.1969-03-06.vietnam-hanoi |
| XXX, 37 | Thông báo 05-TB/TW, 14-3-1969, BBT (sáng 6-1), vận động thanh niên | entered: cal.1969-01-06.vietnam-hanoi |
| XXX, 42 | Thông báo 06-TB/TW, 20-3-1969, BBT (17, 18, 27-1), Sơn La, Nghĩa Lộ, Lai Châu | entered: cal.1969-01-17.vietnam-hanoi-2 (a central act on three provinces; the merger may pass it over under R18) |
| XXX, 48 | Thông tri 234-TT/TW, 19-4-1969, kỷ niệm 1-5, khẩu hiệu | passed over: a commemoration |
| XXX, 53 | Nghị quyết BCT 187-NQ/TW, 22-4-1969, các ngày kỷ niệm lớn năm 1970 | passed over: commemorations (Lenin's centenary, the Party at 40, Hồ at 80, the DRV at 25) |
| XXX, 62 | Điện BBT số 130, 7-5-1969, tiến công ngoại giao | entered: cal.1969-05-07.vietnam-hanoi |
| XXX, 65 | Thông báo 07-TB/TW, 9-5-1969, BBT (14-3), nội thương | entered: cal.1969-03-14.vietnam-hanoi |
| XXX, 72 | Chỉ thị 170-CT/TW, 10-5-1969, thi đua, Đại hội Anh hùng lần thứ V | entered: cal.1969-05-10.vietnam-hanoi-2 |
| XXX, 76 | Đề cương báo cáo về mặt trận đấu tranh ngoại giao (Hội nghị lần thứ 16, 8-10/5) | cited in cal.1969-05-08.vietnam-hanoi (the plenum) |
| XXX, 118 | Nghị quyết BCT 188-NQ/TW, 10-5-1969, tình hình và nhiệm vụ | entered: cal.1969-05-08.vietnam-hanoi (the Sixteenth Plenum) |
| XXX, 144 | Bài nói của đồng chí Lê Duẩn tại Hội nghị lần thứ 16, tháng 5-1969 | cited in cal.1969-05-08.vietnam-hanoi |
| XXX, 171 | Chỉ thị 171-CT/TW, 12-5-1969, sinh hoạt chính trị mừng thọ Hồ Chủ tịch | entered: cal.1969-05-12.vietnam-hanoi |
| XXX, 177 | Nghị quyết BBT 189-NQ/TW, 22-5-1969, Ban Nghiên cứu kinh tế nông thôn miền Nam | entered: cal.1969-05-22.vietnam-hanoi |
| XXX, 179 | Nghị quyết BCT 191-NQ/TW, 24-5-1969, quy hoạch Thủ đô Hà Nội | entered: cal.1969-05-24.vietnam-hanoi |
| XXX, 188 | Điện BBT, 27-5-1969, gửi Bảy Cường, đấu tranh chính trị | entered: cal.1969-05-27.vietnam-hanoi |
| XXX, 189 | Điện BBT số 111, 9-6-1969, Chính phủ Cách mạng lâm thời | entered: cal.1969-06-09.vietnam-hanoi |
| XXX, 192 | Thông tri 235-TT/TW, 10-6-1969, ủng hộ Chính phủ Cách mạng lâm thời | entered: cal.1969-06-10.vietnam-hanoi |
| XXX, 196 | Thông tri 236-TT/TW, 13-6-1969, giải thể Bộ Tư lệnh giao thông vận tải Khu IV | entered: cal.1969-06-13.vietnam-hanoi |
| XXX, 198 | Thông báo 09-TB/TW, 14-6-1969, BBT và Thường vụ HĐCP (28-4 đến 3-5), kế hoạch 1970 | entered: cal.1969-04-28.vietnam-hanoi |
| XXX, 206 | Thông tri 237-TT/TW, 18-6-1969, điều tra tội ác Mỹ | entered: cal.1969-06-18.vietnam-hanoi |
| XXX, 209 | Thông tri 238-TT/TW, 18-6-1969, Điều lệ hợp tác xã | entered: cal.1969-06-18.vietnam-hanoi-2 |
| XXX, 212 | Nghị quyết BCT 190-NQ/TW, 19-6-1969, giúp Đảng X (Lào) | entered: cal.1969-06-19.vietnam-hanoi |
| XXX, 219 | Thông tri 239-TT/TW, 25-6-1969, thiếu niên, nhi đồng | entered: cal.1969-06-25.vietnam-hanoi |
| XXX, 222 | Nghị quyết BCT "1733"-NQ/TW, 9-8-1969, tổ chức thuộc Hội đồng Chính phủ | entered: cal.1969-08-09.vietnam-hanoi (a Check on the number) |
| XXX, 225 | Thông tri 240-TT/TW, 14-8-1969, kỷ niệm Cách mạng Tháng Tám | passed over: a commemoration |
| XXX, 228 | Thông cáo đặc biệt, 4-9-1969 (Nhân Dân, 5-9) | entered: cal.1969-09-04.vietnam-hanoi; its note (228–29 n.) the source of cal.1969-09-02.vietnam-hanoi |
| XXX, 232 | Lời kêu gọi của BCH, 3-9-1969 (Nhân Dân, 5-9) | entered: cal.1969-09-03.vietnam-hanoi |
| XXX, 237 | Danh sách Uỷ ban Lễ tang Nhà nước (Nhân Dân, 5-9) | cited in cal.1969-09-04.vietnam-hanoi |
| XXX, 240 | Chỉ thị BCT 172-CT/TW, 4-9-1969, Lễ quốc tang; khẩu hiệu, quy định, chương trình (5-9) | entered: cal.1969-09-04.vietnam-hanoi-2 |
| XXX, 253 | Di chúc: các bản in nguyên văn bản thảo (1965, 1968, 10-5-1969) | entered: cal.1968-05.vietnam-hanoi (the 1968 draft) and cal.1969-05-10.vietnam-hanoi (the last part); the 1965 draft, before the span of this volume, named there |
| XXX, 313 | Di chúc công bố năm 1969 | cited in cal.1969-05-10.vietnam-hanoi |
| XXX, 321 | Điếu văn của BCH, do Lê Duẩn đọc, 9-9-1969 | entered: cal.1969-09-09.vietnam-hanoi |
| XXX, 328 | Thông báo 14-TB/TW, 4-12-1969, Quyết định BCT (sáng 29-11), thi hài và lăng Hồ Chủ tịch | entered: cal.1969-11-29.vietnam-hanoi |
| XXX, 330 | Chỉ thị BCT 173-CT/TW, 29-9-1969, học tập và làm theo Di chúc | entered: cal.1969-09-29.vietnam-hanoi |
| XXX, 337 | Thông tri 241-TT/TW, 6-10-1969, Ban Tài chính thương nghiệp | entered: cal.1969-10-06.vietnam-hanoi |
| XXX, 339 | Điện BBT số 00, 24-10-1969, đấu tranh chính trị ở miền Nam | entered: cal.1969-10-24.vietnam-hanoi |
| XXX, 342 | Thông báo 12-TB, 29-10-1969, BBT (24-25/10), đời sống ở thành phố 1970 | entered: cal.1969-10-24.vietnam-hanoi-2 |
| XXX, 350 | Nghị quyết BCT 194-NQ/TW, 20-11-1969, giặc Mỹ lái máy bay bị bắt | entered: cal.1969-11-20.vietnam-hanoi |
| XXX, 353 | Thông tri 242-TT/TW, 21-11-1969, lối sống cần, kiệm, liêm | entered: cal.1969-11-21.vietnam-hanoi |
| XXX, 357 | Thông tri 244-TT/TW, 6-12-1969, ba ngày kỷ niệm tháng 12 | passed over: a commemoration |
| XXX, appendix | Phụ lục: Thư của BCH, 12-2-1969, gửi Đại hội XXIII Đảng Cộng sản Đan Mạch | entered: cal.1969-02-12.vietnam-hanoi |
| XXX, appendix | Phụ lục: Thư của BCH, 2-8-1969, gửi Đại hội X Đảng Cộng sản Rumani | entered: cal.1969-08-02.vietnam-hanoi |
| XXX, appendix | Phụ lục: Thư của BCH, 12-11-1969, gửi Đại hội XXXI Đảng Cộng sản Anh | entered: cal.1969-11-12.vietnam-hanoi |
| XXX, appendix | Phụ lục: Nghị quyết Hội nghị TƯC lần thứ chín, tháng 7-1969 | entered: cal.1969-07.vietnam-hanoi (a Check on the month) |
| XXX, appendix | Phụ lục: Nghị quyết Thường vụ TƯC 12-NQNT, 5-10-1969, bộ máy Chính phủ Cách mạng lâm thời | entered: cal.1969-10-05.vietnam-hanoi |
| XXX, appendix | Phụ lục: Nghị quyết Thường vụ TƯC 14-NQNT, 30-10-1969, chiến tranh du kích | entered: cal.1969-10-30.vietnam-hanoi |
| XXX, appendix | Phụ lục: Nghị quyết Hội nghị Khu uỷ V lần thứ chín, tháng 4-1969, giành dân | entered: cal.1969-04.vietnam-hanoi |
| XXX, appendix | Phụ lục: Nghị quyết Khu uỷ V 08-NQKUV, tháng 4-1969, xây dựng đảng | entered: cal.1969-04.vietnam-hanoi-2 |
| XXX, appendix | Phụ lục: Nghị quyết Khu uỷ V, "tháng 4 năm 1969," kế hoạch một năm xây dựng Khu A | passed over: misdated; its matter runs to February 1970 ("từ đầu năm 1970 đến nay," "đến tháng 2-1970"), so 1970, outside the span; a lead |

### Where batch 16 stopped (1968–69)

Both volumes done, every document read at its heading, date, issuer, signer, operative sections and close (the long reports as above), to the last page of each copy (XXIX, PDF 387; XXX, PDF 267): 82 documents in vol. 29 (69 entered, 7 cited on 4 entries held, 6 passed over) and 56 headings in vol. 30 (46 rows entered as 48 entries, 4 cited within those entries, 6 passed over). Passed over: 9 commemorations, Region V's undated economic resolution of 1968 and its misdated "April 1969" resolution on Area A (1970): the last two for leads. Stopped cleanly, the patch checked to 0 errors. No witnesses file.

### Audit (batch 16, 1965–66)

Auditor: batch 16, Nov. 14, 2026 (a Saturday), `inbox/2026-11-14-b16-vkd-1965-66.yaml` (117 ops). Corrected patch: `inbox/2026-11-14-b16-vkd-1965-66-audited.yaml` (patch name kept, `2026-11-14-b16-vkd-1965-66`; 121 ops; patch-check 0 errors, 40 warnings, all the same-day "one event?"/duplicate prompts for separate documents). Both PDFs fetched afresh (358 and 228 PDF pages, title pages "Hà Nội - 2003"), split into halves as the reader did; the offset (2 × PDF − 6 left, − 5 right) confirmed. Every entry's heading checked by script against the volume (number, issuing body, day, signer, first and last page); the `c` lines sampled in every month against the text.

- Upheld as written: 76 adds. Corrected: 26 (15 by the signer's `name:` tag alone, `name:le-duc-tho`, `name:truong-chinh`, `name:le-duan`, the keys the calendar uses; Tố Hữu, Phạm Hùng, Lê Văn Lương have none). Text: `cal.1965-03-03.vietnam-hanoi` (signer, Tố Hữu, added); `cal.1965-12-28.vietnam-hanoi` (634–39, not 642: 640 is blank, 641 the appendix's title); `cal.1966-06-01.vietnam-hanoi` (forty-five years of the party's rule, not "after the Revolution"); `cal.1966-08-29.vietnam-hanoi` (the exemptions and deferments of instruction no. 48 and decision no. 63 to be kept, not "studied"; the Check rewritten: the July call-up and decision no. 158 need not conflict); Hồ Chí Minh's three speeches (`cal.1965-01-22`, `cal.1966-01-16`, `cal.1966-04.vietnam-hanoi`): the volume prints them from his *Toàn tập* (2002, 2000, 2000), so "Made public" is that print, not 2003.
- Dropped: `cal.1965-12-21.vietnam-hanoi` and `-2` (the Politburo's report and Lê Duẩn's speech to the Twelfth Plenum, no day of their own: cites on the plenum's entry, as batch 12 entered its plenums, one session one entry); `cal.1966-06-22.vietnam-hanoi` (circular no. 182-TT/TW: the observance's plan, a meeting, a week of propaganda, films, an exhibition; no policy act beyond the commemoration: passed over with the batch's other anniversaries).
- The Eleventh Plenum: the volume settles Mar. 25–27 (the resolution's heading, XXVI, 96; the outline, 56; the introduction): a `variant` on `cal.1965-03-28.vietnam`, unit A. The outline report names no author (not "the Politburo's"). The Twelfth: Dec. 21–27 (XXVII, 35 n.; the closing speech "chiều ngày 27", XXVI, 626); the introduction to vol. XXVI has Dec. 21–26, not 21–27 as the reader's notes give: a `variant` on `cal.1965-12-27.vietnam-2`, unit A. Lê Duẩn's speech: the forecast of 150–200,000 and 300–400,000 troops is the Ninth and Eleventh Plenums' (542), not the Eleventh's alone.
- The held entries' cites rewritten to one pinpoint and one parenthetical each, with units: the resolution of the Twelfth B–D, Lê Duẩn's speech B, the report and the closing speech `?`; the Eleventh's outline A. The check on `cal.1966-07-16.vietnam` dropped (the entry already dates the appeal July 17). A `variant` on `cal.1965-01-02.vietnam-hanoi`: the volume's "chưa được khắc phục một cách triệt để" (not thoroughly overcome), XXVI, 3, against Asselin's "not yet successfully overcome".
- The five greetings (Italy, Canada, Mongolia, the CPUSA, Japan): the volume prints each from the Party archive; whether *Nhân Dân* printed them is not settled here (the custom: XXVII, 220 has the press print the greeting to the Chinese party). Under the owner's ruling of Nov. 14 (territorial visibility; a ruling party counts as government) each is `vis:only:drv+<the congress's country>`, "Made public: 2003.", the parties' `polity:` tags dropped (Mongolia's kept), with a Check on where the congress met, whether the greeting was read there and whether *Nhân Dân* printed it.

### Audit (batch 16, 1968–69)

Auditor: Claude (Opus), Nov. 14, 2026 (a Saturday). Corrected patch: `inbox/2026-11-14-b16-vkd-1968-69-audited.yaml` (patch name the reader's, `2026-11-14-b16-vkd-1968-69`, so the ledger's claims hold; 128 ops: 113 adds, 8 cites, 2 variants, 5 checks; `./bib patch-check` 0 errors, 33 warnings, all the same-day "one event?"/duplicate prompts for separate documents, and the ledger's claims of `2026-11-14-b16-lskc-3` on Apr. 28, May 8 and Sept. 4, 1969, which are other acts). The reader's file left in place. Both PDFs fetched afresh (387 and 267 PDF pages; "Microsoft Word - VK Dang TT - Tap 29", printed to PDF by PScript5 and Ghostscript 8.15, Mar. 7, 2019), split into halves, the TCVN3 table of `tools/vn/vkd2txt.py`; vol. 24's copy fetched as well for its jump. Every add's heading, number, day, issuing body, signer and first and last folio checked by script against the copy; `c` read against the text in every month (Jan. 21, Feb. 8 and 10, May 8 and 17, July 4 and 16, Aug. 1968, Oct. 20, Dec. 1968; Feb. 11, May 27, June 19, the COSVN conference of July, the testament, Sept. 2–4, Oct. 24, Nov. 29 and the three greetings of 1969, and the figures of Sept. 25, 1968, Jan. 13, Mar. 14 and Apr. 28, 1969). PDFs and texts deleted.

**The pages.** What is certain:

- The jumps are the copy's own folios, not the converter's: the page images print them (PDF 122: "387" over the last page of directive no. 158, under the running head of notice no. 07, which begins on the facing page). The copy is not a scan of the print but a re-set Word text, its folios Word's own: the front matter is numbered −6, −4, −3, −2, 0; each jump falls at a section break a page before a document (the restart's running head already the next document's); the running heads themselves are the file's, not the print's (vol. 30's pages of February 1969 headed "di chúc của chủ tịch hồ chí minh"); and vol. 24's copy, from the same maker, jumps 776→863 at the very same numbers. So no rebound or misnumbered printing: an artifact of the e-text.
- The print's pages, where they are known (vol. 29): circular no. 220 begins at 324 (vol. 30's editors, the copy's XXX, 196 n.; the copy's folio 587); the Politburo's cable of Oct. 10 at 468 (the editors' own note, the copy's 964 n.) and 468–74 (Nguyen, 124 n.57; the copy's 940–48); its cable to COSVN of Oct. 20, 484–87 (Nguyen, 127 n.66; the copy's 960–63); circular no. 224 begins at 554 (vol. 30's editors, the copy's XXX, 335 n.; the copy's 1020). Vol. 30: the editors' note on a passage perhaps lost in COSVN's ninth conference stands at 365 (their own reference, the copy's PDF 183R).
- No consistent mapping can be derived. Counting the copy's pages in order (book = 2 × PDF − 7 on the right, − 8 on the left), the four points of vol. 29 fall at 338, 489, 509 and 569 against the print's 324, 468, 484 and 554: the copy runs 14, 21, 25 and 15 pages ahead, its density against the print's changing document by document (Oct. 10–20: 20 copy pages to 16 printed; Oct. 20–Dec. 12: 60 to 70). Any re-paging off those points would be off by up to ten pages. Vol. 30: the count gives 361 for the print's 365, so its folios 1–265 run within a few pages of the print, and those from 313 (the jump at the testament as published) some 43–47 ahead of it; no printed facsimile can fill the gap, since the editors' 365 falls 47 pages short of where the copy's numbering would put it.
- The other copies of this maker drift the same way, by the editors' cross-references in vols. 29–30: vol. 26, no. 99-CT/TW at 198 in the print (copy 190), no. 100 at 204 (copy 196), resolution no. 123 at 277 (copy 267), directive no. 105 at 332 (copy 318); vol. 27, nos. 137 and 180 at 101 and 157 (the copy the same) but no. 183 at 256 (copy 252); vol. 24, the Ninth Plenum's resolution at 716 (copy 691). The iTextSharp copies agree with the print: vol. 23, no. 53 at 507; vol. 28, nos. 143, 149, 150 at 201, 276, 297, though no. 207 is 493 by the editors and 468 in that copy. **Vol. 24 wants nothing at 777–862**: PDF 388R ends the Ninth Plenum's communiqué (the copy's 768–76, after the international resolution, 691–767) and PDF 389L opens the resolution on the South at "863"; in the print Asselin has the international resolution at 716–800 and the resolution on the South at 811–62 (Nguyen, 716–810, for the former), so the copy's resolution and communiqué fill the print's 716–810 and nothing stands between them and the resolution on the South: the batch-12 note on missing pages should be withdrawn.

How the cites read, as proposed and done: every cite of vols. XXIX and XXX gives the copy's folio, as the reader gave it, except where the print's page is established: `cal.1968-08-02.vietnam-hanoi` (XXIX, 324), `cal.1968-12-12.vietnam-hanoi` (XXIX, 554), the held `cal.1968-10-10.vietnam-paris` (XXIX, 468–74) and `cal.1968-10-20.vietnam-paris` (XXIX, 484–87), each "the print's", the copy's folios in the parenthetical. For the card (not edited here), proposed: "Vols. XXIV, XXVI, XXVII, XXIX and XXX are cited by the folios of the copies read (re-set Word texts printed to PDF in 2019, on the Drive), not the print's pages, from which they drift by up to some 25 pages, and by more after the copies' own jumps (XXIX from 223, XXX from 265); the print's page, where known, is so marked." A re-paging needs the printed volumes.

**Adds.** 117 read: 90 upheld, 23 corrected, 4 dropped, none turned into a cite (no add repeats an act the calendar holds: the 1968 `vietnam`, `vietnam-tet`, `vietnam-paris`, `vietnam-operations`, `vietnam-air-war`, `vietnam-diplomacy` entries and the 1968–69 `china-leadership` and `soviet-union-leadership` ones searched; the calendar's Vietnam threads stop at Jan. 18, 1969; the ledger's `lskc-3` claims for 1969 are other acts).

- Dropped (ledger marked "not used ..., audit b16"): `cal.1968-05-17.vietnam-hanoi`, the Politburo's cable no. 253 to Region IX: misdated in the volume, its matter of 1970 ("Việt Nam hoá chiến tranh"; the enemy has lately carried the war into Cambodia to save "the reactionaries of K"), outside the span, a lead for 1970; `cal.1968-01-12.vietnam-hanoi` (cable no. 06 to Vĩnh Linh on its own work), `cal.1968-07-04.vietnam-hanoi` (cable no. 21 answering Vĩnh Linh's secretary) and `cal.1969-01-17.vietnam-hanoi-2` (notice no. 06, the plans of Sơn La, Nghĩa Lộ and Lai Châu): provincial matters, passed over (R18; the ruling of Nov. 12). Kept as more than local: the cables on transport through Region IV (June 13, July 26, 1968), the Red River flood (Aug. 11), the Trị–Thiên–Huế committee (Oct. 16), Hanoi's master plan (May 24, 1969).
- Signers' tags added: `name:le-duc-tho` (Jan. 16 twice, Feb. 10, 1968; Aug. 9, 1969; the cable of Dec. 1968, signed "Thọ"), `name:truong-chinh` (Mar. 1, 1968), `name:le-duan` (Oct. 16, 1968), `name:nguyen-duy-trinh` (June 19, 1969, its signer supplied); `name:ngo-minh-loan` (FRUS's DRV ambassador at Peking, Aug. 9, 1969). Signers supplied: Oct. 24, 1969 (Lê Văn Lương), Oct. 24–25 (Trần Xuân Bách), Nov. 29 (Lê Văn Lương).
- Pages: COSVN's sixth conference 1275–1313 (1314 is the letter to Moscow); notice no. 21, 1171–79; the appeal of July 20, 571–74.
- `cal.1968-10-20.vietnam-hanoi`: the cable does not say it follows that of Oct. 10 (the editors' comparison, kept in the note); `c` gives its own words.
- `cal.1968-12.vietnam-hanoi`: kept at the volume's date with the Check, now noting the signer "Thọ" (Lê Đức Thọ, in Hanoi in February 1968, before he left for Paris in June: `cal.1968-06-03.vietnam-paris`); its matter is the Tết offensive's first weeks. Not redated: the volume dates it, and nothing outside the volume does.
- The testament: `cal.1969-05-10.vietnam-hanoi` no longer says the 1969 text "omits" anything: it names the two printings, the drafts printed whole (XXX, 255–65) and the testament as published in 1969 (313–20), and says the drafts ask for cremation and the published text does not; the 1965 draft asks for the ashes buried on a hill near Tam Đảo or Ba Vì and some sent to the South (258–59), not divided in three, which is the 1968 pages' (261). `cal.1968-05.vietnam-hanoi`: the pages written at 78 (260–61, undated, "absolutely secret") and the added pages of May 1968 (262–64) told apart. Both with a Check: whether the drafts were first published with the Politburo's notice no. 151-TB/TW of Aug. 19, 1989 (XXX, 228 n.).
- Hồ's death: `cal.1969-09-02.vietnam-hanoi` kept, Sept. 2, 9:47 a.m., announced as Sept. 3, from the notice of 1989 the editors quote (229 n.); "Made public: 1989." The call of Sept. 3 now gives the announced day as announced. A Check on the held `cal.1969-09-03.china-leadership` ("Hồ Chí Minh dies in Hanoi") gives the day now established.
- The greetings (the owner's ruling of Nov. 14): Denmark `vis:only:drv+denmark`, Britain `vis:only:drv+uk`, no polity tag for either party; Romania, a ruling party, `vis:only:drv+romania`, `polity:romania` kept; each "Made public: 2004." (from the Party archive) and a Check on where the congress met, whether the greeting was read there and whether *Nhân Dân* printed it. The British letter also thanks the party for Gollan's delegation to Hồ's funeral (added).
- Held entries: the Fourteenth Plenum's one cite split into three (the resolution, 51, unit A; Lê Duẩn's speech, 1–41, and the Planning Commission's report, 69–161, units `?`); the cites of the appeals of July 20 and Nov. 3 give their quotations in translation only; the Oct. 10 variant's quotation in translation; the reader's Checks on Oct. 10 and 20 rewritten (the year, 2004; the copy's folios not the print's); the Check on `cal.1968-02.vietnam` (169–72).
- Upheld as flagged: the misdated Region V resolution of "April 1969" (its matter 1970) passed over; COSVN's ninth conference at July 1969 with its Check ("early July" in its text, August in COSVN's of Oct. 5; the "Hồ Chí Minh class" drive "just past"); the number "1733" with its Check; the Sixteenth Plenum one entry of its three documents; resolution no. 185 on its session's days.

Persons named with no name entry (and none in `sources/frus-names`): as the reader listed, less Ngô Minh Loan (tagged), and John Gollan added.
