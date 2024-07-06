import hashlib
import os

def get_hash(text, prefix="", suffix=""):
    text = prefix + text + suffix
    encoded_string = text.encode('utf-8', errors='ignore')
    hash_value = hashlib.sha256(encoded_string).hexdigest()
    return hash_value


def get_hash_file(file_path, prefix="", suffix="", use_chunked=True, chunk_size=4096):
    sha256_hash = hashlib.sha256()
    
    # Prefix를 해시 업데이트
    sha256_hash.update(prefix.encode('utf-8', errors='ignore'))
    
    file_size = os.path.getsize(file_path)
    
    # 파일을 읽어와서 해시 업데이트
    with open(file_path, "rb") as f:
        if use_chunked and file_size > chunk_size:
            # 큰 파일을 처리할 때 부분적으로 읽어오는 방식
            for byte_block in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(byte_block)
        else:
            # 작은 파일을 처리할 때 파일 전체를 한 번에 읽어오는 방식
            file_content = f.read()
            sha256_hash.update(file_content)
    
    # Suffix를 해시 업데이트
    sha256_hash.update(suffix.encode('utf-8', errors='ignore'))
    
    return sha256_hash.hexdigest()
