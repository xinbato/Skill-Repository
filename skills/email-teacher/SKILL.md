---
name: email-teacher
description: Soạn thảo email và thông điệp chuẩn mực gửi giảng viên, thầy cô giáo về các vấn đề học tập (xin nghỉ học, xin phép vắng mặt, xin gia hạn nộp bài tập lớn/đồ án/deadline, hoặc hỏi bài, giải đáp thắc mắc bài giảng). Tự động kích hoạt ngay cả khi người dùng không dùng từ khóa "email" (ví dụ "xin nghỉ học hôm nay", "nhờ thầy dời hạn nộp bài", "hỏi cô câu hỏi lab 3", "sick leave note for teacher", "ask professor for deadline extension"). Mẫu quy chuẩn bằng tiếng Việt và tự động thích ứng theo ngôn ngữ của người dùng.
---

# Email Teacher (Soạn Thư Gửi Giảng Viên / Thầy Cô)

## Tổng quan
Skill này hướng dẫn AI Agent soạn thảo thư tín / email học thuật gửi đến thầy cô giáo, giảng viên đại học/cao đẳng một cách chuẩn mực, lễ phép và chuyên nghiệp.

Đặc điểm nổi bật:
- **Đa dạng ngôn ngữ (Multi-language Adaptation)**: Mẫu quy chuẩn được định nghĩa bằng tiếng Việt nhưng Agent **bắt buộc thích ứng theo ngôn ngữ của người dùng** (Tiếng Việt, Tiếng Anh, Tiếng Nhật, v.v.) hoặc ngôn ngữ được yêu cầu.
- **Kích hoạt không cần chữ "email"**: Tự động nhận diện ý định liên hệ thầy cô khi người dùng nói về xin nghỉ, xin gia hạn, hỏi bài.
- **Đầy đủ dữ liệu nhận diện**: Đảm bảo luôn có MSSV, Mã lớp/Lớp học phần, Tên môn học, Lý do rõ ràng và Tiêu đề chuẩn.

---

## Khi nào kích hoạt Skill (Triggers)
Kích hoạt skill khi người dùng có ý định trao đổi với thầy cô, giảng viên, **ngay cả khi KHÔNG có chữ "email"** trong câu hỏi:

1. **Xin nghỉ học / vắng mặt:**
   - *"Mai em bị ốm xin thầy cho em nghỉ học một buổi"*
   - *"Thầy ơi hôm nay nhà em có việc đột xuất không lên lớp được"*
   - *"I have a fever and need to miss tomorrow's lecture"*
2. **Xin gia hạn bài tập / deadline / nộp muộn:**
   - *"Xin cô cho nhóm em lùi deadline bài tập lớn sang tuần sau"*
   - *"Máy tính bị hỏng nên chưa kịp nộp lab, nhờ thầy cho em nộp muộn"*
   - *"Can I request a deadline extension for Assignment 2 from Dr. Smith?"*
3. **Hỏi bài / thắc mắc kiến thức / đồ án:**
   - *"Em chưa hiểu thuật toán A* thầy giảng hôm trước, nhờ thầy giải thích lại"*
   - *"Em gặp lỗi khi chạy code đồ án, muốn xin thầy lịch hẹn tư vấn"*
   - *"I have a question about slide 12 of the database lecture"*

---

## Các thông tin BẮT BUỘC phải có trong thư

Giảng viên thường quản lý hàng trăm sinh viên mỗi kỳ, do đó một bức thư đạt chuẩn phải bao gồm:

1. **Tiêu đề thư (Subject Line)**: Rõ ràng, tuân theo quy tắc:
   `[Tên Môn Học/Mã Môn] - [Mã Lớp Học Phần] - [MSSV - Họ và tên] - [Mục đích thư]`
2. **Lời chào trang trọng (Salutation)**: Kính gửi Thầy/Cô kèm tên hoặc học hàm (GS/PGS/TS/ThS).
3. **Thông tin nhận diện sinh viên (Student Info)**:
   - Họ và tên sinh viên
   - Mã số sinh viên (MSSV)
   - Lớp sinh hoạt / Lớp học phần / Nhóm thực hành
4. **Nội dung & Lý do cụ thể (Core Message & Reason)**: Trình bày sự việc trung thực, ngắn gọn, đi thẳng vào vấn đề.
5. **Kế hoạch khắc phục / Cam kết (Action Plan)**:
   - Nếu xin nghỉ: Tự học bài qua slide, mượn vở bạn, hoàn thành bài tập buổi nghỉ.
   - Nếu xin gia hạn: Báo cáo tiến độ hiện tại, lý do khách quan, cam kết mốc thời gian nộp bài chính xác.
   - Nếu hỏi bài: Tóm tắt điểm đã hiểu, nêu cụ thể khúc mắc và các phương án đã thử tự giải quyết.
6. **Lời cảm ơn & Lời chúc (Formal Sign-off)**: Lịch sự, bày tỏ lòng biết ơn đối với thời gian của thầy/cô.
7. **Chữ ký cuối thư (Signature)**: Tên, MSSV, SĐT, Email sinh viên.

---

## Nguyên tắc thích ứng Đa ngôn ngữ (Language Adaptation Rule)

1. **Phát hiện ngôn ngữ**:
   - Nếu người dùng nhập tiếng Việt -> Xuất email bằng **Tiếng Việt**.
   - Nếu người dùng nhập tiếng Anh (hoặc yêu cầu tiếng Anh) -> Xuất email bằng **Tiếng Anh**.
   - Nếu người dùng nhập ngôn ngữ khác (Pháp, Nhật, Hàn...) -> Xuất email bằng chính **ngôn ngữ đó**.
2. **Chuẩn hóa văn phong bản địa**:
   - **Tiếng Việt**: Xưng *"Em"*, gọi *"Thầy/Cô"*, lời chào *"Kính gửi Thầy/Cô..."*, lời kết *"Kính chúc Thầy/Cô..."*.
   - **Tiếng Anh**: Xưng *"I"*, gọi *"Dear Professor [Họ]/Dear Dr. [Họ]"*, tránh dùng "Hey/Hi teacher", lời kết *"Sincerely / Respectfully"*.
   - **Tiếng Nhật**: Dùng kính ngữ sonkeigo/kenjougo, gọi `[Họ] 先生`, mở đầu `いつもお世話になっております`, kết `よろしくお願い申し上げます`.

---

## Quy trình thực hiện của Agent (Step-by-Step)

```text
[Người dùng gửi yêu cầu]
         │
         ▼
[Bước 1: Xác định Ngôn ngữ & Mục đích (Nghỉ học / Gia hạn / Hỏi bài)]
         │
         ▼
[Bước 2: Trích xuất thông tin (Tên, MSSV, Lớp, Môn, Lý do)]
         │ (Nếu người dùng chưa cung cấp đủ, sử dụng placeholder [IN HOA] nổi bật)
         ▼
[Bước 3: Chọn cấu trúc chuẩn & bản địa hóa văn phong phù hợp]
         │
         ▼
[Bước 4: Tạo bức thư hoàn chỉnh (Tiêu đề + Thân bài + Chữ ký) & Ghi chú nhắc nhở đính kèm minh chứng]
```

---

## Các Mẫu Quy Chuẩn (Templates)

### Mẫu 1: Xin phép nghỉ học / vắng mặt (Leave of Absence)

#### Bản Tiếng Việt:
```text
Tiêu đề: [Mã Môn Học - Tên Môn] - [Mã Lớp HP] - [MSSV] - [Họ và Tên] - Xin phép vắng mặt buổi học ngày [DD/MM/YYYY]

Kính gửi Thầy/Cô [Họ và tên Giảng viên],

Em tên là: [Họ và Tên Sinh Viên]
Mã số sinh viên: [MSSV]
Hiện đang theo học môn [Tên Môn Học], mã lớp [Mã Lớp Học Phần], ca học [Thứ / Tiết học].

Em viết thư này kính xin phép Thầy/Cô cho em được vắng mặt trong buổi học ngày [Thứ..., ngày DD/MM/YYYY] vì lý do: [Lý do cụ thể, ví dụ: bị sốt xuất huyết phải điều trị theo chỉ định của bác sĩ / gia đình có việc hiếu đột xuất].

Trong thời gian nghỉ, em cam kết sẽ:
1. Tự ôn tập kiến thức qua slide bài giảng và giáo trình.
2. Mượn vở ghi chép của các bạn trong lớp để bổ sung bài học.
3. Hoàn thành đầy đủ bài tập được giao cho buổi học này.

(Nếu có minh chứng: Em xin gửi đính kèm giấy chứng nhận y tế/giấy xác nhận của cơ sở y tế để Thầy/Cô xác thực ạ.)

Em kính mong Thầy/Cô thông cảm và tạo điều kiện cho em. Em xin chân thành cảm ơn Thầy/Cô!

Kính chúc Thầy/Cô luôn dồi dào sức khỏe và công tác tốt.

Kính thư,
[Họ và Tên Sinh Viên]
MSSV: [MSSV]
Lớp: [Mã Lớp Sinh Hoạt / Lớp HP]
Số điện thoại: [Số điện thoại]
Email: [Email sinh viên]
```

#### Bản Tiếng Anh tương ứng (Reference):
```text
Subject: [Course Code - Course Title] - [Class Section] - [Student ID] - [Full Name] - Absence Request for [Date]

Dear Professor [Instructor's Last Name],

My name is [Full Name], Student ID: [Student ID], currently enrolled in your [Course Title] class (Section: [Class Section], scheduled on [Day/Time]).

I am writing this email to respectfully request permission to be absent from class on [Date] due to [Reason, e.g., unexpected illness / doctor-advised medical care / family emergency].

To ensure I do not fall behind, I have arranged to:
1. Review the lecture slides and assigned readings thoroughly.
2. Borrow notes from my classmates to catch up on discussion points.
3. Complete and submit all coursework assigned for that session on time.

(Attached is my medical certificate for your review.)

Thank you very much for your time and understanding.

Sincerely,
[Full Name]
Student ID: [Student ID]
Class: [Class Section]
Phone: [Phone Number]
Email: [Student Email]
```

---

### Mẫu 2: Xin gia hạn nộp bài / nộp muộn (Deadline Extension)

#### Bản Tiếng Việt:
```text
Tiêu đề: [Mã Môn Học - Tên Môn] - [Mã Lớp HP] - [MSSV] - [Họ và Tên] - Đơn xin gia hạn nộp [Tên Bài Tập/Đồ Án]

Kính gửi Thầy/Cô [Họ và tên Giảng viên],

Em là: [Họ và Tên Sinh Viên], MSSV: [MSSV]
Thành viên nhóm: [Tên Nhóm - nếu có]
Hiện đang tham gia lớp học phần [Tên Môn Học], mã lớp [Mã Lớp].

Theo lịch trình của môn học, hạn nộp [Tên Bài Tập/Đồ Án] là vào lúc [Giờ, Ngày DD/MM/YYYY]. Tuy nhiên, em/nhóm em viết thư này kính xin Thầy/Cô xem xét cho phép em/nhóm em được gia hạn thời gian nộp bài đến: [Giờ, Ngày mới mong muốn].

Lý do xin gia hạn:
[Trình bày lý do trung thực, rõ ràng, ví dụ: Thiết bị thu thập dữ liệu bị lỗi kỹ thuật cần thời gian cấu hình lại / Thành viên phụ trách phần cốt lõi gặp sự cố sức khỏe đột xuất / Thuật toán gặp lỗi ngoại lệ cần thêm thời gian tối ưu hóa kết quả].

Tiến độ hiện tại của bài tập:
- Đã hoàn thành: [Nêu các phần đã làm được, ví dụ: 70% nội dung gồm báo cáo và giao diện].
- Phần đang hoàn thiện: [Nêu nội dung còn lại cần thêm thời gian].

(Em xin gửi đính kèm bản thảo/mã nguồn hiện tại để Thầy/Cô tiện theo dõi tiến độ.)

Em rất mong nhận được sự thông cảm và hướng dẫn của Thầy/Cô. Em xin chân thành cảm ơn Thầy/Cô!

Kính chúc Thầy/Cô nhiều sức khỏe.

Kính thư,
[Họ và Tên Sinh Viên]
MSSV: [MSSV]
Lớp: [Mã Lớp]
Số điện thoại: [Số điện thoại]
```

#### Bản Tiếng Anh tương ứng (Reference):
```text
Subject: [Course Code - Course Name] - [Class Section] - [Student ID] - [Full Name] - Request for Extension: [Assignment Name]

Dear Professor [Instructor's Last Name],

My name is [Full Name], Student ID: [Student ID], from your [Course Name] class (Section: [Class Section]).

I am writing to respectfully request an extension for [Assignment/Project Name], currently due on [Current Due Date]. If possible, I would be deeply grateful if the deadline could be extended until [Proposed New Date & Time].

Reason for request:
[Explain reason concisely, e.g., unexpected hardware failure / unforeseen medical issue / additional time needed to resolve critical edge-case bugs in data processing].

Current Progress:
- Completed: [e.g., 70% of the project, including theoretical background and base system architecture].
- Remaining tasks: [e.g., Final testing, bug fixing, and formatting the documentation].

(I have attached our current draft/codebase to demonstrate our ongoing work.)

Thank you very much for your understanding and consideration.

Sincerely,
[Full Name]
Student ID: [Student ID]
Email: [Student Email]
```

---

### Mẫu 3: Hỏi bài / Giải đáp thắc mắc chuyên môn (Academic Inquiry)

#### Bản Tiếng Việt:
```text
Tiêu đề: [Mã Môn Học - Tên Môn] - [Mã Lớp HP] - [MSSV] - [Họ và Tên] - Thắc mắc về [Nội dung câu hỏi/Bài giảng]

Kính gửi Thầy/Cô [Họ và tên Giảng viên],

Em tên là: [Họ và Tên Sinh Viên], MSSV: [MSSV]
Sinh viên lớp học phần [Tên Môn Học], mã lớp [Mã Lớp].

Trong quá trình tự học và làm bài tập môn học [Tên Môn Học] (thuộc [Chương / Buổi học số / Slide số]), em gặp phải một vấn đề chưa hiểu rõ và mong nhận được sự hướng dẫn của Thầy/Cô:

1. Vấn đề thắc mắc:
[Mô tả câu hỏi cụ thể, ví dụ: Em chưa hiểu rõ cách tính ma trận chuyển trạng thái trong bài toán X...]

2. Những bước em đã tự tìm hiểu:
- Em đã đọc lại giáo trình tại trang [Số trang] và slide bài giảng [Số slide].
- Em đã thử giải theo hướng [Mô tả ngắn gọn], nhưng kết quả bị [Lỗi / Không khớp với đáp án].

(Nếu có hình ảnh/code: Em xin gửi đính kèm ảnh chụp màn hình bài làm và thông báo lỗi để Thầy/Cô tiện theo dõi.)

Nếu câu hỏi cần trao đổi trực tiếp, em kính xin Thầy/Cô cho em biết khung giờ Thầy/Cô có thể tiếp sinh viên (office hours) để em có thể đến gặp Thầy/Cô ạ.

Em xin chân thành cảm ơn sự tận tình giúp đỡ của Thầy/Cô!

Kính chúc Thầy/Cô luôn dồi dào sức khỏe.

Kính thư,
[Họ và Tên Sinh Viên]
MSSV: [MSSV]
Lớp: [Mã Lớp]
Số điện thoại: [Số điện thoại]
```

#### Bản Tiếng Anh tương ứng (Reference):
```text
Subject: [Course Code - Course Name] - [Class Section] - [Student ID] - [Full Name] - Question regarding [Topic / Lecture #]

Dear Professor [Instructor's Last Name],

My name is [Full Name], Student ID: [Student ID], currently enrolled in your [Course Name] class (Section: [Class Section]).

While reviewing the material from [Lecture / Chapter / Slide #], I encountered a question regarding [Specific Concept/Problem] and would appreciate your guidance:

Question details:
[Brief and precise description of your query].

What I have investigated so far:
- I reviewed the textbook section on page [Page #] and lecture notes.
- I attempted to resolve it by [describe approach], but encountered [specific error or unexpected outcome].

(Attached is a screenshot of my code and error output for your reference.)

If this requires further discussion, please let me know if you have available office hours this week where I could meet with you.

Thank you very much for your time and guidance.

Sincerely,
[Full Name]
Student ID: [Student ID]
Email: [Student Email]
```

---

## Bảng Đối Chiếu Thuật Ngữ & Xưng Hô Đa Ngôn Ngữ

| Yếu tố | Tiếng Việt | Tiếng Anh | Tiếng Nhật |
| :--- | :--- | :--- | :--- |
| **Xưng hô giảng viên** | Thầy / Cô, Kính gửi Thầy/Cô | Professor [Name] / Dr. [Name] | [Họ] 先生 |
| **Tự xưng** | Em | I | 私 (わたし) |
| **Mã số sinh viên** | MSSV | Student ID | 学籍番号 (Gakuseki bangou) |
| **Lớp học phần** | Lớp học phần / Mã lớp | Class Section / Course Code | 受講クラス・講義コード |
| **Xin nghỉ học** | Xin phép vắng mặt / nghỉ học | Leave of Absence / Absence Request | 欠席届 (Kesseki-todoke) |
| **Xin gia hạn** | Xin gia hạn nộp bài / lùi hạn | Request for Deadline Extension | 提出期限延長のお願い |
| **Hỏi bài** | Thắc mắc kiến thức / hỏi bài | Question on Lecture / Course Query | 講義内容に関する質問 |
| **Lời kết** | Kính chúc Thầy/Cô sức khỏe... | Sincerely / Best regards | よろしくお願い申し上げます |

---

## Tiêu chí Kiểm tra (Quality Checklist)
Trước khi xuất kết quả cho người dùng, Agent kiểm tra:
- [ ] Tiêu đề có chứa đủ: Tên Môn Học + Mã Lớp + MSSV + Tên Sinh Viên + Mục đích.
- [ ] Lời chào mở đầu trang trọng, phù hợp xưng hô học thuật.
- [ ] Các thông tin thiếu được đánh dấu bằng placeholder rõ ràng (ví dụ `[MSSV]`, `[MÃ LỚP]`).
- [ ] Ngôn ngữ xuất ra trùng khớp với ngôn ngữ người dùng yêu cầu hoặc sử dụng trong câu hỏi.
- [ ] Văn phong lịch sự, khiêm tốn, đúng chuẩn mực sư phạm.
