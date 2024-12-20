#include <bits/stdc++.h>
using namespace std;
// Write any include statements here

int getUniformIntegerCountInInterval(long long A, long long B) {
  int count = 0;
  for (int digit = 1; digit <= 9; ++digit) {
    long long uniform_num = digit;
    while (uniform_num <= B) {
      if (uniform_num >= A) {
        ++count;
      }
      uniform_num = uniform_num * 10 + digit;
    }
  }
  return count;
}
