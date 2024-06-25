# tools
Cách sử dụng code:
B1: Tải 2 file trên về, đặt cùng một thư mục
B2: Chuyển tất cả ảnh vào một thư mục (nếu thư mục đặt chung với 2 file trên thì chỉ cần đặt tên thư mục là input)
B3: Copy đường dẫn của thư mục nguồn thay vào phần INPUT_PATH
B4: Khởi động tool: python resize_tool.py 
B5: Ảnh được resize sẽ nằm trong thư mục tương ứng với path bắt đầu bằng "output/"(chạy code sẽ thấy)

*Lưu ý: + Tool sẽ quét tất cả các thư mục để tìm ảnh nên có thể để nhiều thư mục ảnh trong file input 
        + Có thể chỉnh sửa target_size_mb trong file resize_50mb.py để thay đổi kích thước mong muốn
        + Ảnh đầu ra không thể chính xác so với kích thước mong muốn, chỉ có thể ở mức gần nhất có thể so với kích thước mong muốn 
