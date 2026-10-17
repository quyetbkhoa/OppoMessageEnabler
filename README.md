# Oppo Messages Enabler

Module Magisk / KernelSU / APatch mở chặn Oppo Messages (`com.android.mms`) và Mind Pilot (`com.oplus.aiassistant`) trên ROM có sẵn các ứng dụng này. Bản **v1.0.3** chỉ bật hai package trong danh sách cho phép; không chép cấu hình của phân vùng này sang phân vùng khác.

[Tải v1.0.3](https://github.com/quyetbkhoa/OppoMessageEnabler/releases/tag/v1.0.3) · [Changelog](CHANGELOG.md) · [Phân tích lỗi bản cũ](docs/BUG_ANALYSIS.md)

## Thiết bị đã kiểm tra

| Mục | Kết quả |
| --- | --- |
| Thiết bị | OnePlus CPH2745 |
| ROM | `CPH2745_16.0.10.601(EX01)` |
| Root manager | KernelSU-Next |
| Sau reboot | Oppo Messages và Mind Pilot được nhận, không bị tắt; Mind Space, Omoji và Quick Share extension vẫn có sẵn |
| Đối chiếu trước/sau v1.0.3 | Chỉ thêm Mind Pilot; không mất package; danh sách ứng dụng bị tắt và lựa chọn SMS giữ nguyên trên user 0/998/999 |

Đã kiểm tra trạng thái ứng dụng và cấu hình sau reboot. Chưa kiểm thử gửi/nhận SMS/OTP hoặc tác vụ AI bên trong Mind Pilot. Magisk, APatch và ROM khác cần kiểm tra riêng.

## Phạm vi thay đổi

- Mỗi lần boot, đọc `app_v2.xml` gốc của từng phân vùng, chỉ đổi thẻ `disable` của **`com.android.mms`** và **`com.oplus.aiassistant`** thành `enable`, giữ nguyên thuộc tính và các nội dung khác.
- Chỉ bind-mount file có thay đổi; giữ nguyên `/my_product` nếu file này không chặn Oppo Messages.
- Giữ nguyên toàn bộ `feature_rsa*.xml`, Mind Space, Omoji và các quy tắc OEM khác.
- Đặt Oppo Messages làm SMS mặc định cho user 0 một lần. Không tắt Google Messages, không thay đổi hồ sơ nhân bản hoặc hồ sơ công việc.
- Khi nâng cấp từ bản đã cài, giữ lựa chọn SMS hiện tại, không chạy lại bước đặt mặc định.
- Không xóa package cache hoặc dữ liệu ứng dụng. Định dạng quy tắc SMS chưa hỗ trợ sẽ được bỏ qua thay vì thay bằng cấu hình cố định.

## Cài đặt / cập nhật

1. Tải [Oppo_Messages_Enabler_v1.0.3.zip](https://github.com/quyetbkhoa/OppoMessageEnabler/releases/download/v1.0.3/Oppo_Messages_Enabler_v1.0.3.zip).
2. Cài ZIP qua trình quản lý root rồi khởi động lại; không giải nén hoặc chép XML thủ công vào hệ thống.
3. Kiểm tra Mind Pilot, Mind Space, Omoji và Oppo Messages sau khi máy khởi động xong.
4. Nếu cần đổi ứng dụng SMS, dùng Settings. Module không ép lại lựa chọn trên mỗi lần boot.

Bản cũ đã tắt Google Messages bằng Package Manager trên nhiều user; tắt/gỡ module không tự hoàn tác trạng thái này. Muốn khôi phục Google Messages về trạng thái mặc định, chạy với root cho từng user bị ảnh hưởng, ví dụ `pm default-state --user 0 com.google.android.apps.messaging` (máy có hồ sơ 998/999 cần thực hiện riêng). Không bật hàng loạt ứng dụng khác: nhiều quy tắc chặn đã có sẵn từ ROM.

Tắt/gỡ bản mới rồi reboot sẽ bỏ lớp ghi đè XML. Quyền SMS mặc định và trạng thái bật Oppo Messages là cài đặt được lưu bởi Android; có thể đổi lại trong Settings.

## Kiểm tra và build

```sh
python -m unittest discover -s tests -v
python tools/build.py
```

Build tạo ZIP cài đặt và file `.zip.sha256` để đối chiếu SHA-256. ZIP chỉ chứa script, bộ vá và metadata của module; không kèm APK, cấu hình ROM trích xuất hay dữ liệu chẩn đoán.

`tools/audit_device.py` và `tools/verify_device.py` dành riêng cho máy KernelSU đang kết nối qua ADB, có các file được liệt kê trong mã. Chúng dùng BusyBox mount namespace riêng để đọc ROM gốc và thử bind-mount, rồi kiểm tra bảng mount của PID 1 không thay đổi. Không thay thế kiểm tra sau reboot.

`tools/restore_live_device.py` là công cụ khôi phục một lần cho máy đã kiểm tra, chỉ chạy sau khi đã sao lưu và cài ZIP; không nằm trong module.

Xem [phân tích lỗi và kết quả kiểm tra](docs/BUG_ANALYSIS.md). Tương thích ROM khác cần kiểm tra trên thiết bị thực tế; không có cam kết đã test mọi phiên bản ColorOS/OxygenOS/Realme UI.
