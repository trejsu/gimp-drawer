def memory_usage():
    status = None
    result = {'peak': 0, 'size': 0, 'rss': 0}
    try:
        status = open('/proc/self/status')
        for line in status:
            parts = line.split()
            key = parts[0][2:-1].lower()
            if key in result:
                result[key] = int(parts[1]) // 1000
    finally:
        if status is not None:
            status.close()
    return result
