# Changelog

## v1.0.3 — 2026-10-18

### Thêm

- Mở chặn Mind Pilot (`com.oplus.aiassistant`) bên cạnh Oppo Messages (`com.android.mms`) nếu APK có sẵn trong ROM.
- Kiểm thử danh sách cho phép: chỉ đổi thẻ `disable` thành `enable` cho đúng hai package; giữ nguyên package tên gần giống, comment và các quy tắc khác.
- Build ZIP với LF, quyền Unix thống nhất và checksum SHA-256; GitHub Release kèm ghi chú phát hành.

### Sửa lỗi so với v1.0.1

- Bỏ XML cố định từng ghi đè lên nhiều phân vùng, gây mất Mind Space, Omoji và Quick Share extension trên ROM đã kiểm tra.
- Tạo bản vá riêng từ cấu hình gốc hiện tại của từng phân vùng; chỉ bind-mount khi có thay đổi được hỗ trợ.
- Bỏ toàn bộ cơ chế ghi đè `feature_rsa*.xml`, giữ nguyên khai báo tính năng và ứng dụng mặc định của ROM.
- Bỏ lệnh tắt Google Messages, vòng lặp sửa hồ sơ nhân bản/công việc và xóa package cache toàn hệ thống.
- Giữ SELinux context của XML gốc. Định dạng quy tắc chưa hỗ trợ được bỏ qua thay vì thay bằng cấu hình cố định.
- Giữ lựa chọn SMS khi nâng cấp; lần cài mới chỉ thiết lập SMS user 0 một lần.
- Sửa thông tin phiên bản/tác giả trong installer và báo lỗi nếu thiếu hàm cài module.

### Xác minh

- 7 nhóm kiểm thử tự động đạt.
- Cài và reboot trên OnePlus CPH2745, ROM `CPH2745_16.0.10.601(EX01)`, KernelSU-Next.
- So với v1.0.2: user 0 chỉ thêm Mind Pilot, không mất package; user 998/999 không thêm hoặc mất package. Danh sách ứng dụng bị tắt và SMS role giữ nguyên sau khi máy ổn định.
- Product và feature giữ nguyên; stock chỉ mở chặn đúng hai package; log module không có lỗi.
- Chưa kiểm thử tác vụ AI hoặc gửi/nhận SMS/OTP thực tế; chưa xác minh trên root manager/ROM khác.

`versionCode=202` để cao hơn bản cài cũ mang `versionCode=200`.

## v1.0.2 — 2026-10-18 (bản sửa nội bộ, không phát hành tag)

- Sửa lỗi ghi đè chéo phân vùng, khôi phục quy tắc OEM và chỉ mở chặn Oppo Messages.
- Khôi phục Mind Space, Omoji và Quick Share extension trên máy đã kiểm tra.
- Bỏ tác động lên Google Messages và hồ sơ khác; thêm công cụ đối chiếu cấu hình và kiểm thử.

## v1.0.1

- Bản phát hành đầu tiên, mở Oppo Messages bằng XML cố định và tự tắt Google Messages.
- Cách ghi đè cấu hình của bản này có thể làm mất ứng dụng/tính năng hệ thống; nên nâng cấp lên v1.0.3.
