# Phân tích lỗi mất Mind Space

## Bằng chứng trên thiết bị ngày 18/10/2026

- Máy: OnePlus CPH2745, build `CPH2745_16.0.10.601(EX01)`.
- Bản repository: v1.0.1. Bản đang cài báo v2.0, versionCode 200; hai script boot có cùng cách ghi đè gây lỗi.
- Bản cũ bind cùng một `app_v2.xml` cố định lên cả `/my_stock` và `/my_product`.
- ROM gốc có hai file khác nhau: stock chặn nhiều ứng dụng; product chứa các quy tắc riêng theo vùng. Chép file stock đè lên product làm mất các quy tắc này.

## Toàn bộ khác biệt trong quy tắc package trên máy này

| Package | Quy tắc gốc bị mất / thay đổi | Trạng thái quan sát trước sửa |
| --- | --- | --- |
| `com.oplus.aimemory` (Mind Space) | Mất `enable`, priority 7 ở product; bị thay bằng `disable`, priority 10 | `pm path` không tìm thấy |
| `com.oplus.omoji` (Omoji) | Mất `enable`, priority 7 ở product; bị thay bằng `disable`, priority 10 | `pm path` không tìm thấy |
| `com.google.android.mosey` (Quick Share extension) | Mất `enable`, priority 7 ở product; bị thay bằng `disable`, priority 10 | `pm path` không tìm thấy |
| `com.oplus.nearcomm` | Mất `enable`, priority 7 ở product | Vẫn được cài cho user 0; chưa biến mất |
| `com.qpon.platform` | Mất `del_enable`, priority 7, `Qpon.apk` ở product | `pm path` không tìm thấy; chưa xác nhận APK có sẵn trên máy |
| `com.oplus.doublewake.settings` | Mất `disable`, priority 5 ở product | `pm path` không tìm thấy; mất quy tắc tắt, chưa phải bằng chứng mất tính năng |
| `com.google.android.apps.messaging` | Bị thêm `disable`, priority 10 ở cả hai file; script còn gọi `pm disable` và `pm disable-user` | User 0, 998, 999 đều `enabled=3` (disabled-user) |
| `com.android.mms` | Stock: `disable` thành `enable`; product: bị thêm `enable` | Có `/product/priv-app/Mms/Mms.apk`, đang giữ SMS role |

Các package còn lại trong cấu hình cố định đã bị chặn sẵn ở stock của ROM này. Không đủ căn cứ nói module làm mất toàn bộ danh bạ, gọi điện, eSIM, cloud, theme store, thanh toán hoặc vệ tinh. Khôi phục đúng là giữ quy tắc gốc từng phân vùng, không bật tất cả package bị chặn.

`feature_rsa4.0_t3_default_app.xml` gốc trên máy này chỉ khác package SMS. Không quan sát thấy file feature khác bị ghi đè trên máy này. Wildcard trong script cũ có thể ghi đè nhiều file trên ROM khác; bản mới bỏ hoàn toàn cơ chế này.

## Bản sửa

1. Bỏ hai XML cố định và vòng lặp ghi đè `feature_rsa*.xml`.
2. Tạo bản vá riêng từ ROM hiện tại của từng phân vùng, chỉ sửa thẻ chặn chính xác `com.android.mms`. Không dùng lại ROM cũ sau OTA.
3. Giữ SELinux context gốc; không mount khi không có thay đổi hoặc quy tắc SMS chưa hỗ trợ.
4. Chỉ cấu hình SMS user 0; bỏ lệnh tắt Google Messages và vòng lặp sửa user khác.
5. Bỏ xóa package cache toàn hệ thống; sửa thông tin installer và đóng gói LF / quyền Unix thống nhất.

## Kiểm tra trước triển khai

- 5 nhóm kiểm thử parser: chỉ đổi MMS, bảo toàn comment/CDATA/thuộc tính, nhiều quy tắc SMS, không đổi file product, bỏ qua đầu vào chưa hỗ trợ; có đối chiếu XML ROM thực tế.
- Đã chạy script boot và Android awk trong mount namespace riêng: chỉ stock thay đổi; product và feature giữ nguyên từng byte; bind mount và SELinux context thành công; log không có lỗi.
- Bảng mount PID 1 không đổi sau các lượt kiểm tra bằng công cụ namespace.
- Đã reboot và xác nhận bằng Package Manager sau triển khai; chưa kiểm tra gửi/nhận SMS/OTP thực tế.

XML thu thập từ máy lưu cục bộ trong `diagnostics/`, không đưa vào Git hay ZIP.

## Khôi phục đã thực hiện trên máy

- Sao lưu nguyên module cũ tại `/data/adb/oppo_messages_enabler-backups/20261018-before-fix/module`.
- KernelSU-Next xác nhận cài thành công ZIP mới; sau reboot module v1.0.2, versionCode 201 được kích hoạt.
- Tháo đúng ba lớp mount của module cũ đã xác minh; trả product và feature về file gốc; áp dụng lớp stock mới chỉ sửa Oppo Messages.
- Khôi phục Google Messages về `default` cho user 0, 998 và 999; Oppo Messages vẫn giữ SMS role.
- Sau reboot: Mind Space (`/product/app/AIMemory/AIMemory.apk`), Omoji (`/mnt/opex/com.oplus.Omoji@16001003/app/app.apk`) và Quick Share extension (`/system_ext/priv-app/MoseyApp/MoseyApp.apk`) đã được Package Manager nhận lại; `com.oplus.nearcomm` vẫn có sẵn.
- Đã đọc APK Mosey bằng Android SDK aapt2: tên ứng dụng là **Quick Share extension**.
- Product và feature khớp toàn bộ quy tắc ROM gốc; stock chỉ đổi thẻ MMS; SMS role vẫn là Oppo Messages; Google Messages không bị tắt trên user 0/998/999; log boot module trống.
- `com.qpon.platform` và `com.oplus.doublewake.settings` không được Package Manager đăng ký sau reboot. Quy tắc OEM của chúng đã được khôi phục nguyên vẹn; không tự cài thêm hoặc ép bật những package này.
- Chưa kiểm tra thao tác giao diện, chia sẻ qua Quick Share, hay gửi/nhận SMS/OTP thực tế.

`tools/restore_live_device.py` là script khôi phục một lần cho đúng trạng thái đã kiểm tra của máy này; có điều kiện kiểm tra bản sao lưu, versionCode và nguồn mount. Không phải script boot của module và không nằm trong ZIP.

## Cập nhật v1.0.3: mở chặn thêm Mind Pilot

Theo yêu cầu người dùng, danh sách cho phép hiện chỉ gồm Oppo Messages (`com.android.mms`) và Mind Pilot (`com.oplus.aiassistant`). Bộ vá chỉ đổi `disable` thành `enable` cho đúng hai package này; các quy tắc khác không thay đổi. Khi nâng cấp, installer bỏ qua thiết lập SMS để giữ nguyên lựa chọn hiện tại.

Đã cài v1.0.3, versionCode 202 qua KernelSU và reboot thiết bị. Bản trước cập nhật được sao lưu tại `/data/adb/oppo_messages_enabler-backups/20261018-before-v103/module`.

Kết quả đối chiếu sau khi máy ổn định:

- Mind Pilot được đăng ký từ `/product/priv-app/aiassistant/aiassistant.apk`, `installed=true`, `enabled=0` (trạng thái mặc định, không bị tắt).
- So với trước cập nhật, stock chỉ đổi thẻ Mind Pilot thành `enable`; product và feature giữ nguyên. Oppo Messages đã được mở chặn từ bản trước và không thay đổi trong lần này.
- Danh sách package cài cho user 0 chỉ thêm `com.oplus.aiassistant`, không mất package nào; user 998/999 không thêm hoặc mất package.
- Toàn bộ danh sách ứng dụng bị tắt của user 0/998/999 khớp trước cập nhật, kể cả Google Messages; không ép bật lại ứng dụng do người dùng đã tắt.
- SMS role không thay đổi; log module trống; 7 nhóm kiểm thử đều đạt.

Đã xác nhận trạng thái đăng ký/bật ứng dụng; chưa kiểm thử tác vụ AI bên trong Mind Pilot.
