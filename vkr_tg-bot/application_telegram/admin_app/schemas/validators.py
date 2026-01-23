def format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"

    size_units = ["B", "KB", "MB", "GB"]
    index = 0
    while size_bytes >= 1024 and index < len(size_units) - 1:
        size_bytes /= 1024
        index += 1

    return f"{size_bytes:.2f} {size_units[index]}"
