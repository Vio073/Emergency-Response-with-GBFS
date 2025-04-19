import heapq  # Untuk priority queue (mengelola antrian berdasarkan prioritas)

# Representasi kota dalam bentuk grid 2D:
# S = Start (ambulans)
# H = Goal (rumah sakit)
# T = Traffic (kemacetan, tidak bisa dilewati)
# . = Jalan terbuka
grid = [
    ['S', '.', '.', '.', '.'],
    ['T', 'T', '.', 'T', '.'],
    ['.', '.', '.', '.', '.'],
    ['T', '.', 'T', '.', 'H']
]

# Ukuran grid
rows, cols = len(grid), len(grid[0])

# Fungsi untuk menemukan posisi karakter tertentu di dalam grid (misalnya 'S' atau 'H')
def find_position(char):
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == char:
                return (i, j)
    return None  # Jika tidak ditemukan

# Fungsi heuristik: menghitung jarak Manhattan antara dua titik (baris, kolom)
# Jarak Manhattan cocok untuk grid karena hanya menghitung gerakan horizontal dan vertikal
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Implementasi Greedy Best-First Search (GBFS)
def gbfs(start, goal):
    # Priority queue yang menyimpan (heuristik, posisi)
    open_set = [(manhattan(start, goal), start)]

    # Dictionary untuk melacak node sebelumnya dalam jalur
    came_from = {}

    # Set untuk melacak node yang sudah dikunjungi
    visited = set()
    visited.add(start)

    while open_set:
        # Ambil node dengan nilai heuristik terkecil
        _, current = heapq.heappop(open_set)

        # Jika sampai ke goal, rekonstruksi dan kembalikan jalurnya
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Balik urutan dari start ke goal

        # Periksa 4 arah (atas, bawah, kiri, kanan)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = current[0] + dx, current[1] + dy
            neighbor = (ni, nj)

            # Validasi tetangga: masih dalam grid dan bukan titik kemacetan ('T')
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] != 'T':
                if neighbor not in visited:
                    visited.add(neighbor)                  # Tandai sudah dikunjungi
                    came_from[neighbor] = current          # Simpan rute sebelumnya
                    heapq.heappush(open_set, (manhattan(neighbor, goal), neighbor))  # Masukkan ke antrian berdasarkan heuristik

    # Jika tidak ditemukan jalur
    return None

# Fungsi untuk menampilkan grid dengan jalur (*)
def print_grid_with_path(path):
    visual_grid = [row[:] for row in grid]  # Salin isi grid agar tidak merusak aslinya
    for r, c in path:
        if visual_grid[r][c] not in ('S', 'H'):
            visual_grid[r][c] = '*'         # Tanda jalur menggunakan '*'
    for row in visual_grid:
        print(' '.join(row))               # Cetak grid baris demi baris

# Jalankan program utama
start = find_position('S')  # Temukan posisi ambulans
goal = find_position('H')   # Temukan posisi rumah sakit
path = gbfs(start, goal)    # Jalankan algoritma GBFS

# Tampilkan hasil
if path:
    print("Path from ambulance to hospital:")
    print(path)
    print("\nGrid with path:")
    print_grid_with_path(path)
else:
    print("No path found from ambulance to hospital.")
