# this is a redo of number islands again
# remember it was a bfs implementation
# self quiz: how do you bfs?
# first you gotta mark everything you haven't visited, and then add the root to a Q not a stack ? and then over that you basically keep going lvl by lvl until the q gets empty




from collections import deque


def numIslands(grid: list[list[str]]) -> int:
    m = len(grid)
    n = len(grid[0])

    def valid(x: int, y: int) -> bool:
        return (x< m) and (y < n)

    # idea is like make the bfs ONLY work for '1' and then loop through the whole matrix, only calling bfs on the instance where we find a '1' and pos of the 1 is False in seen
    seen = [[False for _ in range(n)] for _ in range(m)]
    DIRS = [(0,1), (1,0), (0,-1), (-1, 0)]
    def bfs(x, y):
        if not valid(x, y):
            return
        q = deque([(x,y)])

        while q:
            x,y = q.popleft()
            seen[x][y] = True
            for (i, j) in DIRS:
                xi = x + i
                yj = y + j
                if valid(xi, yj):
                    if grid[xi][yj] == '1' and not seen[xi][yj]:
                        q.appendleft((xi,yj))
                        seen[xi][yj] = True
    islands = 0
    for r in range(0, m):
        for c in range(0, n):
            if grid[r][c] == '1' and not seen[r][c]:
                bfs(r,c)
                islands+=1

    return islands

grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]

print(grid)



print(numIslands(grid))
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
print(numIslands(grid))
