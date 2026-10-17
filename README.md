# Oppo Messages Enabler

A Magisk / KernelSU / APatch module to enable native **Oppo Messages** (`com.android.mms`) and replace Google Messages on ColorOS, OxygenOS, and Realme UI devices.

---

## 📱 Tested Device
- **Device**: OnePlus 15
- **ROM**: India (IN) `16.0.1.60x` (ColorOS 16 / OxygenOS 16)
- **Status**: ✅ Hoạt động hoàn hảo 100% (SMS/OTP, cuộc gọi, âm báo, thông báo nổi, icon UXIcons chính chủ)

---

## 🌟 Tính năng nổi bật / Features

- **Mở khóa Tin nhắn gốc (Oppo Messages)**: Gỡ bỏ quy tắc chặn trong file cấu hình `app_v2.xml` của hệ thống bằng phương pháp `mount --bind` an toàn, không can thiệp vật lý vào phân vùng hệ thống (read-only).
- **Hỗ trợ đa phân vùng (Universal Partition Support)**: Tự động phát hiện và bind-mount trên mọi phân vùng (`/my_stock`, `/my_product`, `/my_heytap`, `/odm`).
- **Thay thế hoàn toàn Google Messages**: Tự động vô hiệu hóa Google Messages để tránh xung đột thông báo và trùng lặp trình xử lý SMS.
- **Tương thích tính năng Nhân bản ứng dụng (App Cloner / MultiApp)**: Tự động quét tất cả User Profile (`User 0`, `User 998`, `User 999`) và vô hiệu hóa Google Messages triệt để, không lo bị sinh icon "Tin nhắn 1", "Tin nhắn 2" bản sao.
- **Tự động cấp quyền SMS mặc định**: Tự động thiết lập Oppo Messages làm ứng dụng SMS mặc định của hệ thống (`android.app.role.SMS`) ngay khi boot.
- **An toàn tuyệt đối**: Gỡ module là máy tự động quay về nguyên bản 100%.

---

## 📋 Yêu cầu / Requirements

1. Thiết bị **Oppo**, **OnePlus** hoặc **Realme** chạy **ColorOS 14/15/16**, **OxygenOS 14/15/16**, hoặc **Realme UI 5.0/6.0**.
2. Thiết bị đã được root bằng một trong các công cụ:
   - **KernelSU** / **KernelSU-Next**
   - **APatch**
   - **Magisk**

---

## 🚀 Hướng dẫn cài đặt / Installation

1. Tải file zip `Oppo_Messages_Enabler_v1.0.1.zip` từ mục **[Releases](https://github.com/quyetbkhoa/OppoMessageEnabler/releases)**.
2. Mở trình quản lý root (**KernelSU** / **APatch** / **Magisk**).
3. Vào tab **Mô-đun (Modules)** -> Chọn **Cài đặt từ bộ nhớ (Install from storage)**.
4. Chọn file zip vừa tải về.
5. Sau khi cài đặt hoàn tất, nhấn **Khởi động lại (Reboot)** điện thoại.
6. Sau khi máy khởi động lại:
   - Vào ứng dụng **Tin nhắn** lần đầu và nhấn **Đồng ý** điều khoản dịch vụ của Oppo.
   - Thưởng thức giao diện Tin nhắn thuần ColorOS mượt mà, hỗ trợ giao diện gốc của máy!

---

## 👤 Tác giả / Author
- **Author**: `quyetbkhoa`
- **GitHub**: [quyetbkhoa](https://github.com/quyetbkhoa)
- **Repository**: [OppoMessageEnabler](https://github.com/quyetbkhoa/OppoMessageEnabler)
