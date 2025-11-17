README – Invoice Agent
Tổng quan

Invoice Agent là một workflow kiểu ReAct nhỏ, có chức năng tiếp nhận văn bản hóa đơn thô, trích xuất dữ liệu có cấu trúc, lưu trữ nó trong bộ nhớ, tính tổng theo tháng và tùy chọn hiển thị biểu đồ doanh thu. Agent điều phối các bước của nó thông qua một kế hoạch có thể cấu hình và có thể chạy trực tiếp từ main.py với một file văn bản đầu vào.

Thành phần chính

core/agent.py: vòng lặp ReAct (lập kế hoạch → thực thi → phản tư), quản lý trạng thái và ghi log thời gian chạy. Hỗ trợ chạy từ file thông qua run_from_file.

core/planner.py: tạo kế hoạch động dựa trên yêu cầu của người dùng (trích xuất, lưu trữ, tổng hợp, trực quan hóa, kết thúc).

core/memory.py: lịch sử phiên xử lý và theo dõi trạng thái thành công được sử dụng cho phản tư và thử lại.

tools/:

extraction.py: tạo prompt tới LLM (thông qua utils/llm.py) để trả về JSON hóa đơn phù hợp với schema yêu cầu.

storage.py: lưu các dict hóa đơn trong action_context["invoice_storage"], xử lý trùng lặp và báo cáo các ID mới/được cập nhật.

calculation.py: tổng hợp số tiền hóa đơn theo tháng và lưu kết quả vào monthly_total_storage.

visualization.py: sử dụng matplotlib để vẽ biểu đồ doanh thu hàng tháng (invoice_revenue_chart.png).

control.py: tóm tắt kết thúc workflow và hướng dẫn phục hồi nếu có lỗi.

Cấu hình / Thiết lập

config/settings.py: thiết lập thông tin LLM (thông tin đăng nhập / mô hình), giới hạn retry, tên file biểu đồ mặc định, v.v. Đảm bảo GROQ_API_KEY hợp lệ trước khi chạy.

Yêu cầu Python 3.11+ và các dependency trong requirements.txt (nếu không có, cài đặt thủ công matplotlib và litellm).

Chạy

Đặt hoặc dán văn bản hóa đơn vào invoices.txt (mỗi khối hóa đơn sử dụng định dạng “HÓA ĐƠN BÁN HÀNG … ---”).

Từ thư mục gốc repo:

python main.py


Log đầu ra sẽ hiển thị tiến trình lập kế hoạch/thực thi, mọi lỗi parse JSON của LLM, hóa đơn được lưu, tổng theo tháng và trạng thái biểu đồ.

File biểu đồ (khi được tạo) là invoice_revenue_chart.png trong thư mục gốc dự án.

Kiểm thử

tests/test_tools.py bao phủ kiểm thử xác thực, lưu trữ và tính tổng. Chạy:

python -m unittest tests.test_tools

Ghi chú / Hạn chế

Trích xuất phụ thuộc LLM; đầu vào lớn có thể vượt token và gây lỗi JSON hoặc phản hồi bị giới hạn tần suất.

Trạng thái được lưu trong bộ nhớ; không có cơ sở dữ liệu tồn tại lâu sau khi chạy.

Việc trực quan hóa yêu cầu matplotlib. Nếu thiếu, tool sẽ báo cách cài đặt.

Các file __pycache__ được tạo tự động và có thể bỏ qua hoặc thêm vào .gitignore.
