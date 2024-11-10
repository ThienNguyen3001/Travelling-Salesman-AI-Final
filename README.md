<summary><h1>Giai đoạn 1: Code thuật toán (đã hoàn thành)</h1></summary>
<details>

### Selection
- **Roulette Wheel Selection** - *Hưởng*
- **Tournament Selection** - *Huy*
- **Rank Selection** - *Nhựt*
- **Elitism Selection** - *(đã làm)*

### Crossover
- **Single-Point Crossover** - *Huy*
- **Two-Point Crossover** - *Nhựt*
- **Uniform Crossover** - *Hưởng*
- **Order Crossover** - *(đã làm)*

### Mutation
- **Scramble Mutation** - *Nhựt*
- **Inversion Mutation** - *Huy*
- **Insertion Mutation** - *Hưởng*
- **Swap Mutation** - *(đã làm)*

</details>
<summary><h1>Giai đoạn 2: Thí nghiệm</h1></summary>
<details>
  
## Thí nghiệm chia làm 4 phần riêng: 
### 1. Ảnh hưởng của tham số đến fitness (Hưởng)
* Chỉ dùng 3 thuật toán mặc định: selection = 'elitism', crossover = 'order', mutation = 'swap'
* Chọn data 6 cities làm chuẩn, chỉ cần xét 1 data
* Chỉ cần đánh giá thông qua fitness, không cần qua kết quả
* Lấy bộ tham số này, duyệt theo kiểu 1 cái tăng thì 2 cái còn lại giữ nguyên: 
  - Population_size = [100,500,1000]
  - Generations = [100,500,1000]
  - Mutation_rate = [0.01,0.05,0.1]
### 2. Ảnh hưởng của các thuật toán khác nhau đến fitness (Huy)
* Dùng 3 bộ thuật toán đã làm bữa trước, dùng theo bộ mà từng người làm, không nên xáo. Không làm lại bộ thuật toán ở mục 1
* Data, đánh giá: Như mục 1
* Tham số này dùng cho cả 4 bộ:
  - Population_size = 100
  - Generations = 100
  - Mutation_rate = 0.01
### 3. Ảnh hưởng của các dữ liệu bài toán đến kết quả (Nhựt)
* Thuật toán: Như mục 1
* Data: Test hết trừ bộ 6 cities
* Đánh giá: Dùng độ lệch để đánh giá, vd: kq gốc là 1248, kq chạy ra là 1300, đánh giá |1300-1248| = 52. Nên viết hàm vẽ đồ thị kết hợp vòng lặp để vẽ
* Tham số: Như mục 2
### 4. Đánh giá, cải thiện một số tham số và lựa chọn 1 số thuật toán để tìm ra được kết quả chính xác nhất có thể (Thiện)
* Người làm cái này sẽ cố gắng thay thế bất kì tham số nào, chọn bất kì thuật toán nào để giải được càng nhiều data chính xác nhất và nhanh nhất càng tốt. Rồi rút ra lựa chọn thuật toán nào, tham số nào để kết luận toàn bài.
</details>

Giai đoạn 3: UI, tiểu luận và slide (12/10 - 26/10)
