# Bài tập lớn KTHP Phân tích thiết kế giải thuật

- Đề tài: Xây dựng ứng dụng sinh mê cung và tìm đường đi sử dụng DFS, BFS và Backtracking 
- Nhóm thực hiện: Nhóm 12
- Danh sách sinh viên thực hiện

    |Họ và tên sinh viên|Công việc thực hiện|Phần trăm đóng góp|
    |---|---|---|
    | Lê Huỳnh Anh Khôi|Triển khai DFS + Backtracking trong tìm đường đi và sinh mê cung|100%|
    | Võ Đức Thịnh| Triển khai BFS|100%|
    | Nguyễn Đức Tỉnh|Thiết kế giao diện ứng dụng, tích hợp thuật toán vào giao diện|100%|
    |Nguyễn Minh Hiếu|Tìm hiểu, phân tích cơ sở lý thuyết và cách áp dụng trong ứng dụng, thuyết trình|100%|
    |Nguyễn Trí Đức|Triển khai Prim sinh mê cung, tìm đường đi ngắn nhất với thuật toán A* và Dijkstra|100%|
    |Trương Công Huy|Đánh giá ứng dụng|100%|

## Cơ sở lý thuyết

Ứng dụng mô phỏng mê cung dưới dạng một ma trận hai chiều gồm các ô đi được và các ô tường. Mỗi ô trong lưới được xem như một đỉnh của đồ thị, còn các ô kề nhau theo 4 hướng lên, xuống, trái, phải được xem là các cạnh hợp lệ nếu không bị chặn bởi tường.

### Sinh mê cung

#### Recursive DFS + Backtracking

Ứng dụng sinh mê cung bằng kỹ thuật Recursive Backtracking. Quy trình chung là khởi tạo toàn bộ lưới ở trạng thái tường, sau đó bắt đầu từ một ô xuất phát hợp lệ và đi sâu theo từng nhánh chưa thăm. Mỗi lần mở rộng, thuật toán chọn ngẫu nhiên thứ tự 4 hướng di chuyển, kiểm tra ô kế tiếp có nằm trong biên và chưa được thăm hay không, rồi phá bức tường nằm giữa hai ô để tạo thành đường đi mới.

Để mê cung có cấu trúc đẹp và dễ duyệt, kích thước hàng và cột thường được điều chỉnh về số lẻ. Điểm bắt đầu và điểm kết thúc được đặt gần hai góc đối diện của mê cung, sau đó được mở đường trực tiếp để đảm bảo luôn tồn tại lối đi hợp lệ. Cách sinh này tạo ra mê cung liên thông, không bị cô lập vùng và cho hình dạng đường đi tự nhiên.

Về độ phức tạp, thuật toán sinh mê cung bằng DFS quay lui thường có thời gian xấp xỉ O(R × C) vì mỗi ô hợp lệ được mở rộng và xử lý hữu hạn lần, đồng thời cần không gian O(R × C) cho lưới mê cung và ngăn xếp đệ quy. Cách sinh này đảm bảo mê cung có lối đi liên thông, các bức tường được bố trí tự nhiên và hạn chế tạo ra vùng cô lập không thể đi tới.

#### Prim

Bên cạnh Recursive Backtracking, ứng dụng còn hỗ trợ sinh mê cung bằng thuật toán Prim ngẫu nhiên hóa. Cách tiếp cận này bắt đầu từ một ô đường đi ban đầu, sau đó duy trì tập các ô biên có khả năng nối vào vùng đã mở. Ở mỗi bước, thuật toán chọn ngẫu nhiên một ô biên, phá bức tường giữa ô đó và ô cha tương ứng, rồi đưa các ô biên mới vào danh sách xét tiếp.

So với DFS quay lui, Prim có xu hướng mở rộng mê cung theo kiểu lan tỏa đều hơn, tạo ra cấu trúc ít thiên lệch theo một nhánh dài. Về lý thuyết, thuật toán có thời gian và không gian xấp xỉ O(R × C) do mỗi ô và các cạnh biên liên quan được xử lý hữu hạn số lần. Trong ứng dụng này, Prim phù hợp khi cần một mê cung có hình thức cân đối, ổn định và dễ quan sát khi hiển thị trực quan.

### Tìm đường đi

Ứng dụng hỗ trợ nhiều thuật toán tìm đường đi để so sánh cách duyệt và chất lượng đường đi thu được.

- DFS đi sâu theo từng nhánh trước khi quay lui. Thuật toán này phù hợp để khảo sát nhiều khả năng đường đi và có thể tìm thấy một đường hợp lệ khá nhanh trong một số trường hợp, nhưng không đảm bảo đường đi ngắn nhất.
- BFS duyệt theo từng lớp khoảng cách từ điểm xuất phát. Nhờ cơ chế hàng đợi, BFS đảm bảo tìm được đường đi ngắn nhất nếu đường đi tồn tại.

Ngoài BFS và DFS, chương trình còn cài đặt A* và Dijkstra:

- A* kết hợp chi phí đã đi qua và hàm heuristic Manhattan để ưu tiên các ô có khả năng tiến gần đích hơn. Nhờ đó, A* thường giảm số ô phải xét so với duyệt mù trong các mê cung lớn, nhưng vẫn giữ được tính tối ưu nếu heuristic phù hợp.
- Dijkstra tìm đường ngắn nhất bằng cách luôn chọn ô có chi phí tích lũy nhỏ nhất từ điểm xuất phát. Trong mê cung không trọng số, Dijkstra cho kết quả tương đương BFS về chất lượng đường đi, nhưng được biểu diễn bằng hàng đợi ưu tiên.

Về độ phức tạp lý thuyết, BFS có thời gian chạy xấp xỉ O(R × C) với R là số hàng và C là số cột, đồng thời cần không gian O(R × C) cho tập ô đã thăm và cấu trúc lưu cha. DFS có thể hoạt động rất nhanh trên một số mê cung nhỏ hoặc cấu trúc thuận lợi, nhưng trong trường hợp phải thử nhiều nhánh quay lui thì chi phí có thể tăng mạnh theo số lượng nhánh cần xét. A* và Dijkstra đều có độ phức tạp thời gian xấp xỉ O(E × log V) với V là số ô và E là số liên kết hợp lệ, do sử dụng hàng đợi ưu tiên để chọn trạng thái tốt nhất ở mỗi bước.

## Cấu trúc thư mục của ứng dụng

- `algorithms/`: Chứa các thuật toán sinh mê cung và tìm đường đi như DFS, BFS, A*, Dijkstra và Prim.
- `controllers/`: Điều phối luồng xử lý giữa giao diện và các thuật toán, đồng thời quản lý trạng thái mê cung hiện tại.
- `models/`: Định nghĩa các models như mê cung, điểm tọa độ, hướng di chuyển và robot mô phỏng quá trình tìm đường.
- `utils/`: Chứa các hàm hỗ trợ kiểm tra đường đi và xử lý dữ liệu dùng chung.
- `views/`: Xây dựng giao diện người dùng gồm cửa sổ chính, bảng điều khiển và khu vực hiển thị mê cung.
- `app.py`: Nơi khởi tạo chính của ứng dụng.

### `algorithms`

Folder `algorithms` chứa toàn bộ phần xử lý thuật toán của ứng dụng. Mỗi file đảm nhận một vai trò riêng, và mỗi vai trò gắn trực tiếp với một thuật toán cụ thể.

#### `dfs.py`

File này dùng thuật toán DFS theo hai hướng khác nhau. Thứ nhất là sinh mê cung bằng Recursive Backtracking: chương trình bắt đầu từ một ô hợp lệ, đi sâu ngẫu nhiên qua các ô chưa thăm, rồi phá tường giữa hai ô để mở đường. Thứ hai là tìm tất cả đường đi khả thi từ điểm đầu đến điểm cuối bằng DFS kết hợp quay lui: khi đi đến một ô mới, thuật toán đánh dấu ô đó là đã đi qua, tiếp tục thử các nhánh khác, và khôi phục lại trạng thái khi quay lui.

Với phần sinh mê cung, DFS phù hợp vì nó tạo ra các hành lang dài, có tính ngẫu nhiên cao và dễ đảm bảo mê cung liên thông. Với phần tìm đường, DFS không nhằm tìm đường ngắn nhất mà nhằm liệt kê các đường đi có thể có, sau đó controller sẽ lấy đường ngắn nhất trong tập kết quả để hiển thị.

#### `bfs.py`

File này cài đặt BFS để tìm đường đi ngắn nhất trong mê cung. BFS dùng hàng đợi để duyệt theo từng lớp khoảng cách tính từ điểm xuất phát. Khi thăm một ô mới, thuật toán lưu lại ô cha của nó trong `parent` để có thể truy vết ngược từ đích về nguồn sau khi tìm thấy đường đi.

BFS phù hợp khi mục tiêu là lấy đường đi ngắn nhất và ổn định. Trong ứng dụng, đây là thuật toán tìm đường chính vì nó dễ giải thích, dễ theo dõi bằng animation và cho kết quả tối ưu trên mê cung không trọng số.

#### `prim.py`

File này cài đặt thuật toán Prim ngẫu nhiên hóa để sinh mê cung. Khác với DFS quay lui, Prim không đi sâu theo một nhánh cố định mà luôn duy trì một tập các ô biên có thể nối vào vùng đã mở. Ở mỗi bước, thuật toán chọn ngẫu nhiên một ô biên, phá bức tường giữa ô biên và ô cha của nó, rồi thêm các ô biên mới vào danh sách xét tiếp.

Prim tạo ra mê cung có xu hướng mở rộng đều hơn, ít thiên lệch theo một hành lang dài, nên phù hợp khi muốn sinh mê cung có hình dạng cân đối và dễ quan sát.

#### `a_star.py`

File này cài đặt thuật toán A* để tìm đường đi ngắn nhất. A* kết hợp hai thành phần: chi phí thực tế đã đi từ điểm đầu đến ô hiện tại, và chi phí ước lượng từ ô hiện tại đến đích bằng khoảng cách Manhattan. Nhờ đó, thuật toán ưu tiên mở rộng các ô có khả năng dẫn tới đích nhanh hơn.

Trong code, A* dùng hàng đợi ưu tiên để luôn chọn trạng thái có giá trị đánh giá tốt nhất. Thuật toán này thường hiệu quả hơn BFS trên các mê cung lớn vì nó giảm số ô cần xét, nhưng vẫn giữ được tính tối ưu nếu heuristic phù hợp.

#### `dijkstra.py`

File này cài đặt thuật toán Dijkstra để tìm đường đi ngắn nhất. Dijkstra luôn chọn ô có tổng chi phí từ nguồn nhỏ nhất, cũng thông qua hàng đợi ưu tiên. Khi mê cung không có trọng số khác nhau giữa các bước di chuyển, Dijkstra cho kết quả tương đương BFS về độ dài đường đi.

Trong ứng dụng, Dijkstra hữu ích để minh họa một cách tiếp cận khác với BFS: thay vì duyệt theo lớp, thuật toán duyệt theo chi phí tích lũy. Điều này làm rõ khái niệm đường đi ngắn nhất dựa trên chi phí trong đồ thị.


### `models`

Folder `models` là nơi mô tả các entities cốt lõi mà ứng dụng dùng để lưu và truyền trạng thái giữa giao diện, bộ điều khiển và thuật toán.

- `Point`: Biểu diễn một tọa độ trên lưới theo cặp `x`, `y`. `Point` còn hỗ trợ phép cộng và nhân vô hướng để thuận tiện khi tính ô kề và bước di chuyển.
- `Maze`: Đại diện cho toàn bộ mê cung với số hàng, số cột, ma trận `grid`, điểm bắt đầu và điểm kết thúc. Mỗi phần tử của `grid` mô tả trạng thái một ô, trong đó giá trị 0 là đường đi và 1 là tường. Đây là đối tượng trung tâm được truyền cho các thuật toán sinh và tìm đường.
- `Directions`: Là một `Enum` mô tả 4 hướng di chuyển cơ bản gồm lên, xuống, trái và phải. Việc gom các hướng vào một kiểu dữ liệu riêng giúp các thuật toán duyệt lưới nhất quán và dễ mở rộng.
- `Robot`: Là mô hình lưu trạng thái trong quá trình duyệt mê cung. Đối tượng này giữ vị trí hiện tại, thứ tự các ô đã duyệt, danh sách các đường đi khả thi và đường đi ngắn nhất. Nhờ vậy, controller có thể lấy dữ liệu đã tính toán để cập nhật giao diện và thống kê hiệu năng.

Các mô hình này phối hợp với nhau theo nguyên tắc: `Maze` cung cấp không gian làm việc, `Point` mô tả vị trí, `Directions` chuẩn hóa bước di chuyển và `Robot` lưu lại kết quả sau khi thuật toán kết thúc.

## Ứng dụng

Khi sử dụng ứng dụng, người dùng có thể sinh mê cung ngẫu nhiên, nhập mê cung từ tệp JSON, lưu mê cung ra tệp JSON từ local hoặc tự chỉnh sửa mê cung trực tiếp trên lưới.

Bảng điều khiển cho phép chọn chế độ chuột để vẽ tường hoặc đặt điểm bắt đầu/kết thúc, sau đó chọn thuật toán phù hợp để giải mê cung.

Luồng thao tác cơ bản như sau: người dùng tạo hoặc nạp mê cung, đặt kích thước và điểm đầu/cuối nếu cần, chọn thuật toán tìm đường, rồi nhấn nút giải mê cung. 


Kết quả được hiển thị bằng hiệu ứng tô màu các ô đã duyệt, vẽ lại đường đi cuối cùng và cập nhật các thông số như số ô đã duyệt, độ dài đường đi và thời gian chạy. Giao diện cũng hỗ trợ cuộn và phóng to/thu nhỏ để quan sát các mê cung lớn.

## Đánh giá

Phần đánh giá được thực hiện trên cùng một cặp điểm đầu và điểm cuối để bảo đảm tính công bằng giữa các thuật toán. Tất cả phép đo dùng cùng vị trí bắt đầu, cùng vị trí kết thúc và cùng bộ kích thước lưới tăng dần gồm `11 x 11`, `31 x 31`, và `51 x 51`. Trong giao diện, thời gian chạy được chốt tại thời điểm các ô màu vàng chạm đến đích; phần robot chỉ là hiệu ứng trực quan đi theo sau.

### Sinh mê cung

Bảng dưới đây ghi nhận thời gian sinh mê cung của hai thuật toán đang có trong code:

| Kích thước mê cung | Recursive Backtracking | Prim |
|---|---:|---:|
| 11 x 11 | 0.2785 ms | 0.1571 ms |
| 31 x 31 | 1.5793 ms | 0.9371 ms |
| 51 x 51 | 3.3615 ms | 2.5846 ms |

Kết quả cho thấy Prim sinh mê cung nhanh hơn Recursive Backtracking ở cả ba kích thước đã đo. Khi kích thước lưới tăng, thời gian sinh của cả hai thuật toán đều tăng theo, đúng với kỳ vọng về độ phức tạp theo số ô cần xử lý.

### Tìm đường đi

Bảng dưới đây ghi nhận thời gian tìm đường trên cùng một mê cung được sinh từ Recursive Backtracking để bảo đảm mọi thuật toán pathfinding cùng làm việc trên một cấu trúc đầu vào giống nhau. Ở đây, thời gian được hiểu là thời gian thuật toán hoàn tất việc tìm đường trước khi phần robot đi đến ô đích.

| Kích thước mê cung | DFS | BFS | A* | Dijkstra |
|---|---:|---:|---:|---:|
| 11 x 11 | 0.1109 ms | 0.1653 ms | 0.1651 ms | 0.1620 ms |
| 31 x 31 | 0.9391 ms | 1.1530 ms | 1.1735 ms | 1.3165 ms |
| 51 x 51 | 1.4580 ms | 1.7916 ms | 1.9355 ms | 2.1165 ms |

Số ô đã duyệt và độ dài đường đi tương ứng của từng lần đo như sau: `11 x 11` có độ dài đường đi `41`, `31 x 31` có độ dài `261`, và `51 x 51` có độ dài `393`. Ở cùng một mê cung, DFS duyệt ít trạng thái hơn các thuật toán còn lại trong bộ đo này, trong khi BFS, A* và Dijkstra vẫn trả về cùng độ dài đường đi tối ưu.

**Kết luận từ số liệu đo**: khi kích thước lưới tăng, thời gian xử lý của tất cả thuật toán đều tăng. Ở phần sinh mê cung, Prim nhanh hơn Recursive Backtracking trong cả ba mốc đo. Ở phần tìm đường, DFS có thời gian nhanh nhất trong bộ benchmark này, còn BFS, A* và Dijkstra giữ cùng độ dài đường đi nhưng có thời gian cao hơn tùy theo chiến lược duyệt và số trạng thái phải xét. Nhìn từ phía giao diện, số liệu runtime cũng đã được đồng bộ để phản ánh đúng thời điểm các ô vàng chạm đích.

## Cách chạy ứng dụng
* Yêu cầu Python: Python >= 3.1x
* Hỗ trợ hệ điều hành: Windows, Linux (Ubuntu 26.04)
* Lệnh chạy ứng dụng:

```bash
# Với Windows
python -m venv venv
./venv/Scripts/activate.bat
pip install -r requirements.txt
python app.py
```

```bash
# Với Linux
python3 -m venv venv 
source ./venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

