import json

class FileProcessor:
    """Utils hỗ trợ đọc/ghi định dạng JSON/Dict/Obj từ local vào ứng dụng
    """
    @staticmethod
    def write_json(file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, "Thành công"
        except Exception as e:
            return False, str(e)

    #Đọc dữ liệu từ file JSON
    @staticmethod
    def read_json(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return True, data
        except Exception as e:
            return False, str(e)