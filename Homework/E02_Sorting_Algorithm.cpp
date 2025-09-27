#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>

struct Record {
    int id;
    std::string name;
    int price;
    int sold;
    float rating;
};


class Search {
private:
    std::vector<Record> dataset;

    // Kiểm tra xem "search_type" có hợp lệ không
    void validate_search_type(const std::string& search_type) const {
        if (search_type != "id" && search_type != "name" && search_type != "price") {
            throw std::invalid_argument(
                "[Error] Cột '" + search_type + "' không tồn tại. "
                "Các cột hợp lệ: id, name, price"
            );
        }
    }

public:
    Search(std::vector<Record> data) : dataset(data) {}

    // Linear Search – hoạt động với mọi trường
    Record* linear_search(const std::string& search_type, const std::string& value) {
        validate_search_type(search_type);

        for (auto& record : dataset) {
            if (search_type == "name" && record.name == value) {
                return &record;
            }
        }
        return nullptr; // không tìm thấy
    }

    Record* linear_search(const std::string& search_type, int value) {
        validate_search_type(search_type);

        for (auto& record : dataset) {
            if (search_type == "id" && record.id == value) {
                return &record;
            }
        }
        return nullptr;
    }

    Record* linear_search(const std::string& search_type, double value) {
        validate_search_type(search_type);

        for (auto& record : dataset) {
            if (search_type == "price" && record.price == value) {
                return &record;
            }
        }
        return nullptr;
    }

    // Binary Search – CHỈ DÙNG KHI dataset đã được SẮP XẾP THEO "id"
    Record* binary_search(const std::string& search_type, int key_id) {
        if (search_type != "id") {
            throw std::invalid_argument("Binary search chỉ hỗ trợ tìm theo 'id'.");
        }

        int left = 0;
        int right = static_cast<int>(dataset.size()) - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            int mid_id = dataset[mid].id;

            if (mid_id == key_id) {
                return &dataset[mid];
            } else if (mid_id < key_id) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return nullptr;
    }
};