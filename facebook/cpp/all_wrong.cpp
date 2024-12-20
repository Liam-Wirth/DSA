#include <bits/stdc++.h>
using namespace std;
// Write any include statements here

string getWrongAnswers(int N, string C) {
  for (int i = 0; i < N; i++) {
    if (C[i] == 'A') {
      C[i] = 'B';
    } else if (C[i] == 'B') {
      C[i] = 'A';
    }
  }

  return C; 
}
