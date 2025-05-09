#include <iostream>

int main() {
  int melon;
  std::cin >> melon;
  if (melon % 2 == 0 && melon > 2) {
    std::cout << "yes" << std::endl;
  } else {
    std::cout << "no" << std::endl;
  }
  return 0;
}
