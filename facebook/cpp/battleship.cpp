#include <bits/stdc++.h>
#include <numeric>
#include <vector>
using namespace std;

double getHitProbability(int R, int C, vector<vector<int>> G) {
  int count = 0;
  for (int i = 0; i < R; i++) {
    for (int j = 0; j < C; j++) {
      count += G[i][j];
    }
  }
  // Write your code here
  return (double)count / (R * C);
}

double evilIters(int R, int C, vector<vector<int>> G) {
  // Evil rust like way of doing it (implemented purely out of curiousity)
  int count =
      std::accumulate(G.begin(), G.end(), 0.0, [](int acc, const auto &row) {
        return acc + accumulate(row.begin(), row.end(), 0);
      });
  return (double)count / (R + C);
}
// Write any include statements here

