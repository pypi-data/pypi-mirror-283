import subprocess
import os

def run_lloyd_kmeans(num_iterations, threshold, num_clusters, seed, file_paths):
    return run_cpp_program("lloyd_kmeans", num_iterations, threshold, num_clusters, seed, file_paths)

def run_geokmeans(num_iterations, threshold, num_clusters, seed, file_paths):
    return run_cpp_program("geokmeans", num_iterations, threshold, num_clusters, seed, file_paths)

def run_cpp_program(algorithm, num_iterations, threshold, num_clusters, seed, file_paths):
    # Kontrol: Num_iterations pozitif bir tamsayı mı?
    if not isinstance(num_iterations, int) or num_iterations <= 0:
        raise ValueError("Number of iterations must be a positive integer.")
    
    # Kontrol: Threshold pozitif bir float mı?
    if not isinstance(threshold, float) or threshold <= 0:
        raise ValueError("Threshold must be a positive float.")
    
    # Kontrol: Num_clusters pozitif bir tamsayı mı?
    if not isinstance(num_clusters, int) or num_clusters <= 0:
        raise ValueError("Number of clusters must be a positive integer.")
    
    # Kontrol: Seed pozitif bir tamsayı mı?
    if not isinstance(seed, int) or seed <= 0:
        raise ValueError("Seed must be a positive integer.")
    
    # Kontrol: Dosya yolları listesi doğru mu?
    if not isinstance(file_paths, list) or not all(isinstance(path, str) for path in file_paths):
        raise ValueError("File paths must be a list of strings.")
    
    # Kontrol: Her dosya mevcut mu?
    for path in file_paths:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")

    # Dosya yollarını virgülle birleştir
    file_paths_str = ",".join(file_paths)
    
    # Komut oluştur
    command = [
        os.path.join(os.path.dirname(__file__), 'yeni44.out'),  # C++ executable dosyasının yolu
        algorithm,
        str(num_iterations),
        str(threshold),
        str(num_clusters),
        str(seed),
        file_paths_str
    ]
    
    # C++ programını çalıştır
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result.stdout  # Program çıktısını döndür
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error occurred while running the program: {e.stderr}")
