#include "../include/json.hpp"
#include "../include/utils.hpp"
#include <cctype>
#include <ctime>
#include <iostream>
#include <string>
#include <termios.h>
#include <unistd.h>

using namespace nlohmann;
std::string get_hidden_password();
bool authenticated();
void admin_interface();
void client_interface();
void save_user(const std::string &username, const std::string &password,
               const std::string &role);

void save_ticket(const std::string &subject, const std::string &description);
void show_tickets();

const std::string DATA_FILE = "data.json";
std::string ROLE;
std::string username;
std::string password;

char buffer;

int main() {

  std::cout << "Ticketing System!" << std::endl;
  bool authStatus = authenticated();
  if (authStatus == false) {
    return 1;
  }

  if (ROLE == "admin") {
    admin_interface();
  } else if (ROLE == "client") {
    client_interface();
  }

  return 0;
}

void admin_interface() {
  std::cout << "ADMIN INTERFACE" << std::endl;
  std::cout << "Select: " << std::endl;
  std::cout << "\t [1] View Tickets" << std::endl;
  std::cout << "\t [2] Create Client" << std::endl;
  std::cout << std::endl;

  std::cin >> buffer;
  switch (buffer) {
  case '1': {
    show_tickets();
    break;
  }
  case '2': {
    std::string user;
    std::string pass;
    std::cout << "Username: ";
    std::cin >> user;
    pass = get_hidden_password();
    save_user(user, pass, "client");
    break;
  }
  }
}

void client_interface() {
  std::cout << "CLIENT INTERFACE" << std::endl;
  std::cout << "Select: " << std::endl;
  std::cout << "\t [1] Add Ticket" << std::endl;
  std::cout << "\t [2] View Tickets" << std::endl;
  std::cout << std::endl;

  std::cin >> buffer;

  switch (buffer) {
  case '1': {
    std::string subject;
    std::string desc;
    std::cout << "ADD TICKETS" << std::endl;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    std::cout << "Subject: ";
    std::getline(std::cin, subject);
    std::cout << "Description: ";
    std::getline(std::cin, desc);

    save_ticket(subject, desc);

    break;
  }
  case '2': {
    show_tickets();
    break;
  }
  }
}

void show_tickets() {

  std::cout << "TICKETS" << std::endl;

  json data = load_data();

  if (!data.contains("tickets") || !data["tickets"].is_object()) {
    std::cout << "No tickets found.\n";
    return;
  }

  for (auto &ticket : data["tickets"].items()) {
    std::cout << ticket.key() << ".) " << ticket.value()["subject"] << "\n";
    std::cout << "\t Description: " << ticket.value()["description"]
              << std::endl;
    std::cout << std::endl;
  }
}

void save_ticket(const std::string &subject, const std::string &description) {
  try {
    if (subject.empty() || description.empty()) {
      std::cout << "Validation Error: Subject and description are required.\n";
      return;
    }

    json data = load_data();
    std::string ticket_id = get_new_ticket_id(data);

    json new_ticket = {{"subject", subject},
                       {"description", description},
                       {"client", username},
                       {"status", "Open"},
                       {"conversation",
                        {{
                            {"sender", "client"},
                            {"message", description},
                            {"timestamp", get_current_timestamp()},
                        }}}};

    data["tickets"][ticket_id] = new_ticket;
    save_data(data);

    std::cout << "Ticket #" << ticket_id << " created successfully!\n";

  } catch (const std::exception &e) {
    std::cerr << "Error: Failed to create ticket: " << e.what() << '\n';
  }
}

void save_user(const std::string &username, const std::string &password,
               const std::string &role) {
  try {
    json data = load_data();

    if (!data.is_object() || !data.contains("users")) {
      std::cout << "Error: Invalid or corrupted data\n";
      return;
    }

    if (data["users"].contains(username)) {
      std::cout << "Error: User already exists\n";
      return;
    }

    data["users"][username] = {{"password", password}, {"role", role}};
    save_data(data);
    std::cout << "Success: User '" << username << "' created successfully!\n";
  } catch (const std::exception &e) {
    std::cerr << "Error: Failed to create user: " << e.what() << '\n';
  }
}

std::string get_hidden_password() {
  std::string password;
  termios oldt, newt;

  std::cout << "Password: ";
  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~ECHO;
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);

  std::cin >> password;

  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
  std::cout << std::endl;
  return password;
}

bool authenticated() {

  json data = load_data();

  std::cout << "Username: ";
  std::cin >> username;
  password = get_hidden_password();

  if (data.contains("users")) {
    for (auto &user_item : data["users"].items()) {

      if (user_item.key() == username) {
        if (user_item.value()["password"] == password) {
          std::cout << "Authentication successful!\n";
          ROLE = user_item.value()["role"];
          return true;
        } else {
          std::cout << "Incorrect password!\n";
          return false;
        }
      }
    }
    std::cout << "User not found!\n";
  }

  return false;
}
