#include "../include/utils.hpp"
#include <chrono>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>

const std::string DATA_FILE = "data.json";

json load_data() {
  json initial_data = {
      {"users", {{"admin", {{"password", "admin123"}, {"role", "admin"}}}}},
      {"tickets", json::object()}};

  std::ifstream file(DATA_FILE);
  if (!file) {
    std::ofstream new_file(DATA_FILE);
    if (!new_file) {
      std::cout << "Could not Open file for writing\n" << std::endl;
      return initial_data;
    }

    new_file << initial_data.dump(2);
    new_file.close();

    file.open(DATA_FILE);
    if (!file) {
      std::cerr << "Failed to reopen file after creation.\n";
      return initial_data;
    }
  }

  json j;
  file >> j;
  return j;
}

void save_data(const json &data) {
  std::ofstream file(DATA_FILE);
  if (!file) {
    std::cerr << "Error: Unable to open file for writing: " << DATA_FILE
              << std::endl;
    return;
  }
  file << data.dump(2);
  file.close();
}

std::string get_new_ticket_id(const json &data) {
  int max_id = 0;

  if (data.contains("tickets") && data["tickets"].is_object()) {
    for (auto &item : data["tickets"].items()) {
      const std::string &key = item.key();

      if (!key.empty() && std::all_of(key.begin(), key.end(), ::isdigit)) {
        int id = std::stoi(key);
        if (id > max_id) {
          max_id = id;
        }
      }
    }
  }

  return std::to_string(max_id + 1);
}

std::string get_current_timestamp() {
  auto now = std::chrono::system_clock::now();
  std::time_t time = std::chrono::system_clock::to_time_t(now);

  std::stringstream ss;
  ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
  return ss.str();
}
