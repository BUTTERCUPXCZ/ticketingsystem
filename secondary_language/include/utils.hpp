#ifndef UTILS_HPP
#define UTILS_HPP

#include "../include/json.hpp"
#include <string>

using json = nlohmann::json;

json load_data();
void save_data(const json &data);
std::string get_new_ticket_id(const json &data);
std::string get_current_timestamp();

#endif
