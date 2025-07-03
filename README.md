Với mục tiêu thực hiện được một quy trình đầy đủ để khai thác dữ liệu, em đưa ra một ví dụ thực nghiệm là: Khai thác dữ liệu từ trang web của Worldbank (https://data.worldbank.org/indicator).
Quy trình xử lý dữ liệu gồm nhiều bước cùng với sự lựa chọn các công cụ hỗ trợ, sau đây là sơ đồ thực hiện:

![image](https://github.com/user-attachments/assets/43cc0ab6-236d-43eb-9fb5-5357a250b10a)

Báo cáo gồm các nội dung:
1.	Giới thiệu web https://data.worldbank.org/indicator và các dữ liệu.
2.	Scraping dữ liệu
3.	Quy trình biến đổi và load dữ liệu
4.	Sử dụng Airflow
5.	Truy vấn SQL và hiển thị dữ liệu bằng Influxdb

II.	GIỚI THIỆU WEB WORLDBANK VÀ CÁC DỮ LIỆU

![image](https://github.com/user-attachments/assets/6bc8931c-4d92-4299-8cde-58d584bbd2ed)<br>
Các dữ liệu mà Ngân hàng Thế Giới cung cấp được thu thập trong vòng 50 năm qua, gồm nhiều chủ đề như tài chính, kinh doanh, y tế, kinh tế, phát triển con người. Hiện người dùng đã có thể truy cập trên 7.000 chỉ số phát triển.<br>
Trang Chỉ số (Indicators) liệt kê 331 chỉ số trong bộ Chỉ số Phát triển Thế giới (WDI) theo vần ABC. Hàng năm, Ngân hàng Thế giới tổng hợp dữ liệu phát triển từ các dữ liệu gốc của mình và các nguồn khác được công nhận trên toàn thế giới để xây dựng bộ Chỉ số Phát triển Thế giới. Đây là công cụ để đánh giá tiến độ phát triển các nền kinh tế. 
Các con số kể những câu chuyện về con người ở  các quốc gia mới nổi và đang phát triển, qua đó đóng góp một phần vào công cuộc xóa đói giảm nghèo.<br>
Ở đồ án cuối kỳ này, tôi sẽ lấy các dữ liệu của trang Chỉ số này và dữ liệu được sử dụng để phân tích cũng như hiển thị trên một chương trình ở dưới máy tính cá nhân.

III.	QUY TRÌNH ETL<br>

III.1.	Extract

Việc lấy dữ liệu từ web được thực hiện bằng một đoạn code Python tên scraping.py, sử dụng thư viện Urllib và Xpath. Dữ liệu được lưu ở folder trên máy.

![image](https://github.com/user-attachments/assets/7642cf39-a53d-4dde-a1a5-12069854c295)

III.2.	Transform - Load

Quá trình transform - load gồm có 3 bước:

                Upzip     =>    Cleaning    =>      Processing
                
Dữ liệu down về là các file .zip được chứa theo từng thư mục theo từng chỉ số:
 
![image](https://github.com/user-attachments/assets/083aaeb2-46e2-4502-b906-f753454745df)


Tiếp đến ta cần xử lý file này để lấy ra các dữ liệu gồm:
•	Last Update Date
•	Country Name
•	Country Code
•	Indicator Name
•	Indicator Code
•	Years
•	Values

Với bảng dữ liệu này, ta xử lý và load lên database của Influxdb bằng đoạn code Python với tên upload.py. Dữ liệu được định dạng theo yêu cầu riêng của Influxdb.

![image](https://github.com/user-attachments/assets/b95720dc-1181-4160-ae1e-80412dda5fe9)

IV.	SỬ DỤNG AIRFLOW

Các source code Python có thể run độc lập. Tuy nhiên, trong quá trình khai thác dữ liệu từ web, dữ liệu cần được cập nhật thường xuyên, các task được chạy tuần tự hoặc song song, việc thiết lập thời gian chạy của mỗi task thế nào thì cần được lên lịch trình và setup chạy cụ thể. Một ứng dụng hữu ích cho mục tiêu này đó là airflow.

Tất cả các task xây dựng đều có thể chạy song song. Nhưng vì nhiệm vụ Scraping, đây là task cần nhiều thời gian để hoàn thành. Ta để Scraping ở một DAG riêng lẻ. Việc download được setup scheduler là 1 ngày.

Các task còn lại sẽ được đưa vào DAG thứ hai và thử cách chạy tuần tự, scheduler được setup lặp lại theo từng phút. Sau mỗi task, dữ liệu ở thư mục input sẽ bị xóa đi để tránh chồng lắp dữ liệu.

Do đó, khi hoàn thành các task, các folder sẽ được tạo mới, nhưng đây là các folder trống.
![image](https://github.com/user-attachments/assets/3c9afee0-2693-46f0-be06-1bc7f54b3bc3)<br>
![image](https://github.com/user-attachments/assets/7e464999-2f18-45dc-a7b5-8c5da40c494b)<br>
![image](https://github.com/user-attachments/assets/e8730726-0e57-4e16-8f12-344f0417d994)<br>
Các task được xây dựng bằng đoạn code Python được đặt trong folder dags của thư mục Airflow:<br>
![image](https://github.com/user-attachments/assets/7ae5febd-fbb2-4899-a5fb-09465e14df68)

V.	TRUY VẤN SQL VÀ HIỂN THỊ DỮ LIỆU BẰNG INFLUXDB

InfluxDB là một cơ sở dữ liệu chuỗi thời gian phổ biến. Báo cáo sử dụng phiên bản Influxdb 1.8.9. Việc truy vấn trên Influxdb sử dụng một ngôn ngữ giống như SQL. Hiện nay, Influxdb đã phát triển đến phiên bản 2.0 và việc truy vấn đã chuyển sang ngôn ngữ NoSQL. Tuy nhiên, định dạng dữ liệu đưa vô chương trình là không thay đổi.

![image](https://github.com/user-attachments/assets/f58ca8ee-d542-435e-9bfe-bb921d8c5f6f)

So với các hệ cơ sở dữ liệu khác, InfluxDB không cung cấp nhiều dạng biểu đồ, chủ yếu phục vụ cho hiển thị chuỗi dữ liệu thời gian, gồm có:

![image](https://github.com/user-attachments/assets/7d1ad357-3cac-4b37-8e00-8081f9e2bf58)

Đây là giao diện chương trình để lựa chọn dữ liệu hiển thị

![image](https://github.com/user-attachments/assets/ced37147-6c66-4537-8973-2d4bcb3779fc)

Sau đây là một Dashboard ví dụ từ dữ liệu trang web WorldBank: 

![image](https://github.com/user-attachments/assets/63a164e5-4ab7-41cb-8ae9-d909766042ee)

VI.	KẾT LUẬN

Tới đây, quá trình xử lý dữ liệu có thể xem như hoàn thành. Ta có thể phân tích dữ liệu một cách chi tiết hơn nữa. Việc lựa chọn Influxdb ở trong bài báo này không quá phù hợp. Influxdb rất phù hợp nhận dữ liệu streaming từ các thiết bị iot, hiển thị dữ liệu time series, đánh giá tốc độ hệ thống. Với dữ liệu ở báo cáo này, ta có thể tìm kiếm một hệ cơ sở dữ liệu tốt hơn để hiển thị.







